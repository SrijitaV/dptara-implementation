"""
Run a fair, repeatable comparison of DPTARA and the three
paper-informed baseline strategy variants.

Run from the project root:
    python -m experiments.run_comparison

Outputs:
    results/comparison_raw.csv
    results/comparison_summary.csv
    results/plots/*.png
    results/experiment_notes.md

Important:
A-PBRA, NBIHA and CORA-GT are heuristic, paper-informed adaptations
in this implementation. They are not claimed to be exact reproductions
of the original papers.
"""

from contextlib import redirect_stdout
from pathlib import Path
import io
import sys

import matplotlib.pyplot as plt
import pandas as pd

# Ensure imports work when this file is run as a module from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.simulator import DPTARASimulator


ALGORITHMS = ["DPTARA", "A-PBRA", "NBIHA", "CORA-GT"]
DURATIONS_SECONDS = [5, 10, 20, 40]
SEEDS = [42, 43, 44, 45, 46]
ARRIVAL_RATE = 5.0


def run_one_experiment(algorithm, duration, seed):
    """Run one fresh simulator instance and return its metrics."""
    simulator = DPTARASimulator(
        simulation_duration=duration,
        arrival_rate=ARRIVAL_RATE,
        seed=seed,
        algorithm=algorithm,
    )

    # Keep the terminal readable while preserving simulator behavior.
    with redirect_stdout(io.StringIO()):
        results = simulator.run()

    row = {
        "algorithm": algorithm,
        "simulation_duration_seconds": duration,
        "arrival_rate_tasks_per_second": ARRIVAL_RATE,
        "seed": seed,
    }

    # Keep all numeric metrics returned by the simulator.
    for key, value in results.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            row[key] = value

    # Explicitly retain the most important fields, even if a metric is absent.
    important_metrics = [
        "total_tasks",
        "completed_tasks",
        "completion_rate_percent",
        "unallocated_tasks",
        "on_time_tasks",
        "late_completed_tasks",
        "deadline_miss_rate_percent",
        "deadline_met_rate_percent",
        "average_latency",
        "average_execution_time",
        "total_energy_consumption",
        "average_system_utilization_percent",
        "average_balancing_rate_percent",
        "simulation_clock",
        "generated_tasks",
    ]

    for key in important_metrics:
        row.setdefault(key, 0.0)

    return row


def make_summary(raw):
    """Average results over seeds for each algorithm and workload duration."""
    metric_columns = [
        column
        for column in raw.select_dtypes(include="number").columns
        if column not in {
            "seed",
            "arrival_rate_tasks_per_second",
            "simulation_duration_seconds",
        }
    ]

    summary = (
        raw.groupby(
            ["simulation_duration_seconds", "algorithm"],
            as_index=False
        )[metric_columns]
        .mean()
    )

    # Convert seconds to milliseconds for easier interpretation in tables/plots.
    summary["average_latency_ms"] = summary["average_latency"] * 1000.0
    summary["average_execution_time_ms"] = (
        summary["average_execution_time"] * 1000.0
    )

    return summary


