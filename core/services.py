# core/services.py
from storage.in_memory import InMemoryStorage
from core.models import Project, Task, ProjectId, TaskId, Status
from typing import get_args
from datetime import datetime

class ProjectService:
    """Handles the business logic for projects."""
    def __init__(self, storage: InMemoryStorage, max_projects: int):
        self._storage = storage
        self._max_projects = max_projects

    def create_project(self, name: str, description: str) -> Project:
        """Creates a new project after validation."""
        # Check project limit
        if len(self._storage.get_all_projects()) >= self._max_projects:
            raise ValueError(f"Cannot create new project. Maximum limit of {self._max_projects} reached.")
        
        if self._storage.find_project_by_name(name):
            raise ValueError(f"Project with name '{name}' already exists.")
        
        if len(name) > 30:
            raise ValueError("Project name cannot exceed 30 characters.")
        if len(description) > 150:
            raise ValueError("Project description cannot exceed 150 characters.")

        return self._storage.create_project(name, description)

    def get_all_projects(self) -> list[Project]:
        return self._storage.get_all_projects()
    
    def delete_project(self, project_id: ProjectId) -> None:
        self._storage.delete_project(project_id)

    def edit_project(self, project_id: ProjectId, new_name: str, new_description: str) -> Project:
        """Edits an existing project after validating the new data."""
        if len(new_name) > 30:
            raise ValueError("Project name cannot exceed 30 characters.")
        if len(new_description) > 150:
            raise ValueError("Project description cannot exceed 150 characters.")

        existing_project = self._storage.find_project_by_name(new_name)
        if existing_project and existing_project.id != project_id:
            raise ValueError(f"Another project with the name '{new_name}' already exists.")

        updated_project = self._storage.update_project(project_id, new_name, new_description)
    
        if updated_project is None:
            raise ValueError(f"Project with ID {project_id} not found.")

        return updated_project

class TaskService:
    """Handles the business logic for tasks."""
    def __init__(self, storage: InMemoryStorage, max_tasks: int):
        self._storage = storage
        self._max_tasks = max_tasks

    def add_task_to_project(self, project_id: ProjectId, title: str, description: str, deadline_str: str | None) -> Task:
        """Adds a new task to a specific project after validation."""
        # Check task limit for the given project
        if len(self._storage.get_tasks_by_project(project_id)) >= self._max_tasks:
            raise ValueError(f"Cannot add new task. Maximum limit of {self._max_tasks} tasks per project reached.")

        if len(title) > 30:
            raise ValueError("Task title cannot exceed 30 characters.")
        if len(description) > 150:
            raise ValueError("Task description cannot exceed 150 characters.")

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid deadline format. Please use YYYY-MM-DD.")

        return self._storage.create_task(project_id, title, description, deadline)

    def get_project_tasks(self, project_id: ProjectId) -> list[Task]:
        return self._storage.get_tasks_by_project(project_id)

    def delete_task(self, task_id: TaskId) -> None:
        """Deletes a task."""
        if not self._storage.delete_task(task_id):
            raise ValueError(f"Task with ID {task_id} not found.")

    def edit_task(self, task_id: TaskId, new_title: str, new_description: str, new_deadline_str: str | None) -> Task:
        """Edits an existing task after validation."""
        if len(new_title) > 30:
            raise ValueError("Task title cannot exceed 30 characters.")
        if len(new_description) > 150: # Added validation
            raise ValueError("Task description cannot exceed 150 characters.")

        new_deadline = None
        if new_deadline_str:
            try:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid deadline format. Please use YYYY-MM-DD.")
        
        updated_task = self._storage.update_task(task_id, new_title, new_description, new_deadline)
        
        if updated_task is None:
            raise ValueError(f"Task with ID {task_id} not found.")
            
        return updated_task

    def change_task_status(self, task_id: TaskId, new_status: str) -> Task:
        """Changes the status of a task after validation."""
        if new_status not in get_args(Status):
            raise ValueError(f"Invalid status '{new_status}'. Must be one of {get_args(Status)}.")
        
        updated_task = self._storage.update_task_status(task_id, new_status) # type: ignore
        
        if updated_task is None:
            raise ValueError(f"Task with ID {task_id} not found.")
            
        return updated_task