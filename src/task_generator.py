
import random
from .models.entities import Task


class TaskGenerator:
    """
    Generates healthcare IoT tasks.

    Task arrivals follow a Poisson process, implemented
    using exponentially distributed inter-arrival times.

    Task categories and priority values can be configured
    through task_profiles.

    Any task-category proportions or priority values not
    specified by the paper must be treated as implementation
    assumptions.
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
        if arrival_rate <= 0:
            raise ValueError("Arrival rate must be positive.")

        if min_size_mb <= 0 or max_size_mb < min_size_mb:
            raise ValueError("Invalid task size range.")

        if min_deadline <= 0 or max_deadline < min_deadline:
            raise ValueError("Invalid task deadline range.")

        self.arrival_rate = arrival_rate
        self.min_size_mb = min_size_mb
        self.max_size_mb = max_size_mb
        self.min_deadline = min_deadline
        self.max_deadline = max_deadline

        self.rng = random.Random(seed)
        self.next_task_id = 1

    def _select_task_profile(
        self,
        task_profiles,
        task_type,
        original_priority
    ):
        """
        Select a task category and its original priority.

        Each profile must contain:
            task_type
            original_priority
            probability
        """

        if task_profiles is None:
            if not task_type:
                raise ValueError("Task type cannot be empty.")

            return task_type, original_priority

        if not task_profiles:
            raise ValueError("Task profiles cannot be empty.")

        total_probability = 0.0
        weights = []

        for profile in task_profiles:
            required_keys = {
                "task_type",
                "original_priority",
                "probability"
            }

            if not required_keys.issubset(profile):
                raise ValueError(
                    "Each task profile must contain "
                    "task_type, original_priority, and probability."
                )

            if not profile["task_type"]:
                raise ValueError("Task type cannot be empty.")

            if profile["probability"] < 0:
                raise ValueError("Probability cannot be negative.")

            total_probability += profile["probability"]
            weights.append(profile["probability"])

        if abs(total_probability - 1.0) > 1e-9:
            raise ValueError(
                "Task profile probabilities must sum to 1.0."
            )

        selected_profile = self.rng.choices(
            task_profiles,
            weights=weights,
            k=1
        )[0]

        return (
            selected_profile["task_type"],
            selected_profile["original_priority"]
        )

    def generate_tasks(
        self,
        duration_seconds,
        task_type="normal",
        original_priority=1.0,
        task_profiles=None
    ):
        """
        Generate tasks during the specified simulation duration.

        If task_profiles is provided, task categories and
        priorities are sampled according to their probabilities.

        Otherwise, the original single-category behaviour
        is preserved.
        """

        if duration_seconds < 0:
            raise ValueError("Duration cannot be negative.")

        tasks = []
        current_time = 0.0

        while True:

            # Generate the next inter-arrival time.
            inter_arrival_time = self.rng.expovariate(
                self.arrival_rate
            )

            current_time += inter_arrival_time

            if current_time > duration_seconds:
                break

            # Generate task size.
            size_mb = self.rng.uniform(
                self.min_size_mb,
                self.max_size_mb
            )

            # Generate task deadline.
            deadline = self.rng.uniform(
                self.min_deadline,
                self.max_deadline
            )

            # Select task category and original priority.
            selected_type, selected_priority = (
                self._select_task_profile(
                    task_profiles,
                    task_type,
                    original_priority
                )
            )

            task = Task(
                task_id=self.next_task_id,
                size_mb=round(size_mb, 2),
                original_priority=selected_priority,
                arrival_time=round(current_time, 6),
                deadline=round(deadline, 2),
                task_type=selected_type
            )

            tasks.append(task)
            self.next_task_id += 1

        return tasks
