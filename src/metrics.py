
class Metrics:
    """
    Collects and calculates performance metrics
    for the DPTARA simulation.

    Deadline classification:
        - Completed before deadline: on-time.
        - Completed after deadline: deadline miss.
        - Incomplete after deadline: deadline miss.
        - Incomplete before deadline: unresolved.

    System utilization:
        Calculated as time-weighted CPU utilization using
        task allocation and execution intervals.
    """

    def calculate_metrics(self, tasks, resources, current_time=None):

        total_tasks = len(tasks)

        completed_tasks = [
            task for task in tasks
            if task.status == "completed"
            and task.completion_time is not None
        ]

        completed_count = len(completed_tasks)

        # --------------------------------------------------
        # 1. COMPLETION RATE
        # --------------------------------------------------

        completion_rate = (
            completed_count / total_tasks * 100
            if total_tasks > 0 else 0.0
        )

        incomplete_count = total_tasks - completed_count

        # --------------------------------------------------
        # 2. LATENCY AND EXECUTION TIME
        # --------------------------------------------------

        latencies = [
            task.completion_time - task.arrival_time
            for task in completed_tasks
        ]

        average_latency = (
            sum(latencies) / len(latencies)
            if latencies else 0.0
        )

        execution_times = [
            task.execution_time
            for task in completed_tasks
        ]

        average_execution_time = (
            sum(execution_times) / len(execution_times)
            if execution_times else 0.0
        )

        # --------------------------------------------------
        # 3. ENERGY CONSUMPTION
        # --------------------------------------------------

        total_energy = sum(
            task.energy_consumption
            for task in tasks
        )

        # --------------------------------------------------
        # 4. DEADLINE PERFORMANCE
        # --------------------------------------------------

        tolerance = 1e-9

        on_time_count = 0
        late_completed_count = 0
        expired_incomplete_count = 0
        unresolved_count = 0

        deadline_violations = []

        for task in tasks:

            deadline_time = (
                task.arrival_time + task.deadline
            )

            if (
                task.status == "completed"
                and task.completion_time is not None
            ):

                latency = (
                    task.completion_time - task.arrival_time
                )

                violation = latency - task.deadline

                if violation > tolerance:
                    late_completed_count += 1
                    deadline_violations.append(violation)
                else:
                    on_time_count += 1

            else:

                if current_time is not None:

                    if current_time >= deadline_time:
                        expired_incomplete_count += 1
                    else:
                        unresolved_count += 1

                else:
                    unresolved_count += 1

        deadline_missed_count = (
            late_completed_count + expired_incomplete_count
        )

        deadline_met_rate = (
            on_time_count / total_tasks * 100
            if total_tasks > 0 else 0.0
        )

        deadline_miss_rate = (
            deadline_missed_count / total_tasks * 100
            if total_tasks > 0 else 0.0
        )

        total_deadline_violation = sum(
            deadline_violations
        )

        average_deadline_violation = (
            total_deadline_violation / len(deadline_violations)
            if deadline_violations else 0.0
        )

        maximum_deadline_violation = (
            max(deadline_violations)
            if deadline_violations else 0.0
        )

        minimum_deadline_violation = (
            min(deadline_violations)
            if deadline_violations else 0.0
        )

        # --------------------------------------------------
        # 5. UNALLOCATED TASKS
        # --------------------------------------------------

        unallocated_count = sum(
            1 for task in tasks
            if task.status == "unallocated"
        )

        # --------------------------------------------------
        # 6. TIME-WEIGHTED SYSTEM UTILIZATION
        # --------------------------------------------------

        total_capacity = sum(
            resource.capacity
            for resource in resources
        )

        system_utilization = 0.0

        if (
            total_capacity > 0
            and current_time is not None
            and current_time > 0
        ):

            total_cpu_time = 0.0

            for task in tasks:

                resource_id = task.assigned_resource

                if resource_id is None:
                    continue

                allocated_load = task.allocated_load

                if allocated_load is None:
                    allocated_load = task.cpu_demand_mips

                if allocated_load is None or allocated_load <= 0:
                    continue

                if task.start_time is None:
                    continue

                start_time = max(0.0, task.start_time)

                # Completed tasks use their actual completion time.
                # Running tasks are measured up to current_time.
                if (
                    task.status == "completed"
                    and task.completion_time is not None
                ):
                    end_time = task.completion_time
                else:
                    end_time = current_time

                end_time = min(end_time, current_time)

                duration = max(0.0, end_time - start_time)

                total_cpu_time += allocated_load * duration

            total_available_cpu_time = (
                total_capacity * current_time
            )

            system_utilization = (
                total_cpu_time / total_available_cpu_time * 100
            )

        # --------------------------------------------------
        # 7. RETURN RESULTS
        # --------------------------------------------------

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_count,
            "incomplete_tasks": incomplete_count,
            "completion_rate_percent": completion_rate,

            "on_time_tasks": on_time_count,
            "late_completed_tasks": late_completed_count,
            "expired_incomplete_tasks": expired_incomplete_count,
            "deadline_missed_tasks": deadline_missed_count,
            "unresolved_tasks": unresolved_count,

            "deadline_met_rate_percent": deadline_met_rate,
            "deadline_miss_rate_percent": deadline_miss_rate,

            "total_deadline_violation": total_deadline_violation,
            "average_deadline_violation": average_deadline_violation,
            "maximum_deadline_violation": maximum_deadline_violation,
            "minimum_deadline_violation": minimum_deadline_violation,

            "unallocated_tasks": unallocated_count,

            "average_latency": average_latency,
            "average_execution_time": average_execution_time,

            "total_energy_consumption": total_energy,
            "system_utilization_percent": system_utilization
        }
