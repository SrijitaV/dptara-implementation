
# Implementation Blueprint

## 1. Implementation Objective

The objective of this project is to implement and evaluate the Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation (DPTARA) framework described in the research paper.

The implementation uses Python to develop a simulation environment containing task generation, resource management, task scheduling, execution, energy calculation, load prediction, load balancing, and performance evaluation components.

The project distinguishes between:

1. Components already implemented and independently tested.
2. Components integrated and validated through simulation experiments.
3. Components requiring further integration or validation.
4. Paper features that have not yet been reproduced.

The major components considered in the implementation are:

- Task generation and classification.
- Dynamic task prioritization.
- Historical load prediction.
- Adaptive resource allocation.
- Edge and cloud resource selection.
- Energy calculation and management.
- Event-driven simulation.
- Performance evaluation.
- Comparison against baseline algorithms.

---

## 2. Current System Architecture

The current simulator models two computing resource categories:

1. Edge servers (Hospital Workstations).
2. A centralized cloud server.

The paper describes an additional IoT device layer that generates computational tasks. The current implementation uses an aggregate task generator rather than explicitly simulating the behavior of all 50 IoT devices.

### 2.1 Task Generation

Location: `src/task_generator.py`

Responsibilities:

- Generate tasks using a Poisson arrival process.
- Generate task sizes using the specified uniform distribution.
- Assign task deadlines.
- Generate task attributes required by the simulator.

The current implementation uses the paper's task arrival rate, task size range, and deadline range.

### 2.2 Edge Resources

Responsibilities:

- Represent edge computing resources.
- Maintain resource capacity and current load.
- Track processing speed, power consumption, and network latency.
- Support task allocation and resource release.

The simulator initializes 10 edge resources.

### 2.3 Cloud Resource

Responsibilities:

- Provide additional computing capacity.
- Accept tasks when suitable edge resources are unavailable.
- Represent higher network latency and power consumption compared with edge resources.

The simulator initializes one cloud resource.

**Scope limitation:** The current architecture does not implement a separate local-device computing layer or explicitly model 50 individual IoT devices.

---

## 3. Python Module Structure and Responsibilities

### 3.1 Task Generation Module

Location: `src/task_generator.py`

Responsibilities:

- Generate tasks using a Poisson arrival process.
- Generate task sizes using a uniform distribution.
- Assign task deadlines.
- Generate task attributes used by scheduling and execution.

**Status:** Implemented and tested.

### 3.2 Entity Models

Location: `src/models/entities.py`

Responsibilities:

- Represent tasks.
- Represent computational resources.
- Maintain task and resource attributes.
- Track task states and resource assignments.

**Status:** Implemented.

### 3.3 Resource Management Module

Location: `src/resource_manager.py`

Responsibilities:

- Initialize edge and cloud resources.
- Maintain resource capacity.
- Track current resource load.
- Check resource availability.
- Update resource load after allocation.
- Release allocated load after task completion.

**Status:** Implemented and tested through resource allocation and event-driven execution experiments.

**Modeling limitation:** The current allocator reserves task-size load in MB against resource capacity represented in MIPS. This follows the current implementation model but does not establish a physically consistent CPU reservation model.

### 3.4 Dynamic Priority Module

Location: `src/models/priority_model.py`

Responsibilities:

- Calculate dynamically adjusted task priorities.
- Consider original task priority.
- Consider task waiting time.
- Consider resource load.
- Apply the priority equation described in the paper.

The implementation uses coefficients of 1.0 for alpha, beta, and gamma as implementation settings because the paper does not provide exact numerical values.

**Status:** Priority calculation and priority scheduling have been independently tested. Full integration of dynamic priority into the main resource allocation workflow remains pending.

### 3.5 Load Prediction Module

Location: `src/models/load_predictor.py`

Responsibilities:

- Maintain historical resource utilization observations.
- Use Linear Regression to estimate future utilization.
- Generate predicted load values.
- Provide predictions to components that use load estimates.

**Status:** Implemented and independently tested.

The current predictor uses historical utilization observations and Linear Regression. It differs from the load prediction equation described in the paper and must be treated as an implementation approach rather than an exact reproduction of that equation.

### 3.6 Resource Allocation Module

Location: `src/resource_allocator.py`

Responsibilities:

- Identify eligible computing resources.
- Prefer eligible edge resources.
- Select the least-loaded eligible edge resource.
- Use the cloud resource as a fallback when edge allocation is unavailable.
- Reserve resource load.
- Release resource load after task execution.

