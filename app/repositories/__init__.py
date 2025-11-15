from __future__ import annotations

from sqlalchemy.orm import Session


class BaseRepository:
    """Base repository holding a SQLAlchemy Session."""

    def __init__(self, session: Session) -> None:
        self._session = session
