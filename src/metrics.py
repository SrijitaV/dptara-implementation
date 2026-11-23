
class Metrics:
    """
    Collects and calculates performance metrics
    for the DPTARA simulation.

    Deadline classification:
        - Completed before deadline: on-time.
        - Completed after deadline: deadline miss.
        - Incomplete after deadline: deadline miss.
        - Incomplete before deadline: unresolved.
    """

    def calculate_metrics(self, tasks, resources, current_time=None):

        total_tasks = len(tasks)

        completed_tasks = [
            task for task in tasks
            if task.status == "completed"
            and task.completion_time is not None
        ]

        completed_count = len(completed_tasks)

        completion_rate = (
            completed_count / total_tasks * 100
            if total_tasks > 0 else 0.0
        )

        # --------------------------------------------------
        # 1. LATENCY AND EXECUTION TIME
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
        # 2. ENERGY CONSUMPTION
        # --------------------------------------------------

        # Include energy consumed by all tasks, including
        # tasks that have started but not yet completed.
        total_energy = sum(
            task.energy_consumption
            for task in tasks
        )

        # --------------------------------------------------
        # 3. DEADLINE PERFORMANCE
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

            if task.status == "completed":

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

                # Classify incomplete tasks only when their
                # deadlines have actually expired.
                if current_time is not None:

                    if current_time >= deadline_time:
                        expired_incomplete_count += 1
                    else:
                        unresolved_count += 1

                else:
                    unresolved_count += 1

        deadline_missed_count = (
            late_completed_count
            + expired_incomplete_count
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
        # 4. UNALLOCATED AND INCOMPLETE TASKS
        # --------------------------------------------------

        unallocated_count = sum(
            1 for task in tasks
            if task.status == "unallocated"
        )

        incomplete_count = total_tasks - completed_count

        # --------------------------------------------------
        # 5. RESOURCE UTILIZATION
        # --------------------------------------------------

        total_capacity = sum(
            resource.capacity
            for resource in resources
        )

        total_load = sum(
            resource.current_load
            for resource in resources
        )

        system_utilization = (
            total_load / total_capacity * 100
            if total_capacity > 0 else 0.0
        )

        # This is the utilization snapshot at the time
        # metrics are calculated, not time-averaged utilization.

        # --------------------------------------------------
        # 6. RETURN RESULTS
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
