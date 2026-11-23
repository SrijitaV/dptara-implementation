
import math

from .models.entities import Resource


class ResourceManager:
    """
    Maintains computing resources and tracks their utilization.
    """

    def __init__(self):
        self.resources = {}

    def register_resource(self, resource):

        if not isinstance(resource, Resource):
            raise TypeError("Expected a Resource object.")

        if resource.resource_id in self.resources:
            raise ValueError(
                f"Resource {resource.resource_id} already exists."
            )

        if (
            not math.isfinite(resource.capacity)
            or resource.capacity <= 0
        ):
            raise ValueError(
                "Resource capacity must be positive and finite."
            )

        if (
            not math.isfinite(resource.processing_speed_mips)
            or resource.processing_speed_mips <= 0
        ):
            raise ValueError(
                "Resource processing speed must be positive and finite."
            )

        if (
            not math.isfinite(resource.current_load)
            or not 0 <= resource.current_load <= resource.capacity
        ):
            raise ValueError("Invalid initial resource load.")

        self.resources[resource.resource_id] = resource

    def get_resource(self, resource_id):
        return self.resources.get(resource_id)

    def get_all_resources(self):
        return list(self.resources.values())

    def get_available_resources(self, resource_type=None):

        available = []

        for resource in self.resources.values():

            if resource.status != "active":
                continue

            if resource.available_capacity <= 0:
                continue

            if (
                resource_type is not None
                and resource.resource_type != resource_type
            ):
                continue

            available.append(resource)

        return available

    def add_load(self, resource_id, load):

        resource = self.get_resource(resource_id)

        if resource is None:
            raise ValueError("Resource not found.")

        if resource.status != "active":
            raise ValueError("Resource is not active.")

        if (
            not isinstance(load, (int, float))
            or not math.isfinite(load)
        ):
            raise ValueError("Load must be a finite number.")

        if load <= 0:
            raise ValueError("Load must be positive.")

        tolerance = 1e-10 * max(
            1.0,
            abs(resource.capacity),
            abs(resource.current_load),
            abs(load)
        )

        available = resource.available_capacity

        if load > available + tolerance:
            raise ValueError("Insufficient resource capacity.")

        # Prevent tiny floating-point over-allocation.
        resource.current_load += min(load, available)

    def release_load(self, resource_id, load):

        resource = self.get_resource(resource_id)

        if resource is None:
            raise ValueError("Resource not found.")

        if (
            not isinstance(load, (int, float))
            or not math.isfinite(load)
        ):
            raise ValueError("Load must be a finite number.")

        if load <= 0:
            raise ValueError("Load must be positive.")

        tolerance = 1e-10 * max(
            1.0,
            abs(resource.capacity),
            abs(resource.current_load),
            abs(load)
        )

        if load > resource.current_load + tolerance:
            raise ValueError(
                f"Cannot release more load than allocated. "
                f"Resource: {resource_id}, "
                f"Available load: {resource.current_load}, "
                f"Requested release: {load}"
            )

        remaining_load = resource.current_load - load

        # Correct tiny floating-point residuals.
        if abs(remaining_load) <= tolerance:
            remaining_load = 0.0

        resource.current_load = max(0.0, remaining_load)

    def get_resource_status(self):

        status = []

        for resource in self.resources.values():

            status.append({
                "resource_id": resource.resource_id,
                "resource_type": resource.resource_type,
                "capacity": resource.capacity,
                "current_load": resource.current_load,
                "available_capacity": resource.available_capacity,
                "utilization": resource.utilization,
                "status": resource.status
            })

        return status

    def reset_loads(self):

        for resource in self.resources.values():
            resource.current_load = 0.0
