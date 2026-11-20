
class Metrics:
    """
    Collects and calculates performance metrics
    for the DPTARA simulation.
    """

    def calculate_metrics(self, tasks, resources):

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

        # 1. End-to-end latency
        latencies = [
            task.completion_time - task.arrival_time
            for task in completed_tasks
        ]

        average_latency = (
            sum(latencies) / len(latencies)
            if latencies else 0.0
        )

        # 2. Execution time
        execution_times = [
            task.execution_time
            for task in completed_tasks
        ]

        average_execution_time = (
            sum(execution_times) / len(execution_times)
            if execution_times else 0.0
        )

        # 3. Energy consumption
        total_energy = sum(
            task.energy_consumption
            for task in completed_tasks
        )

        # 4. Deadline performance
        on_time_tasks = []
        late_completed_tasks = []

        for task in completed_tasks:

            latency = task.completion_time - task.arrival_time

            if latency <= task.deadline:
                on_time_tasks.append(task)
            else:
                late_completed_tasks.append(task)

        on_time_count = len(on_time_tasks)
        late_completed_count = len(late_completed_tasks)

        # Include late and incomplete tasks in deadline misses.
        deadline_missed_count = total_tasks - on_time_count

        deadline_met_rate = (
            on_time_count / total_tasks * 100
            if total_tasks > 0 else 0.0
        )

        deadline_miss_rate = (
            deadline_missed_count / total_tasks * 100
            if total_tasks > 0 else 0.0
        )

        # Calculate actual deadline violations.
        deadline_violations = [
            (
                task.completion_time
                - task.arrival_time
                - task.deadline
            )
            for task in late_completed_tasks
        ]

        total_deadline_violation = sum(deadline_violations)

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

        # 5. Unallocated tasks
        unallocated_count = sum(
            1 for task in tasks
            if task.status == "unallocated"
        )

        # 6. Instantaneous resource utilization
        total_capacity = sum(
            resource.capacity for resource in resources
        )

        total_load = sum(
            resource.current_load for resource in resources
        )

        system_utilization = (
            total_load / total_capacity * 100
            if total_capacity > 0 else 0.0
        )

        # 7. Return metrics
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_count,
            "completion_rate_percent": completion_rate,

            "on_time_tasks": on_time_count,
            "late_completed_tasks": late_completed_count,
            "deadline_missed_tasks": deadline_missed_count,
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
