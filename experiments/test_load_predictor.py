
from src.models.load_predictor import LoadPredictor


def main():

    predictor = LoadPredictor(max_history=50)

    print("\n" + "=" * 65)
    print("             DPTARA - LOAD PREDICTION TEST")
    print("=" * 65)

    # Simulate historical resource utilization observations
    resource_id = "E1"

    observations = [
        (0, 0.20),
        (1, 0.30),
        (2, 0.40),
        (3, 0.50),
        (4, 0.55)
    ]

    print("\nHistorical Resource Utilization")
    print("-" * 45)
    print(f"{'Time':<15}{'Utilization':<15}")

    for time, utilization in observations:
        predictor.record_observation(
            resource_id, time, utilization
        )
        print(f"{time:<15}{utilization:<15.2f}")

    # Predict future utilization
    future_times = [5, 6, 7]

    print("\nFuture Load Predictions")
    print("-" * 45)
    print(f"{'Future Time':<15}{'Predicted Load':<15}")

    for future_time in future_times:

        predicted_load = predictor.predict_load(
            resource_id, future_time
        )

        print(
            f"{future_time:<15}"
            f"{predicted_load:<15.4f}"
        )

    # Test prediction for an unknown resource
    print("\nTesting Invalid Resource")

    try:
        predictor.predict_load("E99", 5)

    except ValueError as error:
        print("Expected error:", error)

    print("\n" + "=" * 65)
    print("Load Predictor test completed successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()