def save_metric_plot(summary, metric, ylabel, filename, multiply=1.0):
    """Create one comparison plot across workload durations."""
    plt.figure(figsize=(9, 5))

    for algorithm in ALGORITHMS:
        subset = summary[summary["algorithm"] == algorithm].sort_values(
            "simulation_duration_seconds"
        )
        if subset.empty:
            continue

        plt.plot(
            subset["simulation_duration_seconds"],
            subset[metric] * multiply,
            marker="o",
            linewidth=2,
            label=algorithm,
        )

    plt.xlabel("Task generation duration (seconds)")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs Workload Duration")
    plt.xticks(DURATIONS_SECONDS)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def main():
    results_dir = PROJECT_ROOT / "results"
    plots_dir = results_dir / "plots"
    results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    total_runs = len(ALGORITHMS) * len(DURATIONS_SECONDS) * len(SEEDS)
    print("=" * 68)
    print("DPTARA ALGORITHM COMPARISON")
    print("=" * 68)
    print(f"Algorithms: {', '.join(ALGORITHMS)}")
    print(f"Durations: {DURATIONS_SECONDS} seconds")
    print(f"Arrival rate: {ARRIVAL_RATE} tasks/second")
    print(f"Seeds: {SEEDS}")
    print(f"Total simulation runs: {total_runs}")
    print("\nRunning experiments...\n")

    rows = []
    run_number = 0

    for duration in DURATIONS_SECONDS:
        for seed in SEEDS:
            for algorithm in ALGORITHMS:
                run_number += 1
                print(
                    f"[{run_number}/{total_runs}] "
                    f"{algorithm}, duration={duration}s, seed={seed}"
                )

                row = run_one_experiment(algorithm, duration, seed)
                rows.append(row)

    raw = pd.DataFrame(rows)
    raw_path = results_dir / "comparison_raw.csv"
    raw.to_csv(raw_path, index=False)

    summary = make_summary(raw)
    summary_path = results_dir / "comparison_summary.csv"
    summary.to_csv(summary_path, index=False)

    # Metric plots. Latency and execution time are converted from seconds to ms.
    plots = [
        ("average_latency", "Average latency (ms)", "average_latency.png", 1000.0),
        (
            "average_execution_time",
            "Average execution time (ms)",
            "average_execution_time.png",
            1000.0,
        ),
        (
            "total_energy_consumption",
            "Total energy consumption (J)",
            "total_energy_consumption.png",
            1.0,
        ),
        (
            "completion_rate_percent",
            "Completion rate (%)",
            "completion_rate.png",
            1.0,
        ),
        (
            "deadline_miss_rate_percent",
            "Deadline miss rate (%)",
            "deadline_miss_rate.png",
            1.0,
        ),
        (
            "average_system_utilization_percent",
            "Normalized resource-load ratio (%)",
            "normalized_resource_load.png",
            1.0,
        ),
        (
            "average_balancing_rate_percent",
            "Load-balancing rate (%)",
            "average_balancing_rate.png",
            1.0,
        ),
    ]

    for metric, ylabel, filename, multiplier in plots:
        if metric in summary.columns:
            save_metric_plot(
                summary,
                metric,
                ylabel,
                plots_dir / filename,
                multiply=multiplier,
            )

    notes = """# Experiment notes

## Experimental setup
- Algorithms: DPTARA, A-PBRA, NBIHA and CORA-GT.
- Task arrival rate: 5 tasks/second.
- Task generation durations: 5, 10, 20 and 40 seconds.
- Random seeds: 42, 43, 44, 45 and 46.
- Each run creates a fresh simulator instance.
- Matching seeds and durations are used across algorithms to make the
  generated task workload and resource configuration reproducible.

## Interpretation and limitations
- A-PBRA, NBIHA and CORA-GT are paper-informed heuristic adaptations
  in this implementation, not verified exact reproductions of the
  original algorithms.
- The target paper does not fully specify all baseline pseudocode or
  all parameters needed for exact reproduction.
- The simulator uses task size (MB) as a normalized resource-load
  proxy. Its reported normalized resource-load ratio must not be
  described as measured physical CPU utilization.
- The paper's computing-time expression and the relationship between
  task size and CPU demand have unit/model limitations. Interpret
  latency and execution-time results as outputs of this simulator's
  stated model, not as calibrated real-world measurements.
- Compare the algorithms using the generated CSV files. Do not alter
  measured results to match values reported in the paper.
"""

    notes_path = results_dir / "experiment_notes.md"
    notes_path.write_text(notes, encoding="utf-8")

    print("\n" + "=" * 68)
    print("EXPERIMENTS COMPLETED")
    print("=" * 68)
    print(f"Raw results:     {raw_path}")
    print(f"Summary results: {summary_path}")
    print(f"Plots folder:   {plots_dir}")
    print(f"Experiment notes:{notes_path}")
    print("\nMean results by duration and algorithm:")
    display_columns = [
        "simulation_duration_seconds",
        "algorithm",
        "total_tasks",
        "completion_rate_percent",
        "average_latency_ms",
        "total_energy_consumption",
        "deadline_miss_rate_percent",
    ]
    available_columns = [
        column for column in display_columns if column in summary.columns
    ]
    print(summary[available_columns].to_string(index=False))


if __name__ == "__main__":
    main()
