
"""
Workload-intensity experiment for DPTARA and baseline algorithms.

Run from the project root:
    python -m experiments.run_comparison

Tests different task arrival rates while keeping durations,
algorithms and random seeds consistent.

Outputs are saved separately in:
    results/workload_intensity/
"""

from contextlib import redirect_stdout
from pathlib import Path
import io
import sys

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
# PROJECT IMPORTS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.simulator import DPTARASimulator


# --------------------------------------------------
# EXPERIMENT CONFIGURATION
# --------------------------------------------------

ALGORITHMS = [
    "DPTARA",
    "A-PBRA",
    "NBIHA",
    "CORA-GT"
]

DURATIONS_SECONDS = [5, 10, 20, 40]

ARRIVAL_RATES = [5.0, 10.0, 15.0, 20.0]

SEEDS = [42, 43, 44, 45, 46]


# --------------------------------------------------
# SINGLE EXPERIMENT
# --------------------------------------------------

def run_one_experiment(algorithm, duration, arrival_rate, seed):

    simulator = DPTARASimulator(
        simulation_duration=duration,
        arrival_rate=arrival_rate,
        seed=seed,
        algorithm=algorithm
    )

    with redirect_stdout(io.StringIO()):
        results = simulator.run()

    row = {
        "algorithm": algorithm,
        "simulation_duration_seconds": duration,
        "arrival_rate_tasks_per_second": arrival_rate,
        "seed": seed
    }

    for key, value in results.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            row[key] = value

    important_metrics = [
        "total_tasks",
        "completed_tasks",
        "incomplete_tasks",
        "completion_rate_percent",
        "unallocated_tasks",
        "on_time_tasks",
        "late_completed_tasks",
        "expired_incomplete_tasks",
        "deadline_missed_tasks",
        "unresolved_tasks",
        "deadline_miss_rate_percent",
        "deadline_met_rate_percent",
        "average_latency",
        "average_execution_time",
        "total_energy_consumption",
        "system_utilization_percent",
        "average_system_utilization_percent",
        "average_balancing_rate_percent",
        "simulation_clock",
        "generated_tasks"
    ]

    for key in important_metrics:
        row.setdefault(key, 0.0)

    return row


# --------------------------------------------------
# SUMMARY GENERATION
# --------------------------------------------------

def make_summary(raw):

    excluded_columns = {
        "seed",
        "simulation_duration_seconds",
        "arrival_rate_tasks_per_second"
    }

    metric_columns = [
        column
        for column in raw.select_dtypes(include="number").columns
        if column not in excluded_columns
    ]

    summary = (
        raw.groupby(
            [
                "simulation_duration_seconds",
                "arrival_rate_tasks_per_second",
                "algorithm"
            ],
            as_index=False
        )[metric_columns]
        .mean()
    )

    summary["average_latency_ms"] = (
        summary["average_latency"] * 1000.0
    )

    summary["average_execution_time_ms"] = (
        summary["average_execution_time"] * 1000.0
    )

    summary["energy_per_completed_task_j"] = (
        summary["total_energy_consumption"]
        / summary["completed_tasks"].replace(0, float("nan"))
    )

    return summary


# --------------------------------------------------
# PLOT GENERATION
# --------------------------------------------------

def save_metric_plot(summary, metric, ylabel, filename, duration):

    plt.figure(figsize=(9, 5))

    duration_data = summary[
        summary["simulation_duration_seconds"] == duration
    ]

    for algorithm in ALGORITHMS:

        subset = duration_data[
            duration_data["algorithm"] == algorithm
        ].sort_values("arrival_rate_tasks_per_second")

        if subset.empty:
            continue

        plt.plot(
            subset["arrival_rate_tasks_per_second"],
            subset[metric],
            marker="o",
            linewidth=2,
            label=algorithm
        )

    plt.xlabel("Task arrival rate (tasks/second)")
    plt.ylabel(ylabel)

    plt.title(
        f"{ylabel} vs Arrival Rate "
        f"(Task generation duration: {duration}s)"
    )

    plt.xticks(ARRIVAL_RATES)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(filename, dpi=300)
    plt.close()


# --------------------------------------------------
# EXPERIMENT NOTES
# --------------------------------------------------

