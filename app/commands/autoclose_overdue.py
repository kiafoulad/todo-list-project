from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv

from app.db.session import SessionLocal
from app.exceptions import AppError
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def run_autoclose_overdue() -> int:
    """
    Close all overdue tasks by setting their status to 'done'.

    A task is considered overdue if:
      - it has a non-null deadline
      - deadline < now (UTC)
      - status is not 'done'
    """
    load_dotenv()

    max_tasks_per_project = int(os.getenv("MAX_TASKS_PER_PROJECT", "20"))
    now = datetime.utcnow()

    closed_count = 0

    # Use a single DB session for the whole operation
    with SessionLocal() as session:
        project_repo = ProjectRepository(session=session)
        task_repo = TaskRepository(session=session)
        task_service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks_per_project=max_tasks_per_project,
        )

        overdue_tasks = task_repo.list_overdue_open_tasks(now)

        for task in overdue_tasks:
            task_service.change_task_status(task_id=task.id, new_status="done")
            closed_count += 1

    print(
        f"[autoclose_overdue] Closed {closed_count} task(s) "
        f"at {now.isoformat()} (UTC)."
    )
    return closed_count


if __name__ == "__main__":
    try:
        run_autoclose_overdue()
    except AppError as exc:
        # Keep it simple: print the error to stdout/stderr
        print(f"[autoclose_overdue] Error: {exc}")
