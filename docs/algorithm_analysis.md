
# Algorithm Analysis

This document describes the algorithms presented in the DPTARA research paper, their mathematical formulations, their current implementation, and the differences between the paper and the Python simulation.

The implementation status refers to the current repository and its individual module tests. Individual validation does not automatically establish complete integration into the event-driven simulation.

---

## 1. Algorithm 1: DPTARA Algorithm

### 1.1 Objective

The Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation (DPTARA) algorithm aims to schedule incoming tasks and allocate available resources in a healthcare edge computing environment.

The framework considers:

- Dynamic task prioritization.
- Adaptive resource allocation.
- Load balancing.
- Task execution and completion.
- Energy consumption.
- Prediction of future resource loads.

The paper describes a hierarchical environment involving local hardware resources, edge resources, and cloud resources.

**Current implementation scope:** The Python simulator initializes 10 edge resources and one cloud resource. Local resource execution is not currently simulated.

### 1.2 Inputs

The paper describes the following inputs:

- T: Set of incoming tasks.
- RL: Set of local resources.
- RE: Set of edge resources.
- RC: Cloud server.

In the current simulation, the active resource set consists of edge resources and one cloud resource.

### 1.3 Outputs

The algorithm evaluates:

- Task execution times.
- Load balancing rates.
- Energy consumption.
- Task performance metrics.
- Predicted future resource loads.

### 1.4 Initialization

The simulation initializes:

- Task and resource entities.
- Resource management components.
- Task generation mechanism.
- Resource allocation mechanism.
- Task execution mechanism.
- Energy management component.
- Metrics collection.
- Load prediction and load balancing components.

The simulator initializes 10 edge resources and one cloud resource using the configured simulation parameters.

### 1.5 Task Prioritization

For an incoming task, the paper uses Algorithm 2 to calculate its dynamically adjusted priority.

The implementation includes:

1. Retrieving the task's original priority.
2. Calculating its aging contribution.
3. Considering the current resource load.
4. Computing the adjusted priority.
5. Using priority values in the priority scheduling component.

The priority calculation and priority scheduling components have been implemented and tested individually.

Complete integration of priority-based scheduling into the event-driven simulation requires further validation.

### 1.6 Resource Selection

The paper describes resource selection across local, edge, and cloud resources.

The current Python implementation follows a more limited allocation strategy:

1. Identify eligible edge resources.
2. Check whether the task can be accommodated by the available resource capacity.
3. Prefer edge resources over the cloud.
4. Among eligible edge resources, select the least-loaded resource.
5. If no eligible edge resource is available, consider the cloud resource.
6. Allocate the task and update the resource load.

The current eligibility check compares task size with available resource capacity.

**Modeling limitation:** Task size is represented in MB, while resource capacity is described using CPU-related units. The paper does not provide sufficient detail to establish a physically consistent conversion. The implementation therefore does not invent a per-task CPU-demand distribution.

### 1.7 Cloud Allocation

The current allocator uses the cloud as a fallback destination.

The allocation procedure is:

1. Search for an eligible edge resource.
2. If one is available, select the least-loaded eligible edge resource.
3. If no eligible edge resource is available, check cloud availability.
4. Allocate the task to the cloud if it satisfies the implemented capacity condition.
5. If no resource is eligible, the task remains unallocated.

The current implementation does not reproduce every priority-based resource reclamation, task splitting, or partial allocation mechanism that may be described in the paper.

### 1.8 Task Execution

After allocation, the task executor:

1. Validates the task and its assigned resource.
2. Calculates network transmission delay.
3. Calculates execution time using the relationship described in the paper.
4. Determines task start and completion times.
5. Updates task execution status.
6. Calculates energy consumption through the energy manager.

The implementation uses:

\[
T_{computing}=\frac{\delta}{\psi_{resource}}
\]

Where:

- \(\delta\): Task input data size.
- \(\psi_{resource}\): Processing speed of the assigned resource.

