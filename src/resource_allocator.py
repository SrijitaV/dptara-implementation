
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Allocates tasks to local, edge, or cloud resources.

    CPU demand is calculated using:
        Workload (MI) / Deadline (seconds)

    The instructions-per-MB conversion is an
    implementation assumption, not a paper-specified value.
    """

    def __init__(
        self,
        resource_manager,
        instructions_per_mb=1000.0
    ):

        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("Expected a ResourceManager object.")

        if instructions_per_mb <= 0:
            raise ValueError("Instructions per MB must be positive.")

        self.resource_manager = resource_manager
        self.instructions_per_mb = instructions_per_mb

    def calculate_cpu_demand(self, task):
        """
        Estimate task workload and required CPU capacity.

        Workload (MI) = Task size (MB) * Instructions per MB

        CPU demand (MIPS) = Workload (MI) / Deadline (seconds)
        """

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        if task.deadline <= 0:
            raise ValueError("Task deadline must be positive.")

        workload = (
            task.size_mb * self.instructions_per_mb
        )

        cpu_demand = workload / task.deadline

        task.workload_mi = workload
        task.cpu_demand_mips = cpu_demand

        return cpu_demand

    def _find_least_loaded_resource(self, resources, cpu_demand):
        """
        Find the least-utilized resource that can
        accommodate the required CPU demand.
        """

        eligible_resources = [
            resource
            for resource in resources
            if resource.available_capacity >= cpu_demand
        ]

        if not eligible_resources:
            return None

        return min(
            eligible_resources,
            key=lambda resource: resource.utilization
        )

    def allocate_task(self, task):
        """
        Allocate a task using hierarchical allocation.

        Selection order:
            1. Local resources
            2. Edge resources
            3. Cloud resources

        Resources are selected according to available
        CPU capacity and current utilization.
        """

        if not isinstance(task, Task):
            raise TypeError("Expected a Task object.")

        if task.status != "pending":
            raise ValueError("Only pending tasks can be allocated.")

        # Step 1: Calculate task CPU demand
        cpu_demand = self.calculate_cpu_demand(task)

        # Step 2: Retrieve active resources
        all_resources = (
            self.resource_manager.get_available_resources()
        )

        # Step 3: Try local resources first
        local_resources = [
            resource for resource in all_resources
            if resource.resource_type == "local"
        ]

        selected_resource = self._find_least_loaded_resource(
            local_resources,
            cpu_demand
        )

        # Step 4: Try edge resources if local resources fail
        if selected_resource is None:

            edge_resources = [
                resource for resource in all_resources
                if resource.resource_type == "edge"
            ]

            selected_resource = self._find_least_loaded_resource(
                edge_resources,
                cpu_demand
            )

        # Step 5: Try cloud resources if edge resources fail
        if selected_resource is None:

            cloud_resources = [
                resource for resource in all_resources
                if resource.resource_type == "cloud"
            ]

            selected_resource = self._find_least_loaded_resource(
                cloud_resources,
                cpu_demand
            )

        # Step 6: Handle allocation failure
        if selected_resource is None:
            task.status = "unallocated"
            return None

        # Step 7: Reserve CPU capacity
        self.resource_manager.add_load(
            selected_resource.resource_id,
            cpu_demand
        )

        # Step 8: Update task information
        task.assigned_resource = selected_resource.resource_id
        task.status = "allocated"

        return selected_resource


    def release_task(self, task):
        """
        Release CPU capacity reserved for a task.
        """

        if task.assigned_resource is None:
            raise ValueError("Task has no assigned resource.")

        if task.cpu_demand_mips is None:
            raise ValueError("Task CPU demand is unavailable.")

        if task.status not in ("allocated", "running", "completed"):
            raise ValueError("Task is not in a releasable state.")

        self.resource_manager.release_load(
            task.assigned_resource,
            task.cpu_demand_mips
        )

        task.assigned_resource = None

