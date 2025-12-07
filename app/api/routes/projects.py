from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_project_service
from app.api.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["projects"],
)


@router.get(
    "",
    response_model=List[ProjectRead],
    summary="List all projects",
)
def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> List[ProjectRead]:
    """Return all projects ordered by id."""
    return service.get_all_projects()


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """Create a new project."""
    return service.create_project(
        name=payload.name,
        description=payload.description,
    )


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Update an existing project",
)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """Update an existing project."""
    return service.edit_project(
        project_id=project_id,
        new_name=payload.name,
        new_description=payload.description,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
) -> None:
    """Delete a project by id."""
    service.delete_project(project_id)
