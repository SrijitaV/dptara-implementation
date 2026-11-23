
# Mathematical Model

## 1. Resource Utilization Efficiency

### Equation (14)

\[
\eta_i = \frac{U_{effective}}{C_{total}}
\times (1-R_{downtime})
\]

Where:

- eta_i: Efficiency of resource i.
- U_effective: Effective resource utilization.
- C_total: Total resource capacity.
- R_downtime: Downtime rate based on historical reliability data.

### Explanation

The efficiency metric evaluates how effectively computational resources are utilized under varying load conditions.

Effective utilization accounts for high-priority tasks, normal-priority tasks, resource utilization, and the Resource Utilization Factor (RUF).

The downtime factor adjusts the efficiency according to resource reliability.

## 2. Energy Consumption Model

### Equation (15)

\[
E = \sum_{i=1}^{n}
\frac{P_i}{\eta_i}
(T_{end,i}-T_{start,i})
\]

Where:

- E: Total energy consumption.
- n: Number of resources/tasks considered.
- P_i: Power consumption of resource i.
- eta_i: Efficiency of resource i.
- T_start,i: Task execution start time.
- T_end,i: Task execution end time.

### Explanation

The energy consumption model considers resource-specific power consumption, efficiency, and task execution duration.

Lower resource efficiency increases the calculated energy consumption for a given power consumption and execution duration.

## 3. Energy Optimization Strategies

The paper describes four strategies:

1. Dynamic Resource Allocation:
   Prioritizes high-priority tasks for low-latency edge processing.

2. Idle Resource Management:
   Transitions idle resources into low-power states.

3. Intelligent Task Offloading:
   Offloads lower-urgency or higher-energy-requirement tasks to cloud servers.

4. Energy-Aware Scheduling:
   Predicts future workload patterns and adjusts configurations proactively.

## 4. Implementation Considerations

The Python implementation will require:

- Resource utilization tracking.
- Resource capacity tracking.
- Downtime tracking.
- Efficiency calculation.
- Power consumption tracking.
- Task execution time tracking.
- Energy consumption calculation.
- Resource power-state management.

Note: The precise calculation of effective utilization and
the Resource Utilization Factor must be verified against
the paper's earlier mathematical definitions before coding.