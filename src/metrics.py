
class Metrics:
    """
    Collects and calculates performance metrics
    for the DPTARA simulation.

    Resource utilization calculated here represents
    the instantaneous utilization at measurement time.
    """

    def calculate_metrics(self, tasks, resources):

        # -----------------------------------------
        # 1. Task completion statistics
        # -----------------------------------------

        total_tasks = len(tasks)

        completed_tasks = [
            task for task in tasks
            if task.status == "completed"
            and task.completion_time is not None
        ]

        completed_count = len(completed_tasks)

        completion_rate = (
            (completed_count / total_tasks) * 100
            if total_tasks > 0 else 0.0
        )

        # -----------------------------------------
        # 2. Average end-to-end latency
        # -----------------------------------------

        latencies = [
            task.completion_time - task.arrival_time
            for task in completed_tasks
        ]

        average_latency = (
            sum(latencies) / len(latencies)
            if latencies else 0.0
        )

        # -----------------------------------------
        # 3. Average execution time
        # -----------------------------------------

        execution_times = [
            task.execution_time
            for task in completed_tasks
        ]

        average_execution_time = (
            sum(execution_times) / len(execution_times)
            if execution_times else 0.0
        )

        # -----------------------------------------
        # 4. Total energy consumption
        # -----------------------------------------

        total_energy = sum(
            task.energy_consumption
            for task in completed_tasks
        )

        # -----------------------------------------
        # 5. Instantaneous system utilization
        # -----------------------------------------

        total_capacity = sum(
            resource.capacity for resource in resources
        )

        total_load = sum(
            resource.current_load for resource in resources
        )

        system_utilization = (
            (total_load / total_capacity) * 100
            if total_capacity > 0 else 0.0
        )

        # -----------------------------------------
        # 6. Return all metrics
        # -----------------------------------------

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_count,
            "completion_rate_percent": completion_rate,
            "average_latency": average_latency,
            "average_execution_time": average_execution_time,
            "total_energy_consumption": total_energy,
            "system_utilization_percent": system_utilization
        }
