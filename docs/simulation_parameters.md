
# Simulation Parameters and Experimental Configuration

## 1. Introduction

This document records the simulation environment, system parameters, hardware configuration, workload characteristics, network properties, and evaluation metrics described in the DPTARA research paper.

It also documents the corresponding configuration used in the current Python implementation.

Three categories are distinguished throughout this document:

1. **Paper-specified parameters:** Values and configurations reported in the original research paper.
2. **Implementation configuration:** Values and settings used in the current Python simulator.
3. **Unspecified details:** Parameters or procedures that the paper does not define precisely and that require explicit implementation decisions.

The purpose is to maintain traceability between the original paper and the implementation.

---

## 2. Simulation Environment

The paper evaluates DPTARA in a healthcare-oriented edge computing environment.

The architecture described in the paper consists of:

1. Internet of Things (IoT) devices generating computational tasks.
2. Hospital Workstations (HWs) functioning as edge servers.
3. A centralized cloud server handling tasks that cannot be processed at the edge.

The paper reports using Python for simulation.

### 2.1 System Architecture Parameters

| Parameter | Paper Specification | Current Implementation |
|---|---:|---|
| Number of IoT devices | 50 | Individual IoT device behavior is not explicitly modeled |
| Number of HWs (edge servers) | 10 | 10 edge resources |
| Number of cloud servers | 1 | 1 cloud resource |
| Simulation environment | Healthcare-oriented edge computing | Python-based event-driven simulation |
| Simulation language | Python | Python |

**Implementation note:** The current simulator models the edge and cloud resources directly. It does not reproduce a separate 50-device IoT layer with individual device-level behavior.

---

## 3. Task Generation Parameters

Tasks are generated according to the workload characteristics reported in the paper.

### 3.1 Task Arrival Distribution

The paper specifies a Poisson task arrival process.

Arrival rate:

\[
\lambda = 5 \text{ tasks/second}
\]

The current task generator uses the specified arrival rate.

### 3.2 Task Size Distribution

The paper specifies a uniform task-size distribution:

\[
\delta_i \sim Uniform(5,50)\text{ MB}
\]

The current task generator uses the 5–50 MB range.

### 3.3 Task Deadline Distribution

The paper specifies:

\[
D_i \sim Uniform(10,100)\text{ seconds}
\]

The current task generator uses the 10–100 second deadline range.

### 3.4 Task Parameters Summary

| Parameter | Paper Specification | Current Implementation |
|---|---|---|
| Task arrival distribution | Poisson | Implemented |
| Arrival rate | 5 tasks/sec | 5 tasks/sec |
| Task size distribution | Uniform | Implemented |
| Task size range | 5–50 MB | 5–50 MB |
| Deadline distribution | Uniform | Implemented |
| Deadline range | 10–100 sec | 10–100 sec |

**Important modeling limitation:** The paper represents task requirements using task data size and required processing capability, but does not provide a precise numerical distribution for per-task CPU demand. The current implementation does not invent a separate CPU-demand distribution.

---

## 4. Hardware Configuration

The paper considers two types of computational resources:

- Edge nodes (Hospital Workstations).
- Cloud nodes.

### 4.1 Edge Node Configuration

| Parameter | Paper Specification |
|---|---:|
| CPU capacity | 500–3000 MIPS |
| CPU utilization | 0.5 |
| RAM capacity | 32 GB |
| Power consumption | 50 W |

### 4.2 Cloud Node Configuration

| Parameter | Paper Specification |
|---|---:|
| CPU capacity | 2000–10000 MIPS |
| CPU utilization | 2.0 (virtual machines) |
| RAM capacity | 64 GB |
| Power consumption | 200 W |

### 4.3 Hardware Comparison

| Parameter | Edge Node | Cloud Node |
|---|---:|---:|
| CPU MIPS | [500, 3000] | [2000, 10000] |
| CPU utilization | 0.5 | 2.0 |
| RAM | 32 GB | 64 GB |
| Power | 50 W | 200 W |

### 4.4 Current Implementation Configuration

The simulator initializes:

