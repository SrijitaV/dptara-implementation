
"""
Paper-informed baseline strategy variants for DPTARA comparison.

These are transparent experimental adaptations, not claimed
exact reproductions of the original baseline papers.
"""


class BaseStrategy:
    name = "Base"

    def task_score(self, task, current_time):
        return 0.0

    def resource_score(self, task, resource):
        return 0.0

    def rank_tasks(self, tasks, current_time):
        return sorted(
            tasks,
            key=lambda task: (
                -self.task_score(task, current_time),
                task.arrival_time,
                task.task_id
            )
        )

    def rank_resources(self, task, resources):
        return sorted(
            resources,
            key=lambda resource: self.resource_score(task, resource)
        )


class APBRAStrategy(BaseStrategy):
    """Priority-based resource allocation heuristic."""

    name = "A-PBRA"

    PRIORITY_TYPES = {
        "critical", "high", "priority", "emergency"
    }

    def task_score(self, task, current_time):
        task_type = str(task.task_type).lower()

        if task_type in self.PRIORITY_TYPES:
            return 2.0 + task.original_priority

        return task.original_priority

    def resource_score(self, task, resource):
        return (
            resource.utilization,
            resource.network_latency_ms
        )


class NBIHAStrategy(BaseStrategy):
    """Resource-characteristic matching heuristic."""

    name = "NBIHA"

    def task_score(self, task, current_time):
        remaining_time = (
            task.arrival_time + task.deadline - current_time
        )
        return -remaining_time

    def resource_score(self, task, resource):
        speed = max(resource.processing_speed_mips, 1e-9)
        power = max(resource.power_consumption_w, 0.0)

        workload = task.workload_mi

        if workload is None or workload <= 0:
            raise ValueError("Task must have a valid workload in MI.")

        compute_time = workload / speed
        network_delay = resource.network_latency_ms / 1000.0

        return (
            resource.utilization
            + compute_time
            + network_delay
            + power / 1000.0
        )


class CORAGTStrategy(BaseStrategy):
    """
    Game-inspired utility-based resource selection heuristic.

    Uses a congestion-sensitive penalty and a nonlinear
    utilization cost. This is an experimental adaptation,
    not an exact reproduction of the original CORA-GT method.
    """

    name = "CORA-GT"

    def task_score(self, task, current_time):
        remaining_time = (
            task.arrival_time + task.deadline - current_time
        )
        return -remaining_time

    def resource_score(self, task, resource):
        speed = max(resource.processing_speed_mips, 1e-9)
        power = max(resource.power_consumption_w, 0.0)

        workload = task.workload_mi

        if workload is None or workload <= 0:
            raise ValueError("Task must have a valid workload in MI.")

        utilization = max(0.0, min(resource.utilization, 1.0))

        compute_time = workload / speed
        network_delay = resource.network_latency_ms / 1000.0

        # Nonlinear congestion penalty.
        congestion_penalty = utilization ** 2

        # Resource cost considers execution delay and energy.
        execution_cost = compute_time + network_delay
        energy_cost = power / 1000.0

        # Lower score represents a more desirable resource.
        return (
            execution_cost * (1.0 + 2.0 * utilization)
            + congestion_penalty
            + energy_cost
        )


def get_strategy(name):
    """Return a baseline strategy by its registered name."""

    strategies = {
        "A-PBRA": APBRAStrategy,
        "NBIHA": NBIHAStrategy,
        "CORA-GT": CORAGTStrategy
    }

    if name not in strategies:
        raise ValueError(f"Unknown baseline strategy: {name}")

    return strategies[name]()
