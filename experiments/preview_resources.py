
from src.models.entities import Resource
from src.resource_manager import ResourceManager


def main():

    manager = ResourceManager()

    # Create sample resources.
    # These are illustrative test values, not paper parameters.

    edge1 = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=100,
        current_load=20,
        processing_speed_mips=1000,
        power_consumption_w=50,
        network_latency_ms=5
    )

    cloud1 = Resource(
        resource_id="C1",
        resource_type="cloud",
        capacity=500,
        current_load=100,
        processing_speed_mips=5000,
        power_consumption_w=200,
        network_latency_ms=50
    )

    manager.register_resource(edge1)
    manager.register_resource(cloud1)

    print("\n========== RESOURCE MANAGER TEST ==========")

    print("\nRegistered resources:")

    for resource in manager.get_all_resources():
        print(
            resource.resource_id,
            resource.resource_type,
            resource.utilization
        )

    print("\nAdding load to E1...")
    manager.add_load("E1", 30)

    print("E1 current load:", manager.get_resource("E1").current_load)

    print("\nReleasing load from E1...")
    manager.release_load("E1", 10)

    print("E1 current load:", manager.get_resource("E1").current_load)

    print("\nAvailable edge resources:")

    for resource in manager.get_available_resources("edge"):
        print(resource.resource_id)

    print("\nFinal resource status:")

    for item in manager.get_resource_status():
        print(item)

    print("\nResource Manager test completed successfully.")


if __name__ == "__main__":
    main()