**Status:** Implemented and tested.

The current implementation does not reproduce all the resource reclamation, partial allocation, task splitting, and priority-based resource preemption behavior described in the paper.

### 3.7 Load Balancing Module

Location: `src/load_balancer.py`

Responsibilities:

- Calculate the load balancing rate.
- Evaluate resource load distribution.
- Apply the balancing-rate formula described in Algorithm 3.

**Status:** Implemented and independently tested.

The current module calculates the balancing-rate metric. This should not be interpreted as proof that a complete task migration or dynamic load redistribution mechanism has been implemented.

The formula can produce negative values. These are retained as raw formula outputs rather than clamped to a percentage range.

### 3.8 Energy Management Module

Location: `src/energy_manager.py`

Responsibilities:

- Track resource power consumption.
- Calculate resource utilization efficiency.
- Calculate energy consumption.
- Use task execution duration in energy calculations.

**Status:** Implemented and independently tested.

The energy manager implements the efficiency and energy equations described in the paper.

Dynamic idle-resource low-power transitions and the complete energy-aware scheduling framework have not been verified as implemented.

### 3.9 Task Execution Module

Location: `src/task_executor.py`

Responsibilities:

- Validate task allocation and execution state.
- Calculate execution duration using the current processing-time model.
- Incorporate network latency.
- Record task start and completion times.
- Invoke energy calculation.
- Update task execution status.

**Status:** Implemented and tested.

**Modeling limitation:** The current execution-time calculation follows the paper's stated relationship between task size and resource processing speed. However, task size in MB and processing speed in MIPS have inconsistent units, and the paper does not specify the required conversion.

### 3.10 Simulation Engine

Location: `src/simulator.py`

Responsibilities:

- Initialize simulation components.
- Coordinate task arrivals.
- Schedule task execution.
- Process completion events.
- Maintain simulation time.
- Release resources after task completion.
- Collect simulation results.

**Status:** Event-driven simulation is implemented and tested.

The event-driven execution test validates task allocation, execution, completion-event processing, and resource release. Further validation of simultaneous arrivals and completions is still important.

### 3.11 Metrics and Evaluation Module

Location: `src/metrics.py`

Responsibilities:

- Calculate task completion statistics.
- Calculate deadline met and miss rates.
- Calculate average task latency.
- Calculate average execution time.
- Calculate total energy consumption.
- Calculate resource-load metrics.

**Status:** Implemented and tested.

The simulator also calculates time-weighted resource-load measurements.

The current normalized resource-load ratio should not be interpreted as physical CPU utilization because task-size load and CPU capacity use different units.

---

## 4. Current Simulation Workflow

The current implementation follows an event-driven execution process.

1. Initialize simulation parameters.
2. Initialize edge and cloud resources.
3. Initialize task generation and simulation components.
4. Generate incoming tasks.
5. Schedule task arrival events.
6. Process task arrivals.
7. Identify eligible computing resources.
8. Select the least-loaded eligible edge resource.
9. Use cloud fallback when edge allocation is unavailable.
10. Reserve resource load for the allocated task.
11. Calculate task execution and network delay.
12. Schedule task completion events.
13. Process task completion events.
14. Calculate energy consumption.
15. Release allocated resource load.
16. Update performance metrics.
17. Produce simulation results.

The priority model, load predictor, and load balancing module have also been developed and tested. Their complete integration into one unified scheduling workflow remains an area of further development.

---

## 5. Algorithm Implementation Mapping

| Paper Component | Implementation Module | Current Status |
|---|---|---|
| Algorithm 1: DPTARA | `resource_allocator.py` | Partial implementation |
| Algorithm 2: Dynamic Task Prioritization | `priority_model.py` | Implemented and independently tested |
| Algorithm 3: CalculateBalancingRate | `load_balancer.py` | Implemented and tested |
| Linear Regression | `load_predictor.py` | Implemented and tested |
| Energy calculation | `energy_manager.py` | Implemented and tested |
| Task generation | `task_generator.py` | Implemented and tested |
| Resource management | `resource_manager.py` | Implemented and tested |
| Task execution | `task_executor.py` | Implemented and tested |
| Simulation execution | `simulator.py` | Implemented and tested |
| Performance evaluation | `metrics.py` | Implemented and tested |
| Baseline algorithms | `baselines/` | Pending implementation |

**Note:** A module being implemented and independently tested does not necessarily mean that the complete algorithm described in the paper has been reproduced or integrated.

