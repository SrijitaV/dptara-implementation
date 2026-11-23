
from src.models.entities import Task, Resource
from src.simulator import DPTARASimulator


def create_task(task_id, arrival_time, size=2.0):
    return Task(
        task_id=task_id,
        size_mb=size,
        original_priority=1.0,
        arrival_time=arrival_time,
        deadline=20.0,
        task_type="normal"
    )


def create_simulator():
    simulator = DPTARASimulator(
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42
    )

    resource = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=1000,
        current_load=0.0,
        processing_speed_mips=1000,
        power_consumption_w=50,
        network_latency_ms=10
    )

    simulator.resource_manager.register_resource(resource)
    simulator.resources = simulator.resource_manager.get_all_resources()

    return simulator, resource


def test_simultaneous_arrivals():
    simulator, resource = create_simulator()

    tasks = [
        create_task(1, 0.0),
        create_task(2, 0.0),
        create_task(3, 0.0)
    ]

    for task in tasks:
        simulator._handle_arrival(task)

    assert len(simulator.waiting_tasks) == 0
    assert sum(task.status == "running" for task in tasks) >= 1

    print("Simultaneous arrivals: PASSED")


def test_simultaneous_completions():
    simulator, resource = create_simulator()

    tasks = [
        create_task(1, 0.0),
        create_task(2, 0.0)
    ]

    for task in tasks:
        simulator._handle_arrival(task)

    running_tasks = [task for task in tasks if task.status == "running"]

    assert len(running_tasks) == 2

    completion_times = [task.completion_time for task in running_tasks]
    assert completion_times[0] == completion_times[1]

    for task in running_tasks:
        simulator._handle_completion(task, resource)

    assert all(task.status == "completed" for task in running_tasks)
    assert resource.current_load == 0

    print("Simultaneous completions: PASSED")


def test_completion_and_arrival_at_same_time():
    simulator, resource = create_simulator()

    first_task = create_task(1, 0.0)
    simulator._handle_arrival(first_task)

    second_task = create_task(
        2,
        first_task.completion_time
    )

    simulator._record_utilization_interval(
        first_task.completion_time
    )

    simulator._handle_completion(first_task, resource)
    simulator._handle_arrival(second_task)

    assert first_task.status == "completed"
    assert second_task.status == "running"

    print("Completion and arrival at same time: PASSED")


def main():
    print("\nSIMULTANEOUS EVENT VALIDATION")
    print("=" * 55)

    test_simultaneous_arrivals()
    test_simultaneous_completions()
    test_completion_and_arrival_at_same_time()

    print("\nALL SIMULTANEOUS EVENT TESTS PASSED")
    print("=" * 55)


if __name__ == "__main__":
    main()
