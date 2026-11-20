
class TaskExecutor:
    """
    Executes allocated tasks on computing resources.

    Computational execution time:
        Workload (MI) / Allocated CPU demand (MIPS)

    The workload conversion factor is an implementation
    assumption, not a parameter specified by the paper.
    """

    def execute_task(self, task, resource, current_time):

        # 1. Validate task
        if task.status != "allocated":
            raise ValueError("Task must be allocated before execution.")

        if task.assigned_resource != resource.resource_id:
            raise ValueError("Task is not assigned to this resource.")

        if task.workload_mi is None or task.workload_mi <= 0:
            raise ValueError("Invalid computational workload.")

        if task.cpu_demand_mips is None or task.cpu_demand_mips <= 0:
            raise ValueError("Invalid allocated CPU demand.")

        # 2. Validate resource
        if resource.status != "active":
            raise ValueError("Resource is not active.")

        if resource.processing_speed_mips <= 0:
            raise ValueError("Invalid resource processing speed.")

        if task.cpu_demand_mips > resource.processing_speed_mips:
            raise ValueError("Allocated CPU demand exceeds processing speed.")

        if resource.network_latency_ms < 0:
            raise ValueError("Network latency cannot be negative.")

        if current_time < task.arrival_time:
            raise ValueError("Execution cannot precede task arrival.")

        # 3. Calculate computational execution time
        execution_time = task.workload_mi / task.cpu_demand_mips

        # 4. Calculate network delay
        network_delay = resource.network_latency_ms / 1000.0

        # 5. Calculate execution timestamps
        task.start_time = current_time + network_delay
        task.execution_time = execution_time
        task.completion_time = task.start_time + execution_time

        # 6. Calculate energy consumption
        from .energy_manager import EnergyManager

        energy_manager = EnergyManager()

        task.energy_consumption = energy_manager.calculate_energy(
            resource,
            task.start_time,
            task.completion_time
        )

        # 7. Task is now running, not completed.
        # Completion is recorded when its event is processed.
        task.status = "running"

        return task
