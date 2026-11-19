
from src.models.entities import Resource
from src.energy_manager import EnergyManager


# Initialize energy manager
manager = EnergyManager()

# Create an edge resource
edge = Resource(
    resource_id="E1",
    resource_type="edge",
    capacity=100,
    current_load=50,
    power_consumption_w=50,
    downtime_rate=0.05
)

# Calculate efficiency
efficiency = manager.calculate_efficiency(edge)

# Calculate energy for 10 seconds
energy = manager.calculate_energy(
    edge,
    start_time=0,
    end_time=10
)

print("\n========== DPTARA ENERGY MANAGEMENT TEST ==========")

print(f"Resource ID: {edge.resource_id}")
print(f"Resource Utilization: {edge.utilization:.2f}")
print(f"Resource Efficiency: {efficiency:.4f}")
print(f"Power Consumption: {edge.power_consumption_w} W")
print(f"Execution Duration: 10 seconds")
print(f"Energy Consumption: {energy:.4f} Joules")

print("\nEnergy Management test completed successfully.")
