from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.exceptions import AppError
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


DATE_FORMAT = "%Y-%m-%d"


def _input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


def _input_optional_date(prompt: str) -> Optional[datetime]:
    raw = input(prompt).strip()
    if not raw:
        return None

    try:
        return datetime.strptime(raw, DATE_FORMAT)
    except ValueError:
        print(f"Invalid date format. Expected {DATE_FORMAT}. Deadline will be empty.")
        return None


def _print_projects(project_repo: ProjectRepository) -> None:
    projects = project_repo.list_all()

    if not projects:
        print("No projects found.")
        return

    print("\nProjects:")
    for p in projects:
        print(f"- [{p.id}] {p.name} (created at: {p.created_at})")
    print()


def _print_tasks_for_project(task_repo: TaskRepository, project_id: int) -> None:
    tasks = task_repo.list_by_project(project_id)

    if not tasks:
        print("No tasks found for this project.")
        return

    print(f"\nTasks for project {project_id}:")
    for t in tasks:
        status = getattr(t, "status", "unknown")
        deadline = getattr(t, "deadline", None)
        print(f"- [{t.id}] {t.title} | status={status} | deadline={deadline}")
    print()


def _create_project(project_repo: ProjectRepository) -> None:
    print("\n=== Create Project ===")
    name = _input_non_empty("Project name: ")
    description = input("Project description (optional): ").strip()

    try:
        project = project_repo.create(name=name, description=description)
        print(f"Project created with id={project.id}\n")
    except AppError as exc:
        print(f"Error creating project: {exc}\n")


def _edit_project(project_repo: ProjectRepository, project_id: int) -> None:
    project = project_repo.get_by_id(project_id)
    if project is None:
        print("Project not found.\n")
        return

    print("\n=== Edit Project ===")
    print(f"Current name: {project.name}")
    new_name = input("New name (leave empty to keep current): ").strip()
    if not new_name:
        new_name = project.name

    current_description = project.description or ""
    print(f"Current description: {current_description}")
    new_description = input("New description (leave empty to keep current): ").strip()
    if not new_description:
        new_description = project.description

    try:
        updated = project_repo.update(project_id, new_name, new_description)
        print(f"Project {updated.id} updated.\n")
    except AppError as exc:
        print(f"Error updating project: {exc}\n")


def _delete_project(project_repo: ProjectRepository, project_id: int) -> bool:
    project = project_repo.get_by_id(project_id)
    if project is None:
        print("Project not found.\n")
        return False

    print(f"\n=== Delete Project {project_id} ===")
    print(f"Name: {project.name}")
    confirm = input("Are you sure? This may also delete its tasks. [y/N]: ").strip().lower()
    if confirm != "y":
        print("Delete cancelled.\n")
        return False

    try:
        project_repo.delete(project_id)
        print("Project deleted.\n")
        return True
    except AppError as exc:
        print(f"Error deleting project: {exc}\n")
        return False


def _create_task(task_repo: TaskRepository, project_id: int) -> None:
    print(f"\n=== Create Task for project {project_id} ===")
    title = _input_non_empty("Task title: ")
    description = input("Task description (optional): ").strip()
    deadline = _input_optional_date(
        f"Deadline (optional, format {DATE_FORMAT}, leave empty for none): "
    )

    try:
        task = task_repo.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        print(f"Task created with id={task.id}\n")
    except AppError as exc:
        print(f"Error creating task: {exc}\n")


def _change_task_status(task_service: TaskService) -> None:
    print("\n=== Change Task Status ===")
    raw_id = _input_non_empty("Task id: ")

    try:
        task_id = int(raw_id)
    except ValueError:
        print("Task id must be an integer.\n")
        return

    new_status = _input_non_empty("New status (e.g. 'todo', 'in-progress', 'done'): ")

    try:
        updated = task_service.change_task_status(task_id=task_id, new_status=new_status)
        print(f"Task {updated.id} status updated to '{updated.status}'.\n")
    except AppError as exc:
        print(f"Error changing task status: {exc}\n")


def _project_menu(
    project_repo: ProjectRepository,
    task_repo: TaskRepository,
    task_service: TaskService,
    project_id: int,
) -> None:
    while True:
        print(f"\n=== Project {project_id} Menu ===")
        print("1) List tasks")
        print("2) Add task")
        print("3) Change task status")
        print("4) Edit project")
        print("5) Delete project")
        print("6) Back to main menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            _print_tasks_for_project(task_repo, project_id)
        elif choice == "2":
            _create_task(task_repo, project_id)
        elif choice == "3":
            _change_task_status(task_service)
        elif choice == "4":
            _edit_project(project_repo, project_id)
        elif choice == "5":
            deleted = _delete_project(project_repo, project_id)
            if deleted:
                return
        elif choice == "6":
            return
        else:
            print("Invalid choice. Please try again.\n")


def run_console(
    project_repo: ProjectRepository,
    task_repo: TaskRepository,
    task_service: TaskService,
) -> None:
    print("=== Todo List (RDB + SQLAlchemy) ===")

    while True:
        print("\n=== Main Menu ===")
        print("1) List projects")
        print("2) Create project")
        print("3) Open project")
        print("4) Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            _print_projects(project_repo)
        elif choice == "2":
            _create_project(project_repo)
        elif choice == "3":
            raw_id = _input_non_empty("Project id: ")
            try:
                project_id = int(raw_id)
            except ValueError:
                print("Project id must be an integer.\n")
                continue

            _project_menu(project_repo, task_repo, task_service, project_id)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.\n")
