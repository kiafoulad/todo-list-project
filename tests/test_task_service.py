from __future__ import annotations

import pytest

from app.exceptions import AppError
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


@pytest.fixture
def task_service(db_session):
    """
    Build a TaskService instance wired to a fresh test database session.

    We reuse the real repositories, but the underlying engine is the
    in-memory SQLite engine provided by the test fixtures.
    """
    project_repo = ProjectRepository(session=db_session)
    task_repo = TaskRepository(session=db_session)

    service = TaskService(
        task_repo=task_repo,
        project_repo=project_repo,
        max_tasks_per_project=20,
    )

    # Returning all three so tests can also inspect repositories directly if needed.
    return service, project_repo, task_repo


def test_change_task_status_for_existing_task(task_service):
    """
    Changing the status of an existing task should persist the new status.
    """
    service, project_repo, task_repo = task_service

    # Arrange: create a project and a task
    project = project_repo.create(
        name="Test Project",
        description="Project for TaskService status tests",
    )

    task = task_repo.create(
        project_id=project.id,
        title="Initial Task",
        description="Task that will change status",
        deadline=None,
    )

    # Act
    updated = service.change_task_status(task_id=task.id, new_status="done")

    # Assert
    assert updated.id == task.id
    assert updated.status == "done"


def test_change_task_status_for_missing_task_raises(task_service):
    """
    Changing the status of a non-existing task should raise a business error.
    """
    service, project_repo, task_repo = task_service

    missing_task_id = 9999

    with pytest.raises(AppError):
        service.change_task_status(task_id=missing_task_id, new_status="done")
