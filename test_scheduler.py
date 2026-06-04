from app.scheduler.task_manager import (
    TaskManager
)

TaskManager.create_task(
    user_id=123,
    query="AI news",
    schedule_type="daily",
    schedule_value="08:00"
)

tasks = TaskManager.get_tasks(
    123
)

print(tasks)