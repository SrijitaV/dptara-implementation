# Workload-Intensity Experiment Notes

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
