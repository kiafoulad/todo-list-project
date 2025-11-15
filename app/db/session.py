from __future__ import annotations

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "todolist_db")
DB_USER = os.getenv("DB_USER", "todolist_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret_password")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=DB_ECHO)

# Session factory (not autocommit, not autoflush)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency-style session generator.

    Usage pattern:
        with SessionLocal() as session:
            ...
    """
    with SessionLocal() as session:
        yield session
