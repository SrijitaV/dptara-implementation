
from src.models.entities import Resource
from src.load_balancer import LoadBalancer


def main():

    balancer = LoadBalancer()

    # Create sample computing resources
    resources = [
        Resource("E1", "edge", 100, 50),
        Resource("E2", "edge", 100, 50),
        Resource("C1", "cloud", 500, 170)
    ]

    print("\n" + "=" * 65)
    print("          DPTARA - LOAD BALANCING TEST")
    print("=" * 65)

    # Calculate average load
    total_load = sum(r.current_load for r in resources)
    average_load = total_load / len(resources)

    print(f"\nTotal Resource Load: {total_load}")
    print(f"Number of Resources: {len(resources)}")
    print(f"Average Resource Load: {average_load:.2f}")

    print("\nResource Balancing Results:")
    print("-" * 65)

    print(
        f"{'Resource':<12}"
        f"{'Load':<12}"
        f"{'Average':<12}"
        f"{'Balancing Rate':<18}"
    )

    print("-" * 65)

    results = balancer.calculate_all_balancing_rates(resources)

    # Validate Algorithm 3 balancing-rate calculations
    expected_rates = {
        "E1": 55.5555555556,
        "E2": 55.5555555556,
        "C1": 11.1111111111
    }

    for resource_id, expected in expected_rates.items():
        assert abs(results[resource_id] - expected) < 0.01, (
            f"Incorrect balancing rate for {resource_id}"
        )

    print("\nAlgorithm 3 formula validation: PASSED")

    for resource in resources:

        rate = results[resource.resource_id]

        print(
            f"{resource.resource_id:<12}"
            f"{resource.current_load:<12.2f}"
            f"{average_load:<12.2f}"
            f"{rate:<18.2f}%"
        )

    print("-" * 65)

    # Test zero-load handling
    empty_resources = [
        Resource("E3", "edge", 100, 0),
        Resource("C2", "cloud", 500, 0)
    ]

    zero_rate = balancer.calculate_all_balancing_rates(
        empty_resources
    )

    assert all(rate == 100.0 for rate in zero_rate.values())

    print("\nZero-load test: PASSED")
    print("Load balancing calculation: SUCCESSFUL")

    print("=" * 65)


if __name__ == "__main__":
    main()
