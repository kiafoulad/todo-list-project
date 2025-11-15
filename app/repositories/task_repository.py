from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.exceptions import NotFoundError
from app.models import TaskORM
from app.repositories import BaseRepository


class TaskRepository(BaseRepository):
    """Repository for TaskORM entities."""

    def __init__(self, session: Session | None = None) -> None:
        if session is None:
            session = SessionLocal()
        super().__init__(session)

    # --- Query methods ---

    def get_by_id(self, task_id: int) -> TaskORM:
        task = self._session.get(TaskORM, task_id)
        if task is None:
            raise NotFoundError("Task", task_id)
        return task

    def list_by_project(self, project_id: int) -> List[TaskORM]:
        stmt = (
            select(TaskORM)
            .where(TaskORM.project_id == project_id)
            .order_by(TaskORM.id)
        )
        result = self._session.execute(stmt).scalars().all()
        return list(result)

    def list_overdue_open_tasks(self, now: datetime) -> List[TaskORM]:
        """Return tasks whose deadline has passed and are not yet done."""
        stmt = (
            select(TaskORM)
            .where(TaskORM.deadline.is_not(None))
            .where(TaskORM.deadline < now)
            .where(TaskORM.status != "done")
            .order_by(TaskORM.deadline)
        )
        result = self._session.execute(stmt).scalars().all()
        return list(result)

    # --- Command methods ---

    def create(
        self,
        project_id: int,
        title: str,
        description: str,
        deadline: datetime | None = None,
    ) -> TaskORM:
        task = TaskORM(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def update(
        self,
        task_id: int,
        new_title: str,
        new_description: str,
        new_deadline: datetime | None,
    ) -> TaskORM:
        """Update an existing task."""
        task = self._session.get(TaskORM, task_id)
        if task is None:
            raise NotFoundError("Task", task_id)

        task.title = new_title
        task.description = new_description
        task.deadline = new_deadline

        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        task = self._session.get(TaskORM, task_id)
        if task is None:
            raise NotFoundError("Task", task_id)

        self._session.delete(task)
        self._session.commit()

    def update_status(self, task_id: int, new_status: str) -> TaskORM:
        task = self._session.get(TaskORM, task_id)
        if task is None:
            raise NotFoundError("Task", task_id)

        task.status = new_status
        self._session.commit()
        self._session.refresh(task)
        return task
