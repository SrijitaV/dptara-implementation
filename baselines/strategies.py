
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
    """
    Adaptive priority-based resource allocation proxy.

    Priority/critical tasks are considered before normal tasks.
    Within a resource tier, prefer lower normalized load and
    lower network delay.
    """

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
    """
    Resource-characteristic matching proxy.

    Ranks resources using normalized load, processing speed,
    network latency, and power consumption.

    The paper's per-task CPU demand is unspecified, so task
    size is not treated as a fabricated CPU requirement.
    """

    name = "NBIHA"

    def task_score(self, task, current_time):
        # Earlier deadlines receive preference.
        remaining_time = (
            task.arrival_time + task.deadline - current_time
        )
        return -remaining_time

    def resource_score(self, task, resource):
        speed = max(resource.processing_speed_mips, 1e-9)
        power = max(resource.power_consumption_w, 0.0)

        return (
            resource.utilization
            + (1.0 / speed)
            + (resource.network_latency_ms / 1000.0)
            + (power / 1000.0)
        )


class CORAGTStrategy(BaseStrategy):
    """
    Game-inspired utility-based resource selection proxy.

    Balances processing capability against congestion,
    network delay, and power consumption.

    This is not an exact reconstruction of the original
    CORA-GT game or its payoff function.
    """

    name = "CORA-GT"

    def task_score(self, task, current_time):
        remaining_time = (
            task.arrival_time + task.deadline - current_time
        )

        # Prefer tasks with less remaining deadline slack.
        return -remaining_time

    def resource_score(self, task, resource):
        speed = max(resource.processing_speed_mips, 1e-9)
        power = max(resource.power_consumption_w, 0.0)

        estimated_compute_time = task.size_mb / speed
        network_delay = resource.network_latency_ms / 1000.0

        utility = (
            1.0
            - resource.utilization
            - estimated_compute_time
            - network_delay
            - (power / 1000.0)
        )

        # Lower score means higher utility.
        return -utility


def get_strategy(name):
    """Return a baseline strategy by its registered name."""

    strategies = {
        "A-PBRA": APBRAStrategy,
        "NBIHA": NBIHAStrategy,
        "CORA-GT": CORAGTStrategy
    }

    if name not in strategies:
        raise ValueError(
            f"Unknown baseline strategy: {name}"
        )

    return strategies[name]()
