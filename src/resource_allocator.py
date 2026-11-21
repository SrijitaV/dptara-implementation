
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Resource allocation based on DPTARA Algorithm 1.

    Capacity condition:
        resource.current_load + task.size_mb <= resource.capacity

    Eligible resources are ranked by current load.
    Local/edge resources are preferred; cloud is the fallback.

    Note:
        The paper's allocation equation compares task size with
        resource capacity. This implementation preserves that
        equation, while documenting the unit ambiguity.
    """

    def __init__(
        self,
        resource_manager,
        instructions_per_mb=1000.0,
        load_predictor=None
    ):
        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("Expected a ResourceManager object.")

        if instructions_per_mb <= 0:
            raise ValueError("Instructions per MB must be positive.")

        self.resource_manager = resource_manager
        self.instructions_per_mb = instructions_per_mb
        self.load_predictor = load_predictor

    def _find_least_loaded_resource(self, resources, task):
        eligible_resources = []

        for resource in resources:
            if resource.status != "active":
                continue

            if (
                resource.current_load + task.size_mb
                <= resource.capacity
            ):
                eligible_resources.append(resource)

        if not eligible_resources:
            return None

        return min(
            eligible_resources,
            key=lambda resource: resource.current_load
        )

    def allocate_task(self, task, current_time=0.0):
        """
        Hierarchical allocation:
            1. Local resources
            2. Edge resources
            3. Cloud resources
        """

        if not isinstance(task, Task):
            raise TypeError("Expected a Task object.")

        if task.status != "pending":
            raise ValueError("Only pending tasks can be allocated.")

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        all_resources = (
            self.resource_manager.get_available_resources()
        )

        local_edge_resources = [
            resource for resource in all_resources
            if resource.resource_type in ("local", "edge")
        ]

        cloud_resources = [
            resource for resource in all_resources
            if resource.resource_type == "cloud"
        ]

        selected_resource = self._find_least_loaded_resource(
            local_edge_resources,
            task
        )

        if selected_resource is None:
            selected_resource = self._find_least_loaded_resource(
                cloud_resources,
                task
            )

        if selected_resource is None:
            task.status = "unallocated"
            return None

        # Reserve the task-size load specified by Algorithm 1.
        self.resource_manager.add_load(
            selected_resource.resource_id,
            task.size_mb
        )

        task.assigned_resource = selected_resource.resource_id
        task.allocated_load = task.size_mb
        task.status = "allocated"

        return selected_resource

    def release_task(self, task):
        """Release the reserved resource load after task completion."""

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