**Unit limitation:** The paper combines MB and MIPS without specifying a conversion factor. The implementation follows the stated relationship without inventing one. Therefore, execution-time values should be interpreted as outputs of the implemented simulation model.

### 1.9 Load Prediction and Load Balancing

The simulation contains two separate components:

- A historical utilization-based Linear Regression predictor.
- A load-balancing component that calculates resource-level balancing scores.

The predictor estimates future utilization from historical observations.

The load balancer evaluates the deviation between individual resource load and average resource load.

The current regression predictor is an implementation choice and is not an exact reproduction of the paper's Equation (13).

### 1.10 Main Constraints

The current allocation model applies the following conditions:

- A task is allocated only when an eligible resource is found.
- Resource load is updated after allocation.
- Edge resources are preferred over cloud resources.
- The least-loaded eligible edge resource is selected.
- Allocated load is released when the task completes.

The current implementation does not establish deadline feasibility through a CPU-demand-based allocation calculation.

### 1.11 Algorithm 1 Implementation Status

| Component | Status |
|---|---|
| Task generation | Implemented and tested |
| Resource initialization | Implemented and tested |
| Edge resource allocation | Implemented and tested |
| Cloud fallback | Implemented and tested |
| Task execution | Implemented and tested |
| Energy calculation | Implemented and tested |
| Dynamic priority calculation | Implemented and tested individually |
| Priority scheduling | Implemented and tested individually |
| Load prediction | Implemented and tested individually |
| Load balancing | Implemented and tested individually |
| Event-driven simulation | Implemented and tested |
| Complete priority integration | Requires further validation |
| Complete predictive load-balancing integration | Requires further validation |
| Local resource simulation | Not implemented |
| Baseline algorithm comparison | Pending |

---

## 2. Algorithm 2: Dynamic Task Prioritization

### 2.1 Purpose

Algorithm 2, DynamicTaskPrioritization, dynamically adjusts task priority according to original priority, waiting time, deadline, and current resource load.

Its objective is to give appropriate scheduling preference to tasks according to their urgency and system conditions.

### 2.2 Input and Output

- **Input:** Task \(T_i\).
- **Output:** Adjusted priority of task \(T_i\).

### 2.3 Mathematical Formulation

The paper defines dynamic task priority using Equation (11):

\[
P_i = \alpha P_{orig,i}
+ \beta \left(\frac{T_{current}-T_{arrival,i}}{D_i}\right)
- \gamma L_{current,i}
\]

Where:

- \(P_i\): Dynamically calculated task priority.
- \(P_{orig,i}\): Original task priority.
- \(\alpha\): Weight assigned to original priority.
- \(\beta\): Weight assigned to the aging factor.
- \(\gamma\): Weight assigned to current resource load.
- \(T_{current}\): Current system time.
- \(T_{arrival,i}\): Task arrival time.
- \(D_i\): Task deadline.
- \(L_{current,i}\): Current resource load.

### 2.4 Components of the Priority Function

**A. Original Priority Contribution**

The original priority represents the intrinsic importance of a task.

The coefficient \(\alpha\) controls its contribution to the final priority.

**B. Task Aging Contribution**

The aging factor measures elapsed time since task arrival relative to its deadline allowance.

As waiting time increases, the aging contribution increases.

**C. Resource Load Penalty**

The current resource load is subtracted from the priority calculation.

The coefficient \(\gamma\) controls the influence of this penalty.

### 2.5 Algorithm Workflow

The priority calculation follows these steps:

1. Receive a task.
2. Retrieve its original priority and arrival time.
3. Obtain the current simulation time.
4. Retrieve deadline information.
5. Obtain the relevant resource-load value.
6. Calculate the aging factor.
7. Calculate adjusted priority using Equation (11).
8. Update the task priority.
9. Return the calculated priority.

### 2.6 Relationship with Algorithm 1

Algorithm 1 uses the adjusted priority as part of the task scheduling process.

The current repository contains a priority model and a priority scheduling component. Both have been tested individually.

