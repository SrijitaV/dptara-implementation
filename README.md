
# DPTARA Implementation

### Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation for Healthcare Edge Computing

A Python-based implementation and experimental study of the DPTARA framework proposed in the research paper:

**"Dynamic priority-based task scheduling and adaptive resource allocation algorithms for efficient edge computing in healthcare systems."**

This project focuses on understanding the proposed scheduling and resource allocation methodology, implementing its major components, developing an event-driven simulation environment, and evaluating system performance.

The implementation also investigates ambiguities and limitations in the original paper that affect reproducibility.

---

## 1. Research Paper

**Title:** Dynamic priority-based task scheduling and adaptive resource allocation algorithms for efficient edge computing in healthcare systems

**Authors:** J. Anand and B. Karthikeyan

**Journal:** Results in Engineering, Volume 25 (2025), Article 104342

**DOI:** https://doi.org/10.1016/j.rineng.2025.104342

---

## 2. Project Overview

Healthcare applications increasingly depend on IoT devices to collect and process patient information. These applications may require timely processing of monitoring data, emergency alerts, and other healthcare-related computational tasks.

Cloud computing provides substantial computational resources, but communication with distant cloud servers can introduce additional latency.

Mobile Edge Computing (MEC) addresses this challenge by bringing computational resources closer to end devices.

However, edge environments have several challenges:

- Limited computational capacity at edge servers.
- Dynamic task arrivals and varying workloads.
- Different task priorities and deadlines.
- Resource allocation under changing system conditions.
- Uneven workload distribution across servers.
- Energy consumption during task execution.
- Deciding when cloud resources should be used.

The DPTARA paper proposes a framework combining dynamic task prioritization, adaptive resource allocation, load balancing, and energy-aware resource management.

This project implements and evaluates selected components of that framework through a Python-based simulation.

---

## 3. Research Objectives

The objectives of this project are:

1. Study the DPTARA framework and understand its mathematical models and algorithms.
2. Implement the dynamic task priority calculation.
3. Develop resource allocation mechanisms for edge and cloud resources.
4. Build an event-driven task execution simulator.
5. Implement load prediction and load balancing components.
6. Evaluate task completion, latency, deadline, resource-load, and energy metrics.
7. Validate individual modules and their interactions through experiments.
8. Identify implementation gaps and ambiguities in the original paper.
9. Explore possible improvements to the scheduling and resource allocation methodology.
10. Compare the proposed framework with alternative algorithms in future experiments.

---

## 4. System Architecture

The simulation models an IoT-assisted healthcare edge computing environment.

### 4.1 IoT Task Generation

The task generator produces computational tasks using the workload parameters described in the research paper.

Each task contains information such as:

- Task identifier.
- Arrival time.
- Input data size.
- Deadline.
- Original priority.
- Execution status.
- Assigned processing resource.

### 4.2 Edge Computing Layer

The simulation initializes 10 Hospital Workstations (HWs), which act as edge servers.

Each edge resource has attributes including:

- Processing capacity.
- Available resource capacity.
- Power consumption.
- Network transmission latency.
- Current workload.

The resource allocator prefers eligible edge resources and selects the least-loaded eligible edge resource.

### 4.3 Cloud Computing Layer

The simulation initializes one cloud server.

The cloud server provides an alternative allocation destination when an eligible edge resource is unavailable.

### 4.4 Event-Driven Simulation

The simulator manages task arrivals, allocation, execution, completion, and resource release through simulation events.

The event-driven design allows multiple tasks to be processed during a simulation run while maintaining the simulation clock and resource state.

**Implementation scope:** The current simulation includes 10 edge servers and one cloud server. Local resource execution and a complete three-layer local-edge-cloud architecture are not currently implemented.

---

## 5. Implemented Algorithms and Components

### 5.1 Dynamic Task Prioritization

The paper defines dynamic task priority using:

\[
P_i = \alpha P_{orig,i}
+ \beta \left(\frac{T_{current}-T_{arrival,i}}{D_i}\right)
- \gamma L_{current,i}
\]

Where:

- \(P_i\): Dynamically calculated task priority.
- \(P_{orig,i}\): Original task priority.
- \(T_{current}\): Current simulation time.
- \(T_{arrival,i}\): Task arrival time.
- \(D_i\): Task deadline.
- \(L_{current,i}\): Current resource load.
- \(\alpha,\beta,\gamma\): Scaling coefficients.

