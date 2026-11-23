
class EnergyManager:
    """
    Calculates resource efficiency and energy consumption.

    Equation (14):
        eta = (U_effective / C_total) * (1 - R_downtime)

    Equation (15):
        E = (P / eta) * execution_duration

    Resource current_load already includes allocated CPU demand.
    """

    def calculate_efficiency(self, resource):

        if resource.capacity <= 0:
            raise ValueError("Resource capacity must be positive.")

        if not 0 <= resource.downtime_rate <= 1:
            raise ValueError(
                "Downtime rate must be between 0 and 1."
            )

        if resource.current_load < 0:
            raise ValueError("Resource load cannot be negative.")

        if resource.current_load > resource.capacity:
            raise ValueError("Resource load exceeds capacity.")

        effective_utilization = (
            resource.current_load / resource.capacity
        )

        efficiency = (
            effective_utilization
            * (1 - resource.downtime_rate)
        )

        return efficiency

    def calculate_energy(self, resource, start_time, end_time):

        if start_time < 0 or end_time < 0:
            raise ValueError(
                "Execution timestamps cannot be negative."
            )

        if end_time < start_time:
            raise ValueError(
                "End time cannot precede start time."
            )

        if resource.power_consumption_w < 0:
            raise ValueError(
                "Power consumption cannot be negative."
            )

        efficiency = self.calculate_efficiency(resource)

        if efficiency <= 0:
            raise ValueError(
                "Cannot calculate energy with zero efficiency."
            )

        execution_duration = end_time - start_time

        energy = (
            resource.power_consumption_w / efficiency
        ) * execution_duration

        return energy

    def calculate_total_energy(self, energy_values):
        return sum(energy_values)
