
class LoadBalancer:
    """
    Calculates load balancing rates across computing resources
    using Algorithm 3 of the DPTARA research paper.
    """

    def calculate_balancing_rate(self, target_resource, resources):
        """
        Calculate balancing rate for a selected resource.

        Parameters:
            target_resource: Resource whose balancing rate is calculated.
            resources: List of all computing resources.

        Returns:
            Load balancing rate as a percentage.
        """

        if not resources:
            raise ValueError("Resource list cannot be empty.")

        if not any(
            r.resource_id == target_resource.resource_id
            for r in resources
        ):
            raise ValueError("Target resource not found.")

        # Step 1: Calculate total resource load
        total_load = sum(
            resource.current_load
            for resource in resources
        )

        # Step 2: Count total resources
        num_resources = len(resources)

        # Step 3: Calculate average load
        average_load = total_load / num_resources

        # Handle the case where all resources have zero load
        if average_load == 0:
            return 100.0

        # Step 4: Calculate balancing rate
        balancing_rate = (
            1 - abs(
                target_resource.current_load - average_load
            ) / average_load
        ) * 100

        # Step 5: Return balancing rate
        return balancing_rate

    def calculate_all_balancing_rates(self, resources):
        """
        Calculate balancing rates for all resources.
        """

        return {
            resource.resource_id:
                self.calculate_balancing_rate(resource, resources)
            for resource in resources
        }