The priority model and priority scheduling logic have been implemented and tested individually.

The coefficients used in the current implementation are configuration choices because the paper does not specify their exact numerical values.

Full integration of dynamic priority into the complete simulation workflow remains subject to further validation.

### 5.2 Adaptive Resource Allocation

The current resource allocator:

- Checks resource eligibility using available capacity.
- Prefers edge resources over cloud resources.
- Selects the least-loaded eligible edge resource.
- Uses the cloud as a fallback when no eligible edge resource is available.
- Updates resource load during allocation.
- Releases allocated load after task completion.

The current implementation uses task input size as the allocated resource-load quantity.

The paper does not provide a sufficiently specified numerical CPU-demand distribution for individual tasks. Therefore, the implementation does not invent per-task CPU demand values.

### 5.3 Load Prediction

A historical utilization-based Linear Regression predictor has been implemented.

It uses previously observed resource utilization values to estimate future utilization.

The current predictor is an implementation-level approach and is not an exact reproduction of the paper's load-prediction equation.

The paper describes its prediction model as:

\[
L_{pred,t} = L_{current,t} +
\sum_i \lambda_i S_i(1-p_i)
\]

The difference between the paper's equation and the implemented regression-based predictor is retained as an implementation limitation for further investigation.

### 5.4 Load Balancing

A load-balancing component has been implemented to evaluate workload distribution across available resources.

The implementation calculates the balancing score using the equation described in the paper:

\[
LB =
\left(
1-\frac{|L_i-L_{avg}|}{L_{avg}}
\right)\times 100
\]

The raw formula can produce negative values when a resource's load differs significantly from the average load.

Therefore, this score is reported as the formula-based balancing score and should not be interpreted as a conventional percentage constrained between 0% and 100%.

### 5.5 Task Execution

The task executor calculates execution time using the computing-time relationship described in the paper:

\[
T_{computing} = \frac{\delta}{\psi_{resource}}
\]

Where:

- \(\delta\): Task input data size.
- \(\psi_{resource}\): Processing speed of the assigned resource.

Network transmission delay is also included in the simulated task timeline.

**Important modeling limitation:** The paper expresses task size in MB and processing speed in MIPS without specifying the conversion required to obtain physically consistent execution time. The current implementation follows the stated mathematical relationship without introducing an unsupported conversion factor. Consequently, the resulting execution times should be interpreted as simulation-model outputs rather than validated real-world processing times.

### 5.6 Energy Management

The energy manager implements the energy-related calculations described in the paper.

The paper defines resource efficiency as:

\[
\eta_i =
\left(\frac{U_{effective}}{C_{total}}\right)
(1-R_{downtime})
\]

Energy consumption is calculated using:

\[
E =
\sum_i
\left(\frac{P_i}{\eta_i}\right)
(T_{end,i}-T_{start,i})
\]

The energy manager and its calculation logic have been tested independently.

### 5.7 Metrics

The metrics module evaluates:

- Total generated tasks.
- Completed tasks.
- Completion rate.
- Unallocated tasks.
- Tasks completed before their deadlines.
- Late completed tasks.
- Deadline miss rate.
- Deadline met rate.
- Average latency.
- Average execution time.
- Total energy consumption.
- Resource-load ratio.
- Load-balancing score.

The simulator also calculates time-weighted average normalized resource load.

**Metric limitation:** The current resource-load calculation compares task-size-based load values with capacities expressed in MIPS. This is not dimensionally equivalent to physical CPU utilization. The reported metric is therefore labelled as an average normalized resource-load ratio, not actual CPU utilization.

---

## 6. Simulation Parameters

The following parameters are taken from the original research paper.

### 6.1 Workload and System Parameters

| Parameter | Paper Value |
|---|---|
| Number of IoT devices | 50 |
| Number of edge servers (HWs) | 10 |
| Number of cloud servers | 1 |
| Task arrival distribution | Poisson |
| Task arrival rate | 5 tasks/sec |
| Task size | 5–50 MB |
| Task deadline | 10–100 seconds |
| Edge power consumption | 50 W |
| Cloud power consumption | 200 W |
| Edge transmission latency | 5–10 ms |
| Cloud transmission latency | 50–100 ms |

### 6.2 Hardware Configuration

