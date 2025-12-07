# ToDoList CLI Application

A command-line ToDoList application built with Python and Object-Oriented Programming (OOP) principles.

The project is developed in two main phases:

- **Phase 1 – In-Memory storage**: tasks and projects are stored in memory.
- **Phase 2 – Relational Database (PostgreSQL)**: data is stored in a real database using SQLAlchemy and Alembic.

The current default entry point uses **PostgreSQL + SQLAlchemy** (Phase 2).

---

## Features

### Project Management

Users can:

- Create new projects.
- Edit an existing project (name, description).
- Delete a project (with cascade deletion of all its tasks).
- List all projects.
- Open a project and work with its tasks.

### Task Management

Inside a project, users can:

- Create tasks with:
  - title
  - description
  - deadline (optional)
  - status: `todo`, `doing`, `done`
- Edit tasks:
  - title, description, deadline, status.
- Delete tasks.
- List all tasks of a project.
- Change task status by task id (from the project menu).

### Overdue Tasks (Phase 2)

With the relational database layer, the application supports:

- Querying **overdue open tasks** (deadline in the past, status not `done`).
- Automatically changing the status of overdue tasks to `done` via dedicated commands.

---

## Tech Stack & Tools

- **Language**: Python 3.11
- **Paradigm**: Object-Oriented Programming (OOP)
- **Architecture**:
  - Domain models and services
  - Repository layer based on SQLAlchemy ORM
  - CLI layer for user interaction
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Dependency Management**: Poetry
- **Environment Variables**: python-dotenv
- **Tests**: pytest
- **Container**: Docker Compose (for PostgreSQL service)
- **Scheduling**: `schedule` library (for periodic overdue auto-close)

---

## Project Structure

High-level folder structure:

```text
.
├── app/
│   ├── main.py                    # Application entry point (CLI + DB wiring)
│   ├── cli/
│   │   └── console.py             # Console menus and user interaction
│   ├── db/
│   │   ├── base.py                # SQLAlchemy Base and metadata
│   │   └── session.py             # Engine + SessionLocal creation
│   ├── models/
│   │   ├── project.py             # Project ORM model
│   │   └── task.py                # Task ORM model
│   ├── repositories/
│   │   ├── project_repository.py  # ProjectRepository (CRUD, queries)
│   │   └── task_repository.py     # TaskRepository (CRUD, overdue queries)
│   ├── services/
│   │   ├── project_service.py     # Business logic for projects
│   │   └── task_service.py        # Business logic for tasks
│   ├── commands/
│   │   ├── autoclose_overdue.py   # Command to auto-close overdue tasks once
│   │   └── scheduler.py           # Command to run auto-close periodically
│   └── exceptions/                # Custom exception types
│
├── core/                          # Initial in-memory domain layer (Phase 1)
├── storage/
│   └── in_memory.py               # In-memory storage implementation (Phase 1)
│
├── migrations/
│   ├── env.py                     # Alembic environment configuration
│   └── versions/                  # Auto-generated migration scripts
│
├── tests/
│   ├── conftest.py                # Test configuration and fixtures
│   ├── test_project_repository.py # Tests for ProjectRepository
│   ├── test_task_service.py       # Tests for TaskService
│   └── test_task_overdue.py       # Tests for overdue task behaviour
│
├── .env.example                   # Example environment variables
├── .gitignore
├── alembic.ini                    # Alembic configuration file
├── docker-compose.yml             # PostgreSQL Docker service
├── poetry.lock
├── pyproject.toml                 # Poetry configuration
└── README.md
