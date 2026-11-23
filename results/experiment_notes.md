# Experiment notes

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
