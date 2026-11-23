
# Research Paper Analysis

## 1. Paper Information

**Title:** Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation Algorithms for Efficient Edge Computing in Healthcare Systems

**Authors:** J. Anand and B. Karthikeyan

**Journal:** Results in Engineering

**Volume:** 25

**Publication Year:** 2025

**Article Number:** 104342

**DOI:** https://doi.org/10.1016/j.rineng.2025.104342

---

## 2. Research Problem

Healthcare monitoring systems increasingly depend on Internet of Things (IoT) devices such as wearable sensors and medical monitoring equipment.

These devices continuously generate data that must be processed within an acceptable time. Some tasks, such as emergency alerts, require immediate processing, while routine monitoring tasks can tolerate longer delays.

Traditional cloud computing systems process data in remote data centres. This can introduce communication latency and make them unsuitable for applications requiring rapid responses.

Mobile Edge Computing (MEC) addresses this limitation by bringing computational resources closer to IoT devices. However, edge resources are limited and may become overloaded when many devices generate tasks simultaneously.

The paper identifies several challenges:

- High latency when processing healthcare tasks through remote cloud servers.
- Limited computational resources at edge nodes.
- Uneven workload distribution across edge nodes.
- Different urgency levels among healthcare tasks.
- Increased energy consumption due to inefficient resource allocation.
- Difficulty maintaining performance under changing task arrival rates.

The central problem addressed by the paper is how to schedule healthcare tasks dynamically and allocate available edge and cloud resources efficiently while considering task priorities, latency, energy consumption, and resource utilization.

---

## 3. Research Objectives

The proposed DPTARA mechanism aims to:

1. Dynamically adjust task priorities according to their urgency and system conditions.
2. Reduce task processing and response delays by prioritizing critical healthcare requests.
3. Allocate computational resources adaptively across edge and cloud infrastructure.
4. Balance workloads across available computing resources.
5. Reduce energy consumption through adaptive resource management.
6. Improve resource utilization.
7. Evaluate the proposed mechanism against existing approaches.

The paper considers four major performance objectives:

- Average latency
- Task execution time
- Energy consumption
- Resource utilization

---

## 4. Proposed System Architecture

The proposed architecture consists of three main components.

### 4.1 IoT Devices

IoT devices generate healthcare-related tasks.

Examples include:

- Patient monitoring data
- Emergency alerts
- Routine health check-up data

These tasks are submitted for processing.

### 4.2 Edge Servers

Edge servers are located closer to the IoT devices and process tasks locally whenever sufficient resources are available.

Their purpose is to reduce communication delays and avoid unnecessary cloud processing.

The paper describes hospital workstations (HWs) acting as edge servers.

### 4.3 Cloud Server

The cloud provides additional computational resources when edge resources are insufficient.

Tasks that cannot be handled locally can be shifted to the cloud.

Cloud processing offers additional capacity but introduces higher network latency.

### 4.4 Overall Workflow

The conceptual workflow is:

1. IoT devices generate healthcare tasks.
2. Tasks are submitted to the computing infrastructure.
3. The system evaluates task priorities.
4. Dynamic priority adjustment determines the urgency of tasks.
5. The resource allocation mechanism identifies suitable computing resources.
6. Tasks are processed at edge servers when possible.
7. Cloud resources are used when edge resources are insufficient.
8. The system monitors resource conditions and performance.
9. Energy consumption, latency, execution time, and resource utilization are evaluated.

The architecture combines task scheduling, resource allocation, load balancing, and energy management.

---

## 5. Proposed DPTARA Methodology

The proposed approach combines multiple mechanisms.

### 5.1 Dynamic Priority-Based Task Scheduling

Healthcare tasks do not all have the same urgency.

For example, an emergency alert should receive higher priority than a routine monitoring request.

The paper uses a dynamic priority mechanism to adjust task priorities according to:

- Original task priority
- Time elapsed since task arrival
- Task deadline
- Current system load

The priority calculation is described by:

P_i = α P_orig,i + β ((T_current - T_arrival,i) / D_i) - γ L_current,i

Where:

- P_i = dynamically calculated priority of task i
- P_orig,i = original priority of task i
- T_current = current simulation time
- T_arrival,i = task arrival time
- D_i = task deadline
- L_current,i = current system load
- α, β, γ = weighting coefficients

The equation combines the original task priority, elapsed time relative to the deadline, and current system load.

