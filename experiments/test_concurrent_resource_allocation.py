
from src.models.entities import Task, Resource
from src.resource_manager import ResourceManager
from src.resource_allocator import ResourceAllocator


def create_task(task_id, size_mb, deadline):
    return Task(
        task_id=task_id,
        size_mb=size_mb,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=deadline,
        task_type="normal",
        workload_mi=size_mb * 100.0,
        cpu_demand_mips=50.0
    )


def main():

    print("\nCONCURRENT RESOURCE ALLOCATION TEST")
    print("=" * 55)

    # 1. Initialize resources
    manager = ResourceManager()

    edge1 = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=1000,
        processing_speed_mips=1000,
        power_consumption_w=50
    )

    edge2 = Resource(
        resource_id="E2",
        resource_type="edge",
        capacity=1000,
        processing_speed_mips=1000,
        power_consumption_w=50
    )

    manager.register_resource(edge1)
    manager.register_resource(edge2)

    allocator = ResourceAllocator(manager)

    print("\n1. Resources initialized: PASSED")

    # 2. Allocate first task
    task1 = create_task(1, 2, 10)

    resource1 = allocator.allocate_task(task1)

    assert resource1 is not None
    assert task1.status == "allocated"

    print(f"2. Task 1 allocated to {resource1.resource_id}: PASSED")

    # 3. Allocate second task
    task2 = create_task(2, 2, 10)

    resource2 = allocator.allocate_task(task2)

    assert resource2 is not None
    assert task2.status == "allocated"

    assert resource1.resource_id != resource2.resource_id

    print(f"3. Task 2 allocated to {resource2.resource_id}: PASSED")

    # 4. Verify simultaneous allocation loads
    assert edge1.current_load == 50
    assert edge2.current_load == 50

    print("4. Simultaneous resource allocation loads: PASSED")

    # 5. Verify capacity limits
    for resource in manager.get_all_resources():
        assert resource.current_load <= resource.capacity

    print("5. Resource capacity validation: PASSED")

    # 6. Release both task allocations
    allocator.release_task(task1)
    allocator.release_task(task2)

    assert edge1.current_load == 0
    assert edge2.current_load == 0

    print("6. Resource load release: PASSED")

    # 7. Test allocation failure
    task3 = create_task(3, 1001, 10)

    resource3 = allocator.allocate_task(task3)

    assert resource3 is None
    assert task3.status == "unallocated"

    print("7. Insufficient capacity handling: PASSED")

    print("\n" + "=" * 55)
    print("ALL RESOURCE ALLOCATION TESTS PASSED")
    print("=" * 55)


if __name__ == "__main__":
    main()
