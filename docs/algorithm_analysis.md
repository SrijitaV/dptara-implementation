
# Algorithm Analysis

## 1. Algorithm 1: DPTARA Algorithm

### 1.1 Objective

The Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation (DPTARA) algorithm schedules incoming tasks and allocates available resources across a hierarchical computing environment consisting of local hardware resources, edge resources, and a cloud server.

Its objectives include:
- Dynamic task prioritization.
- Efficient resource allocation.
- Load balancing.
- Reduced task execution time.
- Reduced energy consumption.
- Prediction of future resource loads.

### 1.2 Inputs

- T: Set of incoming tasks.
- RL: Set of local resources.
- RE: Set of edge resources.
- RC: Cloud server.

### 1.3 Outputs

- Task execution times.
- Load balancing rates.
- Energy consumption.
- Task execution metrics.
- Predicted future resource loads.

### 1.4 Initialization

The algorithm initializes:

- task_metrics: Dictionary for storing task performance metrics.
- load_forecaster: Linear Regression model for future load prediction.
- Resource queues and resource utilization information.

Tasks are categorized into:

- Rp: High-priority tasks.
- Rn: Normal-priority tasks.

Total resource demand is calculated separately for both categories using task sizes.

### 1.5 Task Prioritization

For every incoming task:

1. Calculate its dynamically adjusted priority using Algorithm 2.
2. Initialize selected_resource as None.
3. Initialize minimum load as infinity.

### 1.6 Resource Selection

The algorithm examines resources in:

Rtotal = RL union RE union {RC}

For each resource:

1. Check whether current_load + task_size is within capacity.
2. Check whether the resource's current load is lower than the minimum load found so far.
3. Select the feasible resource with the lowest current load.

### 1.7 Cloud Allocation

If no local or edge resource can handle a task:

1. Check available resources and priority-based allocation.
2. Verify whether the cloud server has sufficient capacity.
3. Allocate the task to the cloud if feasible.
4. If the cloud is also overloaded, report the overloaded condition.

### 1.8 Task Queuing and Execution

After resource selection:

1. Insert the task into the selected resource's queue.
2. Increase the resource's current load by the task size.
3. Process queued tasks.
4. Record task execution start time.
5. Simulate task execution.
6. Calculate completion time.
7. Calculate resource efficiency.
8. Calculate energy consumption.
9. Update task_metrics.

### 1.9 Load Prediction

After task execution, the algorithm uses the initialized Linear Regression model to predict future resource loads using task-size information.

The predicted loads are reported and the performance metrics are plotted.

### 1.10 Main Constraints

The resource allocation process follows these constraints:

- C1: Resource load must not exceed its capacity.
- C2: Task priority must align with the resource allocation policy.
- C3: Cloud resource load must not exceed cloud capacity.

### 1.11 Supporting Algorithms

Algorithm 1 depends on:

- Algorithm 2: DynamicTaskPrioritization()
- Algorithm 3: CalculateBalancingRate()
- Linear Regression: Future load prediction.

### 1.12 Implementation Considerations

The Python implementation requires:

- Task representation.
- Resource representation.
- Resource queues.
- Capacity checking.
- Priority-based task ordering.
- Resource selection.
- Cloud fallback.
- Task execution simulation.
- Execution-time calculation.
- Energy calculation.
- Load balancing calculation.
- Future load prediction.
- Metric collection and visualization.

### 1.13 Unspecified Details Requiring Investigation

The paper does not fully specify:

- The exact resource queue scheduling mechanism.
- The handling of a task when every resource is overloaded.
- The exact execution-time simulation procedure.
- The complete training data and prediction procedure for Linear Regression.
- The precise mechanics of priority-based resource reservation.

These details must be investigated and documented before implementation decisions are finalized.

## 2. Algorithm 2: Dynamic Task Prioritization

### 2.1 Purpose

Algorithm 2, DynamicTaskPrioritization, dynamically adjusts the priority of incoming tasks based on their original priority, waiting time, deadline, and current resource load.

