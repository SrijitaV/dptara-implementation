
from .models.entities import Task
from .resource_manager import ResourceManager


class ResourceAllocator:
    """
    Deadline-aware resource allocator.

    Workload:
        workload_mi = task.size_mb * instructions_per_mb

    Minimum CPU demand:
        cpu_demand_mips = workload_mi / available_compute_time

    The reserved CPU load and resource capacity are both measured
    in MIPS.
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

    def calculate_cpu_demand(self, task, resource=None):
        """Calculate workload and minimum CPU demand."""

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

        workload = task.size_mb * self.instructions_per_mb

        cpu_demand = workload / available_compute_time

        return workload, cpu_demand

    def _find_least_loaded_resource(
        self,
        resources,
        task,
        current_time=0.0
    ):
        """Find the eligible resource with the lowest projected load."""

        eligible_resources = []

        for resource in resources:

            if resource.status != "active":
                continue

            demand_details = self.calculate_cpu_demand(
                task,
                resource
            )

            if demand_details is None:
                continue

            workload, cpu_demand = demand_details

            # Check available CPU capacity.
            if resource.available_capacity < cpu_demand:
                continue

            # Use processing speed when configured.
            # Otherwise, fall back to the resource's CPU capacity.
            processing_capacity = (
                resource.processing_speed_mips
                if resource.processing_speed_mips > 0
                else resource.capacity
            )

            if processing_capacity < cpu_demand:
                continue

            predicted_utilization = resource.utilization

            # Use prediction when historical observations exist.
            if (
                self.load_predictor is not None
                and resource.resource_id in self.load_predictor.history
                and self.load_predictor.history[resource.resource_id]
            ):
                future_time = current_time + task.deadline

                predicted_utilization = (
                    self.load_predictor.predict_load(
                        resource.resource_id,
                        future_time
                    )
                )

            projected_utilization = (
                predicted_utilization
                + cpu_demand / resource.capacity
            )

            eligible_resources.append(
                (
                    resource,
                    workload,
                    cpu_demand,
                    projected_utilization
                )
            )

        if not eligible_resources:
            return None

        return min(
            eligible_resources,
            key=lambda item: item[3]
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
                task,
                current_time
            )

            if selected is not None:
                break

        if selected is None:
            task.status = "unallocated"
            return None

        (
            selected_resource,
            workload,
            cpu_demand,
            _
        ) = selected

        # Reserve CPU demand in MIPS.
        self.resource_manager.add_load(
            selected_resource.resource_id,
            cpu_demand
        )

        task.workload_mi = workload
        task.cpu_demand_mips = cpu_demand
        task.allocated_load = cpu_demand
        task.assigned_resource = selected_resource.resource_id
        task.status = "allocated"

        return selected_resource

    def release_task(self, task):
        """Release the CPU load reserved for the task."""

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
