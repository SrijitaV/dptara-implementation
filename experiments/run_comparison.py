
"""
Run a fair, repeatable comparison of DPTARA and three
paper-informed baseline strategy variants.

Run from the project root:
    python -m experiments.run_comparison

Outputs:
    results/comparison_raw.csv
    results/comparison_summary.csv
    results/plots/*.png
    results/experiment_notes.md

Important:
    A-PBRA, NBIHA and CORA-GT are heuristic, paper-informed
    adaptations. They are not claimed to be exact reproductions
    of the original algorithms.
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

SEEDS = [42, 43, 44, 45, 46]

ARRIVAL_RATE = 5.0


# --------------------------------------------------
# SINGLE EXPERIMENT
# --------------------------------------------------

def run_one_experiment(algorithm, duration, seed):
    """
    Run one fresh simulator instance and return its metrics.
    """

    simulator = DPTARASimulator(
        simulation_duration=duration,
        arrival_rate=ARRIVAL_RATE,
        seed=seed,
        algorithm=algorithm
    )

    # Suppress verbose simulator output during batch experiments.
    with redirect_stdout(io.StringIO()):
        results = simulator.run()

    row = {
        "algorithm": algorithm,
        "simulation_duration_seconds": duration,
        "arrival_rate_tasks_per_second": ARRIVAL_RATE,
        "seed": seed
    }

    # Preserve all numeric metrics.
    for key, value in results.items():

        if isinstance(value, (int, float)) and not isinstance(
            value, bool
        ):
            row[key] = value

    # Ensure important metrics are always present.
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
    """
    Calculate mean metrics across random seeds for each
    algorithm and workload duration.
    """

    metric_columns = [
        column
        for column in raw.select_dtypes(
            include="number"
        ).columns
        if column not in {
            "seed",
            "arrival_rate_tasks_per_second",
            "simulation_duration_seconds"
        }
    ]

    summary = (
        raw.groupby(
            [
                "simulation_duration_seconds",
                "algorithm"
            ],
            as_index=False
        )[metric_columns]
        .mean()
    )

    # Convert seconds to milliseconds for presentation.
    summary["average_latency_ms"] = (
        summary["average_latency"] * 1000.0
    )

    summary["average_execution_time_ms"] = (
        summary["average_execution_time"] * 1000.0
    )

    return summary


# --------------------------------------------------
# PLOT GENERATION
# --------------------------------------------------

def save_metric_plot(
    summary,
    metric,
    ylabel,
    filename,
    multiply=1.0
):
    """
    Generate a comparison plot across workload durations.
    """

    plt.figure(figsize=(9, 5))

    for algorithm in ALGORITHMS:

        subset = summary[
            summary["algorithm"] == algorithm
        ].sort_values(
            "simulation_duration_seconds"
        )

        if subset.empty:
            continue

        plt.plot(
            subset["simulation_duration_seconds"],
            subset[metric] * multiply,
            marker="o",
            linewidth=2,
            label=algorithm
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


# --------------------------------------------------
# EXPERIMENT NOTES
# --------------------------------------------------

def write_experiment_notes(results_dir):

    notes = """# Experiment Notes

## 1. Experimental setup

- Algorithms: DPTARA, A-PBRA, NBIHA and CORA-GT.
- Task arrival rate: 5 tasks/second.
- Task generation durations: 5, 10, 20 and 40 seconds.
- Random seeds: 42, 43, 44, 45 and 46.
- Each experiment creates a fresh simulator instance.
- Matching seeds and durations are used across algorithms.
- The simulation initializes 10 edge servers and one cloud server.

## 2. Computational model

The implementation distinguishes three quantities:

- Task input data size: MB.
- Computational workload: MI.
- CPU demand: MIPS.

The current task generator uses configurable implementation
assumptions of 100 MI per MB and a CPU demand uniformly
sampled between 50 and 250 MIPS.

These numerical assumptions are not specified by the paper.
They must be treated as simulation parameters and subjected
to sensitivity analysis.

Execution time is calculated using:

    Execution time = Workload (MI) / Processing speed (MIPS)

Resource utilization is calculated using reserved CPU demand
relative to resource CPU capacity.

## 3. Algorithm implementations

- DPTARA uses dynamic task priority and resource allocation.
- A-PBRA is a paper-informed priority-based heuristic.
- NBIHA is a paper-informed resource-matching heuristic.
- CORA-GT is a game-inspired utility-based heuristic.

The three baseline implementations are experimental
adaptations, not verified exact reproductions of the original
algorithms or their optimization procedures.

## 4. Performance metrics

The experiment records:

- Task completion rate.
- Average task latency.
- Average execution time.
- Total energy consumption.
- Deadline miss rate.
- Deadline met rate.
- Average system utilization.
- Jain's fairness index for resource utilization distribution.

