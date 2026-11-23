
import random
from .models.entities import Task


class TaskGenerator:
    """
    Generates healthcare IoT tasks.

    Task arrivals follow a Poisson process.

    Task size, computational workload and CPU demand are
    generated separately.

    Workload and CPU-demand parameters are implementation
    assumptions because the paper does not specify their
    numerical distributions.
    """

    def __init__(
        self,
        arrival_rate=5.0,
        min_size_mb=5,
        max_size_mb=50,
        min_deadline=10,
        max_deadline=100,
        mi_per_mb=100.0,
        min_cpu_demand_mips=50.0,
        max_cpu_demand_mips=250.0,
        seed=None
    ):
        if arrival_rate <= 0:
            raise ValueError("Arrival rate must be positive.")

        if min_size_mb <= 0 or max_size_mb < min_size_mb:
            raise ValueError("Invalid task size range.")

        if min_deadline <= 0 or max_deadline < min_deadline:
            raise ValueError("Invalid task deadline range.")

        if mi_per_mb <= 0:
            raise ValueError("MI per MB must be positive.")

        if min_cpu_demand_mips <= 0:
            raise ValueError("Minimum CPU demand must be positive.")

        if max_cpu_demand_mips < min_cpu_demand_mips:
            raise ValueError("Invalid CPU demand range.")

        self.arrival_rate = arrival_rate
        self.min_size_mb = min_size_mb
        self.max_size_mb = max_size_mb
        self.min_deadline = min_deadline
        self.max_deadline = max_deadline

        self.mi_per_mb = mi_per_mb
        self.min_cpu_demand_mips = min_cpu_demand_mips
        self.max_cpu_demand_mips = max_cpu_demand_mips

        self.rng = random.Random(seed)
        self.next_task_id = 1

    def _select_task_profile(
        self,
        task_profiles,
        task_type,
        original_priority
    ):
        if task_profiles is None:
            if not task_type:
                raise ValueError("Task type cannot be empty.")

            return task_type, original_priority

        if not task_profiles:
            raise ValueError("Task profiles cannot be empty.")

        weights = []

        for profile in task_profiles:
            required_keys = {
                "task_type",
                "original_priority",
                "probability"
            }

            if not required_keys.issubset(profile):
                raise ValueError(
                    "Each profile must contain task_type, "
                    "original_priority and probability."
                )

            if not profile["task_type"]:
                raise ValueError("Task type cannot be empty.")

            if profile["probability"] < 0:
                raise ValueError("Probability cannot be negative.")

            weights.append(profile["probability"])

        if abs(sum(weights) - 1.0) > 1e-9:
            raise ValueError(
                "Task profile probabilities must sum to 1.0."
            )

        selected = self.rng.choices(
            task_profiles,
            weights=weights,
            k=1
        )[0]

        return (
            selected["task_type"],
            selected["original_priority"]
        )

    def generate_tasks(
        self,
        duration_seconds,
        task_type="normal",
        original_priority=1.0,
        task_profiles=None
    ):
        if duration_seconds < 0:
            raise ValueError("Duration cannot be negative.")

        tasks = []
        current_time = 0.0

        while True:

            inter_arrival_time = self.rng.expovariate(
                self.arrival_rate
            )

            current_time += inter_arrival_time

            if current_time > duration_seconds:
                break

            size_mb = self.rng.uniform(
                self.min_size_mb,
                self.max_size_mb
            )

            deadline = self.rng.uniform(
                self.min_deadline,
                self.max_deadline
            )

            # Computational workload (MI).
            workload_mi = size_mb * self.mi_per_mb

            # CPU demand (MIPS).
            cpu_demand_mips = self.rng.uniform(
                self.min_cpu_demand_mips,
                self.max_cpu_demand_mips
            )

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
                task_type=selected_type,
                workload_mi=round(workload_mi, 2),
                cpu_demand_mips=round(cpu_demand_mips, 2)
            )

            tasks.append(task)
            self.next_task_id += 1

        return tasks
