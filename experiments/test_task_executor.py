
from src.models.entities import Task, Resource
from src.task_executor import TaskExecutor


def main():

    print("\n========== DPTARA TASK EXECUTION TEST ==========")

    # 1. Initialize resource
    resource = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=1000,
        current_load=200,
        processing_speed_mips=2000,
        power_consumption_w=50,
        network_latency_ms=5,
        downtime_rate=0.0
    )

    # 2. Create an allocated task
    task = Task(
        task_id=1,
        size_mb=10,
        original_priority=5,
        arrival_time=0,
        deadline=50,
        task_type="emergency",
        assigned_resource="E1",
        status="allocated"
    )

    # Simulate the values normally populated by ResourceAllocator.
    task.workload_mi = 10000.0
    task.cpu_demand_mips = 200.0
    task.allocated_load = 200.0

    # 3. Initialize executor
    executor = TaskExecutor()

    current_time = 1.0

    # 4. Execute task
    result = executor.execute_task(
        task,
        resource,
        current_time
    )

    # 5. Display results
    print("\nResource Information")
    print("------------------------------")
    print(f"Resource ID: {resource.resource_id}")
    print(f"CPU Speed: {resource.processing_speed_mips} MIPS")
    print(f"Network Latency: {resource.network_latency_ms} ms")

    print("\nTask Execution Results")
    print("------------------------------")
    print(f"Task ID: {result.task_id}")
    print(f"Task Status: {result.status}")
    print(f"Assigned Resource: {result.assigned_resource}")
    print(f"Execution Time: {result.execution_time:.4f} seconds")
    print(f"Start Time: {result.start_time:.4f} seconds")
    print(f"Completion Time: {result.completion_time:.4f} seconds")
    print(f"Energy Consumption: {result.energy_consumption:.4f} Joules")

    # 6. Verify calculations
    assert result.status == "running"
    assert result.assigned_resource == "E1"
    assert abs(result.execution_time - 5.0) < 1e-6
    assert abs(result.start_time - 1.005) < 1e-6
    assert abs(result.completion_time - 6.005) < 1e-6
    assert result.energy_consumption > 0

    print("\nExecution calculations verified successfully!")

    print("\n========== TASK EXECUTION TEST PASSED ==========")


if __name__ == "__main__":
    main()
