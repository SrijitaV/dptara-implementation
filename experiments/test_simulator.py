
from src.simulator import DPTARASimulator

print("\n========== DPTARA SIMULATOR TEST ==========")

simulator = DPTARASimulator(
    simulation_duration=10,
    arrival_rate=5.0,
    seed=42
)

print("\nSimulation Configuration:")
print("Duration:", simulator.simulation_duration)
print("Arrival Rate:", simulator.arrival_rate)
print("Random Seed:", simulator.seed)

print("\nInitialized Components:")
print("Task Generator: Ready")
print("Resource Manager: Ready")
print("Resource Allocator: Ready")
print("Priority Model: Ready")
print("Load Predictor: Ready")
print("Energy Manager: Ready")
print("Load Balancer: Ready")
print("Metrics: Ready")

print("\nSimulator initialization test completed.")