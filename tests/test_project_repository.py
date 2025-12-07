from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError, UniqueConstraintError
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository


@pytest.fixture
def project_repo(db_session: Session) -> ProjectRepository:
    """Provide a ProjectRepository wired to the test database session."""
    return ProjectRepository(session=db_session)


@pytest.fixture
def task_repo(db_session: Session) -> TaskRepository:
    """Provide a TaskRepository wired to the test database session."""
    return TaskRepository(session=db_session)


def test_create_project_persists_and_lists(project_repo: ProjectRepository) -> None:
    """A created project should be returned and appear in list_all()."""
    created = project_repo.create(
        name="Repo Test Project",
        description="Created via ProjectRepository tests",
    )

    assert created.id is not None
    assert created.name == "Repo Test Project"

    projects = project_repo.list_all()
    assert any(p.id == created.id for p in projects)


def test_create_project_with_duplicate_name_raises(
    project_repo: ProjectRepository,
) -> None:
    """Creating two projects with the same name should raise UniqueConstraintError."""
    project_repo.create(
        name="Duplicate Name",
        description="First project",
    )

    with pytest.raises(UniqueConstraintError):
        project_repo.create(
            name="Duplicate Name",
            description="Second project with same name",
        )


def test_update_project_changes_name_and_description(
    project_repo: ProjectRepository,
) -> None:
    """Updating a project should change its persisted fields."""
    project = project_repo.create(
        name="Old Name",
        description="Old description",
    )

    updated = project_repo.update(
        project_id=project.id,
        new_name="New Name",
        new_description="New description",
    )

    assert updated.id == project.id
    assert updated.name == "New Name"
    assert updated.description == "New description"


def test_update_missing_project_raises_not_found(
    project_repo: ProjectRepository,
) -> None:
    """Updating a missing project should raise NotFoundError."""
    missing_id = 9999

    with pytest.raises(NotFoundError):
        project_repo.update(
            project_id=missing_id,
            new_name="Does not matter",
            new_description="Does not matter",
        )


def test_delete_project_cascades_to_tasks(
    project_repo: ProjectRepository,
    task_repo: TaskRepository,
) -> None:
    """Deleting a project should also remove its tasks."""
    project = project_repo.create(
        name="Project With Tasks",
        description="Used to check cascade delete",
    )

    task1 = task_repo.create(
        project_id=project.id,
        title="Task 1",
        description="First task",
        deadline=None,
    )
    task2 = task_repo.create(
        project_id=project.id,
        title="Task 2",
        description="Second task",
        deadline=None,
    )

    tasks_before = task_repo.list_by_project(project.id)
    assert {t.id for t in tasks_before} == {task1.id, task2.id}

    project_repo.delete(project.id)

    remaining_tasks = task_repo.list_by_project(project.id)
    assert remaining_tasks == []
