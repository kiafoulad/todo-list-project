from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


@pytest.fixture
def task_env(db_session):
    project_repo = ProjectRepository(session=db_session)
    task_repo = TaskRepository(session=db_session)
    service = TaskService(
        task_repo=task_repo,
        project_repo=project_repo,
        max_tasks_per_project=20,
    )
    return project_repo, task_repo, service


def _create_sample_tasks(
    project_repo: ProjectRepository,
    task_repo: TaskRepository,
    now: datetime,
    project_name: str,
):
    """
    Create a project with several tasks used to test overdue behaviour.

    Tasks created:
    - overdue_open_older: deadline in the past, status != "done"
    - overdue_open_newer: deadline in the past, status != "done"
    - done_task: deadline in the past, status "done"
    - future_task: deadline in the future
    - no_deadline_task: deadline is None
    """
    project = project_repo.create(
        name=project_name,
        description="Project used for overdue task tests",
    )

    overdue_open_older = task_repo.create(
        project_id=project.id,
        title="Overdue older",
        description="Old overdue task",
        deadline=now - timedelta(days=2),
    )

    overdue_open_newer = task_repo.create(
        project_id=project.id,
        title="Overdue newer",
        description="Newer overdue task",
        deadline=now - timedelta(days=1),
    )

    done_task = task_repo.create(
        project_id=project.id,
        title="Overdue but done",
        description="Should not be returned as overdue open",
        deadline=now - timedelta(days=3),
    )
    task_repo.update_status(done_task.id, "done")

    future_task = task_repo.create(
        project_id=project.id,
        title="Future task",
        description="Deadline is in the future",
        deadline=now + timedelta(days=1),
    )

    no_deadline_task = task_repo.create(
        project_id=project.id,
        title="No deadline task",
        description="Task without a deadline",
        deadline=None,
    )

    return {
        "project": project,
        "overdue_open_older": overdue_open_older,
        "overdue_open_newer": overdue_open_newer,
        "done_task": done_task,
        "future_task": future_task,
        "no_deadline_task": no_deadline_task,
    }


def test_list_overdue_open_tasks_filters_by_deadline_and_status(task_env):
    """
    list_overdue_open_tasks should return only tasks that:
    - have a non-null deadline
    - deadline < now
    - status is not "done"
    """
    project_repo, task_repo, _service = task_env
    now = datetime.utcnow()

    tasks = _create_sample_tasks(
        project_repo,
        task_repo,
        now,
        project_name="Overdue Project (filter test)",
    )

    overdue_tasks = task_repo.list_overdue_open_tasks(now)

    overdue_ids = [t.id for t in overdue_tasks]
    expected_ids = {
        tasks["overdue_open_older"].id,
        tasks["overdue_open_newer"].id,
    }

    assert set(overdue_ids) == expected_ids

    # The repository orders by deadline ascending, so "older" should come first.
    assert overdue_tasks[0].id == tasks["overdue_open_older"].id
    assert overdue_tasks[1].id == tasks["overdue_open_newer"].id


def test_auto_close_overdue_tasks_with_service(task_env):
    """
    Simulate the auto-close behaviour:
    - list overdue open tasks
    - set their status to 'done' using TaskService
    - verify that there are no overdue open tasks afterwards
    """
    project_repo, task_repo, service = task_env
    now = datetime.utcnow()

    _create_sample_tasks(
        project_repo,
        task_repo,
        now,
        project_name="Overdue Project (auto-close test)",
    )

    overdue_before = task_repo.list_overdue_open_tasks(now)
    assert len(overdue_before) > 0

    for task in overdue_before:
        service.change_task_status(task_id=task.id, new_status="done")

    overdue_after = task_repo.list_overdue_open_tasks(now)
    assert overdue_after == []
