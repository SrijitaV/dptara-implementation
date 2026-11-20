
from src.simulator import DPTARASimulator

def main():

    print("\nTEST: FULL DPTARA SIMULATION")
    print("-" * 55)

    simulator = DPTARASimulator(
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42
    )

    results = simulator.run()

    print("\nTEST VALIDATION")
    print("-" * 55)

    assert results["total_tasks"] > 0

    assert (
        results["completed_tasks"]
        <= results["total_tasks"]
    )

    assert (
        0 <= results["completion_rate_percent"] <= 100
    )

    assert results["average_latency"] >= 0

    assert results["average_execution_time"] >= 0

    assert results["total_energy_consumption"] >= 0

    print("Task generation: PASSED")
    print("Task processing: PASSED")
    print("Performance metrics: PASSED")

    print("\nFULL SIMULATION TEST PASSED")

if __name__ == "__main__":
    main()