- 10 edge resources.
- 1 cloud resource.
- Edge processing capacities within the paper's 500–3000 MIPS range.
- Cloud processing capacity within the paper's 2000–10000 MIPS range.
- Edge power consumption of 50 W.
- Cloud power consumption of 200 W.

The resource initialization tests verify the resource counts, CPU capacity ranges, power configurations, and network latency ranges.

**Modeling limitation:** The CPU utilization values of 0.5 and 2.0 are reproduced as reported in the paper. Their exact interpretation is not sufficiently specified. They should not automatically be treated as measured utilization percentages.

The RAM values are paper specifications. Their use in actual resource allocation must be verified separately.

---

## 5. Network Configuration

The paper specifies different network transmission latency ranges for edge and cloud connections.

| Parameter | Edge Connection | Cloud Connection |
|---|---:|---:|
| Network latency | 5–10 ms | 50–100 ms |

The current resource initialization uses latency values within the corresponding edge and cloud ranges.

The lower edge latency represents the advantage of processing tasks closer to the data source, while cloud communication introduces additional network delay.

The task executor incorporates resource network latency into task start time.

---

## 6. Performance Evaluation Metrics

The paper evaluates DPTARA using several performance metrics.

### 6.1 Latency

Measures the delay experienced by tasks during processing and resource allocation.

The paper specifies:

- Priority-based requests: maximum latency tolerance of 250 ms.
- Normal requests: maximum latency tolerance of 400 ms.

These latency thresholds must be distinguished from the task deadlines generated using the 10–100 second distribution.

### 6.2 Average Response Time

Measures the average response time of incoming resource requests.

### 6.3 Resource Utilization

Measures the effectiveness of computational resource usage across the system.

### 6.4 Task Execution Time

Measures the time required to execute assigned tasks.

### 6.5 Energy Consumption

Measures the energy consumed by computational resources during task execution.

### 6.6 Metrics in the Current Implementation

The current implementation collects:

- Task completion rate.
- Deadline met rate.
- Deadline miss rate.
- Average latency.
- Average execution time.
- Total energy consumption.
- Average normalized resource-load ratio.
- Average load balancing rate.

**Important limitation:** The current normalized resource-load ratio is calculated using task-size load and resource capacity. Since task size is measured in MB and resource capacity is represented in MIPS, this ratio should not be interpreted as physically measured CPU utilization.

---

## 7. Workload and Experimental Configurations

The paper evaluates the proposed algorithm under varying workload conditions.

These paper-reported scenarios are separate from the experiments currently executed in the Python implementation.

### 7.1 Resource Request Variations

The paper reports comparisons at different resource request counts, including:

- 10 resource requests.
- 50 resource requests.
- 100 resource requests.

### 7.2 Task Configuration Variations

For robustness evaluation, the paper varies:

- Task size.
- Task priority.
- Network latency.
- Number of tasks.

The number of tasks is maintained between 100 and 200 in the configurations discussed.

### 7.3 Additional Reported Workload Conditions

The results section also discusses:

- Energy consumption at 60 and 200 incoming requests.
- Resource utilization at 200 tasks.
- Performance under best-case, average-case, and worst-case scenarios.

These conditions should not be assumed to use an identical workload or experimental configuration.

### 7.4 Experiments Executed in the Current Implementation

The current implementation has been validated using a 10-second task generation window and repeated simulation runs.

#### Full Simulation Validation

| Parameter | Value |
|---|---:|
| Task generation window | 10 seconds |
| Random seed | 42 |
| Generated tasks | 41 |
| Completed tasks | 41 |
| Completion rate | 100% |
| Deadline miss rate | 0% |
| Average latency | 0.0147 seconds |
| Average execution time | 0.0085 seconds |
| Total energy consumption | 2050 J |
| Average normalized resource-load ratio | 0.01% |
| Average load balancing rate | -81.50% |

These are results from the current implementation, not values reported by the research paper.

#### Repeated Simulation Experiments

Five simulation runs were conducted using seeds 42–46.