The paper does not provide exact numerical values for all three weighting coefficients. Therefore, numerical values used in an implementation must be documented as implementation settings rather than paper-specified constants.

### 5.2 Adaptive Resource Allocation

The resource allocation mechanism attempts to assign tasks to suitable computing resources.

The paper describes an edge-first approach:

1. Check available edge resources.
2. Identify an eligible resource.
3. Allocate resources according to task requirements and resource availability.
4. Use cloud resources when edge resources cannot accommodate the task.
5. Manage resource allocation according to task priorities.

The paper also discusses priority-aware resource management, including handling situations where high-priority tasks need resources that are currently occupied by lower-priority tasks.

The complete algorithm must be interpreted together with the paper's resource-capacity conditions and task allocation descriptions.

**Important modelling observation:** The paper's resource-capacity condition combines task size expressed in MB with resource capacity described using CPU-related units. These quantities are dimensionally different. This needs to be acknowledged rather than silently converted using an invented formula.

### 5.3 Predictive Load Balancing

The proposed system considers current and predicted resource loads when distributing tasks.

The load prediction equation presented in the paper is:

L_pred,t = L_current,t + Σ λ_i S_i (1 - p_i)

Where:

- L_pred,t = predicted load at time t
- L_current,t = current system load
- λ_i = task arrival rate
- S_i = task size
- p_i = probability or fraction associated with the task-processing condition, as defined in the paper's model

The predicted load is intended to help the system anticipate future demand and avoid overloading individual resources.

Load balancing distributes workload across available computing resources to improve overall resource utilization.

### 5.4 Energy-Aware Resource Management

Energy efficiency is another important objective of DPTARA.

The paper considers energy consumption while allocating and managing edge and cloud resources.

Its approach discusses:

- Adapting resource usage according to system load.
- Reducing unnecessary dependence on cloud resources.
- Managing energy consumption during task execution.
- Moving idle resources into low-power states.

The effectiveness of energy management is evaluated using the energy consumption metric.

The actual implementation of each energy-saving strategy must be distinguished from the paper's conceptual description.

---

## 6. Mathematical Models and Performance Metrics

### 6.1 Task Computing Time

The paper describes computing time using:

T_computing = δ / ψ_resource

Where:

- δ = task input data size
- ψ_resource = processing capability of the selected resource

The paper's task representation also describes task input size and required processing cycles.

**Unit limitation:** The paper's description uses MB for task size and MIPS for processing speed. Directly dividing MB by MIPS does not produce a physically consistent execution time without an additional conversion or workload model. The paper does not provide a complete numerical conversion rule.

This ambiguity must be considered when reproducing the execution-time model.

### 6.2 Resource Utilization Efficiency

The paper gives the efficiency model:

η_i = (U_effective / C_total) (1 - R_downtime)

Where:

- η_i = resource efficiency
- U_effective = effective resource utilization
- C_total = total resource capacity
- R_downtime = downtime ratio

This model relates effective utilization and resource downtime to overall resource efficiency.

### 6.3 Energy Consumption

The paper describes energy consumption as:

E = Σ (P_i / η_i) (T_end,i - T_start,i)

Where:

- E = total energy consumption
- P_i = power associated with resource i
- η_i = resource efficiency
- T_end,i = task completion time
- T_start,i = task start time

The model incorporates resource power, efficiency, and task execution duration.

### 6.4 Latency

Latency represents the delay experienced during task processing and communication.

The paper evaluates latency for different task categories and compares it with the configured latency tolerance thresholds.

The paper discusses:

- 250 ms maximum latency tolerance for latency-constrained requests.
- 400 ms maximum latency tolerance for delay-tolerant requests.

These are latency thresholds, not the same as the task deadlines used in the simulation.

### 6.5 Task Execution Time

Task execution time measures the time required to execute a task on the selected resource.

It is evaluated separately from communication latency.

### 6.6 Resource Utilization

Resource utilization measures how effectively available computational resources are used.

The paper uses this metric to evaluate whether the proposed allocation mechanism distributes workloads efficiently and avoids unnecessary underutilization.

---

## 7. Simulation Environment and Parameters

The paper describes a healthcare edge-computing simulation environment with the following configuration.

