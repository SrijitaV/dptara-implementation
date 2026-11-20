
from src.simulator import DPTARASimulator


def main():

    print("\nTEST: LOAD PREDICTION INTEGRATION")
    print("-" * 50)

    simulator = DPTARASimulator(
        simulation_duration=10,
        arrival_rate=5,
        seed=42
    )

    simulator.run()

    predictor = simulator.load_predictor

    print("\nRecorded Resource Histories:")

    for resource_id, observations in predictor.history.items():

        print(
            f"{resource_id}: "
            f"{len(observations)} observations"
        )

        assert len(observations) > 0

    assert len(predictor.history) == len(simulator.resources)


    print("\nPredicted Future Resource Utilization:")
    
    future_time = simulator.simulation_clock + 5.0

    for resource_id in predictor.history:

        predicted_load = predictor.predict_load(
            resource_id,
            future_time
        )

        print(
            f"{resource_id}: "
            f"{predicted_load:.4f}"
        )

        assert 0.0 <= predicted_load <= 1.0

    print("\nFUTURE LOAD PREDICTION: PASSED")

    print("\nLOAD OBSERVATION INTEGRATION: PASSED")


if __name__ == "__main__":
    main()
