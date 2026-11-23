
from .energy_manager import EnergyManager


class TaskExecutor:

    def __init__(self, energy_manager=None):
        self.energy_manager = energy_manager or EnergyManager()

    def execute_task(self, task, resource, current_time):

        if task.status != "allocated":
            raise ValueError("Task must be allocated before execution.")

        if task.assigned_resource != resource.resource_id:
            raise ValueError("Task-resource assignment mismatch.")

        if task.workload_mi <= 0:
            raise ValueError("Task workload must be positive.")

        if task.cpu_demand_mips <= 0:
            raise ValueError("Task CPU demand must be positive.")

        if resource.processing_speed_mips <= 0:
            raise ValueError("Resource processing speed must be positive.")

        if current_time < task.arrival_time:
            raise ValueError("Execution cannot start before task arrival.")

        # CPU demand represents the CPU rate reserved for this task.
        allocated_speed = min(
            task.cpu_demand_mips,
            resource.processing_speed_mips
        )

        execution_time = task.workload_mi / allocated_speed

        network_delay = resource.network_latency_ms / 1000.0

        task.start_time = current_time + network_delay
        task.execution_time = execution_time
        task.completion_time = task.start_time + execution_time

        # The allocator has already reserved this task's CPU load.
        task.energy_consumption = self.energy_manager.calculate_energy(
            resource,
            task.start_time,
            task.completion_time
        )

        task.status = "running"

        return task
