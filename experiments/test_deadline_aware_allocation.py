
from src.models.entities import Task, Resource
from src.resource_manager import ResourceManager
from src.resource_allocator import ResourceAllocator


def create_allocator(capacity=1000, latency_ms=10):
    """Create an allocator with one controlled edge resource."""

    manager = ResourceManager()

    resource = Resource(
        resource_id="E1",
        resource_type="edge",
        capacity=capacity,
        current_load=0.0,
        processing_speed_mips=capacity,
        power_consumption_w=50.0,
        network_latency_ms=latency_ms
    )

    manager.register_resource(resource)

    allocator = ResourceAllocator(manager)

    return allocator, resource


def main():

    print("\nDEADLINE-AWARE RESOURCE ALLOCATION TEST")
    print("=" * 62)

    # --------------------------------------------------
    # TEST 1: Feasible task
    # --------------------------------------------------

    allocator, resource = create_allocator(
        capacity=1000,
        latency_ms=10
    )

    task = Task(
        task_id=1,
        size_mb=2.0,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=10.0,
        task_type="normal",
        workload_mi=200.0,
        cpu_demand_mips=250.0
    )

    selected = allocator.allocate_task(task)

    assert selected is not None
    assert task.status == "allocated"
    assert task.assigned_resource == "E1"
    assert task.cpu_demand_mips > 200
    assert resource.current_load == task.cpu_demand_mips

    print("1. Feasible task allocation: PASSED")
    print(f"   CPU demand: {task.cpu_demand_mips:.4f} MIPS")

    # Release the reservation
    allocator.release_task(task)
    task.status = "completed"

    assert resource.current_load == 0.0

    print("2. CPU reservation release: PASSED")

    # --------------------------------------------------
    # TEST 2: Deadline shorter than network delay
    # --------------------------------------------------

    allocator, resource = create_allocator(
        capacity=1000,
        latency_ms=10
    )

    task = Task(
        task_id=2,
        size_mb=2.0,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=0.005,
        task_type="normal",
        workload_mi=200.0,
        cpu_demand_mips=250.0
    )

    selected = allocator.allocate_task(task)

    assert selected is None
    assert task.status == "unallocated"
    assert resource.current_load == 0.0

    print("3. Deadline shorter than network delay: PASSED")

    # --------------------------------------------------
    # TEST 3: Insufficient CPU capacity
    # --------------------------------------------------

    allocator, resource = create_allocator(
        capacity=500,
        latency_ms=10
    )

    task = Task(
        task_id=3,
        size_mb=10.0,
        original_priority=1.0,
        arrival_time=0.0,
        deadline=1.0,
        task_type="normal",
        workload_mi=1000.0,
        cpu_demand_mips=250.0
    )

    selected = allocator.allocate_task(task)

    assert selected is None
    assert task.status == "unallocated"
    assert resource.current_load == 0.0

    print("4. Insufficient CPU capacity handling: PASSED")

    print("\n" + "=" * 62)
    print("ALL DEADLINE-AWARE ALLOCATION TESTS PASSED")
    print("=" * 62)


if __name__ == "__main__":
    main()
