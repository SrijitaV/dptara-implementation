
import random
from .models.entities import Task


class TaskGenerator:
    """
    Generates healthcare IoT tasks using the simulation
    parameters specified in the DPTARA research paper.
    """

    def __init__(
        self,
        arrival_rate=5.0,
        min_size_mb=5,
        max_size_mb=50,
        min_deadline=10,
        max_deadline=100,
        seed=None
    ):
        self.arrival_rate = arrival_rate

        self.min_size_mb = min_size_mb
        self.max_size_mb = max_size_mb

        self.min_deadline = min_deadline
        self.max_deadline = max_deadline

        self.rng = random.Random(seed)

        self.next_task_id = 1

    def generate_tasks(
        self,
        duration_seconds,
        task_type,
        original_priority
    ):
        """
        Generate tasks during the specified simulation duration.

        Inter-arrival times follow an exponential distribution,
        producing a Poisson arrival process.
        """

        if duration_seconds < 0:
            raise ValueError("Duration cannot be negative.")

        if self.arrival_rate <= 0:
            raise ValueError("Arrival rate must be positive.")

        if not task_type:
            raise ValueError("Task type cannot be empty.")

        tasks = []
        current_time = 0.0

        while True:

            # Generate time until the next task arrives
            inter_arrival_time = self.rng.expovariate(
                self.arrival_rate
            )

            current_time += inter_arrival_time

            # Stop when simulation duration is exceeded
            if current_time > duration_seconds:
                break

            # Generate task size
            size_mb = self.rng.uniform(
                self.min_size_mb,
                self.max_size_mb
            )

            # Generate task deadline
            deadline = self.rng.uniform(
                self.min_deadline,
                self.max_deadline
            )

            # Create task using the existing Task model
            task = Task(
                task_id=self.next_task_id,
                size_mb=round(size_mb, 2),
                original_priority=original_priority,
                arrival_time=round(current_time, 6),
                deadline=round(deadline, 2),
                task_type=task_type
            )

            tasks.append(task)

            self.next_task_id += 1

        return tasks
