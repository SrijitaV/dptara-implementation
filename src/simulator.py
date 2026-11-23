
import random
import heapq
import itertools

from .models.entities import Resource
from .models.priority_model import DynamicPriorityModel
from .models.load_predictor import LoadPredictor

from baselines.strategies import get_strategy

from .task_generator import TaskGenerator
from .resource_manager import ResourceManager
from .resource_allocator import ResourceAllocator
from .task_executor import TaskExecutor
from .energy_manager import EnergyManager
from .load_balancer import LoadBalancer
from .metrics import Metrics


class DPTARASimulator:
    """
    Event-driven simulator for DPTARA and its baseline variants.

    Supported algorithms:
        DPTARA
        A-PBRA
        NBIHA
        CORA-GT
    """

    def __init__(
        self,
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42,
        algorithm="DPTARA"
    ):

        if simulation_duration <= 0:
            raise ValueError(
                "Simulation duration must be positive."
            )

        if arrival_rate <= 0:
            raise ValueError(
                "Arrival rate must be positive."
            )

        supported_algorithms = {
            "DPTARA",
            "A-PBRA",
            "NBIHA",
            "CORA-GT"
        }

        if algorithm not in supported_algorithms:
            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            )

        self.simulation_duration = simulation_duration
        self.arrival_rate = arrival_rate
        self.seed = seed
        self.algorithm = algorithm

        self.rng = random.Random(seed)

        self.strategy = (
            None if algorithm == "DPTARA"
            else get_strategy(algorithm)
        )

        # Task generation.
        self.task_generator = TaskGenerator(
            arrival_rate=arrival_rate,
            seed=seed
        )

        # Resource management.
        self.resource_manager = ResourceManager()

        # Load prediction.
        self.load_predictor = LoadPredictor()

        # Resource allocation.
        self.resource_allocator = ResourceAllocator(
            self.resource_manager,
            load_predictor=self.load_predictor,
            strategy=self.strategy
        )

        # Task execution.
        self.task_executor = TaskExecutor()

        # Dynamic priority model.
        self.priority_model = DynamicPriorityModel(
            alpha=1.0,
            beta=1.0,
            gamma=1.0
        )

        # Performance components.
        self.energy_manager = EnergyManager()
        self.load_balancer = LoadBalancer()
        self.metrics = Metrics()

        self.tasks = []
        self.resources = []

        # Simulation state.
        self.simulation_clock = 0.0
        self.event_queue = []
        self.waiting_tasks = []
        self.event_counter = itertools.count()

        # Time-integrated measurements.
        self.utilization_area = 0.0
        self.balancing_rate_area = 0.0
        self.balancing_observation_time = 0.0

    # --------------------------------------------------
    # RESOURCE INITIALIZATION
    # --------------------------------------------------

    def initialize_resources(self):

        if self.resource_manager.get_all_resources():
            raise ValueError(
                "Resources have already been initialized."
            )

        # Initialize 10 edge servers.
        for i in range(1, 11):

            cpu_capacity = self.rng.randint(500, 3000)

            resource = Resource(
                resource_id=f"E{i}",
                resource_type="edge",
                capacity=cpu_capacity,
                current_load=0.0,
                processing_speed_mips=cpu_capacity,
                power_consumption_w=50.0,
                network_latency_ms=round(
                    self.rng.uniform(5, 10), 2
                )
            )

            self.resource_manager.register_resource(resource)

        # Initialize one cloud server.
        cloud_capacity = self.rng.randint(2000, 10000)

        cloud = Resource(
            resource_id="C1",
            resource_type="cloud",
            capacity=cloud_capacity,
            current_load=0.0,
            processing_speed_mips=cloud_capacity,
            power_consumption_w=200.0,
            network_latency_ms=round(
                self.rng.uniform(50, 100), 2
            )
        )

        self.resource_manager.register_resource(cloud)

        self.resources = (
            self.resource_manager.get_all_resources()
        )

        print("\nResources initialized successfully.")
        print("Edge servers: 10")
        print("Cloud servers: 1")
        print(f"Total resources: {len(self.resources)}")

        return self.resources

    # --------------------------------------------------
    # TASK GENERATION
    # --------------------------------------------------

    def generate_tasks(
        self,
        task_type="normal",
        original_priority=1.0,
        task_profiles=None
    ):
        """
        Generate tasks using the configured task profiles.
        """

        self.tasks = self.task_generator.generate_tasks(
            duration_seconds=self.simulation_duration,
            task_type=task_type,
            original_priority=original_priority,
            task_profiles=task_profiles
        )

        print("\nTask generation completed.")
        print(f"Generated tasks: {len(self.tasks)}")

        if task_profiles is not None:

            print("\nGenerated task category distribution:")

            category_counts = {}

            for task in self.tasks:
                category_counts[task.task_type] = (
                    category_counts.get(task.task_type, 0) + 1
                )

            for category, count in sorted(
                category_counts.items()
            ):
                print(f"{category}: {count}")

        return self.tasks

    # --------------------------------------------------
    # SYSTEM UTILIZATION
    # --------------------------------------------------

    def _calculate_system_load(self):
        """
        Calculate normalized aggregate system utilization.
        """

        total_capacity = sum(
            resource.capacity
            for resource in self.resources
        )

        total_load = sum(
            resource.current_load
            for resource in self.resources
        )

        if total_capacity <= 0:
            return 0.0

        return total_load / total_capacity

    def _record_utilization_interval(self, next_time):
        """
        Record resource observations and integrate utilization
        over the elapsed simulation interval.
        """

        elapsed_time = (
            next_time - self.simulation_clock
        )

        if elapsed_time < 0:
            raise ValueError(
                "Simulation time cannot move backwards."
            )

        # Record utilization observations for prediction.
        for resource in self.resources:

            if resource.capacity <= 0:
                continue

            utilization = (
                resource.current_load / resource.capacity
            )

            utilization = max(
                0.0,
                min(1.0, utilization)
            )

            self.load_predictor.record_observation(
                resource.resource_id,
                self.simulation_clock,
                utilization
            )

        total_load = sum(
            resource.current_load
            for resource in self.resources
        )

        # Record Jain's fairness index when resources
        # are carrying load.
        if elapsed_time > 0 and total_load > 0:

            balancing_score = (
                self.load_balancer.calculate_balancing_score(
                    self.resources
                )
            )

            self.balancing_rate_area += (
                balancing_score * elapsed_time
            )

            self.balancing_observation_time += elapsed_time

        # Integrate aggregate CPU load over time.
        self.utilization_area += (
            total_load * elapsed_time
        )

        self.simulation_clock = next_time

    # --------------------------------------------------
    # COMPLETION EVENT
    # --------------------------------------------------

    def _handle_completion(self, task, resource):

        if task.status != "running":
            raise ValueError(
                f"Task {task.task_id} is not running."
            )

        assigned_resource = task.assigned_resource

        # Release the reserved CPU capacity.
        self.resource_allocator.release_task(task)

        # Preserve assignment information for result analysis.
        task.assigned_resource = assigned_resource

        task.status = "completed"

    # --------------------------------------------------
    # TASK DISPATCHING
    # --------------------------------------------------

    def _dispatch_waiting_tasks(self):
        """
        Dispatch waiting tasks using the selected algorithm.
        """

        while self.waiting_tasks:

            # DPTARA: dynamically calculate task priorities.
            if self.algorithm == "DPTARA":

                current_load = self._calculate_system_load()

                for task in self.waiting_tasks:

                    task.priority = (
                        self.priority_model.calculate_priority(
                            task,
                            self.simulation_clock,
                            current_load
                        )
                    )

                ordered_tasks = sorted(
                    self.waiting_tasks,
                    key=lambda task: (
                        -task.priority,
                        task.arrival_time,
                        task.task_id
                    )
                )

            # Baselines: use their own task-ranking strategies.
            else:

                ordered_tasks = self.strategy.rank_tasks(
                    self.waiting_tasks,
                    self.simulation_clock
                )

            task_allocated = False

            for task in ordered_tasks:

                task.status = "pending"

                selected_resource = (
                    self.resource_allocator.allocate_task(
                        task,
                        current_time=self.simulation_clock
                    )
                )

                if selected_resource is None:
                    continue

                self.waiting_tasks.remove(task)

                # Execute the allocated task.
                self.task_executor.execute_task(
                    task,
                    selected_resource,
                    self.simulation_clock
                )

                # Schedule its completion event.
                heapq.heappush(
                    self.event_queue,
                    (
                        task.completion_time,
                        0,
                        next(self.event_counter),
                        "completion",
                        task,
                        selected_resource
                    )
                )

                task_allocated = True
                break

            # Stop if no waiting task can currently be allocated.
            if not task_allocated:
                break

    # --------------------------------------------------
    # ARRIVAL EVENT
    # --------------------------------------------------

    def _handle_arrival(self, task):

        if task.status != "pending":
            raise ValueError(
                f"Task {task.task_id} is not pending."
            )

        self.waiting_tasks.append(task)

        self._dispatch_waiting_tasks()

    # --------------------------------------------------
    # RESET SIMULATION STATE
    # --------------------------------------------------

    def _reset_simulation_state(self):
        """
        Reset transient state before a simulation run.
        """

        self.event_queue = []
        self.waiting_tasks = []
        self.event_counter = itertools.count()

        self.simulation_clock = 0.0

        self.utilization_area = 0.0
        self.balancing_rate_area = 0.0
        self.balancing_observation_time = 0.0

        self.load_predictor.history = {}

        self.resource_manager.reset_loads()

        # Reset task state to allow another run.
        for task in self.tasks:

            task.priority = None
            task.assigned_resource = None
            task.allocated_load = None

            task.start_time = None
            task.completion_time = None

            task.execution_time = 0.0
            task.energy_consumption = 0.0

            task.status = "pending"

    # --------------------------------------------------
    # SIMULATION EXECUTION
    # --------------------------------------------------

    def run(self):

        print(
            "\nStarting event-driven "
            f"{self.algorithm} simulation..."
        )

        if not self.resource_manager.get_all_resources():
            self.initialize_resources()

        if not self.tasks:
            self.generate_tasks()

        self.resources = (
            self.resource_manager.get_all_resources()
        )

        self._reset_simulation_state()

        # Sort tasks by arrival time.
        self.tasks.sort(
            key=lambda task: task.arrival_time
        )

        # Schedule all arrival events.
        for task in self.tasks:

            heapq.heappush(
                self.event_queue,
                (
                    task.arrival_time,
                    1,
                    next(self.event_counter),
                    "arrival",
                    task,
                    None
                )
            )

        # --------------------------------------------------
        # EVENT-DRIVEN SIMULATION LOOP
        # --------------------------------------------------

        while self.event_queue:

            # Get the earliest event timestamp.
            event_time = self.event_queue[0][0]

            # Integrate measurements until this event time.
            self._record_utilization_interval(event_time)

            simultaneous_completions = []
            simultaneous_arrivals = []

            # Collect all events at the same timestamp.
            while (
                self.event_queue
                and self.event_queue[0][0] == event_time
            ):

                event = heapq.heappop(self.event_queue)

                (
                    _,
                    _,
                    _,
                    event_type,
                    task,
                    resource
                ) = event

                if event_type == "completion":

                    simultaneous_completions.append(
                        (task, resource)
                    )

                elif event_type == "arrival":

                    simultaneous_arrivals.append(task)

                else:

                    raise ValueError(
                        f"Unknown event type: {event_type}"
                    )

            # Step 1: Process all completions first.
            for task, resource in simultaneous_completions:

                self._handle_completion(
                    task,
                    resource
                )

            # Step 2: Add all simultaneous arrivals.
            for task in simultaneous_arrivals:

                if task.status != "pending":
                    raise ValueError(
                        f"Task {task.task_id} is not pending."
                    )

                self.waiting_tasks.append(task)

            # Step 3: Dispatch after processing the full batch.
            self._dispatch_waiting_tasks()

        # --------------------------------------------------
        # FINALIZE SIMULATION
        # --------------------------------------------------

        # Any tasks still waiting could not be allocated.
        for task in self.waiting_tasks:
            task.status = "unallocated"

        self.waiting_tasks.clear()

        # Calculate task performance metrics.
        results = self.metrics.calculate_metrics(
            self.tasks,
            self.resources,
            current_time=self.simulation_clock
        )

        # --------------------------------------------------
        # TIME-WEIGHTED SYSTEM UTILIZATION
        # --------------------------------------------------

        total_capacity = sum(
            resource.capacity
            for resource in self.resources
        )

        if (
            total_capacity > 0
            and self.simulation_clock > 0
        ):

            average_utilization = (
                self.utilization_area
                / (
                    total_capacity
                    * self.simulation_clock
                )
            ) * 100.0

        else:
            average_utilization = 0.0

        results["average_system_utilization_percent"] = (
            average_utilization
        )

        # Retain the existing key for compatibility.
        results["system_utilization_percent"] = (
            average_utilization
        )

        # --------------------------------------------------
        # TIME-WEIGHTED LOAD FAIRNESS
        # --------------------------------------------------

        if self.balancing_observation_time > 0:

            average_balancing_rate = (
                self.balancing_rate_area
                / self.balancing_observation_time
            )

        else:
            average_balancing_rate = 0.0

        results["average_balancing_rate_percent"] = (
            average_balancing_rate
        )

        # Additional experiment information.
        results["simulation_duration"] = (
            self.simulation_duration
        )

        results["simulation_clock"] = (
            self.simulation_clock
        )

        results["generated_tasks"] = len(self.tasks)

        results["algorithm"] = self.algorithm

        self.print_results(results)

        return results

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    def print_results(self, results):

        print("\n" + "=" * 58)
        print(
            f"             {self.algorithm} SIMULATION RESULTS"
        )
        print("=" * 58)

        # Simulation overview.
        print("\nSIMULATION OVERVIEW")
        print("-" * 58)

        print(
            f"Task generation window: "
            f"{results['simulation_duration']:.2f} seconds"
        )

        print(
            f"Simulation makespan: "
            f"{results['simulation_clock']:.4f} seconds"
        )

        print(
            f"Total generated tasks: "
            f"{results['total_tasks']}"
        )

        # Task completion.
        print("\nTASK COMPLETION")
        print("-" * 58)

        print(
            f"Completed tasks: "
            f"{results['completed_tasks']}"
        )

        print(
            f"Incomplete tasks: "
            f"{results['incomplete_tasks']}"
        )

        print(
            f"Completion rate: "
            f"{results['completion_rate_percent']:.2f}%"
        )

        print(
            f"Unallocated tasks: "
            f"{results['unallocated_tasks']}"
        )

        # Deadline performance.
        print("\nDEADLINE PERFORMANCE")
        print("-" * 58)

        print(
            f"Tasks completed on time: "
            f"{results['on_time_tasks']}"
        )

        print(
            f"Late completed tasks: "
            f"{results['late_completed_tasks']}"
        )

        print(
            f"Expired incomplete tasks: "
            f"{results['expired_incomplete_tasks']}"
        )

        print(
            f"Unresolved tasks: "
            f"{results['unresolved_tasks']}"
        )

        print(
            f"Deadline miss rate: "
            f"{results['deadline_miss_rate_percent']:.2f}%"
        )

        print(
            f"Deadline met rate: "
            f"{results['deadline_met_rate_percent']:.2f}%"
        )

        print(
            f"Total deadline violation: "
            f"{results['total_deadline_violation']:.6f} seconds"
        )

        print(
            f"Average deadline violation: "
            f"{results['average_deadline_violation']:.6f} seconds"
        )

        print(
            f"Maximum deadline violation: "
            f"{results['maximum_deadline_violation']:.6f} seconds"
        )

        print(
            f"Minimum deadline violation: "
            f"{results['minimum_deadline_violation']:.6f} seconds"
        )

        # Execution performance.
        print("\nEXECUTION PERFORMANCE")
        print("-" * 58)

        print(
            f"Average latency: "
            f"{results['average_latency']:.4f} seconds"
        )

        print(
            f"Average execution time: "
            f"{results['average_execution_time']:.4f} seconds"
        )

        # Energy and resource utilization.
        print("\nENERGY AND RESOURCE UTILIZATION")
        print("-" * 58)

        print(
            f"Total energy consumption: "
            f"{results['total_energy_consumption']:.4f} joules"
        )

        print(
            f"Average system utilization: "
            f"{results['system_utilization_percent']:.2f}%"
        )

        print(
            f"Average load balancing fairness: "
            f"{results['average_balancing_rate_percent']:.2f}%"
        )

        print("\n" + "=" * 58)
