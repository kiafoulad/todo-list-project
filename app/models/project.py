from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    # Only imported for type checking, avoids circular import at runtime
    from app.models.task import TaskORM


class ProjectORM(Base):
    """SQLAlchemy ORM model for the projects table."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # One-to-many relationship with tasks
    tasks: Mapped[List["TaskORM"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
