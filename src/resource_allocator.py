
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Allocates tasks using the resource-selection logic in DPTARA.

    A resource is eligible when:
        current_load + task.size_mb <= resource.capacity

    Selects the least-loaded eligible local/edge resource.
    Uses cloud resources as a fallback.
    """

    def __init__(self, resource_manager, load_predictor=None):
        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("Expected a ResourceManager object.")

        self.resource_manager = resource_manager
        self.load_predictor = load_predictor

    def _find_least_loaded_resource(
        self,
        resources,
        task,
        current_time=None
    ):
        """Find the least-loaded resource that can accommodate the task."""

        eligible_resources = []

        for resource in resources:

            if resource.status != "active":
                continue

            if resource.capacity <= 0:
                continue

            # Paper's allocation condition:
            # current_load + task_size <= resource_capacity
            if task.size_mb > resource.available_capacity:
                continue

            predicted_utilization = resource.utilization

            # Use the load predictor when historical observations exist.
            if (
                self.load_predictor is not None
                and resource.resource_id in self.load_predictor.history
                and self.load_predictor.history[resource.resource_id]
            ):
                future_time = (
                    current_time + task.deadline
                    if current_time is not None
                    else task.arrival_time + task.deadline
                )

                predicted_utilization = (
                    self.load_predictor.predict_load(
                        resource.resource_id,
                        future_time
                    )
                )

            projected_utilization = (
                predicted_utilization
                + task.size_mb / resource.capacity
            )

            eligible_resources.append(
                (resource, projected_utilization)
            )

        if not eligible_resources:
            return None

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

        all_resources = (
            self.resource_manager.get_available_resources()
        )

        # First, consider local and edge resources together.
        local_edge_resources = [
            resource for resource in all_resources
            if resource.resource_type in ("local", "edge")
        ]

        selected_resource = self._find_least_loaded_resource(
            local_edge_resources,
            task,
            current_time
        )

        # If no local/edge resource is suitable, try the cloud.
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

        # Reserve the task size as the allocation load,
        # following the paper's Algorithm 1.
        self.resource_manager.add_load(
            selected_resource.resource_id,
            task.size_mb
        )

        task.assigned_resource = selected_resource.resource_id
        task.allocated_load = task.size_mb

        # CPU demand is not separately specified by the paper.
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
