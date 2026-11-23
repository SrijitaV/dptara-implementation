
class LoadBalancer:
    """
    Measures load distribution using Jain's fairness index.

    Utilization is used instead of raw load so that resources
    with different capacities can be compared.
    """

    def calculate_balancing_score(self, resources):

        if not resources:
            raise ValueError("Resource list cannot be empty.")

        utilizations = [
            max(0.0, min(1.0, resource.utilization))
            for resource in resources
        ]

        n = len(utilizations)
        sum_utilization = sum(utilizations)
        sum_squared = sum(u * u for u in utilizations)

        if sum_squared == 0:
            return 100.0

        score = (
            (sum_utilization ** 2)
            / (n * sum_squared)
        ) * 100.0

        return score

    def calculate_balancing_rate(self, target_resource, resources):
        """
        Compatibility method. Returns the system-wide score.
        """

        if not any(
            r.resource_id == target_resource.resource_id
            for r in resources
        ):
            raise ValueError("Target resource not found.")

        return self.calculate_balancing_score(resources)

    def calculate_all_balancing_rates(self, resources):
        """
        Returns the same system-wide score for each resource.
        """

        score = self.calculate_balancing_score(resources)

        return {
            resource.resource_id: score
            for resource in resources
        }