def write_experiment_notes(results_dir):

    notes = """# Workload-Intensity Experiment Notes

## 1. Experimental setup

- Algorithms: DPTARA, A-PBRA, NBIHA and CORA-GT.
- Arrival rates: 5, 10, 15 and 20 tasks/second.
- Task generation durations: 5, 10, 20 and 40 seconds.
- Random seeds: 42, 43, 44, 45 and 46.
- Each experiment creates a fresh simulator instance.
- Matching seeds, durations and arrival rates are used
  across all algorithms.
- The simulation initializes 10 edge servers and one cloud server.

## 2. Experimental objective

This experiment evaluates algorithm performance under
increasing task arrival intensity.

The objective is to investigate how scheduling, resource
allocation, latency, energy consumption and deadline
performance change as workload intensity increases.

## 3. Computational model

The task generation, execution, resource allocation,
energy and scheduling models remain unchanged from
the original implementation.

The task workload conversion and CPU demand assumptions
remain implementation assumptions.

## 4. Algorithm implementations

- DPTARA uses dynamic task priority and resource allocation.
- A-PBRA is a paper-informed priority-based heuristic.
- NBIHA is a paper-informed resource-matching heuristic.
- CORA-GT is a game-inspired utility-based heuristic.

The baseline implementations are experimental adaptations,
not verified exact reproductions.

## 5. Performance metrics

The experiment records task completion, latency,
execution time, energy, deadline misses, system utilization
and Jain's fairness index.

Jain's fairness index measures resource distribution
fairness, not the speed of load balancing.

## 6. Reproducibility

Each experiment uses a fresh simulator instance.
Five fixed random seeds are used for each configuration.

Results are aggregated using the arithmetic mean.

## 7. Research limitations

The workload-intensity experiment changes task arrival
rate only. Other model parameters remain unchanged.

Results are simulation outputs and should not be presented
as calibrated real-world measurements.

The baseline strategies are paper-informed adaptations.
They are not claimed to be exact reproductions.

## 8. Result interpretation

Use comparison_raw.csv for individual runs.
Use comparison_summary.csv for mean results.

Compare all algorithms at the same arrival rate and
task generation duration.

Do not draw conclusions from a single metric alone.
"""

    notes_path = results_dir / "experiment_notes.md"

    notes_path.write_text(notes, encoding="utf-8")

    return notes_path


# --------------------------------------------------
# MAIN EXPERIMENT RUNNER
# --------------------------------------------------

def main():

    results_dir = PROJECT_ROOT / "results" / "workload_intensity"

    plots_dir = results_dir / "plots"

    results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    total_runs = (
        len(ALGORITHMS)
        * len(DURATIONS_SECONDS)
        * len(ARRIVAL_RATES)
        * len(SEEDS)
    )

    print("=" * 70)
    print("DPTARA WORKLOAD-INTENSITY EXPERIMENT")
    print("=" * 70)

    print(f"Algorithms: {ALGORITHMS}")
    print(f"Durations: {DURATIONS_SECONDS}")
    print(f"Arrival rates: {ARRIVAL_RATES}")
    print(f"Seeds: {SEEDS}")
    print(f"Total simulation runs: {total_runs}")

    rows = []
    run_number = 0

    for duration in DURATIONS_SECONDS:

        for arrival_rate in ARRIVAL_RATES:

            for seed in SEEDS:

                for algorithm in ALGORITHMS:

                    run_number += 1

                    print(
                        f"[{run_number}/{total_runs}] "
                        f"{algorithm} | "
                        f"duration={duration}s | "
                        f"arrival_rate={arrival_rate} | "
                        f"seed={seed}"
                    )

                    row = run_one_experiment(
                        algorithm,
                        duration,
                        arrival_rate,
                        seed
                    )

                    rows.append(row)

    # Save raw results

    raw = pd.DataFrame(rows)

    raw_path = results_dir / "comparison_raw.csv"
    raw.to_csv(raw_path, index=False)

    # Save summary

    summary = make_summary(raw)

    summary_path = results_dir / "comparison_summary.csv"
    summary.to_csv(summary_path, index=False)

    # Generate plots

    plots = [
        (
            "average_latency_ms",
            "Average latency (ms)",
            "average_latency"
        ),
        (
            "average_execution_time_ms",
            "Average execution time (ms)",
            "average_execution_time"
        ),
        (
            "total_energy_consumption",
            "Total energy consumption (J)",
            "total_energy_consumption"
        ),
        (
            "energy_per_completed_task_j",
            "Energy per completed task (J)",
            "energy_per_completed_task"
        ),
        (
            "completion_rate_percent",
            "Completion rate (%)",
            "completion_rate"
        ),
        (
            "deadline_miss_rate_percent",
            "Deadline miss rate (%)",
            "deadline_miss_rate"
        ),
        (
            "average_system_utilization_percent",
            "Average system utilization (%)",
            "system_utilization"
        ),
        (
            "average_balancing_rate_percent",
            "Jain's fairness index (%)",
            "jains_fairness_index"
        )
    ]

    for duration in DURATIONS_SECONDS:

        for metric, ylabel, filename in plots:

            if metric not in summary.columns:
                print(f"Skipping missing metric: {metric}")
                continue

            save_metric_plot(
                summary,
                metric,
                ylabel,
                plots_dir / f"{filename}_{duration}s.png",
                duration
            )

    # Write experiment notes

    notes_path = write_experiment_notes(results_dir)

    # Final report

    print("\n" + "=" * 70)
    print("WORKLOAD-INTENSITY EXPERIMENT COMPLETED")
    print("=" * 70)

    print(f"Raw results: {raw_path}")
    print(f"Summary results: {summary_path}")
    print(f"Plots folder: {plots_dir}")
    print(f"Experiment notes: {notes_path}")

    display_columns = [
        "simulation_duration_seconds",
        "arrival_rate_tasks_per_second",
        "algorithm",
        "total_tasks",
        "completion_rate_percent",
        "average_latency_ms",
        "average_execution_time_ms",
        "total_energy_consumption",
        "deadline_miss_rate_percent",
        "average_system_utilization_percent",
        "average_balancing_rate_percent"
    ]

    available_columns = [
        column for column in display_columns
        if column in summary.columns
    ]

    print("\nSummary:")
    print(summary[available_columns].to_string(index=False))


if __name__ == "__main__":
    main()
