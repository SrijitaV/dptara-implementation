
import statistics

from src.simulator import DPTARASimulator


def run_repeated_simulations(number_of_runs=5):

    results = []

    print("\nDPTARA REPEATED SIMULATION EXPERIMENT")
    print("=" * 55)

    for run_number in range(number_of_runs):

        seed = 42 + run_number

        print(f"\nRunning experiment {run_number + 1}/{number_of_runs}")
        print(f"Random seed: {seed}")

        simulator = DPTARASimulator(
            simulation_duration=10,
            arrival_rate=5.0,
            seed=seed
        )

        result = simulator.run()
        results.append(result)

    metrics = [
        "completion_rate_percent",
        "deadline_miss_rate_percent",
        "average_latency",
        "average_execution_time",
        "total_energy_consumption",
        "system_utilization_percent",
        "average_balancing_rate_percent"
    ]

    print("\n\nAGGREGATED EXPERIMENTAL RESULTS")
    print("=" * 65)

    for metric in metrics:

        values = [result[metric] for result in results]

        mean_value = statistics.mean(values)

        std_value = (
            statistics.stdev(values)
            if len(values) > 1
            else 0.0
        )

        print(f"\n{metric}")
        print(f"Mean: {mean_value:.4f}")
        print(f"Standard deviation: {std_value:.4f}")

    print("\n" + "=" * 65)
    print("REPEATED SIMULATION EXPERIMENT COMPLETED")


if __name__ == "__main__":
    run_repeated_simulations(number_of_runs=5)
