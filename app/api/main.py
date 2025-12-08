from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import projects, tasks


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="ToDo List Web API",
        version="0.1.0",
        description="Web API for managing projects and tasks.",
    )

    @app.get("/api/v1/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    # Register versioned API routers
    app.include_router(projects.router, prefix="/api/v1")
    app.include_router(tasks.router, prefix="/api/v1")

    return app


app = create_app()
