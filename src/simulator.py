
import random
import heapq
import itertools

from .models.entities import Resource
from .models.priority_model import DynamicPriorityModel
from .models.load_predictor import LoadPredictor

from .task_generator import TaskGenerator
from .resource_manager import ResourceManager
from .resource_allocator import ResourceAllocator
from .task_executor import TaskExecutor
from .energy_manager import EnergyManager
from .load_balancer import LoadBalancer
from .metrics import Metrics


class DPTARASimulator:
    """
    Event-driven DPTARA simulation controller.

    Tasks can execute concurrently on different resources.
    CPU allocations remain reserved until task completion.

    This is an initial event-driven implementation.
    """

    def __init__(
        self,
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42
    ):

        if simulation_duration <= 0:
            raise ValueError("Simulation duration must be positive.")

        if arrival_rate <= 0:
            raise ValueError("Arrival rate must be positive.")

        self.simulation_duration = simulation_duration
        self.arrival_rate = arrival_rate
        self.seed = seed

        self.rng = random.Random(seed)

        self.task_generator = TaskGenerator(
            arrival_rate=arrival_rate,
            seed=seed
        )

        self.resource_manager = ResourceManager()

        self.resource_allocator = ResourceAllocator(
            self.resource_manager
        )

        self.task_executor = TaskExecutor()

        self.priority_model = DynamicPriorityModel(
            alpha=1.0,
            beta=1.0,
            gamma=1.0
        )

        self.load_predictor = LoadPredictor()
        self.energy_manager = EnergyManager()
        self.load_balancer = LoadBalancer()
        self.metrics = Metrics()

        self.tasks = []
        self.resources = []

        # Simulation clock
        self.simulation_clock = 0.0

        # Completion events:
        # (completion_time, sequence_number, task, resource)
        # Unified event queue:
        # (event_time, event_order, sequence, event_type, task, resource)
        #
        # Completion events use event_order = 0.
        # Arrival events use event_order = 1.
        # Therefore, completions are processed before arrivals
        # when both occur at the same simulation time.

        self.event_queue = []

        # Tasks waiting for resource allocation.
        self.waiting_tasks = []

        self.event_counter = itertools.count()

        # Time-integrated CPU utilization.
        self.utilization_area = 0.0

    # --------------------------------------------------
    # RESOURCE INITIALIZATION
    # --------------------------------------------------

    def initialize_resources(self):

        if self.resource_manager.get_all_resources():
            raise ValueError("Resources have already been initialized.")

        # Initialize 10 edge servers
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

        # Initialize cloud server
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

        self.resources = self.resource_manager.get_all_resources()

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
        original_priority=1.0
    ):

        self.tasks = self.task_generator.generate_tasks(
            duration_seconds=self.simulation_duration,
            task_type=task_type,
            original_priority=original_priority
        )

        print("\nTask generation completed.")
        print(f"Generated tasks: {len(self.tasks)}")

        return self.tasks

    # --------------------------------------------------
    # SYSTEM UTILIZATION
    # --------------------------------------------------

    def _calculate_system_load(self):

        total_capacity = sum(
            resource.capacity for resource in self.resources
        )

        total_load = sum(
            resource.current_load for resource in self.resources
        )

        if total_capacity <= 0:
            return 0.0

        return total_load / total_capacity

    def _record_utilization_interval(self, next_time):

        elapsed_time = next_time - self.simulation_clock

        if elapsed_time < 0:
            raise ValueError("Simulation time cannot move backwards.")

        current_load = sum(
            resource.current_load for resource in self.resources
        )

        self.utilization_area += current_load * elapsed_time

        self.simulation_clock = next_time


    # --------------------------------------------------
    # EVENT HANDLING AND UTILIZATION
    # --------------------------------------------------

    def _calculate_system_load(self):

        total_capacity = sum(
            resource.capacity for resource in self.resources
        )

        total_load = sum(
            resource.current_load for resource in self.resources
        )

        if total_capacity <= 0:
            return 0.0

        return total_load / total_capacity

    def _record_utilization_interval(self, next_time):

        elapsed_time = next_time - self.simulation_clock

        if elapsed_time < 0:
            raise ValueError("Simulation time cannot move backwards.")

        current_load = sum(
            resource.current_load for resource in self.resources
        )

        self.utilization_area += current_load * elapsed_time
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

        self.resource_allocator.release_task(task)

        # Preserve the resource ID for result analysis.
        task.assigned_resource = assigned_resource

        task.status = "completed"

    # --------------------------------------------------
    # TASK DISPATCHING
    # --------------------------------------------------

    
    def _dispatch_waiting_tasks(self):
        """
        Dispatch waiting tasks according to dynamically
        calculated priority.

        Higher priority values are considered first.
        Priorities are recalculated whenever a task is
        dispatched because system load may have changed.
        """

        while self.waiting_tasks:

            current_load = self._calculate_system_load()

            # Recalculate priority for every waiting task.
            for task in self.waiting_tasks:

                task.priority = self.priority_model.calculate_priority(
                    task,
                    self.simulation_clock,
                    current_load
                )

            # Sort by:
            # 1. Higher priority first.
            # 2. Earlier arrival first when priorities tie.
            # 3. Lower task ID first as a final tie-breaker.
            self.waiting_tasks.sort(
                key=lambda task: (
                    -task.priority,
                    task.arrival_time,
                    task.task_id
                )
            )

            task_allocated = False

            # Try tasks in priority order.
            for task in self.waiting_tasks:

                task.status = "pending"

                selected_resource = (
                    self.resource_allocator.allocate_task(task)
                )

                # If this task cannot be allocated,
                # retain it in the waiting queue and try
                # the next task.
                if selected_resource is None:
                    task.status = "pending"
                    continue

                # Remove only after successful allocation.
                self.waiting_tasks.remove(task)

                self.task_executor.execute_task(
                    task,
                    selected_resource,
                    self.simulation_clock
                )

                # Schedule task completion.
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

                # Resource load has changed. Recalculate
                # priorities before dispatching another task.
                break

            # No waiting task could be allocated.
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

        # Try to dispatch waiting tasks immediately.
        self._dispatch_waiting_tasks()

    # --------------------------------------------------
    # SIMULATION EXECUTION
    # --------------------------------------------------

    def run(self):

        print("\nStarting event-driven DPTARA simulation...")

        if not self.resource_manager.get_all_resources():
            self.initialize_resources()

        if not self.tasks:
            self.generate_tasks()

        # Sort tasks by their arrival times.
        self.tasks.sort(
            key=lambda task: task.arrival_time
        )

        # Reset event-related state.
        self.event_queue = []
        self.waiting_tasks = []
        self.event_counter = itertools.count()
        self.simulation_clock = 0.0
        self.utilization_area = 0.0

        # Schedule every task arrival in the event queue.
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

        # Process events in chronological order.
        while self.event_queue:

            (
                event_time,
                _,
                _,
                event_type,
                task,
                resource
            ) = heapq.heappop(self.event_queue)

            # Account for utilization before changing resource load.
            self._record_utilization_interval(event_time)

            if event_type == "completion":

                self._handle_completion(task, resource)

                # A completed task may free capacity.
                self._dispatch_waiting_tasks()

            elif event_type == "arrival":

                self._handle_arrival(task)

            else:

                raise ValueError(
                    f"Unknown event type: {event_type}"
                )

        # No future events remain. Any tasks still waiting
        # could not be allocated with the available resources.
        for task in self.waiting_tasks:
            task.status = "unallocated"

        self.waiting_tasks.clear()

        # Calculate performance metrics.
        results = self.metrics.calculate_metrics(
            self.tasks,
            self.resources
        )

        total_capacity = sum(
            resource.capacity for resource in self.resources
        )

        if (
            total_capacity > 0
            and self.simulation_clock > 0
        ):

            average_utilization = (
                self.utilization_area
                / (total_capacity * self.simulation_clock)
            ) * 100

        else:

            average_utilization = 0.0

        results["average_system_utilization_percent"] = (
            average_utilization
        )

        results["simulation_duration"] = self.simulation_duration
        results["simulation_clock"] = self.simulation_clock
        results["generated_tasks"] = len(self.tasks)

        self.print_results(results)

        return results


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    def print_results(self, results):

        print("\n" + "=" * 58)
        print("             DPTARA SIMULATION RESULTS")
        print("=" * 58)

        # ----------------------------------------------
        # 1. Simulation overview
        # ----------------------------------------------

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

        # ----------------------------------------------
        # 2. Task completion
        # ----------------------------------------------

        print("\nTASK COMPLETION")
        print("-" * 58)

        print(
            f"Completed tasks: "
            f"{results['completed_tasks']}"
        )

        print(
            f"Completion rate: "
            f"{results['completion_rate_percent']:.2f}%"
        )

        print(
            f"Unallocated tasks: "
            f"{results['unallocated_tasks']}"
        )

        # ----------------------------------------------
        # 3. Deadline performance
        # ----------------------------------------------

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

        # ----------------------------------------------
        # 4. Execution performance
        # ----------------------------------------------

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

        # ----------------------------------------------
        # 5. Energy and resource utilization
        # ----------------------------------------------

        print("\nENERGY AND RESOURCE UTILIZATION")
        print("-" * 58)

        print(
            f"Total energy consumption: "
            f"{results['total_energy_consumption']:.4f} joules"
        )

        print(
            f"Average system utilization: "
            f"{results['average_system_utilization_percent']:.2f}%"
        )

        print("\n" + "=" * 58)
