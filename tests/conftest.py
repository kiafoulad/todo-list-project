from __future__ import annotations

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.base import Base
import app.models  # noqa: F401  # Ensure all ORM models are imported


@pytest.fixture(scope="session")
def engine():
    """
    Create a dedicated in-memory SQLite engine for tests.

    This avoids touching the real PostgreSQL instance and keeps tests fast and isolated.
    """
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine) -> Generator[Session, None, None]:
    """
    Provide a fresh database session for each test.

    The session is rolled back and closed after each test to keep tests isolated.
    """
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()

    try:
        yield session
        session.rollback()
    finally:
        session.close()