| Run | Seed | Generated Tasks | Completion Rate | Deadline Miss Rate |
|---|---:|---:|---:|---:|
| 1 | 42 | 41 | 100% | 0% |
| 2 | 43 | 49 | 100% | 0% |
| 3 | 44 | 52 | 100% | 0% |
| 4 | 45 | 54 | 100% | 0% |
| 5 | 46 | 60 | 100% | 0% |

These runs provide repeatability checks for the current simulator. They do not establish reproduction of all experimental scenarios in the paper.

---

## 8. Benchmark Algorithms

The paper compares DPTARA against three existing approaches:

1. Adaptive and Priority-Based Resource Allocation (A-PBRA).
2. NBIHA.
3. CORA-GT.

The comparative evaluation considers latency, resource utilization, task execution time, and energy consumption.

**Current implementation status:** The baseline algorithms have not yet been implemented and validated. Their descriptions and planned comparison methodology are documented separately in the `baselines` directory.

The paper's reported baseline and DPTARA results must not be presented as results generated by the current simulator.

---

## 9. Unspecified Simulation Details

Although the paper provides important simulation parameters, several implementation details remain unspecified or require further verification.

### 9.1 Simulation Execution

- Total simulation duration used for every paper experiment.
- Number of simulation repetitions.
- Random seed configuration.
- Warm-up period, if any.
- Exact event-driven or time-stepped simulation methodology.

### 9.2 Workload Generation

- Exact procedure for generating Poisson-distributed arrivals.
- Number of priority and normal tasks.
- Probability distribution of task priorities.
- Exact workload generation procedure for individual experiments.
- Numerical distribution of per-task CPU demand.

### 9.3 Hardware and Resource Modeling

- Exact interpretation of CPU utilization values.
- CPU scheduling and processing-time calculation.
- Resource allocation and memory management details.
- Number of virtual machines in the cloud.
- Exact relationship between task data size and required processing cycles.

### 9.4 Network Modeling

- Exact sampling method for network latency.
- Whether network latency is fixed or randomly generated for every task.
- Whether transmission time is calculated separately from network latency.

### 9.5 Performance Evaluation

- Exact measurement procedure for each metric.
- Whether reported metrics are averages across multiple runs.
- Exact procedure for generating best, average, and worst cases.
- Detailed experimental configurations corresponding to every figure.

These details must be investigated before claiming complete reproduction of the paper's experimental methodology.

---

## 10. Implementation Considerations

The following components are present in the current Python project:

| Component | Current Status |
|---|---|
| IoT task generation | Implemented as an aggregate task generator |
| Edge resource initialization | Implemented |
| Cloud resource initialization | Implemented |
| Task arrival and workload management | Implemented |
| Network latency modeling | Implemented |
| Task execution simulation | Implemented |
| Performance metric collection | Implemented |
| Event-driven simulation | Implemented |
| Repeated simulation experiments | Implemented and tested |
| Result visualization | Implemented |
| Baseline algorithm implementations | Pending |

The implementation must continue to distinguish between parameters directly specified by the paper and assumptions introduced to complete the simulation.

The execution-time equation also has a unit-consistency limitation: task size is expressed in MB, while processing speed is expressed in MIPS. The paper does not provide a precise conversion procedure, so the current implementation follows the stated equation without inventing an additional conversion factor.

---

## 11. Source and Parameter Traceability

The primary parameter sources are:

| Information | Source |
|---|---|
| System parameters | Table 3 |
| Hardware configuration | Table 4 |
| Performance metrics | Results and Discussions |
| Latency thresholds | Section 4.1 |
| Task configuration variations | Section 4.2 |
| Energy evaluation | Section 4.3 |
| Resource utilization evaluation | Section 4.4 |

Paper:

J. Anand and B. Karthikeyan, Results in Engineering 25 (2025), 104342.

---

## 12. Documentation Status

**Status:** Paper parameter extraction and current implementation configuration documented.

The principal system, workload, hardware, network, and performance evaluation parameters have been recorded.

The current implementation has been tested using its own simulation configurations, including a 10-second full simulation and five repeated runs.

However, the paper's complete experimental scenarios and baseline comparisons have not yet been reproduced.

Unspecified experimental details remain open for verification or must be clearly documented as implementation assumptions before final comparative experiments.
