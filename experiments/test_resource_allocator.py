
from src.models.entities import Task, Resource
from src.resource_manager import ResourceManager
from src.resource_allocator import ResourceAllocator


def main():

    # Initialize resource manager
    manager = ResourceManager()

    # Register computing resources
    resources = [
        Resource("E1", "edge", 100, 50),
        Resource("E2", "edge", 100, 20),
        Resource("C1", "cloud", 500, 100)
    ]

    for resource in resources:
        manager.register_resource(resource)

    # Initialize allocator
    allocator = ResourceAllocator(manager)

    # Create test tasks
    tasks = [
        Task(1, 30, 5, 0, 50, "emergency"),
        Task(2, 70, 3, 1, 60, "routine"),
        Task(3, 600, 2, 2, 80, "routine")
    ]

    print("\n" + "=" * 65)
    print("          DPTARA - RESOURCE ALLOCATION TEST")
    print("=" * 65)

    print("\nInitial Resource Status:")

    for resource in manager.get_all_resources():
        print(
            f"{resource.resource_id} | "
            f"Type: {resource.resource_type} | "
            f"Load: {resource.current_load} | "
            f"Capacity: {resource.capacity}"
        )

    print("\nTask Allocation Results:")
    print("-" * 65)

    for task in tasks:

        selected = allocator.allocate_task(task)

        if selected is not None:
            print(
                f"Task {task.task_id} | "
                f"Size: {task.size_mb} MB | "
                f"Allocated to: {selected.resource_id} | "
                f"Type: {selected.resource_type}"
            )
        else:
            print(
                f"Task {task.task_id} | "
                f"Size: {task.size_mb} MB | "
                f"Allocation: FAILED - No available resource"
            )

    print("\nFinal Resource Status:")
    print("-" * 65)

    for resource in manager.get_all_resources():

        print(
            f"{resource.resource_id} | "
            f"Type: {resource.resource_type} | "
            f"Load: {resource.current_load:.2f} | "
            f"Available: {resource.available_capacity:.2f} | "
            f"Utilization: {resource.utilization:.2f}"
        )

    print("\n" + "=" * 65)
    print("Resource Allocation Experiment Completed.")
    print("=" * 65)


if __name__ == "__main__":
    main()
