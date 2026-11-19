
class DynamicPriorityModel:
    """
    Calculates dynamic task priorities using the DPTARA
    priority equation (Equation 11).
    """

    def __init__(self, alpha=1.0, beta=1.0, gamma=1.0):

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def calculate_priority(self, task, current_time, current_load=0.0):
        """
        Calculate the dynamic priority of a task.

        Parameters:
            task: Task object
            current_time: Current simulation time
            current_load: Load on the resource handling the task

        Returns:
            Calculated dynamic priority
        """

        if task.deadline <= 0:
            raise ValueError("Task deadline must be positive.")

        if current_time < task.arrival_time:
            raise ValueError("Current time cannot precede task arrival.")

        if current_load < 0:
            raise ValueError("Current load cannot be negative.")

        # Calculate task aging factor
        aging_factor = (
            (current_time - task.arrival_time) / task.deadline
        )

        # Apply DPTARA Equation (11)
        priority = (
            self.alpha * task.original_priority
            + self.beta * aging_factor
            - self.gamma * current_load
        )

        return priority

    def update_priority(self, task, current_time, current_load=0.0):
        """
        Update the priority attribute of the task.
        """

        task.priority = self.calculate_priority(
            task,
            current_time,
            current_load
        )

        return task.priority