Its primary objective is to ensure that urgent tasks receive appropriate scheduling preference while considering the workload of the assigned resources.

### 2.2 Input and Output

- **Input:** Task `Ti`.
- **Output:** Adjusted priority of task `Ti`.

### 2.3 Mathematical Formulation

The paper defines dynamic task priority using Equation (11):

\[
P_i = \alpha P_{orig,i}
+ \beta \left(\frac{T_{current}-T_{arrival,i}}{D_i}\right)
- \gamma L_{current,i}
\]

Where:

- `Pi`: Dynamically calculated task priority.
- `P_orig,i`: Original task priority.
- `alpha`: Weight assigned to original priority.
- `beta`: Weight assigned to the aging factor.
- `gamma`: Weight assigned to current resource load.
- `T_current`: Current system time.
- `T_arrival,i`: Task arrival time.
- `D_i`: Task deadline.
- `L_current,i`: Current load of the resource allocated to the task.

### 2.4 Components of the Priority Function

**A. Original Priority Contribution**

The original priority represents the intrinsic importance of a task. The coefficient alpha controls its contribution to the final priority.

**B. Task Aging Contribution**

The aging factor measures the elapsed time since task arrival relative to its deadline allowance.

As the task waits longer, its aging contribution increases, helping prevent tasks from remaining unattended indefinitely.

**C. Resource Load Penalty**

The current resource load is subtracted from the priority calculation. This penalizes tasks associated with heavily loaded resources and encourages workload balancing.

### 2.5 Algorithm Workflow

1. Receive a task as input.
2. Retrieve its original priority and arrival time.
3. Obtain the current system time.
4. Retrieve its deadline information.
5. Obtain the current load of its allocated resource.
6. Calculate the aging factor.
7. Calculate the adjusted priority using Equation (11).
8. Update the task's priority.
9. Return the adjusted priority.

### 2.6 Relationship with Algorithm 1

Algorithm 1 invokes DynamicTaskPrioritization for every incoming task before selecting a suitable resource.

The adjusted priority is subsequently used as part of the resource selection and scheduling process.

Algorithm 2 therefore acts as a supporting priority-calculation component within the overall DPTARA framework.

### 2.7 Unspecified Implementation Details

The paper does not explicitly establish all the following implementation details:

- Exact values of alpha, beta and gamma.
- Whether deadline is represented as an absolute timestamp or a duration.
- The normalization method for resource load.
- The precise priority sorting convention.
- The frequency of priority recalculation.
- The handling of overdue tasks.
- The exact resource-load measurement interval.

These details must be investigated before finalizing the implementation.

### 2.8 Implementation Considerations

The implementation will require a task representation containing original priority, arrival time, deadline information, and current resource association.

A separate priority calculation function will implement Equation (11) and return the dynamically adjusted priority.

The function will be integrated into the main DPTARA scheduling workflow.

**Note:** Numerical coefficients and other unspecified parameters must be identified through the paper or explicitly documented as experimental implementation assumptions.


## 3. Algorithm 3: CalculateBalancingRate

### 3.1 Purpose

Algorithm 3 calculates the load balancing rate of a selected resource Rj.

Its purpose is to measure how evenly the workload is distributed across the available resources.

The algorithm compares the current load of a particular resource with the average load across all resources.

A resource whose load is close to the average load contributes to better load balancing.

### 3.2 Input and Output

**Input:**
- Rj: The selected resource for which the balancing rate is calculated.
- Rtotal: The set of all available resources.

**Output:**
- balancing_rate: The calculated load balancing rate for resource Rj, expressed as a percentage.

### 3.3 Algorithm Workflow

The algorithm performs the following operations:

1. Calculate the total workload across all available resources by summing their current loads.
2. Count the total number of available resources.
3. Calculate the average workload by dividing the total workload by the number of resources.
4. Compare the current load of the selected resource with the calculated average load.
5. Calculate the balancing rate based on the deviation between the selected resource's load and the average load.
6. Return the calculated balancing rate.

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

