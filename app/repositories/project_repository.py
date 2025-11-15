from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.exceptions import NotFoundError, UniqueConstraintError
from app.models import ProjectORM
from app.repositories import BaseRepository


class ProjectRepository(BaseRepository):
    """Repository for ProjectORM entities."""

    def __init__(self, session: Session | None = None) -> None:
        # Allow passing an external session (e.g., from a service or test)
        # or create a local one for simple use-cases.
        if session is None:
            session = SessionLocal()
        super().__init__(session)

    # --- Query methods ---

    def get_by_id(self, project_id: int) -> ProjectORM:
        project = self._session.get(ProjectORM, project_id)
        if project is None:
            raise NotFoundError("Project", project_id)
        return project

    def get_by_name(self, name: str) -> Optional[ProjectORM]:
        stmt = select(ProjectORM).where(ProjectORM.name == name)
        result = self._session.execute(stmt).scalar_one_or_none()
        return result

    def list_all(self) -> List[ProjectORM]:
        stmt = select(ProjectORM).order_by(ProjectORM.id)
        result = self._session.execute(stmt).scalars().all()
        return list(result)

    def exists_by_name(self, name: str) -> bool:
        return self.get_by_name(name) is not None

    # --- Command methods (mutations) ---

    def create(self, name: str, description: str) -> ProjectORM:
        if self.exists_by_name(name):
            raise UniqueConstraintError(f"Project with name '{name}' already exists")

        project = ProjectORM(name=name, description=description)
        self._session.add(project)

        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            # Extra safety in case of concurrent insert
            raise UniqueConstraintError(
                f"Project with name '{name}' already exists"
            ) from exc

        self._session.refresh(project)
        return project

    def update(self, project_id: int, new_name: str, new_description: str) -> ProjectORM:
        """Update an existing project."""
        project = self._session.get(ProjectORM, project_id)
        if project is None:
            raise NotFoundError("Project", project_id)

        # Check for unique name constraint manually
        existing = self.get_by_name(new_name)
        if existing is not None and existing.id != project.id:
            raise UniqueConstraintError(f"Project with name '{new_name}' already exists")

        project.name = new_name
        project.description = new_description

        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise UniqueConstraintError(
                f"Project with name '{new_name}' already exists"
            ) from exc

        self._session.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        project = self._session.get(ProjectORM, project_id)
        if project is None:
            raise NotFoundError("Project", project_id)

        self._session.delete(project)
        self._session.commit()
