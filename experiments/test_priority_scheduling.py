
from src.simulator import DPTARASimulator
from src.models.entities import Task


def test_priority_scheduling():

    print("\nTEST: DYNAMIC PRIORITY SCHEDULING")
    print("-" * 50)

    simulator = DPTARASimulator(
        simulation_duration=1,
        arrival_rate=1,
        seed=42
    )

    simulator.initialize_resources()

    # All tasks arrive together with identical sizes
    # and deadlines, but different original priorities.
    tasks = [
        Task(
            task_id=1,
            size_mb=5,
            original_priority=1.0,
            arrival_time=0.0,
            deadline=100.0,
            task_type="normal"
        ),
        Task(
            task_id=2,
            size_mb=5,
            original_priority=5.0,
            arrival_time=0.0,
            deadline=100.0,
            task_type="normal"
        ),
        Task(
            task_id=3,
            size_mb=5,
            original_priority=3.0,
            arrival_time=0.0,
            deadline=100.0,
            task_type="normal"
        )
    ]

    simulator.waiting_tasks = tasks.copy()

    simulator._dispatch_waiting_tasks()

    # Recover dispatch order using the event sequence number.
    dispatch_events = sorted(
        simulator.event_queue,
        key=lambda event: event[2]
    )

    dispatch_order = [
        event[4].task_id
        for event in dispatch_events
    ]

    print("\nExpected dispatch order: [2, 3, 1]")
    print("Actual dispatch order:  ", dispatch_order)

    assert dispatch_order == [2, 3, 1], (
        "Priority scheduling order is incorrect."
    )

    print("\nPriority scheduling: PASSED")


if __name__ == "__main__":
    test_priority_scheduling()
