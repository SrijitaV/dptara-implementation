
class EnergyManager:
    """
    Calculates resource efficiency and energy consumption.

    Equation (14):
        eta = (U_effective / C_total) * (1 - R_downtime)

    Equation (15):
        E = (P / eta) * execution_duration

    CPU utilization is measured using MIPS.
    """

    def calculate_efficiency(self, resource):

        # Validate resource capacity.
        if resource.capacity <= 0:
            raise ValueError(
                "Resource capacity must be positive."
            )

        # Validate downtime rate.
        if not 0 <= resource.downtime_rate <= 1:
            raise ValueError(
                "Downtime rate must be between 0 and 1."
            )

        # Validate current resource load.
        if resource.current_load < 0:
            raise ValueError(
                "Resource load cannot be negative."
            )

        if resource.current_load > resource.capacity:
            raise ValueError(
                "Resource load exceeds capacity."
            )

        # Calculate effective utilization.
        effective_utilization = (
            resource.current_load / resource.capacity
        )

        # Equation (14).
        efficiency = (
            effective_utilization
            * (1 - resource.downtime_rate)
        )

        return efficiency

    def calculate_energy(
        self,
        resource,
        start_time,
        end_time
    ):

        # Validate execution timestamps.
        if start_time < 0 or end_time < 0:
            raise ValueError(
                "Execution timestamps cannot be negative."
            )

        if end_time < start_time:
            raise ValueError(
                "End time cannot precede start time."
            )

        # Validate power consumption.
        if resource.power_consumption_w < 0:
            raise ValueError(
                "Power consumption cannot be negative."
            )

        # Calculate efficiency.
        efficiency = self.calculate_efficiency(resource)

        if efficiency <= 0:
            raise ValueError(
                "Cannot calculate energy with zero efficiency."
            )

        # Calculate execution duration.
        execution_duration = end_time - start_time

        # Equation (15).
        energy = (
            resource.power_consumption_w / efficiency
        ) * execution_duration

        return energy

    def calculate_total_energy(self, energy_values):

        return sum(energy_values)
