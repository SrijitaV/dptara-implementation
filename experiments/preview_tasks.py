
from src.task_generator import TaskGenerator


def main():
    generator = TaskGenerator(seed=42)

    tasks = generator.generate_tasks(
        2,
        "priority",
        5
    )

    print("\n" + "=" * 85)
    print("                 DPTARA - TASK GENERATION RESULTS")
    print("=" * 85)

    print(f"\nTotal tasks generated: {len(tasks)}\n")

    header = (
        f"{'ID':<8}"
        f"{'Arrival':<14}"
        f"{'Size (MB)':<14}"
        f"{'Deadline':<14}"
        f"{'Type':<16}"
        f"{'Priority':<10}"
    )

    print(header)
    print("-" * 85)

    for task in tasks:
        print(
            f"{task.task_id:<8}"
            f"{task.arrival_time:<14.4f}"
            f"{task.size_mb:<14.2f}"
            f"{task.deadline:<14.2f}"
            f"{task.task_type:<16}"
            f"{str(task.original_priority):<10}"
        )

    print("-" * 85)
    print("\nTask generation test completed successfully.")


if __name__ == "__main__":
    main()
