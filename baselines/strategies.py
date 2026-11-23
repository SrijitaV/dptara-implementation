
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
    Priority-based resource allocation heuristic.

    Prioritizes critical task types and prefers less-loaded resources.
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
    Resource-characteristic matching heuristic.

    Prefers resources that can accommodate the task while
    minimizing projected utilization and network delay.
    """

    name = "NBIHA"

    def task_score(self, task, current_time):
        remaining_time = (
            task.arrival_time + task.deadline - current_time
        )

        # Prioritize tasks with less remaining time.
        return -remaining_time

    def resource_score(self, task, resource):

        capacity = max(resource.capacity, 1e-9)

        workload = task.workload_mi
        demand = task.cpu_demand_mips

        if workload is None or workload <= 0:
            raise ValueError("Task must have a valid workload in MI.")

        if demand is None or demand <= 0:
            raise ValueError("Task must have valid CPU demand in MIPS.")

        # Execution time must match TaskExecutor.
        execution_time = workload / demand

        projected_utilization = (
            resource.current_load + demand
        ) / capacity

        network_delay = resource.network_latency_ms / 1000.0

        return (
            projected_utilization,
            execution_time,
            network_delay
        )


class CORAGTStrategy(BaseStrategy):
    """
    Game-inspired utility-based resource selection heuristic.

    Uses task urgency, task priority, nonlinear congestion,
    execution delay, and energy-related resource cost.

    This is an experimental adaptation, not an exact
    reproduction of the original CORA-GT method.
    """

    name = "CORA-GT"

    def task_score(self, task, current_time):
        remaining_time = max(
            task.arrival_time + task.deadline - current_time,
            0.001
        )

        urgency = 1.0 / remaining_time

        return (
            0.5 * task.original_priority
            + 10.0 * urgency
        )

    def resource_score(self, task, resource):

        capacity = max(resource.capacity, 1e-9)

        workload = task.workload_mi
        demand = task.cpu_demand_mips

        if workload is None or workload <= 0:
            raise ValueError("Task must have a valid workload in MI.")

        if demand is None or demand <= 0:
            raise ValueError("Task must have valid CPU demand in MIPS.")

        projected_utilization = min(
            (resource.current_load + demand) / capacity,
            1.0
        )

        # Must match TaskExecutor's fixed CPU reservation model.
        execution_time = workload / demand

        network_delay = resource.network_latency_ms / 1000.0

        power_cost = resource.power_consumption_w / 1000.0

        congestion_cost = projected_utilization ** 2

        return (
            0.5 * execution_time
            + 0.3 * network_delay
            + 0.1 * power_cost
            + 0.1 * congestion_cost
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