- A balancing rate close to 100% indicates that the resource load is close to the system-wide average.
- A lower balancing rate indicates a larger deviation from the average workload.
- The algorithm provides a numerical measure of workload distribution across resources.

### 3.6 Implementation Considerations

The implementation requires:

- Maintaining a collection of all available resources.
- Tracking the current workload of each resource.
- Calculating the average workload dynamically.
- Computing the balancing rate for the selected resource.
- Handling cases where the average workload is zero to avoid division by zero.

**Important:** The paper does not explicitly specify the handling of zero average load. This must be documented as an implementation decision rather than attributed to the original algorithm.

### 3.7 Integration with DPTARA

CalculateBalancingRate is used to evaluate the workload distribution across resources.

Its output contributes to the evaluation of the overall scheduling and resource allocation strategy.

The calculated balancing rate can subsequently be used when evaluating the performance of DPTARA against baseline scheduling approaches.

### 3.8 Unspecified Details

The following details require further investigation before implementation:

- Whether balancing rate is calculated after every task allocation or after processing a batch of tasks.
- Whether the balancing rate is calculated for individual resources or aggregated across all resources.
- How zero average workload should be handled.
- How the balancing rate is incorporated into the overall objective function.
- Whether the calculated rate is used directly for scheduling decisions or only for performance evaluation.

These details must be verified against the mathematical model and experimental methodology of the paper.



---

## 4. Linear Regression-Based Load Forecaster

### 4.1 Purpose

The DPTARA framework incorporates Linear Regression as a load forecasting component.

Its purpose is to predict future resource loads using task-related information. These predictions support predictive load balancing and help prevent resource overload.

### 4.2 Position in the DPTARA Workflow

According to Algorithm 1:

1. The load forecaster is initialized using Linear Regression.
2. Tasks are processed and their relevant metrics are recorded.
3. Task sizes are supplied to the prediction component.
4. Future resource loads are predicted.
5. The predicted loads are used as part of the predictive load balancing mechanism.

### 4.3 Input and Output

**Input:**
- Task sizes.
- Historical or previously collected workload information, if available.

**Output:**
- Predicted future resource loads.

Note: The paper explicitly shows task sizes as the prediction input in Algorithm 1. It does not fully define the training dataset or feature construction procedure.

### 4.4 Mathematical Background

A general Linear Regression model can be represented as:

\[
\hat{y}=\beta_0+\beta_1x_1+\cdots+\beta_kx_k
\]

Where:

- \(\hat{y}\): Predicted value.
- \(x_1,\ldots,x_k\): Input features.
- \(\beta_0\): Intercept.
- \(\beta_1,\ldots,\beta_k\): Learned coefficients.

This is the general regression formulation, not a complete regression equation specified by the paper.

### 4.5 Relationship with Predictive Load Balancing

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

This equation describes the paper's predictive load balancing formulation.

The precise relationship between this equation and the Linear Regression predictor requires further verification before implementation.

### 4.6 Implementation Requirements

The following components must be established:

1. Identify the features used for regression.
2. Identify the prediction target.
3. Determine how training samples are generated.
4. Construct the training dataset.
5. Train the Linear Regression model.
6. Generate future load predictions.
7. Evaluate prediction performance.
8. Integrate predictions into the scheduling workflow.

### 4.7 Unspecified Details and Research Questions

The paper does not explicitly provide:

- The complete training dataset.
- The exact independent variables.
- The exact dependent variable.
- The training and testing methodology.
- The regression coefficients.
- The model evaluation metrics.
- The exact relationship between the regression output and Equation (13).

These details must be investigated and documented as implementation decisions.

### 4.8 Implementation Status

Status: Pending implementation.

The regression component has been identified and its role in DPTARA has been documented. Its precise training and prediction methodology must be established before coding.