Jain's fairness index measures distribution fairness.
It should not be interpreted as a direct measure of
the speed or effectiveness of load balancing.

System utilization is time-weighted over the simulation
makespan. It is not merely the final resource-load snapshot.

## 5. Reproducibility

Each experiment uses a fresh simulator instance.
Random seeds are fixed to make task generation and
resource initialization reproducible.

Results are aggregated by algorithm and workload duration
using the arithmetic mean across the five seeds.

## 6. Research limitations

- The paper does not fully specify all baseline pseudocode.
- The paper does not provide all numerical CPU-demand parameters.
- The task-size-to-workload conversion used here is an
  implementation assumption, not a reported paper parameter.
- The chosen priority weights and workload assumptions
  require sensitivity analysis.
- Results are outputs of the implemented simulation model
  and should not be presented as calibrated real-world measurements.
- The paper's reported results must be compared with the
  simulation results without modifying measured outputs
  to force agreement.

## 7. Result interpretation

Use comparison_raw.csv for individual experimental runs.

Use comparison_summary.csv for mean results across seeds.

Examine the plots alongside completion rates, deadline
performance, utilization, and energy consumption.

Do not draw conclusions from a single metric alone.
"""

    notes_path = results_dir / "experiment_notes.md"

    notes_path.write_text(
        notes,
        encoding="utf-8"
    )

    return notes_path


# --------------------------------------------------
# MAIN EXPERIMENT RUNNER
# --------------------------------------------------

def main():

    results_dir = PROJECT_ROOT / "results"

    plots_dir = results_dir / "plots"

    results_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    plots_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    total_runs = (
        len(ALGORITHMS)
        * len(DURATIONS_SECONDS)
        * len(SEEDS)
    )

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

    # Same duration and seed combinations for every algorithm.
    for duration in DURATIONS_SECONDS:

        for seed in SEEDS:

            for algorithm in ALGORITHMS:

                run_number += 1

                print(
                    f"[{run_number}/{total_runs}] "
                    f"{algorithm}, "
                    f"duration={duration}s, "
                    f"seed={seed}"
                )

                row = run_one_experiment(
                    algorithm,
                    duration,
                    seed
                )

                rows.append(row)

    # --------------------------------------------------
    # SAVE RAW RESULTS
    # --------------------------------------------------

    raw = pd.DataFrame(rows)

    raw_path = (
        results_dir / "comparison_raw.csv"
    )

    raw.to_csv(
        raw_path,
        index=False
    )

    # --------------------------------------------------
    # SAVE SUMMARY RESULTS
    # --------------------------------------------------

    summary = make_summary(raw)

    summary_path = (
        results_dir / "comparison_summary.csv"
    )

    summary.to_csv(
        summary_path,
        index=False
    )

    # --------------------------------------------------
    # GENERATE PLOTS
    # --------------------------------------------------

    plots = [
        (
            "average_latency",
            "Average latency (ms)",
            "average_latency.png",
            1000.0
        ),
        (
            "average_execution_time",
            "Average execution time (ms)",
            "average_execution_time.png",
            1000.0
        ),
        (
            "total_energy_consumption",
            "Total energy consumption (J)",
            "total_energy_consumption.png",
            1.0
        ),
        (
            "completion_rate_percent",
            "Completion rate (%)",
            "completion_rate.png",
            1.0
        ),
        (
            "deadline_miss_rate_percent",
            "Deadline miss rate (%)",
            "deadline_miss_rate.png",
            1.0
        ),
        (
            "average_system_utilization_percent",
            "Average system utilization (%)",
            "average_system_utilization.png",
            1.0
        ),
        (
            "average_balancing_rate_percent",
            "Jain's fairness index (%)",
            "jains_fairness_index.png",
            1.0
        )
    ]

    for metric, ylabel, filename, multiplier in plots:

        if metric not in summary.columns:
            print(
                f"Skipping plot: metric '{metric}' not found."
            )
            continue

        save_metric_plot(
            summary,
            metric,
            ylabel,
            plots_dir / filename,
            multiply=multiplier
        )

    # --------------------------------------------------
    # WRITE EXPERIMENT NOTES
    # --------------------------------------------------

    notes_path = write_experiment_notes(
        results_dir
    )

    # --------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------

    print("\n" + "=" * 68)
    print("EXPERIMENTS COMPLETED")
    print("=" * 68)

    print(f"Raw results:      {raw_path}")
    print(f"Summary results:  {summary_path}")
    print(f"Plots folder:     {plots_dir}")
    print(f"Experiment notes: {notes_path}")

    print("\nMean results by duration and algorithm:")

    display_columns = [
        "simulation_duration_seconds",
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
        column
        for column in display_columns
        if column in summary.columns
    ]

    print(
        summary[available_columns].to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()
