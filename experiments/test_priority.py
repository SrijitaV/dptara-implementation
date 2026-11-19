
from src.models.entities import Task
from src.models.priority_model import DynamicPriorityModel


# Create priority model
model = DynamicPriorityModel(
    alpha=1.0,
    beta=1.0,
    gamma=1.0
)

# Create sample tasks
task1 = Task(
    task_id=1,
    size_mb=10,
    original_priority=5,
    arrival_time=0,
    deadline=50,
    task_type="emergency"
)

task2 = Task(
    task_id=2,
    size_mb=20,
    original_priority=3,
    arrival_time=0,
    deadline=50,
    task_type="routine"
)

# Simulate current system time
current_time = 20

# Calculate priorities
p1 = model.update_priority(
    task1, current_time, current_load=20
)

p2 = model.update_priority(
    task2, current_time, current_load=20
)

# Display results
print("\n========== DPTARA PRIORITY TEST ==========")

print(f"Task 1 Priority: {p1:.4f}")
print(f"Task 2 Priority: {p2:.4f}")

print("\nScheduling Order:")

tasks = sorted(
    [task1, task2],
    key=lambda task: task.priority,
    reverse=True
)

for task in tasks:
    print(
        f"Task {task.task_id} | "
        f"Priority: {task.priority:.4f} | "
        f"Type: {task.task_type}"
    )

print("\nPriority model test completed successfully.")
