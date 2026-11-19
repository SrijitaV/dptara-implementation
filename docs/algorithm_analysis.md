
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
