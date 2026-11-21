
class TaskExecutor:
    """
    Executes allocated tasks using the processing-time model
    specified in DPTARA Equations (6) and (9).

    Computing time = task size / resource processing capacity.

    The resource's configured network latency is treated as
    the total transmission delay in this implementation.
    """

    def execute_task(self, task, resource, current_time):

        # 1. Validate task state and assignment.
        if task.status != "allocated":
            raise ValueError(
                "Task must be allocated before execution."
            )

        if task.assigned_resource != resource.resource_id:
            raise ValueError(
                "Task is not assigned to this resource."
            )

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        # 2. Validate resource.
        if resource.status != "active":
            raise ValueError("Resource is not active.")

        if resource.processing_speed_mips <= 0:
            raise ValueError(
                "Invalid resource processing capacity."
            )

        if resource.network_latency_ms < 0:
            raise ValueError(
                "Network latency cannot be negative."
            )

        if current_time < task.arrival_time:
            raise ValueError(
                "Execution cannot precede task arrival."
            )

        # 3. Calculate computing time independently of deadline.
        execution_time = (
            task.size_mb / resource.processing_speed_mips
        )

        # 4. Calculate transmission delay.
        network_delay = resource.network_latency_ms / 1000.0

        # 5. Calculate execution timestamps.
        task.start_time = current_time + network_delay
        task.execution_time = execution_time
        task.completion_time = (
            task.start_time + execution_time
        )

        # 6. Calculate energy consumption.
        from .energy_manager import EnergyManager

        energy_manager = EnergyManager()

        task.energy_consumption = (
            energy_manager.calculate_energy(
                resource,
                task.start_time,
                task.completion_time
            )
        )

        # 7. Completion is handled by the simulator's event queue.
        task.status = "running"

        return task
