
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

    print("\nLOAD OBSERVATION INTEGRATION: PASSED")


if __name__ == "__main__":
    main()
