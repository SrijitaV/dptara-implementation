
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Paper-inspired task allocator.

    IMPORTANT:
    Task size (MB) is used as a normalized load proxy because
    the paper does not specify a per-task CPU-demand model.
    This must not be interpreted as physical CPU utilization.
    """

    def __init__(self, resource_manager, load_predictor=None, strategy=None):
        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("Expected a ResourceManager object.")

        self.resource_manager = resource_manager
        self.load_predictor = load_predictor
        self.strategy = strategy

    def _is_deadline_feasible(self, task, resource, current_time):
        """Estimate whether execution can finish before the deadline."""

        if resource.processing_speed_mips <= 0:
            return False

        network_delay = resource.network_latency_ms / 1000.0

        # Retain the paper's execution-time equation.
        estimated_execution = (
            task.size_mb / resource.processing_speed_mips
        )

        estimated_completion = (
            current_time + network_delay + estimated_execution
        )

        absolute_deadline = task.arrival_time + task.deadline

        return estimated_completion <= absolute_deadline

    def _get_projected_utilization(
        self, resource, task, current_time
    ):
        """Estimate normalized load after allocating this task."""

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
            + task.size_mb / resource.capacity
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

            # Existing normalized-load capacity check.
            if task.size_mb > resource.available_capacity:
                continue

            # Reject resources predicted to exceed capacity.
            projected_utilization = self._get_projected_utilization(
                resource, task, current_time
            )

            if projected_utilization > 1.0:
                continue

            # Reject resources that cannot meet the task deadline.
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

        # Reserve the existing normalized load proxy.
        self.resource_manager.add_load(
            selected_resource.resource_id,
            task.size_mb
        )

        task.assigned_resource = selected_resource.resource_id
        task.allocated_load = task.size_mb

        # No per-task CPU demand is specified by the paper.
        task.workload_mi = None
        task.cpu_demand_mips = None

        task.status = "allocated"

        return selected_resource

    def release_task(self, task):
        """Release the load reserved for an allocated task."""

        if task.assigned_resource is None:
            raise ValueError("Task has no assigned resource.")

        if task.allocated_load is None:
            raise ValueError("Task allocated load is unavailable.")

        if task.status not in (
            "allocated",
            "running",
            "completed"
        ):
            raise ValueError("Task is not in a releasable state.")

        self.resource_manager.release_load(
            task.assigned_resource,
            task.allocated_load
        )

        task.assigned_resource = None
        task.allocated_load = None
