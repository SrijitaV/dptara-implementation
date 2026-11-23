# Experiment Notes

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
