from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.exceptions import (
    ValidationError,
    NotFoundError,
    BusinessRuleViolation,
    AppError,
)
from app.models import TaskORM
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

MAX_TASK_TITLE_LENGTH = 30
MAX_TASK_DESCRIPTION_LENGTH = 150
ALLOWED_STATUSES = ("todo", "doing", "done")


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        max_tasks_per_project: int,
    ) -> None:
        """
        Application service responsible for task-related business logic.
        """
        self._task_repo = task_repo
        self._project_repo = project_repo
        self._max_tasks_per_project = max_tasks_per_project

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: Optional[datetime],
    ) -> TaskORM:
        """
        Entry point used by the Web API layer.

        The API passes `deadline` as a `datetime` instance (or None).
        This method converts it to the `YYYY-MM-DD` string format expected
        by `add_task_to_project` and delegates the actual business logic.
        """
        if deadline is None:
            deadline_str: Optional[str] = None
        else:
            # Keep only the calendar date part, e.g. "2025-12-09".
            deadline_str = deadline.strftime("%Y-%m-%d")

        return self.add_task_to_project(
            project_id=project_id,
            title=title,
            description=description,
            deadline_str=deadline_str,
        )

    def add_task_to_project(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline_str: Optional[str],
    ) -> TaskORM:
        """
        Add a new task to a project after enforcing all business rules.
        """
        # Ensure the project exists (avoid failing later at the DB level).
        try:
            self._project_repo.get_by_id(project_id)
        except NotFoundError as exc:
            raise ValidationError(
                f"Project with id {project_id} does not exist."
            ) from exc

        # Enforce maximum number of tasks per project.
        tasks = self._task_repo.list_by_project(project_id)
        if len(tasks) >= self._max_tasks_per_project:
            raise BusinessRuleViolation(
                "Cannot add new task. "
                f"Maximum limit of {self._max_tasks_per_project} tasks per project reached."
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

        parsed_deadline: Optional[datetime] = None
        if deadline_str:
            try:
                parsed_deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError as exc:
                raise ValidationError(
                    "Invalid deadline format. Please use YYYY-MM-DD."
                ) from exc

        return self._task_repo.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=parsed_deadline,
        )

    def get_project_tasks(self, project_id: int) -> List[TaskORM]:
        """
        Return all tasks for a specific project.
        """
        return self._task_repo.list_by_project(project_id)

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by its identifier.
        """
        try:
            self._task_repo.delete(task_id)
        except NotFoundError as exc:
            # Re-raise so that the caller can decide how to handle it.
            raise exc

    def edit_task(
        self,
        task_id: int,
        new_title: str,
        new_description: str,
        new_deadline_str: Optional[str],
    ) -> TaskORM:
        """
        Update title / description / deadline of an existing task
        after validating the new values.
        """
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
        """
        Change task status after validating that the new value is allowed.
        """
        if new_status not in ALLOWED_STATUSES:
            raise ValidationError(
                f"Invalid status '{new_status}'. Must be one of {ALLOWED_STATUSES}."
            )

        return self._task_repo.update_status(task_id, new_status)