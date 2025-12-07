from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_session
from app.api.schemas import TaskCreate, TaskRead, TaskUpdate
from app.models.task import TaskORM
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

router = APIRouter(prefix="/projects", tags=["tasks"])


def _get_task_service(session: Session) -> TaskService:
    project_repo = ProjectRepository(session=session)
    task_repo = TaskRepository(session=session)
    return TaskService(
        task_repo=task_repo,
        project_repo=project_repo,
        max_tasks_per_project=20,
    )


@router.get("/{project_id}/tasks", response_model=List[TaskRead])
def list_project_tasks(
    project_id: int,
    session: Session = Depends(get_session),
) -> List[TaskRead]:
    project_repo = ProjectRepository(session=session)
    project = project_repo.get(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    stmt = (
        select(TaskORM)
        .where(TaskORM.project_id == project_id)
        .order_by(TaskORM.id)
    )
    tasks = session.execute(stmt).scalars().all()
    return tasks


@router.post(
    "/{project_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task_for_project(
    project_id: int,
    payload: TaskCreate,
    session: Session = Depends(get_session),
) -> TaskRead:
    service = _get_task_service(session)

    try:
        task = service.create_task(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            deadline=payload.deadline,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return task


@router.patch(
    "/{project_id}/tasks/{task_id}",
    response_model=TaskRead,
)
def update_task(
    project_id: int,
    task_id: int,
    payload: TaskUpdate,
    session: Session = Depends(get_session),
) -> TaskRead:
    service = _get_task_service(session)

    task_repo = TaskRepository(session=session)
    task = task_repo.get(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )

    new_title = payload.title if payload.title is not None else task.title
    new_description = (
        payload.description if payload.description is not None else task.description
    )
    new_deadline = payload.deadline if payload.deadline is not None else task.deadline
    new_status = payload.status if payload.status is not None else task.status

    try:
        updated = service.edit_task(
            task_id=task_id,
            title=new_title,
            description=new_description,
            deadline=new_deadline,
            status=new_status,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return updated


@router.delete(
    "/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    project_id: int,
    task_id: int,
    session: Session = Depends(get_session),
) -> None:
    service = _get_task_service(session)

    task_repo = TaskRepository(session=session)
    task = task_repo.get(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )

    try:
        service.delete_task(task_id=task_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return None
