from __future__ import annotations

from dotenv import load_dotenv

from app.cli.console import run_console
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def main() -> None:
    load_dotenv()

    session = SessionLocal()
    try:
        project_repo = ProjectRepository(session=session)
        task_repo = TaskRepository(session=session)

        task_service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks_per_project=20,
        )

        run_console(
            project_repo=project_repo,
            task_repo=task_repo,
            task_service=task_service,
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
