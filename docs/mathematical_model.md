
# Mathematical Model

This document describes the mathematical models related to resource utilization efficiency and energy consumption in the DPTARA research paper, along with their current implementation status.

The original equations are retained, while implementation-specific details and limitations are documented separately.

---

## 1. Resource Utilization Efficiency

### Equation (14)

The paper defines resource utilization efficiency as:

\[
\eta_i =
\frac{U_{effective}}{C_{total}}
\times (1-R_{downtime})
\]

Where:

- \(\eta_i\): Efficiency of resource \(i\).
- \(U_{effective}\): Effective resource utilization.
- \(C_{total}\): Total resource capacity.
- \(R_{downtime}\): Downtime rate based on historical reliability data.

### Explanation

The efficiency metric evaluates how effectively computational resources are utilized under varying load conditions.

Effective utilization accounts for high-priority tasks, normal-priority tasks, resource utilization, and the Resource Utilization Factor (RUF).

The downtime factor adjusts the efficiency according to resource reliability.

### Current Implementation

The energy manager implements the resource efficiency calculation using Equation (14).

The calculation has been independently tested with a sample resource configuration.

Example validation:

| Parameter | Test Value |
|---|---:|
| Resource | E1 |
| Resource utilization | 0.50 |
| Calculated efficiency | 0.4750 |
| Power consumption | 50 W |
| Execution duration | 10 seconds |
| Calculated energy | 1052.6316 J |

This is a module-level validation example, not a result from the full simulation.

---

## 2. Energy Consumption Model

### Equation (15)

The paper defines energy consumption as:

\[
E = \sum_{i=1}^{n}
\frac{P_i}{\eta_i}
(T_{end,i}-T_{start,i})
\]

Where:

- \(E\): Total energy consumption.
- \(n\): Number of resources or execution contributions considered.
- \(P_i\): Power consumption of resource \(i\).
- \(\eta_i\): Efficiency of resource \(i\).
- \(T_{start,i}\): Task execution start time.
- \(T_{end,i}\): Task execution end time.

### Explanation

The energy consumption model considers resource-specific power consumption, efficiency, and execution duration.

For a given power consumption and execution duration, lower resource efficiency increases the calculated energy consumption.

### Current Implementation

The energy manager implements the energy calculation using the relationship described in Equation (15).

The calculation uses:

1. Resource power consumption.
2. Calculated resource efficiency.
3. Execution start time.
4. Execution completion time.

The energy manager has been independently tested.

The task executor also invokes energy calculation during task execution.

The implementation validation confirms that the energy calculation produces the expected result for the tested resource configuration.

---

## 3. Energy Optimization Strategies

The paper describes four energy optimization strategies.

### 3.1 Dynamic Resource Allocation

Prioritizes high-priority tasks for low-latency edge processing.

**Current implementation:** Edge resource allocation and cloud fallback are implemented. Full energy-aware integration of this strategy requires further validation.

### 3.2 Idle Resource Management

Transitions idle resources into low-power states to reduce unnecessary energy consumption.

**Current implementation:** Dynamic low-power state transitions for idle resources have not been verified as implemented.

### 3.3 Intelligent Task Offloading

Offloads lower-urgency or higher-energy-requirement tasks to cloud servers when appropriate.

**Current implementation:** Cloud fallback allocation is implemented. The complete energy-aware offloading decision described by the paper is not currently reproduced.

### 3.4 Energy-Aware Scheduling

Predicts future workload patterns and adjusts resource configurations proactively.

**Current implementation:** A historical utilization-based Linear Regression predictor is implemented. Its complete integration with energy-aware scheduling requires further validation.

---

## 4. Implementation Requirements and Status

| Requirement | Current Status |
|---|---|
| Resource utilization tracking | Implemented |
| Resource capacity tracking | Implemented |
| Downtime-related efficiency calculation | Included in energy model |
| Efficiency calculation | Implemented and tested |
| Power consumption tracking | Implemented |
| Task execution time tracking | Implemented |
| Energy consumption calculation | Implemented and tested |
| Energy calculation during task execution | Implemented |
| Idle resource low-power transitions | Not verified |
| Complete energy-aware task offloading | Requires further validation |
| Predictive energy-aware scheduling | Requires further validation |

---

## 5. Modeling Considerations and Limitations

The following points should be considered when interpreting the energy model and its simulation results.

1. The paper defines resource efficiency and energy consumption through Equations (14) and (15).
2. The exact numerical procedure for calculating every component of effective utilization and the Resource Utilization Factor must be interpreted in conjunction with the paper's earlier mathematical definitions.
3. The implementation includes the efficiency and energy calculations, but this does not establish that every energy optimization strategy described in the paper has been reproduced.
4. Energy results depend on the resource power configuration, efficiency calculation, and simulated execution duration.
5. The task execution-time model has a unit-consistency limitation because the paper does not specify the conversion between task size in MB and processing speed in MIPS.

The energy calculations are implemented and tested, but the complete energy-aware scheduling framework requires further integration and validation.
