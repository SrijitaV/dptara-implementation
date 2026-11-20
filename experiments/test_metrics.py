
from src.models.entities import Task, Resource
from src.metrics import Metrics


def main():

    metrics = Metrics()

    # Create sample tasks
    task1 = Task(
        task_id=1,
        size_mb=10,
        original_priority=5,
        arrival_time=0,
        deadline=20,
        task_type="emergency",
        completion_time=5,
        execution_time=4,
        energy_consumption=10,
        status="completed"
    )

    task2 = Task(
        task_id=2,
        size_mb=20,
        original_priority=3,
        arrival_time=2,
        deadline=30,
        task_type="routine",
        completion_time=10,
        execution_time=6,
        energy_consumption=20,
        status="completed"
    )

    task3 = Task(
        task_id=3,
        size_mb=15,
        original_priority=4,
        arrival_time=4,
        deadline=25,
        task_type="routine"
    )

    tasks = [task1, task2, task3]

    # Create sample resources
    edge = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=100,
        current_load=40
    )

    cloud = Resource(
        resource_id="C1",
        resource_type="cloud",
        capacity=500,
        current_load=100
    )

    resources = [edge, cloud]

    # Calculate metrics
    results = metrics.calculate_metrics(tasks, resources)

    # Display results
    print("\n========== DPTARA METRICS TEST ==========")

    print(f"Total Tasks: {results['total_tasks']}")
    print(f"Completed Tasks: {results['completed_tasks']}")

    print(
        f"Completion Rate: "
        f"{results['completion_rate_percent']:.2f}%"
    )

    print(
        f"Average Latency: "
        f"{results['average_latency']:.2f} seconds"
    )

    print(
        f"Average Execution Time: "
        f"{results['average_execution_time']:.2f} seconds"
    )

    print(
        f"Total Energy Consumption: "
        f"{results['total_energy_consumption']:.2f} Joules"
    )

    print(
        f"System Utilization: "
        f"{results['system_utilization_percent']:.2f}%"
    )

    # Verify expected results
    assert results["total_tasks"] == 3
    assert results["completed_tasks"] == 2
    assert abs(results["completion_rate_percent"] - 66.6667) < 0.01
    assert abs(results["average_latency"] - 6.5) < 0.001
    assert abs(results["average_execution_time"] - 5.0) < 0.001
    assert results["total_energy_consumption"] == 30
    assert abs(results["system_utilization_percent"] - 23.3333) < 0.01

    print("\nAll metric calculations verified successfully!")


if __name__ == "__main__":
    main()