---

## 6. Data Flow

The current main simulation workflow can be represented as follows:

```text
Task Generator
      |
      v
Task Arrival Events
      |
      v
Resource Availability Check
      |
      v
Resource Allocation
      |
      +------> Eligible Edge Resource
      |
      +------> Cloud Fallback
      |
      v
Task Execution
      |
      v
Completion Event
      |
      v
Energy Calculation
      |
      v
Resource Release
      |
      v
Metrics Collection
      |
      v
Simulation Results
```

Additional modules:

- Dynamic Priority Model: calculates task priority.
- Load Predictor: estimates future resource utilization.
- Load Balancer: calculates the balancing-rate metric.
- Energy Manager: calculates efficiency and energy consumption.

These modules have individual validation tests, but their complete end-to-end integration requires further work.

---

## 7. Testing and Validation Strategy

The implementation has been tested at module, integration, and simulation levels.

### 7.1 Module-Level Testing

The following components have been tested independently:

- Task generation.
- Resource initialization.
- Resource management.
- Resource allocation.
- Dynamic priority calculation.
- Priority scheduling.
- Load prediction.
- Load balancing calculation.
- Energy calculation.
- Task execution.
- Metrics calculation.

### 7.2 Integration Testing

The following integration scenarios have been tested:

- Task allocation and execution.
- Resource allocation with cloud fallback.
- Load prediction integration.
- Concurrent resource allocation.
- Event-driven task execution and resource release.
- Full simulation execution.
- Deadline metric validation.

### 7.3 Repeated Simulation Testing

Five simulation runs using random seeds 42–46 were executed to check repeatability.

The experiments recorded task generation, completion rate, deadline metrics, latency, execution time, energy consumption, and resource-load measurements.

### 7.4 Remaining Experimental Validation

The following work remains:

- Complete integration of dynamic priority with the main scheduler.
- Further integration and validation of load prediction and balancing.
- Validation of the complete DPTARA scheduling workflow.
- Reproduction of the paper's experimental scenarios.
- Implementation and evaluation of A-PBRA, NBIHA, and CORA-GT.
- Comparative evaluation using consistent workloads and simulation settings.

---

## 8. Implementation Assumptions and Open Questions

The following limitations and unresolved details must remain visible during further development.

1. **Priority coefficients:** The paper does not provide exact numerical values for alpha, beta, and gamma. The implementation currently uses 1.0 for each coefficient.
2. **Load prediction:** The current historical Linear Regression predictor differs from the paper's stated load prediction equation.
3. **Task CPU demand:** The paper does not provide a precise numerical distribution for per-task CPU demand. No unsupported distribution has been introduced.
4. **Execution-time units:** The relationship between task size in MB and resource processing speed in MIPS has a unit-consistency limitation.
5. **Resource capacity:** The current allocator uses task-size load against resource capacity represented in MIPS. A physically consistent CPU allocation model requires further investigation.
6. **Priority-based resource handling:** Complete priority-based preemption and resource reclamation have not been reproduced.
7. **Energy optimization:** Energy calculation is implemented, but idle-resource low-power transitions have not been verified.
8. **Baseline algorithms:** Their implementations and experimental configurations remain pending.
9. **Paper experimental details:** Some workload and experimental procedures are not fully specified.

Any unspecified numerical values or implementation choices must be documented explicitly rather than presented as values reported by the paper.

---

## 9. Implementation Status

**Status:** Core simulation modules implemented and tested; complete paper-level integration and experimental reproduction remain in progress.

### Completed and Tested

- Task generation.
- Entity models.
- Resource initialization and management.
- Resource allocation and cloud fallback.
- Dynamic priority calculation.
- Priority scheduling validation.
- Historical load prediction.
- Load balancing calculation.
- Energy and efficiency calculation.
- Task execution.
- Event-driven simulation.
- Metrics collection.
- Repeated simulation experiments.

### Remaining Work

- Integrate dynamic priority into the main scheduling workflow.
- Complete integration of load prediction and balancing.
- Revisit the resource capacity and deadline models.
- Validate simultaneous event handling.
- Validate the complete scheduling workflow.
- Reproduce the paper's experimental scenarios.
- Implement and validate baseline algorithms.
- Perform comparative experiments.
- Analyze deviations between the paper and simulation results.

The current implementation provides a working simulation foundation. It should not yet be described as a complete reproduction of every DPTARA algorithm and experimental result.
