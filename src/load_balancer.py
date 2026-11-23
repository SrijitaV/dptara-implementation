
import math


class LoadBalancer:
    """
    Measures load distribution using Jain's Fairness Index.

    Resource utilization is used instead of raw load so that
    resources with different capacities can be compared.

    Jain's Fairness Index:
        J = (sum(U_i)^2) / (n * sum(U_i^2))

    The result is returned as a percentage between 0 and 100.
    """

    def calculate_balancing_score(self, resources):

        if not resources:
            raise ValueError(
                "Resource list cannot be empty."
            )

        utilizations = []

        for resource in resources:

            if resource.capacity <= 0:
                raise ValueError(
                    f"Invalid capacity for resource {resource.resource_id}."
                )

            utilization = resource.utilization

            if not math.isfinite(utilization):
                raise ValueError(
                    f"Invalid utilization for resource {resource.resource_id}."
                )

            if utilization < 0 or utilization > 1:
                raise ValueError(
                    f"Utilization outside valid range for resource "
                    f"{resource.resource_id}."
                )

            utilizations.append(utilization)

        n = len(utilizations)

        sum_utilization = sum(utilizations)

        sum_squared = sum(
            utilization ** 2
            for utilization in utilizations
        )

        # No resource is being used.
        if sum_squared == 0:
            return 100.0

        # Jain's Fairness Index.
        score = (
            (sum_utilization ** 2)
            / (n * sum_squared)
        ) * 100.0

        return max(0.0, min(100.0, score))

    def calculate_balancing_rate(
        self,
        target_resource,
        resources
    ):
        """
        Compatibility method.

        Returns the system-wide Jain's Fairness Index.
        """

        if not any(
            resource.resource_id == target_resource.resource_id
            for resource in resources
        ):
            raise ValueError(
                "Target resource not found."
            )

        return self.calculate_balancing_score(resources)

    def calculate_all_balancing_rates(self, resources):
        """
        Returns the system-wide fairness score for each resource.

        Note:
            These are system-wide scores, not individual
            resource balancing rates.
        """

        score = self.calculate_balancing_score(resources)

        return {
            resource.resource_id: score
            for resource in resources
        }
