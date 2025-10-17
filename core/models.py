# core/models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, NewType

# Using NewType to distinguish between different kinds of IDs for better type safety.
ProjectId = NewType("ProjectId", int)
TaskId = NewType("TaskId", int)

# Defines the allowed statuses for a task.
Status = Literal["todo", "doing", "done"]

@dataclass
class Project:
    """Represents a project that contains tasks."""
    id: ProjectId
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Task:
    """Represents a single task within a project."""
    id: TaskId
    project_id: ProjectId
    title: str
    description: str
    status: Status = "todo"
    deadline: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)