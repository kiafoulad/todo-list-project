from __future__ import annotations

from typing import List
from app.exceptions import NotFoundError  # Import NotFoundError from the correct module

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
    """
    Return all tasks for the given project.

    First we ensure the project exists, otherwise we return 404.
    Then we load all tasks for that project ordered by id.
    """
    project_repo = ProjectRepository(session=session)

    # Ensure project exists; ProjectRepository raises NotFoundError if not.
    try:
        project_repo.get_by_id(project_id)
    except NotFoundError:
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

    # Ensure the task exists and belongs to the given project
    try:
        task = task_repo.get_by_id(task_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )

    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )

    # Compute effective values for a partial update
    new_title = payload.title if payload.title is not None else task.title
    new_description = (
        payload.description if payload.description is not None else task.description
    )

    if payload.deadline is not None:
        new_deadline = payload.deadline
    else:
        new_deadline = task.deadline

    # Convert deadline to 'YYYY-MM-DD' string expected by TaskService
    if new_deadline is None:
        new_deadline_str: str | None = None
    else:
        new_deadline_str = new_deadline.strftime("%Y-%m-%d")

    # First update title / description / deadline via the service layer
    try:
        updated_task = service.edit_task(
            task_id=task_id,
            new_title=new_title,
            new_description=new_description,
            new_deadline_str=new_deadline_str,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Optionally update status if the client provided it
    if payload.status is not None and payload.status != updated_task.status:
        try:
            updated_task = service.change_task_status(
                task_id=task_id,
                new_status=payload.status,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    return updated_task

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

    # Ensure the task exists and belongs to this project
    try:
        task = task_repo.get_by_id(task_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )

    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )

    # Delegate deletion to the service layer
    try:
        service.delete_task(task_id=task_id)
    except NotFoundError:
        # In case the repository/service raises again
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found for this project",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return None