However, their complete integration with the event-driven allocation and execution workflow still requires validation.

### 2.7 Unspecified Implementation Details

The paper does not explicitly establish all the following implementation details:

- Exact numerical values of \(\alpha\), \(\beta\), and \(\gamma\).
- Whether deadline is represented as an absolute timestamp or a duration in every calculation.
- The normalization method for resource load.
- The precise priority sorting convention.
- The frequency of priority recalculation.
- The handling of overdue tasks.
- The exact resource-load measurement interval.

The current implementation uses coefficients of 1.0 as implementation settings. These values are not specified numerical values from the paper.

### 2.8 Implementation Status

**Status: Implemented and individually tested.**

The priority model calculates adjusted task priorities, and the priority scheduling component has been tested using a separate scheduling experiment.

Full integration with the event-driven simulator remains to be validated.

---

## 3. Algorithm 3: CalculateBalancingRate

### 3.1 Purpose

Algorithm 3 calculates the load balancing rate of a selected resource \(R_j\).

Its purpose is to evaluate how closely the workload of an individual resource matches the average workload across all available resources.

### 3.2 Input and Output

**Input:**

- \(R_j\): Selected resource.
- \(R_{total}\): Set of available resources.

**Output:**

- `balancing_rate`: Calculated load balancing score.

### 3.3 Algorithm Workflow

1. Calculate total workload across all available resources.
2. Count the number of resources.
3. Calculate average resource workload.
4. Compare the selected resource's load with the average.
5. Calculate the balancing score.
6. Return the calculated score.

### 3.4 Mathematical Formulation

**Step 1: Total workload**

\[
TotalTasks = \sum_{R_k \in R_{total}} R_k.current\_load
\]

**Step 2: Number of resources**

\[
NumResources = |R_{total}|
\]

**Step 3: Average workload**

\[
AverageLoad = \frac{TotalTasks}{NumResources}
\]

**Step 4: Load balancing rate**

\[
BalancingRate =
\left(
1 -
\frac{|R_j.current\_load - AverageLoad|}
{AverageLoad}
\right)\times 100
\]

### 3.5 Interpretation

- A score close to 100 indicates that the resource load is close to the system-wide average.
- A lower score indicates a larger deviation from the average.
- A negative score is possible when the deviation exceeds the average workload.

**Important:** The formula does not constrain the result to the range 0–100. The implementation preserves the raw formula rather than artificially clamping negative values.

The score should therefore be interpreted as the formula-based balancing score, not as a conventional bounded percentage of balancing effectiveness.

### 3.6 Implementation Considerations

The implementation requires:

- Maintaining a collection of available resources.
- Tracking the current workload of each resource.
- Calculating average workload.
- Computing the balancing score.
- Handling zero average workload to avoid division by zero.

The zero-load handling is an implementation decision because the paper does not explicitly specify this case.

### 3.7 Integration with DPTARA

The load-balancing component evaluates resource workload distribution.

Its output contributes to performance evaluation and can be used when comparing different resource allocation strategies.

### 3.8 Implementation Status

**Status: Implemented and tested.**

The implementation includes the balancing formula and tests for:

- Multiple resources with different loads.
- Average workload calculation.
- Individual resource balancing scores.
- Zero-load handling.
- Negative balancing scores.

The simulator also calculates an average balancing score over observation intervals.

---

## 4. Linear Regression-Based Load Predictor

### 4.1 Purpose

The DPTARA framework incorporates load prediction to estimate future resource conditions and support predictive load balancing.

The paper discusses Linear Regression in its algorithm description, but does not provide a complete specification of its training procedure, features, or dataset.

### 4.2 Position in the DPTARA Workflow

The paper describes a prediction component within the DPTARA workflow.

Its intended role is to estimate future resource loads and help the scheduling mechanism respond to changing workloads.

### 4.3 General Linear Regression Formulation

A general Linear Regression model can be represented as:

\[
\hat{y}=\beta_0+\beta_1x_1+\cdots+\beta_kx_k
\]

