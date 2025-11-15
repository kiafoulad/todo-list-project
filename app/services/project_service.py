from __future__ import annotations

from typing import List

from app.exceptions import (
    ValidationError,
    BusinessRuleViolation,
    NotFoundError,
    UniqueConstraintError,
)
from app.models import ProjectORM
from app.repositories.project_repository import ProjectRepository

MAX_PROJECT_NAME_LENGTH = 30
MAX_PROJECT_DESCRIPTION_LENGTH = 150


class ProjectService:
    """Application service for project-related use-cases."""

    def __init__(self, project_repo: ProjectRepository, max_projects: int) -> None:
        self._project_repo = project_repo
        self._max_projects = max_projects

    def create_project(self, name: str, description: str) -> ProjectORM:
        """Create a new project after applying business rules and validation."""
        name = name.strip()
        description = description.strip()

        if not name:
            raise ValidationError("Project name cannot be empty.")
        if len(name) > MAX_PROJECT_NAME_LENGTH:
            raise ValidationError(
                f"Project name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters."
            )
        if len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Project description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters."
            )

        projects = self._project_repo.list_all()
        if len(projects) >= self._max_projects:
            raise BusinessRuleViolation(
                f"Cannot create new project. Maximum limit of {self._max_projects} projects reached."
            )

        try:
            return self._project_repo.create(name=name, description=description)
        except UniqueConstraintError as exc:
            # Re-raise as validation-level error for the caller
            raise ValidationError(str(exc)) from exc

    def get_all_projects(self) -> List[ProjectORM]:
        """Return all projects ordered by id."""
        return self._project_repo.list_all()

    def delete_project(self, project_id: int) -> None:
        """Delete a project by id. Tasks will be deleted by cascade."""
        try:
            self._project_repo.delete(project_id)
        except NotFoundError as exc:
            # propagate as is – caller can decide how to show the error
            raise exc

    def edit_project(
        self,
        project_id: int,
        new_name: str,
        new_description: str,
    ) -> ProjectORM:
        """Edit an existing project after validation."""
        new_name = new_name.strip()
        new_description = new_description.strip()

        if not new_name:
            raise ValidationError("Project name cannot be empty.")
        if len(new_name) > MAX_PROJECT_NAME_LENGTH:
            raise ValidationError(
                f"Project name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters."
            )
        if len(new_description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Project description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters."
            )

        try:
            return self._project_repo.update(
                project_id=project_id,
                new_name=new_name,
                new_description=new_description,
            )
        except UniqueConstraintError as exc:
            raise ValidationError(str(exc)) from exc
