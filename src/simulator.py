
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
        self.completion_events = []
        self.event_counter = itertools.count()

        # Time-integrated CPU utilization
        self.utilization_area = 0.0

        print("DPTARA Simulator initialized successfully.")

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
    # COMPLETION EVENT HANDLING
    # --------------------------------------------------

    def _complete_next_event(self):

        completion_time, _, task, resource = heapq.heappop(
            self.completion_events
        )

        self._record_utilization_interval(completion_time)

        # Preserve resource assignment for task analysis.
        assigned_resource = task.assigned_resource

        # Release the reserved CPU capacity.
        self.resource_allocator.release_task(task)

        # Restore the resource ID after release.
        task.assigned_resource = assigned_resource

        task.status = "completed"

    def _advance_until(self, target_time):

        while (
            self.completion_events
            and self.completion_events[0][0] <= target_time
        ):
            self._complete_next_event()

        if target_time > self.simulation_clock:
            self._record_utilization_interval(target_time)

    # --------------------------------------------------
    # TASK PROCESSING
    # --------------------------------------------------

    def process_task(self, task):

        # Advance the clock to the task's arrival.
        arrival_time = max(
            task.arrival_time,
            self.simulation_clock
        )

        self._advance_until(arrival_time)

        # Calculate priority at the current dispatch time.
        current_load = self._calculate_system_load()

        task.priority = self.priority_model.calculate_priority(
            task,
            self.simulation_clock,
            current_load
        )

        # Try allocation. If all suitable resources are busy,
        # wait for the next completion event and retry.
        selected_resource = None

        while selected_resource is None:

            selected_resource = self.resource_allocator.allocate_task(
                task
            )

            if selected_resource is not None:
                break

            if not self.completion_events:
                # No running task can free capacity.
                # This task cannot currently be allocated.
                break

            # Wait until at least one task completes.
            self._complete_next_event()

            # The allocator marks failed allocations as unallocated.
            # Reset status to allow another allocation attempt.
            task.status = "pending"

        if selected_resource is None:
            task.status = "unallocated"
            return task

        # Execute using the allocated CPU demand.
        self.task_executor.execute_task(
            task,
            selected_resource,
            self.simulation_clock
        )

        # The executor marks the task completed immediately.
        # Change it to running until its completion event occurs.
        task.status = "running"

        # Schedule its future completion.
        heapq.heappush(
            self.completion_events,
            (
                task.completion_time,
                next(self.event_counter),
                task,
                selected_resource
            )
        )

        return task

    # --------------------------------------------------
    # SIMULATION EXECUTION
    # --------------------------------------------------

    def run(self):

        print("\nStarting event-driven DPTARA simulation...")

        if not self.resource_manager.get_all_resources():
            self.initialize_resources()

        if not self.tasks:
            self.generate_tasks()

        # Process tasks in arrival order.
        self.tasks.sort(
            key=lambda task: task.arrival_time
        )

        for task in self.tasks:
            self.process_task(task)

        # Complete all tasks that are still running.
        while self.completion_events:
            self._complete_next_event()

        # Calculate performance metrics.
        results = self.metrics.calculate_metrics(
            self.tasks,
            self.resources
        )

        total_capacity = sum(
            resource.capacity for resource in self.resources
        )

        # Time-weighted average utilization over the
        # complete simulation makespan.
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

        print(
            f"Completed tasks: "
            f"{results['completed_tasks']}"
        )

        print(
            f"Completion rate: "
            f"{results['completion_rate_percent']:.2f}%"
        )

        print(
            f"Average latency: "
            f"{results['average_latency']:.4f} seconds"
        )

        print(
            f"Average execution time: "
            f"{results['average_execution_time']:.4f} seconds"
        )

        print(
            f"Total energy consumption: "
            f"{results['total_energy_consumption']:.4f} joules"
        )

        print(
            f"Average system utilization: "
            f"{results['average_system_utilization_percent']:.2f}%"
        )

        print("=" * 58)