Where:

- \(\hat{y}\): Predicted value.
- \(x_1,\ldots,x_k\): Input features.
- \(\beta_0\): Intercept.
- \(\beta_1,\ldots,\beta_k\): Learned coefficients.

This is a general regression formulation, not a complete regression equation specified by the paper.

### 4.4 Paper's Predictive Load Equation

The paper defines future load estimation using Equation (13):

\[
L_{pred,t}=L_{current,t}+
\sum_{i=1}^{n}\lambda_i S_i(1-p_i)
\]

Where:

- \(L_{pred,t}\): Predicted resource load.
- \(L_{current,t}\): Current resource load.
- \(\lambda_i\): Task arrival rate.
- \(S_i\): Task size.
- \(p_i\): Probability of successful task completion.
- \(n\): Number of tasks.

This equation describes the paper's predictive load formulation.

### 4.5 Current Implementation

The repository implements a historical utilization-based Linear Regression predictor.

Its operation is:

1. Collect historical resource utilization observations.
2. Maintain a bounded history of observations.
3. Fit or use a regression model based on historical observations.
4. Predict future utilization values.
5. Keep predictions within the configured utilization range.

The current implementation uses historical utilization observations rather than directly implementing the paper's Equation (13).

Therefore, the regression predictor should be considered an implementation-level approximation, not an exact reproduction of the paper's predictive load equation.

### 4.6 Difference Between the Paper and Implementation

| Aspect | Research Paper | Current Implementation |
|---|---|---|
| Prediction approach | Linear Regression is mentioned; Equation (13) gives a load prediction relationship | Historical utilization-based Linear Regression |
| Prediction inputs | Task-related quantities in the described equation | Historical utilization observations |
| Prediction target | Future resource load | Future utilization |
| Complete training procedure | Not fully specified | Implemented using historical observations |
| Equation (13) reproduction | Described by the paper | Not directly implemented |

The difference must be considered when interpreting the simulation results.

### 4.7 Unspecified Details and Research Questions

The paper does not fully provide:

- The complete training dataset.
- Exact independent variables.
- Exact dependent variable.
- Training and testing methodology.
- Regression coefficients.
- Model evaluation metrics.
- Precise relationship between Linear Regression and Equation (13).

These details remain important when attempting a closer reproduction of the original prediction method.

### 4.8 Implementation Status

**Status: Implemented and individually tested.**

The current predictor has been tested using historical utilization observations and future prediction requests.

Its integration with the complete allocation and scheduling workflow requires further validation.

---

## 5. Summary of Algorithm Implementation Status

| Algorithm or Component | Current Status |
|---|---|
| Algorithm 1: DPTARA workflow | Partially implemented |
| Algorithm 2: Dynamic task prioritization | Implemented and individually tested |
| Priority scheduling | Implemented and individually tested |
| Algorithm 3: Load balancing | Implemented and tested |
| Historical Linear Regression predictor | Implemented and tested |
| Paper Equation (13) load prediction | Not directly implemented |
| Edge resource allocation | Implemented and tested |
| Cloud fallback allocation | Implemented and tested |
| Event-driven execution | Implemented and tested |
| Complete end-to-end integration | Requires further validation |
| Baseline algorithm comparison | Pending |

---

## 6. Important Modeling Limitations

The following issues must be considered when interpreting the implementation:

1. The paper does not specify a complete numerical distribution for individual task CPU demand.
2. The computing-time equation combines task size in MB and processing speed in MIPS without specifying a conversion factor.
3. The resource allocation condition compares task size with CPU-related resource capacity.
4. The exact priority coefficients are not specified by the paper.
5. The current regression predictor differs from the paper's Equation (13).
6. Local resource execution is not included in the current simulator.
7. Deadline feasibility is not currently used as a CPU-demand-based allocation rejection condition.
8. Full integration of priority scheduling and predictive load balancing requires further validation.

These limitations are documented explicitly so that implementation assumptions are not confused with the original paper's specifications.
