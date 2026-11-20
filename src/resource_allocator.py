
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Allocates tasks to local, edge, or cloud resources.

    Workload (MI) = Task size (MB) * Instructions per MB

    Available compute time =
        Task deadline - Network delay

    CPU demand (MIPS) =
        Workload / Available compute time

    Instructions per MB is an implementation assumption.
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

    def calculate_cpu_demand(self, task, resource=None):
        """
        Calculate CPU demand after accounting for
        the selected resource's network latency.
        """

        if task.size_mb <= 0:
            raise ValueError("Task size must be positive.")

        if task.deadline <= 0:
            raise ValueError("Task deadline must be positive.")

        network_delay = 0.0

        if resource is not None:
            network_delay = resource.network_latency_ms / 1000.0

        available_compute_time = task.deadline - network_delay

        if available_compute_time <= 0:
            return None

        workload = (
            task.size_mb * self.instructions_per_mb
        )

        cpu_demand = workload / available_compute_time

        return workload, cpu_demand

    def _find_least_loaded_resource(self, resources, task):
        """
        Find the least-utilized resource that can
        accommodate the deadline-aware CPU demand.
        """

        eligible_resources = []

        for resource in resources:

            demand_details = self.calculate_cpu_demand(
                task,
                resource
            )

            if demand_details is None:
                continue

            workload, cpu_demand = demand_details

            if resource.available_capacity >= cpu_demand:
                eligible_resources.append(
                    (resource, workload, cpu_demand)
                )

        if not eligible_resources:
            return None

        return min(
            eligible_resources,
            key=lambda item: item[0].utilization
        )

    def allocate_task(self, task):
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

        all_resources = (
            self.resource_manager.get_available_resources()
        )

        resource_groups = [
            [
                resource for resource in all_resources
                if resource.resource_type == "local"
            ],
            [
                resource for resource in all_resources
                if resource.resource_type == "edge"
            ],
            [
                resource for resource in all_resources
                if resource.resource_type == "cloud"
            ]
        ]

        selected = None

        for group in resource_groups:

            selected = self._find_least_loaded_resource(
                group,
                task
            )

            if selected is not None:
                break

        if selected is None:
            task.status = "unallocated"
            return None

        selected_resource, workload, cpu_demand = selected

        self.resource_manager.add_load(
            selected_resource.resource_id,
            cpu_demand
        )

        task.workload_mi = workload
        task.cpu_demand_mips = cpu_demand
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

        if task.status not in (
            "allocated",
            "running",
            "completed"
        ):
            raise ValueError("Task is not in a releasable state.")

        self.resource_manager.release_load(
            task.assigned_resource,
            task.cpu_demand_mips
        )

        task.assigned_resource = None
