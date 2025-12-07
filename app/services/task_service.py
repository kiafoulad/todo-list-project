from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.exceptions import ValidationError, NotFoundError, BusinessRuleViolation
from app.models import TaskORM
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

MAX_TASK_TITLE_LENGTH = 30
MAX_TASK_DESCRIPTION_LENGTH = 150
ALLOWED_STATUSES = ("todo", "doing", "done")


class TaskService:
    """Application service for task-related use-cases."""

    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        max_tasks_per_project: int,
    ) -> None:
        self._task_repo = task_repo
        self._project_repo = project_repo
        self._max_tasks_per_project = max_tasks_per_project

    def add_task_to_project(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline_str: str | None,
    ) -> TaskORM:
        """Add a new task to a project after validation."""
        # Ensure project exists (otherwise FK error would be raised at DB level)
        try:
            self._project_repo.get_by_id(project_id)
        except NotFoundError as exc:
            raise ValidationError(f"Project with id {project_id} does not exist.") from exc

        tasks = self._task_repo.list_by_project(project_id)
        if len(tasks) >= self._max_tasks_per_project:
            raise BusinessRuleViolation(
                f"Cannot add new task. Maximum limit of "
                f"{self._max_tasks_per_project} tasks per project reached."
            )

        title = title.strip()
        description = description.strip()

        if not title:
            raise ValidationError("Task title cannot be empty.")
        if len(title) > MAX_TASK_TITLE_LENGTH:
            raise ValidationError(
                f"Task title cannot exceed {MAX_TASK_TITLE_LENGTH} characters."
            )
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters."
            )

        deadline: Optional[datetime] = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError as exc:
                raise ValidationError(
                    "Invalid deadline format. Please use YYYY-MM-DD."
                ) from exc

        return self._task_repo.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )

    def get_project_tasks(self, project_id: int) -> List[TaskORM]:
        """Return tasks for a specific project."""
        return self._task_repo.list_by_project(project_id)

    def delete_task(self, task_id: int) -> None:
        """Delete a task by id."""
        try:
            self._task_repo.delete(task_id)
        except NotFoundError as exc:
            raise exc

    def edit_task(
        self,
        task_id: int,
        new_title: str,
        new_description: str,
        new_deadline_str: str | None,
    ) -> TaskORM:
        """Edit an existing task after validation."""
        new_title = new_title.strip()
        new_description = new_description.strip()

        if not new_title:
            raise ValidationError("Task title cannot be empty.")
        if len(new_title) > MAX_TASK_TITLE_LENGTH:
            raise ValidationError(
                f"Task title cannot exceed {MAX_TASK_TITLE_LENGTH} characters."
            )
        if len(new_description) > MAX_TASK_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters."
            )

        new_deadline: Optional[datetime] = None
        if new_deadline_str:
            try:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
            except ValueError as exc:
                raise ValidationError(
                    "Invalid deadline format. Please use YYYY-MM-DD."
                ) from exc

        return self._task_repo.update(
            task_id=task_id,
            new_title=new_title,
            new_description=new_description,
            new_deadline=new_deadline,
        )

    def change_task_status(self, task_id: int, new_status: str) -> TaskORM:
        """Change task status after validating allowed values."""
        if new_status not in ALLOWED_STATUSES:
            raise ValidationError(
                f"Invalid status '{new_status}'. Must be one of {ALLOWED_STATUSES}."
            )

        return self._task_repo.update_status(task_id, new_status)

