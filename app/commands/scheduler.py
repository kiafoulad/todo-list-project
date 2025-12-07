from __future__ import annotations

import time
from datetime import datetime

import schedule

from app.db.session import get_session
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def autoclose_overdue_once() -> None:
    now = datetime.utcnow()

    with get_session() as session:
        project_repo = ProjectRepository(session=session)
        task_repo = TaskRepository(session=session)
        service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks_per_project=20,
        )

        overdue_tasks = task_repo.list_overdue_open_tasks(now)

        if not overdue_tasks:
            print(f"[{now.isoformat()}] No overdue tasks to close.")
            return

        for task in overdue_tasks:
            service.change_task_status(task_id=task.id, new_status="done")

        print(f"[{now.isoformat()}] Closed {len(overdue_tasks)} overdue tasks.")


def main() -> None:
    autoclose_overdue_once()

    schedule.every(5).minutes.do(autoclose_overdue_once)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