| Parameter | Edge Node | Cloud Node |
|---|---:|---:|
| CPU capacity | 500–3000 MIPS | 2000–10000 MIPS |
| CPU utilization factor | 0.5 | 2.0 (VMs) |
| RAM capacity | 32 GB | 64 GB |

### 6.3 Current Simulation Configuration

The current simulator initializes:

- 10 edge resources.
- 1 cloud resource.
- Poisson task arrivals.
- Task sizes sampled from the paper's specified range.
- Task deadlines sampled from the paper's specified range.
- Edge and cloud power and network-latency parameters based on the paper.

Repeated simulation experiments have been performed using random seeds 42–46. These seeds are implementation-level experimental settings, not values specified by the paper.

**Modeling note:** The paper's task deadlines of 10–100 seconds are distinct from the latency tolerance values discussed elsewhere in the paper, such as 250 ms and 400 ms. These values represent different experimental concepts and should not be treated as interchangeable.

---

## 7. Experimental Validation

Individual modules and integration workflows have been tested through Python experiment scripts.

### 7.1 Implemented and Tested Components

| Component | Validation Status |
|---|---|
| Entity models | Implemented |
| Resource manager | Implemented |
| Task generator | Implemented and tested |
| Resource allocator | Implemented and tested |
| Task executor | Implemented and tested |
| Dynamic priority model | Implemented and tested |
| Priority scheduling | Implemented and tested |
| Energy manager | Implemented and tested |
| Load predictor | Implemented and tested |
| Load balancer | Implemented and tested |
| Metrics module | Implemented and tested |
| Event-driven simulator | Implemented and tested |
| Results dashboard | Implemented |

### 7.2 Full Simulation Validation

One validated 10-second simulation run produced the following results:

| Metric | Observed Result |
|---|---:|
| Simulation makespan | 9.8839 seconds |
| Generated tasks | 41 |
| Completed tasks | 41 |
| Completion rate | 100% |
| Unallocated tasks | 0 |
| Tasks completed on time | 41 |
| Late completed tasks | 0 |
| Deadline miss rate | 0% |
| Deadline met rate | 100% |
| Average latency | 0.0147 seconds |
| Average execution time | 0.0085 seconds |
| Total energy consumption | 2050 J |
| Average normalized resource-load ratio | 0.01% |
| Average load-balancing score | -81.50% |

These values are outputs from the current implementation and one particular simulation configuration. They are not reproduced results from the original paper.

The very low normalized resource-load ratio and the execution-time unit limitation should be considered when interpreting these results.

### 7.3 Repeated Simulation Experiments

Five simulation runs were performed using random seeds 42–46.

Across these runs:

- Total task generation varied with the random seed.
- All generated tasks completed in the tested configurations.
- No deadline misses were observed.
- Average latency varied between runs.
- Energy consumption varied with the generated workload.

The repeated experiments provide initial evidence of consistent behavior under the tested configurations. They do not, by themselves, establish equivalence with the original paper's results.

### 7.4 Test Coverage

The project contains 17 active experiment/test modules that have been individually validated.

A legacy deadline-aware allocation test is retained separately because it expects a CPU-demand calculation and deadline-feasibility rejection that are not part of the current allocator model. It is excluded from the active passing-test count.

---

## 8. Baseline Algorithms and Comparative Evaluation

The original paper reports comparisons against the following approaches:

1. **A-PBRA:** Adaptive and Priority-Based Resource Allocation.
2. **NBIHA:** Novel Bio-Inspired Hybrid Algorithm.
3. **CORA-GT:** Computation Offloading and Resource Allocation using Game Theory.

These algorithms are identified as candidates for comparative evaluation.

Their implementations are not currently available in the repository. The `baselines/` directory currently contains documentation only.

A fair comparison will require implementing and validating each baseline against its original description and running all algorithms under consistent workload, resource, and simulation conditions.

### 8.1 Reference Results Reported in the Original Paper

The following values are reproduced from Table 5 of the research paper.

They are paper-reported reference values, not experimental results generated by this repository.

| Metric | DPTARA | A-PBRA | NBIHA | CORA-GT |
|---|---:|---:|---:|---:|
| Latency (ms) | 320 | 350 | 480 | 560 |
| Resource Utilization (%) | 88 | 57 | 48 | 35 |
| Execution Time (ms) | 335 | 540 | 570 | 1100 |
| Energy Consumption (J) | 321 | 600 | 700 | 802 |

