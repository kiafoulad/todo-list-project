from __future__ import annotations

from app.exceptions.base import AppError


class RepositoryError(AppError):
    """Base exception for repository layer errors."""
    pass


class NotFoundError(RepositoryError):
    """Raised when an entity is not found in the data store."""

    def __init__(self, entity_name: str, entity_id: int | None = None) -> None:
        message = f"{entity_name} not found"
        if entity_id is not None:
            message += f" (id={entity_id})"
        super().__init__(message)
        self.entity_name = entity_name
        self.entity_id = entity_id


class UniqueConstraintError(RepositoryError):
    """Raised when a unique constraint is violated."""

    def __init__(self, message: str = "Unique constraint violated") -> None:
        super().__init__(message)
