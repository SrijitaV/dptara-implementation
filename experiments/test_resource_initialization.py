
from src.simulator import DPTARASimulator


print("\n========== DPTARA RESOURCE INITIALIZATION TEST ==========")

simulator = DPTARASimulator(
    simulation_duration=10,
    arrival_rate=5.0,
    seed=42
)

resources = simulator.initialize_resources()

print("\nTotal Resources:", len(resources))

print("\nEDGE SERVERS")
print("-" * 75)

for resource in resources:

    if resource.resource_type == "edge":

        print(
            f"{resource.resource_id} | "
            f"CPU: {resource.capacity} MIPS | "
            f"Power: {resource.power_consumption_w} W | "
            f"Latency: {resource.network_latency_ms} ms"
        )

print("\nCLOUD SERVERS")
print("-" * 75)

for resource in resources:

    if resource.resource_type == "cloud":

        print(
            f"{resource.resource_id} | "
            f"CPU: {resource.capacity} MIPS | "
            f"Power: {resource.power_consumption_w} W | "
            f"Latency: {resource.network_latency_ms} ms"
        )

print("\nRESOURCE INITIALIZATION SUMMARY")
print("Edge Servers:", sum(
    r.resource_type == "edge" for r in resources
))

print("Cloud Servers:", sum(
    r.resource_type == "cloud" for r in resources
))

print("\nResource initialization test completed successfully.")
