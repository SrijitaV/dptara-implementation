
import random

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
    Central simulation controller for the DPTARA framework.

    This version implements a sequential simulation workflow:
        1. Initialize resources.
        2. Generate tasks.
        3. Calculate dynamic priorities.
        4. Allocate tasks.
        5. Execute allocated tasks.
        6. Calculate energy consumption.
        7. Release allocated CPU capacity.
        8. Calculate performance metrics.

    Sequential processing is an initial implementation
    assumption. It is not a claim of exact reproduction
    of the paper's complete scheduling algorithm.
    """

    def __init__(
        self,
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42
    ):

        if simulation_duration <= 0:
            raise ValueError(
                "Simulation duration must be positive."
            )

        if arrival_rate <= 0:
            raise ValueError(
                "Arrival rate must be positive."
            )

        self.simulation_duration = simulation_duration
        self.arrival_rate = arrival_rate
        self.seed = seed

        self.rng = random.Random(seed)

        # Task generation
        self.task_generator = TaskGenerator(
            arrival_rate=arrival_rate,
            seed=seed
        )

        # Resource management and allocation
        self.resource_manager = ResourceManager()

        self.resource_allocator = ResourceAllocator(
            self.resource_manager
        )

        # Task execution
        self.task_executor = TaskExecutor()

        # Dynamic priority calculation
        self.priority_model = DynamicPriorityModel(
            alpha=1.0,
            beta=1.0,
            gamma=1.0
        )

        # Additional framework components
        self.load_predictor = LoadPredictor()
        self.energy_manager = EnergyManager()
        self.load_balancer = LoadBalancer()
        self.metrics = Metrics()

        self.tasks = []
        self.resources = []

        self.simulation_clock = 0.0

        print("DPTARA Simulator initialized successfully.")

    def initialize_resources(self):
        """
        Initialize 10 edge servers and 1 cloud server.
        """

        if self.resource_manager.get_all_resources():
            raise ValueError(
                "Resources have already been initialized."
            )

        # -----------------------------------------
        # 1. Initialize 10 edge servers
        # -----------------------------------------

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

        # -----------------------------------------
        # 2. Initialize 1 cloud server
        # -----------------------------------------

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
        print(f"Edge servers: 10")
        print(f"Cloud servers: 1")
        print(f"Total resources: {len(self.resources)}")

        return self.resources

    def generate_tasks(
        self,
        task_type="normal",
        original_priority=1.0
    ):
        """
        Generate tasks for the configured simulation duration.

        Task type and original priority are configurable
        implementation inputs.
        """

        self.tasks = self.task_generator.generate_tasks(
            duration_seconds=self.simulation_duration,
            task_type=task_type,
            original_priority=original_priority
        )

        print("\nTask generation completed.")
        print(f"Generated tasks: {len(self.tasks)}")

        return self.tasks

    def _calculate_system_load(self):
        """
        Calculate current system utilization as a ratio.
        """

        total_capacity = sum(
            resource.capacity for resource in self.resources
        )

        total_load = sum(
            resource.current_load for resource in self.resources
        )

        if total_capacity <= 0:
            return 0.0

        return total_load / total_capacity

    def process_task(self, task):
        """
        Process one task through allocation and execution.
        """

        # A task cannot be processed before its arrival.
        current_time = max(
            task.arrival_time,
            self.simulation_clock
        )

        # -----------------------------------------
        # 1. Calculate dynamic priority
        # -----------------------------------------

        current_load = self._calculate_system_load()

        task.priority = self.priority_model.calculate_priority(
            task,
            current_time,
            current_load
        )

        # -----------------------------------------
        # 2. Allocate computing resource
        # -----------------------------------------

        selected_resource = self.resource_allocator.allocate_task(
            task
        )

        if selected_resource is None:
            print(
                f"Task {task.task_id}: "
                "No suitable resource available."
            )
            return task

        # -----------------------------------------
        # 3. Execute task
        # -----------------------------------------

        try:
            self.task_executor.execute_task(
                task,
                selected_resource,
                current_time
            )

            # Advance simulation clock to completion.
            self.simulation_clock = task.completion_time

        except Exception:
            task.status = "failed"
            raise

        finally:
            # Release CPU capacity only after execution
            # and energy calculation have finished.
            if task.assigned_resource is not None:
                self.resource_allocator.release_task(task)

        return task

    def run(self):
        """
        Execute the complete sequential simulation.
        """

        print("\nStarting DPTARA simulation...")

        # Initialize resources if not already initialized.
        if not self.resource_manager.get_all_resources():
            self.initialize_resources()

        # Generate tasks.
        if not self.tasks:
            self.generate_tasks()

        # Process tasks in arrival order.
        self.tasks.sort(
            key=lambda task: task.arrival_time
        )

        for task in self.tasks:
            self.process_task(task)

        # -----------------------------------------
        # Calculate final performance metrics
        # -----------------------------------------

        results = self.metrics.calculate_metrics(
            self.tasks,
            self.resources
        )

        # Calculate balancing rates for the final
        # resource state.
        balancing_rates = (
            self.load_balancer.calculate_all_balancing_rates(
                self.resources
            )
            if self.resources else {}
        )

        results["simulation_duration"] = self.simulation_duration
        results["generated_tasks"] = len(self.tasks)
        results["simulation_clock"] = self.simulation_clock
        results["resource_balancing_rates"] = balancing_rates

        self.print_results(results)

        return results

    def print_results(self, results):
        """
        Display simulation performance results.
        """

        print("\n" + "=" * 55)
        print("             DPTARA SIMULATION RESULTS")
        print("=" * 55)

        print(
            f"Simulation duration: "
            f"{results['simulation_duration']:.2f} seconds"
        )

        print(
            f"Simulation clock: "
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
            f"Final instantaneous utilization: "
            f"{results['system_utilization_percent']:.2f}%"
        )

        print("=" * 55)
