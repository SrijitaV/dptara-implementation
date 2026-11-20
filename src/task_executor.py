
class TaskExecutor:
    """
    Executes allocated tasks on computing resources.

    Execution-time calculation uses a configurable workload
    conversion factor because the paper does not specify
    instructions per MB.
    """

    def __init__(self, instructions_per_mb=1000.0):
        if instructions_per_mb <= 0:
            raise ValueError(
                "Instructions per MB must be positive."
            )

        self.instructions_per_mb = instructions_per_mb

    def execute_task(self, task, resource, current_time):
        """
        Execute a task on its assigned computing resource.

        Execution time:
            (Task Size in MB * Instructions per MB)
            / Processing Speed in MIPS

        Network latency is added separately.
        """

        if task.status not in ("allocated", "pending"):
            raise ValueError("Task cannot be executed in its current state.")

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        if resource.processing_speed_mips <= 0:
            raise ValueError("Invalid resource processing speed.")

        if resource.status != "active":
            raise ValueError("Resource is not active.")

        if current_time < task.arrival_time:
            raise ValueError("Execution cannot precede task arrival.")

        if resource.current_load <= 0:
            raise ValueError("Resource has no allocated load.")

        # Step 1: Calculate computational workload
        workload_mi = (
            task.size_mb * self.instructions_per_mb
        )

        # Step 2: Calculate execution duration
        execution_time = (
            workload_mi / resource.processing_speed_mips
        )

        # Step 3: Calculate network delay
        network_delay = resource.network_latency_ms / 1000.0

        # Step 4: Calculate execution start and completion times
        task.start_time = current_time + network_delay

        task.execution_time = execution_time

        task.completion_time = (
            task.start_time + execution_time
        )

        # Step 5: Calculate energy consumption
        from .energy_manager import EnergyManager

        energy_manager = EnergyManager()

        task.energy_consumption = energy_manager.calculate_energy(
            resource,
            task.start_time,
            task.completion_time
        )

        # Step 6: Update task status
        task.status = "completed"

        return task