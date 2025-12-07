from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def get_session() -> Generator[Session, None, None]:
    """Provide a database session for FastAPI dependencies."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_project_service(session: Session = Depends(get_session)) -> ProjectService:
    """Provide a ProjectService instance for request handlers."""
    project_repo = ProjectRepository(session=session)
    # Same limit used in the CLI entrypoint
    return ProjectService(project_repo=project_repo, max_projects=20)


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    """Provide a TaskService instance for request handlers."""
    project_repo = ProjectRepository(session=session)
    task_repo = TaskRepository(session=session)
    return TaskService(
        task_repo=task_repo,
        project_repo=project_repo,
        max_tasks_per_project=20,
    )
