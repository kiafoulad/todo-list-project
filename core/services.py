# core/services.py
from storage.in_memory import InMemoryStorage
from core.models import Project, Task, ProjectId, TaskId

class ProjectService:
    """Handles the business logic for projects."""
    def __init__(self, storage: InMemoryStorage):
        self._storage = storage

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project after validation."""
        # Check for duplicate project names.
        if self._storage.find_project_by_name(name):
            raise ValueError(f"Project with name '{name}' already exists.")
        
        # Add other constraints, e.g., name length validation.
        if len(name) > 30:
            raise ValueError("Project name cannot exceed 30 characters.")

        return self._storage.create_project(name, description)

    def get_all_projects(self) -> list[Project]:
        return self._storage.get_all_projects()
    
    def delete_project(self, project_id: ProjectId) -> None:
        self._storage.delete_project(project_id)

class TaskService:
    """Handles the business logic for tasks."""
    def __init__(self, storage: InMemoryStorage):
        self._storage = storage

    def add_task_to_project(self, project_id: ProjectId, title: str, description: str) -> Task:
        """Adds a new task to a specific project after validation."""
        # Validate title length.
        if len(title) > 30:
            raise ValueError("Task title cannot exceed 30 characters.")
        
        return self._storage.create_task(project_id, title, description)

    def get_project_tasks(self, project_id: ProjectId) -> list[Task]:
        return self._storage.get_tasks_by_project(project_id)
    
    def delete_task(self, task_id: TaskId) -> None:
        """Deletes a task."""
        if not self._storage.delete_task(task_id):
            raise ValueError(f"Task with ID {task_id} not found.")