# ToDoList CLI Application

A simple, command-line ToDoList application built with Python and Object-Oriented Programming (OOP) principles.  
Users can manage multiple projects and tasks in an in-memory storage layer via a clean, menu-driven CLI.

---

## Features ✨

This application allows users to manage their tasks and projects through a command-line interface.

### Project Management

- Create new projects.
- Edit existing projects.
- Delete projects (with cascade deletion of all associated tasks).
- List all created projects.

### Task Management

- Add tasks to a specific project.
- Edit an existing task (title, description, deadline, status).
- Delete a task from a project.
- Change a task's status: `todo`, `doing`, `done`.
- List all tasks within a specific project.

---

## Tech Stack & Tools 🧰

- **Language:** Python
- **Core Principles:** Object-Oriented Programming (OOP), layered architecture
- **Dependency Management:** Poetry
- **Version Control:** Git & GitHub
- **Environment Variables:** python-dotenv

---

## Project Structure 🧱

High-level folder structure:

```text
.
├── cli/
│   └── main.py           # CLI entry point (user interface layer)
├── core/
│   ├── models.py         # Core domain models: Project, Task, IDs, Status
│   └── services.py       # Business logic for projects and tasks
├── storage/
│   └── in_memory.py      # In-memory storage (mock database)
├── tests/                # (Reserved for unit tests)
├── .gitignore
├── .env.example          # Example environment variables
├── pyproject.toml
└── README.md
