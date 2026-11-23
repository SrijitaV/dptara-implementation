
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Allocates tasks using CPU demand measured in MIPS.

    Task input size (MB), computational workload (MI),
    and CPU demand (MIPS) are treated separately.
    """

    def __init__(self, resource_manager, load_predictor=None, strategy=None):

        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("Expected a ResourceManager object.")

        self.resource_manager = resource_manager
        self.load_predictor = load_predictor
        self.strategy = strategy

    def _get_effective_processing_speed(self, task, resource):
        """
        Match TaskExecutor's execution-time calculation.
        """

        return resource.processing_speed_mips

    def _is_deadline_feasible(self, task, resource, current_time):
        """Check whether the task can finish before its deadline."""

        if resource.processing_speed_mips <= 0:
            return False

        if task.workload_mi is None or task.workload_mi <= 0:
            return False

        effective_speed = self._get_effective_processing_speed(
            task, resource
        )

        if effective_speed <= 0:
            return False

        network_delay = resource.network_latency_ms / 1000.0

        estimated_execution = task.workload_mi / effective_speed

        estimated_completion = (
            current_time + network_delay + estimated_execution
        )

        absolute_deadline = task.arrival_time + task.deadline

        return estimated_completion <= absolute_deadline

    def _get_projected_utilization(
        self, resource, task, current_time
    ):
        """Estimate CPU utilization after task allocation."""

        predicted_utilization = resource.utilization

        if (
            self.load_predictor is not None
            and resource.resource_id in self.load_predictor.history
            and self.load_predictor.history[resource.resource_id]
        ):
            absolute_deadline = task.arrival_time + task.deadline

            predicted_utilization = (
                self.load_predictor.predict_load(
                    resource.resource_id,
                    absolute_deadline
                )
            )

        projected_utilization = (
            predicted_utilization
            + task.cpu_demand_mips / resource.capacity
        )

        return projected_utilization

    def _find_least_loaded_resource(
        self, resources, task, current_time
    ):
        """Find the least-loaded eligible resource."""

        eligible_resources = []

        for resource in resources:

            if resource.status != "active":
                continue

            if resource.capacity <= 0:
                continue

            if resource.processing_speed_mips <= 0:
                continue

            if task.cpu_demand_mips > resource.available_capacity:
                continue

            projected_utilization = self._get_projected_utilization(
                resource, task, current_time
            )

            if projected_utilization > 1.0:
                continue

            if not self._is_deadline_feasible(
                task, resource, current_time
            ):
                continue

            eligible_resources.append(
                (resource, projected_utilization)
            )

        if not eligible_resources:
            return None

        if self.strategy is not None:
            return min(
                eligible_resources,
                key=lambda item: self.strategy.resource_score(
                    task, item[0]
                )
            )[0]

        return min(
            eligible_resources,
            key=lambda item: item[1]
        )[0]

    def allocate_task(self, task, current_time=None):
        """Allocate a pending task to a suitable resource."""

        if not isinstance(task, Task):
            raise TypeError("Expected a Task object.")

        if task.status != "pending":
            raise ValueError("Only pending tasks can be allocated.")

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        if task.workload_mi is None or task.workload_mi <= 0:
            raise ValueError("Task workload must be positive.")

        if task.cpu_demand_mips is None or task.cpu_demand_mips <= 0:
            raise ValueError("Task CPU demand must be positive.")

        if current_time is None:
            current_time = task.arrival_time

        absolute_deadline = task.arrival_time + task.deadline

        if current_time > absolute_deadline:
            task.status = "unallocated"
            return None

        all_resources = (
            self.resource_manager.get_available_resources()
        )

        local_edge_resources = [
            resource for resource in all_resources
            if resource.resource_type in ("local", "edge")
        ]

        selected_resource = self._find_least_loaded_resource(
            local_edge_resources,
            task,
            current_time
        )

        # Cloud fallback.
        if selected_resource is None:

            cloud_resources = [
                resource for resource in all_resources
                if resource.resource_type == "cloud"
            ]

            selected_resource = self._find_least_loaded_resource(
                cloud_resources,
                task,
                current_time
            )

        if selected_resource is None:
            task.status = "unallocated"
            return None

        # Reserve CPU demand in MIPS.
        self.resource_manager.add_load(
            selected_resource.resource_id,
            task.cpu_demand_mips
        )

        task.assigned_resource = selected_resource.resource_id
        task.allocated_load = task.cpu_demand_mips
        task.status = "allocated"

        return selected_resource

    def release_task(self, task):
        """Release reserved CPU capacity while preserving assignment metadata."""

        if task.assigned_resource is None:
            raise ValueError("Task has no assigned resource.")

        if task.allocated_load is None:
            raise ValueError("Task allocated load is unavailable.")

        if task.status not in ("allocated", "running"):
            raise ValueError("Task is not in a releasable state.")

        self.resource_manager.release_load(
            task.assigned_resource,
            task.allocated_load
        )
