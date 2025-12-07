from __future__ import annotations

from app.exceptions.base import AppError


class ServiceError(AppError):
    """Base exception for service layer errors."""
    pass


class ValidationError(ServiceError):
    """Raised when input validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class BusinessRuleViolation(ServiceError):
    """Raised when a domain/business rule is violated."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