| Parameter | Paper-specified value |
|---|---:|
| IoT devices | 50 |
| Edge servers / HWs | 10 |
| Cloud servers | 1 |
| Task arrival rate | 5 tasks/second |
| Task size | Uniform distribution: 5–50 MB |
| Task deadline | Uniform distribution: 10–100 seconds |
| Edge CPU capacity | 500–3000 MIPS |
| Cloud CPU capacity | 2000–10000 MIPS |
| Edge RAM | 32 GB |
| Cloud RAM | 64 GB |
| Edge power | 50 W |
| Cloud power | 200 W |
| Edge network latency | 5–10 ms |
| Cloud network latency | 50–100 ms |
| Edge CPU utilization parameter | 0.5 |
| Cloud CPU utilization parameter | 2.0 |

The meaning and operational interpretation of some configuration values, particularly the CPU utilization parameters, require careful examination.

The paper's simulation setup should not be confused with the exact configuration or execution results of the Python implementation.

---

## 8. Experimental Evaluation and Results

The paper evaluates DPTARA against three existing approaches:

1. Adaptive and Priority-Based Resource Allocation (A-PBRA)
2. Novel Bio-Inspired Hybrid Algorithm (NBIHA)
3. CORA-GT

The evaluation considers latency, task execution time, energy consumption, and resource utilization.

### 8.1 Table 5: Reported Performance Comparison

The paper reports the following values:

| Metric | DPTARA | A-PBRA | NBIHA | CORA-GT |
|---|---:|---:|---:|---:|
| Latency (ms) | 320 | 350 | 480 | 560 |
| Resource utilization (%) | 88 | 57 | 48 | 35 |
| Task execution time (ms) | 335 | 540 | 570 | 1100 |
| Energy consumption (J) | 321 | 600 | 700 | 802 |

These are values reported by the research paper. They are not results generated by this repository.

### 8.2 Latency Evaluation

The paper reports that DPTARA reduces latency by dynamically prioritizing urgent tasks and distributing workloads across edge and cloud resources.

It discusses latency performance under varying numbers of resource requests.

The paper states that high-priority requests remain below the 250 ms tolerance threshold and normal requests remain below the 400 ms tolerance threshold in the described experiments.

### 8.3 Task Execution Time Evaluation

The paper reports that DPTARA achieves lower execution times than the three benchmark algorithms.

At 100 resource requests, it reports:

- DPTARA: approximately 335 ms
- A-PBRA: approximately 540 ms
- NBIHA: approximately 570 ms
- CORA-GT: more than 1000 ms

The paper attributes the improvement to dynamic priority adjustment, adaptive allocation, and predictive load balancing.

### 8.4 Energy Consumption Evaluation

The paper reports lower energy consumption for DPTARA compared with the benchmark algorithms.

For example, at 200 incoming requests, the paper reports approximately:

- DPTARA: 410 J
- A-PBRA: 1100 J
- NBIHA: 1400 J
- CORA-GT: 1500 J

The paper attributes these improvements to adaptive energy management and more efficient resource allocation.

### 8.5 Resource Utilization Evaluation

The paper reports that DPTARA achieves approximately 94% resource utilization at 200 tasks.

The reported values for the other algorithms are:

- A-PBRA: approximately 77%
- NBIHA: approximately 62%
- CORA-GT: no more than approximately 54%

The authors attribute the improvement to predictive load balancing and adaptive resource allocation.

---

## 9. Main Contributions and Findings

The main contributions claimed by the paper are:

1. A dynamic priority mechanism for healthcare task scheduling.
2. An adaptive resource allocation approach for edge and cloud resources.
3. Predictive load balancing to manage changing workloads.
4. Energy-aware resource management.
5. Evaluation across multiple performance metrics.
6. Comparison against A-PBRA, NBIHA, and CORA-GT.

The paper concludes that combining task priority, resource allocation, load balancing, and energy management can improve the performance of healthcare-oriented edge computing systems.

---

## 10. Limitations and Points Requiring Careful Interpretation

The following points are important when attempting to reproduce the paper.

### 10.1 Incomplete Parameter Specification

The paper does not clearly specify every numerical parameter required for a complete independent implementation.

For example, the exact values of the priority weighting coefficients are not fully specified.

### 10.2 Task Size and CPU Demand

The paper describes task size and required processing cycles, but does not provide a complete numerical distribution or conversion rule for per-task CPU demand.

An implementation should not invent such values and then claim that they were directly specified by the paper.

### 10.3 Unit Consistency

The computing-time expression divides task size by resource processing speed.

The units MB and MIPS require an additional conversion or workload interpretation to produce physically meaningful execution times.

Similarly, the resource-capacity condition needs careful dimensional interpretation.

