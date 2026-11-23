
from .energy_manager import EnergyManager


class TaskExecutor:

    def __init__(self, energy_manager=None):
        self.energy_manager = energy_manager or EnergyManager()

    def execute_task(self, task, resource, current_time):

        if task.status != "allocated":
            raise ValueError("Task must be allocated before execution.")

        if task.assigned_resource != resource.resource_id:
            raise ValueError("Task-resource assignment mismatch.")

        if task.workload_mi is None or task.workload_mi <= 0:
            raise ValueError("Task workload must be positive.")

        if task.cpu_demand_mips is None or task.cpu_demand_mips <= 0:
            raise ValueError("Task CPU demand must be positive.")

        if resource.processing_speed_mips <= 0:
            raise ValueError("Resource processing speed must be positive.")

        if task.cpu_demand_mips > resource.processing_speed_mips:
            raise ValueError("Task CPU demand exceeds resource processing speed.")

        if current_time < task.arrival_time:
            raise ValueError("Execution cannot start before task arrival.")

        # Use the CPU capacity reserved for this task.
        effective_processing_speed = task.cpu_demand_mips

        execution_time = (
            task.workload_mi / effective_processing_speed
        )

        network_delay = resource.network_latency_ms / 1000.0

        task.start_time = current_time + network_delay
        task.execution_time = execution_time
        task.completion_time = task.start_time + execution_time

        task.energy_consumption = self.energy_manager.calculate_energy(
            resource,
            task.start_time,
            task.completion_time
        )

        task.status = "running"

        return task

