
from src.models.entities import Task, Resource
from src.resource_manager import ResourceManager
from src.resource_allocator import ResourceAllocator


def main():

    print("\n" + "=" * 65)
    print("       DPTARA - RESOURCE ALLOCATION VALIDATION")
    print("=" * 65)

    manager = ResourceManager()

    resources = [
        Resource("E1", "edge", 1000, 500),
        Resource("E2", "edge", 1000, 100),
        Resource("C1", "cloud", 5000, 0)
    ]

    for resource in resources:
        manager.register_resource(resource)

    allocator = ResourceAllocator(manager)

    print("\nInitial Resource Status:")

    for resource in manager.get_all_resources():
        print(
            f"{resource.resource_id} | "
            f"Type: {resource.resource_type} | "
            f"Load: {resource.current_load} | "
            f"Capacity: {resource.capacity}"
        )

    # -----------------------------------------
    # TEST 1: Least-loaded eligible edge server
    # -----------------------------------------

    print("\nTEST 1: Least-loaded edge selection")

    task_1 = Task(1, 5, 1, 0, 100, "routine")

    selected = allocator.allocate_task(task_1)

    assert selected is not None
    assert selected.resource_id == "E2"

    print("Selected resource:", selected.resource_id)
    print("TEST 1 PASSED")

    # Release task before next independent test.
    allocator.release_task(task_1)

    # -----------------------------------------
    # TEST 2: Edge preference over cloud
    # -----------------------------------------

    print("\nTEST 2: Edge preference over cloud")

    task_2 = Task(2, 5, 1, 0, 100, "routine")

    selected = allocator.allocate_task(task_2)

    assert selected is not None
    assert selected.resource_type == "edge"

    print("Selected resource:", selected.resource_id)
    print("TEST 2 PASSED")

    allocator.release_task(task_2)

    # -----------------------------------------
    # TEST 3: Cloud fallback
    # -----------------------------------------

    print("\nTEST 3: Cloud fallback")

    # Temporarily occupy both edge resources.
    edge_1 = manager.get_resource("E1")
    edge_2 = manager.get_resource("E2")

    edge_1.current_load = edge_1.capacity
    edge_2.current_load = edge_2.capacity

    task_3 = Task(3, 5, 1, 0, 10, "routine")

    selected = allocator.allocate_task(task_3)

    assert selected is not None
    assert selected.resource_type == "cloud"

    print("Selected resource:", selected.resource_id)
    print("TEST 3 PASSED")

    print("\n" + "=" * 65)
    print("ALL RESOURCE ALLOCATION TESTS PASSED")
    print("=" * 65)


if __name__ == "__main__":
    main()
