from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# -----------------------------
# Project schemas
# -----------------------------


class ProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Project name",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Short description of the project",
    )


class ProjectCreate(ProjectBase):
    """Payload model for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="New project name",
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="New project description",
    )


class ProjectRead(BaseModel):
    """Response model for returning project data."""
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Task schemas
# -----------------------------


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Task title",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task description",
    )


class TaskCreate(TaskBase):
    """Payload model for creating a task."""
    deadline: Optional[datetime] = Field(
        None,
        description="Optional deadline for the task (UTC ISO 8601)",
    )


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="New task title",
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="New task description",
    )
    deadline: Optional[datetime] = Field(
        None,
        description="New deadline for the task (UTC ISO 8601)",
    )
    status: Optional[str] = Field(
        None,
        description="New status for the task (for example: todo, doing, done)",
    )


class TaskRead(BaseModel):
    """Response model for returning task data."""
    id: int
    project_id: int
    title: str
    description: str
    status: str
    deadline: Optional[datetime] = None
    created_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