---

## 9. Repository Structure

```text
dptara-implementation/
│
├── baselines/
│   ├── README.md
│   └── __init__.py
│
├── data/
│
├── docs/
│   ├── algorithm_analysis.md
│   ├── implementation_blueprint.md
│   ├── mathematical_model.md
│   ├── paper_analysis.md
│   └── simulation_parameters.md
│
├── experiments/
│   ├── test_concurrent_resource_allocation.py
│   ├── test_deadline_aware_allocation.py
│   ├── test_deadline_metrics.py
│   ├── test_energy_manager.py
│   ├── test_event_driven_execution.py
│   ├── test_full_simulation.py
│   ├── test_load_balancer.py
│   ├── test_load_prediction_integration.py
│   ├── test_load_predictor.py
│   ├── test_metrics.py
│   ├── test_metrics_validation.py
│   ├── test_priority.py
│   ├── test_priority_scheduling.py
│   ├── test_repeated_simulations.py
│   ├── test_resource_allocator.py
│   ├── test_resource_initialization.py
│   ├── test_simulator.py
│   └── test_task_executor.py
│
├── results/
│   └── [Experimental screenshots and validation outputs]
│
├── src/
│   ├── models/
│   │   ├── entities.py
│   │   ├── load_predictor.py
│   │   └── priority_model.py
│   │
│   ├── energy_manager.py
│   ├── load_balancer.py
│   ├── metrics.py
│   ├── resource_allocator.py
│   ├── resource_manager.py
│   ├── simulator.py
│   ├── task_executor.py
│   └── task_generator.py
│
├── tests/
│
├── notebooks/
│
├── .gitignore
├── requirements.txt
├── README.md
└── paper implementing .pdf
```

---

## 10. Current Limitations and Open Research Questions

The following points require further investigation before claiming a complete reproduction of the original framework.

1. **Task CPU demand:** The paper does not provide a clear numerical distribution for per-task CPU demand.
2. **Unit consistency:** The computing-time relationship combines task size in MB with processing capacity in MIPS without specifying the necessary conversion.
3. **Resource capacity model:** The resource allocation condition compares task size with resource capacity described in CPU-related units.
4. **Priority coefficients:** Exact numerical values for the priority scaling coefficients are not specified.
5. **Load prediction:** The current historical Linear Regression predictor differs from the prediction equation presented in the paper.
6. **Three-layer execution:** Local resource execution is not included in the current simulation.
7. **Deadline-aware allocation:** Deadline feasibility is not currently used as an allocation rejection condition.
8. **Priority integration:** Full integration of dynamic priority into the event-driven scheduling workflow requires further validation.
9. **Predictive load balancing:** The interaction between load prediction and allocation decisions requires further end-to-end validation.
10. **Baseline comparison:** A-PBRA, NBIHA, and CORA-GT implementations are pending.
11. **Paper result reproduction:** The current simulation outputs have not yet been demonstrated to reproduce the numerical results reported in the original paper.

These limitations are important because implementation choices should not be confused with specifications explicitly provided by the research paper.

---

## 11. Planned Work

The next stages of the project are:

- Refine event handling for simultaneous task arrivals and completions.
- Revisit the deadline and resource allocation model.
- Complete integration of dynamic priority into scheduling.
- Validate the integration of load prediction and load balancing.
- Verify the complete simulation workflow.
- Implement and validate the paper's algorithms and comparison baselines.
- Run the experimental scenarios described in the paper.
- Generate quantitative plots and comparative results.
- Investigate possible improvements to the original scheduling and resource allocation methodology.
- Document experimental deviations and research findings.

---

## 12. Technologies Used

- **Programming Language:** Python
- **Environment:** Python virtual environment
- **Development Environment:** Visual Studio Code
- **Simulation:** Custom event-driven simulation framework
- **Data Analysis and Visualization:** Python-based tools

---

## 13. Project Status

The project currently has a working Python simulation environment with implemented and individually tested modules for task generation, resource management, allocation, execution, priority calculation, load prediction, load balancing, energy management, and performance evaluation.

The current focus is on validating end-to-end integration, addressing modeling limitations, and preparing the framework for comparative experiments and further algorithmic improvements.

**This repository represents an ongoing research implementation, not yet a complete reproduction of every component and experimental result reported in the original paper.**