### 10.4 Baseline Reproduction

The paper reports comparisons against A-PBRA, NBIHA, and CORA-GT.

A fair independent comparison requires implementing and validating these algorithms under consistent workloads, resource configurations, and evaluation conditions.

### 10.5 Simulation Reproducibility

The reported results depend on the simulation configuration, task workloads, resource allocation decisions, and experimental conditions.

Not every implementation detail is sufficiently specified to guarantee exact reproduction of the published results.

### 10.6 Implementation Versus Paper Claims

The paper describes a comprehensive framework. An implementation may initially reproduce only selected mechanisms.

Therefore, every implemented feature must be evaluated separately before claiming complete reproduction.

---

## 11. Mapping the Paper to the Python Implementation

The following table distinguishes the paper's concepts from the current implementation.

| Paper component | Python implementation | Current status |
|---|---|---|
| Task and resource representation | `src/models/entities.py` | Implemented |
| Task generation | `src/task_generator.py` | Implemented |
| Resource management | `src/resource_manager.py` | Implemented |
| Adaptive resource allocation | `src/resource_allocator.py` | Implemented, partial reproduction |
| Task execution | `src/task_executor.py` | Implemented with unit limitation |
| Dynamic priority calculation | `src/models/priority_model.py` | Implemented and tested |
| Priority-based scheduling | Simulator scheduling integration | Partially integrated |
| Load prediction | `src/models/load_predictor.py` | Implemented; method differs from paper equation |
| Load balancing | `src/load_balancer.py` | Implemented metric calculation |
| Energy management | `src/energy_manager.py` | Implemented |
| Performance metrics | `src/metrics.py` | Implemented |
| Event-driven simulation | `src/simulator.py` | Implemented; event edge cases require validation |
| Baseline algorithms | `baselines/` | Not implemented |

This mapping describes the current repository status and should be updated as development progresses.

---

## 12. Current Reproduction Results

The following results belong to the current Python implementation, not the original paper.

In one validated 10-second simulation run with seed 42:

| Metric | Implementation result |
|---|---:|
| Generated tasks | 41 |
| Completed tasks | 41 |
| Completion rate | 100% |
| Unallocated tasks | 0 |
| Deadline miss rate | 0% |
| Average latency | 0.0147 seconds |
| Average execution time | 0.0085 seconds |
| Total energy consumption | 2050 J |
| Average normalized resource-load ratio | 0.01% |
| Average load balancing rate | -81.50% |

The normalized resource-load ratio should not be interpreted as physical CPU utilization because the current implementation reserves task size in MB against resource capacity represented in MIPS.

The load balancing score follows the implemented raw formula and can produce negative values. It should not be interpreted as a conventional bounded percentage.

The results demonstrate that the current simulation executes successfully under the tested configuration. They do not establish that the paper's complete DPTARA methodology has been reproduced.

---

## 13. Future Work

The following work is needed to move toward a more complete and defensible reproduction:

1. Validate simultaneous task arrivals and task completions in the event-driven simulator.
2. Review the deadline and CPU allocation model against the paper.
3. Complete integration of dynamic priority into resource scheduling.
4. Integrate load prediction and load balancing into allocation decisions.
5. Examine the paper's resource preemption and priority-aware allocation behaviour.
6. Investigate the energy-management strategies described in the paper.
7. Validate all experimental scenarios and parameter settings.
8. Implement and validate A-PBRA, NBIHA, and CORA-GT baselines.
9. Compare results using consistent workloads and resource configurations.
10. Document deviations between the paper and the implementation.

---

## 14. Overall Understanding

The central idea of DPTARA is to combine dynamic task prioritization with adaptive resource allocation in a healthcare edge-computing environment.

Instead of treating all tasks equally, the system considers task urgency and changing system conditions. It attempts to process tasks closer to their source, use cloud resources when necessary, balance workloads, and manage energy consumption.

The research problem is therefore not simply task scheduling. It is a combined resource-management problem involving:

- Task urgency
- Resource availability
- Processing delays
- Network latency
- Workload distribution
- Energy consumption

A successful reproduction must demonstrate how these mechanisms interact and how their combined behaviour affects the performance metrics.

**Reference**

Anand, J., and Karthikeyan, B. (2025). Dynamic priority-based task scheduling and adaptive resource allocation algorithms for efficient edge computing in healthcare systems. *Results in Engineering*, 25, 104342. https://doi.org/10.1016/j.rineng.2025.104342
