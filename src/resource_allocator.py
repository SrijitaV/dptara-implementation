
from .models.entities import Task, Resource
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Allocates tasks to local, edge, or cloud resources
    using the DPTARA resource allocation strategy.
    """

    def __init__(self, resource_manager):
        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("Expected a ResourceManager object.")

        self.resource_manager = resource_manager

    def _find_least_loaded_resource(self, resources, task):
        """
        Find the least-loaded resource that can accommodate
        the given task.
        """

        eligible_resources = [
            resource
            for resource in resources
            if resource.current_load + task.size_mb
            <= resource.capacity
        ]

        if not eligible_resources:
            return None

        return min(
            eligible_resources,
            key=lambda resource: resource.current_load
        )

    def allocate_task(self, task):
        """
        Allocate a task using hierarchical resource allocation.

        Selection order:
        1. Local/edge resources
        2. Cloud resource
        3. No allocation if all resources are overloaded
        """

        if not isinstance(task, Task):
            raise TypeError("Expected a Task object.")

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        # Step 1: Get active local and edge resources
        all_resources = self.resource_manager.get_available_resources()

        local_edge_resources = [
            resource
            for resource in all_resources
            if resource.resource_type in ("local", "edge")
        ]

        # Step 2: Select the least-loaded eligible resource
        selected_resource = self._find_least_loaded_resource(
            local_edge_resources,
            task
        )

        # Step 3: If local/edge cannot handle the task,
        # try cloud resources
        if selected_resource is None:

            cloud_resources = [
                resource
                for resource in all_resources
                if resource.resource_type == "cloud"
            ]

            selected_resource = self._find_least_loaded_resource(
                cloud_resources,
                task
            )

        # Step 4: Handle resource unavailability
        if selected_resource is None:
            task.status = "unallocated"
            return None

        # Step 5: Reserve the resource capacity
        self.resource_manager.add_load(
            selected_resource.resource_id,
            task.size_mb
        )

        # Step 6: Update task allocation information
        task.assigned_resource = selected_resource.resource_id
        task.status = "allocated"

        return selected_resource
