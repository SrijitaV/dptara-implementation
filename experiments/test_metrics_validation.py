
from src.metrics import Metrics
from src.models.entities import Task, Resource


def main():

    print("\nDPTARA - METRICS VALIDATION")
    print("-" * 55)

    tasks = [
        Task(
            task_id=1,
            size_mb=10,
            original_priority=1,
            arrival_time=0,
            deadline=5,
            task_type="normal",
            status="completed",
            completion_time=4,
            execution_time=3,
            energy_consumption=10
        ),
        Task(
            task_id=2,
            size_mb=20,
            original_priority=2,
            arrival_time=1,
            deadline=2,
            task_type="priority",
            status="completed",
            completion_time=4,
            execution_time=2,
            energy_consumption=20
        ),
        Task(
            task_id=3,
            size_mb=15,
            original_priority=1,
            arrival_time=2,
            deadline=5,
            task_type="normal",
            status="pending"
        )
    ]

    resources = [
        Resource(
            resource_id="E1",
            resource_type="edge",
            capacity=1000,
            current_load=100
        ),
        Resource(
            resource_id="C1",
            resource_type="cloud",
            capacity=3000,
            current_load=300
        )
    ]

    metrics = Metrics()
    results = metrics.calculate_metrics(tasks, resources)

    expected = {
        "completion_rate_percent": 200 / 3,
        "average_latency": 3.5,
        "average_execution_time": 2.5,
        "total_energy_consumption": 30,
        "on_time_tasks": 1,
        "late_completed_tasks": 1,
        "deadline_missed_tasks": 2,
        "total_deadline_violation": 1,
        "system_utilization_percent": 10
    }

    print("\nCalculated Metrics:")
    for key, value in results.items():
        print(f"{key}: {value}")

    print("\nValidation:")
    for key, expected_value in expected.items():
        actual_value = results[key]

        assert abs(actual_value - expected_value) < 1e-6, (
            f"{key}: expected {expected_value}, got {actual_value}"
        )

        print(f"{key}: PASSED")

    print("\nALL METRICS TESTS PASSED")


if __name__ == "__main__":
    main()
