
class EnergyManager:
    """
    Implements the energy efficiency and energy consumption
    equations described in the DPTARA research paper.

    Equations 14 and 15.
    """

    def calculate_efficiency(self, resource):
        """
        Calculate resource utilization efficiency.

        eta = (U_effective / C_total) * (1 - downtime)
        """

        if resource.capacity <= 0:
            raise ValueError("Resource capacity must be positive.")

        if not 0 <= resource.downtime_rate <= 1:
            raise ValueError("Invalid downtime rate.")

        effective_utilization = resource.current_load

        efficiency = (
            effective_utilization / resource.capacity
        ) * (1 - resource.downtime_rate)

        return efficiency

    def calculate_energy(
        self,
        resource,
        start_time,
        end_time
    ):
        """
        Calculate energy consumption using Equation 15.

        E = (P / eta) * (T_end - T_start)
        """

        if end_time < start_time:
            raise ValueError("End time cannot precede start time.")

        if resource.power_consumption_w < 0:
            raise ValueError("Power consumption cannot be negative.")

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
        """
        Calculate total system energy consumption.
        """

        return sum(energy_values)
