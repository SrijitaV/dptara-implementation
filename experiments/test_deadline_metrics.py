
import math

from src.models.entities import Task, Resource
from src.metrics import Metrics


def main():

    print("\nDEADLINE PERFORMANCE METRICS TEST")
    print("=" * 62)

    # Task 1: Completed within its deadline
    task1 = Task(
        task_id=1,
        size_mb=10,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=10.0,
        task_type="normal",
        completion_time=8.0,
        execution_time=7.0,
        energy_consumption=5.0,
        status="completed"
    )

    # Task 2: Completed after its deadline
    task2 = Task(
        task_id=2,
        size_mb=15,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=5.0,
        task_type="normal",
        completion_time=8.0,
        execution_time=7.0,
        energy_consumption=7.0,
        status="completed"
    )

    # Task 3: Could not be allocated
    task3 = Task(
        task_id=3,
        size_mb=20,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=4.0,
        task_type="normal",
        status="unallocated"
    )

    resource = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=1000.0,
        current_load=0.0,
        processing_speed_mips=1000.0,
        power_consumption_w=50.0
    )

    metrics = Metrics()

    results = metrics.calculate_metrics(
        [task1, task2, task3],
        [resource]
    )

    # Validate expected results
    checks = [
        (
            "Total task count",
            results["total_tasks"] == 3
        ),
        (
            "Completed task count",
            results["completed_tasks"] == 2
        ),
        (
            "On-time task count",
            results["on_time_tasks"] == 1
        ),
        (
            "Late completed task count",
            results["late_completed_tasks"] == 1
        ),
        (
            "Deadline missed task count",
            results["deadline_missed_tasks"] == 2
        ),
        (
            "Unallocated task count",
            results["unallocated_tasks"] == 1
        ),
        (
            "Deadline met rate",
            math.isclose(
                results["deadline_met_rate_percent"],
                100 / 3
            )
        ),
        (
            "Deadline miss rate",
            math.isclose(
                results["deadline_miss_rate_percent"],
                200 / 3
            )
        ),
        (
            "Average deadline violation",
            math.isclose(
                results["average_deadline_violation"],
                3.0
            )
        )
    ]

    for description, passed in checks:
        print(
            f"{description}: "
            f"{'PASSED' if passed else 'FAILED'}"
        )

    print("\nEXPECTED METRIC VALUES")
    print("-" * 62)

    print(f"Total tasks: {results['total_tasks']}")
    print(f"Completed tasks: {results['completed_tasks']}")
    print(f"On-time tasks: {results['on_time_tasks']}")
    print(f"Late completed tasks: {results['late_completed_tasks']}")
    print(f"Unallocated tasks: {results['unallocated_tasks']}")

    print(
        f"Deadline met rate: "
        f"{results['deadline_met_rate_percent']:.2f}%"
    )

    print(
        f"Deadline miss rate: "
        f"{results['deadline_miss_rate_percent']:.2f}%"
    )

    print(
        f"Average deadline violation: "
        f"{results['average_deadline_violation']:.2f} seconds"
    )

    print("=" * 62)

    if all(passed for _, passed in checks):
        print("ALL DEADLINE METRICS TESTS PASSED")
    else:
        raise AssertionError("One or more deadline metrics tests failed.")


if __name__ == "__main__":
    main()
