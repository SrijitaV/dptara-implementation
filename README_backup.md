# DPTARA Implementation

### Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation in Healthcare Edge Computing

An implementation and experimental study of the **DPTARA (Dynamic Priority-Based Task Scheduling and Adaptive Resource Allocation)** framework proposed for healthcare-oriented edge computing environments.

This repository aims to reproduce the methodology presented in the original research paper, evaluate its performance, and provide a foundation for exploring improved task scheduling and resource allocation techniques.

---

## 1. Research Paper

**Original Paper:** Dynamic priority-based task scheduling and adaptive resource allocation algorithms for efficient edge computing in healthcare systems

**Authors:** J. Anand and B. Karthikeyan

**Journal:** Results in Engineering, Volume 25 (2025), Article 104342

**DOI:** https://doi.org/10.1016/j.rineng.2025.104342

---

## 2. Project Overview

Healthcare applications increasingly rely on IoT devices to collect and process real-time patient information. Traditional cloud computing can introduce significant communication latency, making it challenging to handle time-sensitive healthcare tasks.

Mobile Edge Computing (MEC) addresses this problem by bringing computational resources closer to end devices.

However, edge computing environments face several challenges:

- Limited computational resources at edge nodes.
- Dynamic task arrival rates and varying workloads.
- Different urgency and priority levels among tasks.
- Resource allocation and load balancing.
- Energy consumption and processing delays.
- Deciding whether tasks should execute locally, at edge servers, or in the cloud.

The DPTARA framework addresses these challenges through dynamic task prioritization, adaptive resource allocation, predictive load balancing, and energy-aware scheduling.

---

## 3. Research Objectives

The primary objectives of this implementation are:

1. Understand and implement the DPTARA scheduling framework.
2. Implement dynamic priority adjustment for incoming tasks.
3. Develop adaptive resource allocation across local, edge, and cloud resources.
4. Simulate task scheduling under varying workloads.
5. Evaluate system performance using multiple performance metrics.
6. Compare DPTARA against existing scheduling and resource allocation approaches.
7. Identify potential limitations and opportunities for future improvements.

---

## 4. Proposed System Architecture

The framework follows a hierarchical computing architecture consisting of three major components:

### 4.1 IoT Devices

IoT devices generate healthcare-related computational tasks, such as:

- Patient monitoring data.
- Emergency alerts.
- Routine monitoring requests.
- Healthcare data processing tasks.

### 4.2 Edge Servers

Hospital Workstations (HWs) act as edge servers and provide computational resources closer to IoT devices.

Their responsibilities include:

- Receiving incoming tasks.
- Determining task urgency and priority.
- Scheduling tasks.
- Allocating computational resources.
- Processing tasks locally or forwarding them when necessary.

### 4.3 Cloud Server

The cloud provides additional computational resources when local and edge resources are insufficient.

Tasks that cannot be handled by available edge resources may be offloaded to the cloud.

---

## 5. Core Algorithms and Methodology

The DPTARA framework incorporates the following major components.

### 5.1 Dynamic Task Prioritization

Task priorities are dynamically adjusted according to their original priority, waiting time, deadline, and current resource load.

The paper defines the priority function as:

\[
P_i = \alpha P_{orig,i}
+ \beta \left(\frac{T_{current}-T_{arrival,i}}{D_i}\right)
- \gamma L_{current,i}
\]

Where:

- \(P_i\): Dynamically calculated task priority.
- \(P_{orig,i}\): Original task priority.
- \(T_{current}\): Current system time.
- \(T_{arrival,i}\): Task arrival time.
- \(D_i\): Task deadline.
- \(L_{current,i}\): Current resource load.
- \(\alpha,\beta,\gamma\): Scaling coefficients.

### 5.2 Adaptive Resource Allocation

Resources are dynamically allocated according to:

- Task priority.
- Available computational capacity.
- Current resource utilization.
- Task resource requirements.

The framework considers local resources, edge resources, and cloud resources when deciding where to execute a task.

### 5.3 Load Balancing

The framework distributes incoming tasks across available edge nodes to avoid overloading individual servers.

The paper also incorporates Linear Regression for predicting future resource loads.

### 5.4 Task Offloading

Tasks are assigned to the appropriate processing layer depending on resource availability and estimated execution latency.

The framework considers local and cloud processing latency when making allocation decisions.

### 5.5 Energy-Aware Resource Management

The framework considers the energy requirements of edge and cloud resources and dynamically manages resource usage according to task demands and system conditions.

---

## 6. Simulation Environment

The following parameters are taken from the original research paper.

### 6.1 System Parameters

| Parameter | Value |
|---|---|
| Number of IoT devices | 50 |
| Number of edge servers (HWs) | 10 |
| Number of cloud servers | 1 |
| Task arrival distribution | Poisson |
| Arrival rate | 5 tasks/sec |
| Task size | 5–50 MB |
| Task deadline | 10–100 seconds |
| Edge power usage | 50 W |
| Cloud power usage | 200 W |
| Edge transmission latency | 5–10 ms |
| Cloud transmission latency | 50–100 ms |

### 6.2 Hardware Configuration

| Parameter | Edge Node | Cloud Node |
|---|---|---|
| CPU capacity | 500–3000 MIPS | 2000–10000 MIPS |
| CPU utilization factor | 0.5 | 2.0 (virtual machines) |
| RAM capacity | 32 GB | 64 GB |

---

## 7. Performance Evaluation

The implementation will evaluate the following performance metrics:

| Metric | Description |
|---|---|
| Average Latency | Average time taken for task processing and communication |
| Task Execution Time | Time required to execute incoming tasks |
| Energy Consumption | Energy consumed by computing resources |
| Resource Utilization | Percentage of available computational resources being utilized |
| Load Balancing | Distribution of workload across edge nodes |
| Response Time | Time taken to respond to incoming resource requests |

### Baseline Algorithms

The proposed DPTARA framework is compared against the following approaches:

1. **A-PBRA:** Adaptive and Priority-Based Resource Allocation.
2. **NBIHA:** Novel Bio-Inspired Hybrid Algorithm.
3. **CORA-GT:** Computation Offloading and Resource Allocation using Game Theory.

### Performance Results Reported in the Original Paper

The following values are reproduced from Table 5 of the paper. They are reference results, not results generated by this repository.

| Metric | DPTARA | A-PBRA | NBIHA | CORA-GT |
|---|---:|---:|---:|---:|
| Latency (ms) | 320 | 350 | 480 | 560 |
| Resource Utilization (%) | 88 | 57 | 48 | 35 |
| Execution Time (ms) | 335 | 540 | 570 | 1100 |
| Energy Consumption (J) | 321 | 600 | 700 | 802 |

---

## 8. Repository Structure

```text
dptara-implementation/
│
├── docs/
│   └── research_paper.pdf
│
├── src/
│   ├── task_generation/
│   ├── task_prioritization/
│   ├── resource_allocation/
│   ├── load_balancing/
│   ├── task_offloading/
│   └── energy_management/
│
├── algorithms/
│   ├── dptara/
│   └── baseline_algorithms/
│
├── experiments/
│   ├── configurations/
│   └── simulation/
│
├── results/
│   ├── metrics/
│   └── comparisons/
│
├── plots/
│
├── README.md
└── requirements.txt
