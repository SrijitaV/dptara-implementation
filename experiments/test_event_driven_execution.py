
import heapq

from src.models.entities import Task, Resource
from src.simulator import DPTARASimulator


def main():

    print("\nEVENT-DRIVEN EXECUTION TEST")
    print("=" * 58)

    # 1. Initialize simulator
    simulator = DPTARASimulator(
        simulation_duration=10,
        arrival_rate=5.0,
        seed=42
    )

    print("\n1. Simulator initialization: PASSED")

    # 2. Register a controlled edge resource
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

    print("2. Edge resource registration: PASSED")

    # 3. Create a task
    task = Task(
        task_id=1,
        size_mb=2.0,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=10.0,
        task_type="normal"
    )

    # 4. Submit task through the current arrival handler
    simulator._handle_arrival(task)

    assert task.status == "running"
    assert task.assigned_resource == "E1"
    assert task.completion_time is not None
    assert len(simulator.event_queue) == 1

    print("3. Task allocation and execution start: PASSED")

    # 5. Verify CPU reservation
    assert resource.current_load > 0
    assert resource.current_load <= resource.capacity

    reserved_load = resource.current_load

    print(
        f"4. CPU reservation during execution: PASSED "
        f"({reserved_load:.2f} MIPS)"
    )

    # 6. Retrieve and process the completion event
    event = heapq.heappop(simulator.event_queue)

    (
        event_time,
        _,
        _,
        event_type,
        event_task,
        event_resource
    ) = event

    assert event_type == "completion"
    assert event_task is task

    simulator._record_utilization_interval(event_time)
    simulator._handle_completion(event_task, event_resource)

    assert task.status == "completed"
    assert len(simulator.event_queue) == 0

    print("5. Task completion event: PASSED")

    # 7. Verify CPU capacity is released
    assert abs(resource.current_load) < 1e-9

    print("6. CPU capacity release: PASSED")

    # 8. Verify execution information is preserved
    assert task.assigned_resource == "E1"
    assert task.start_time is not None
    assert task.completion_time is not None
    assert task.execution_time > 0
    assert task.energy_consumption > 0

    print("7. Task execution information: PASSED")

    # 9. Display final task details
    print("\nTASK EXECUTION DETAILS")
    print("-" * 58)
    print(f"Task ID: {task.task_id}")
    print(f"Assigned resource: {task.assigned_resource}")
    print(f"Start time: {task.start_time:.4f} seconds")
    print(f"Completion time: {task.completion_time:.4f} seconds")
    print(f"Execution time: {task.execution_time:.4f} seconds")
    print(f"Energy consumption: {task.energy_consumption:.4f} joules")
    print(f"Final resource load: {resource.current_load:.2f} MIPS")

    print("\n" + "=" * 58)
    print("ALL EVENT-DRIVEN EXECUTION TESTS PASSED")
    print("=" * 58)


if __name__ == "__main__":
    main()
