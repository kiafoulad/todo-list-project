# storage/in_memory.py
from core.models import Project, Task, ProjectId, TaskId

class InMemoryStorage:
    """In-memory storage for projects and tasks. Acts as a mock database."""
    _projects: dict[ProjectId, Project]
    _tasks: dict[TaskId, Task]
    _next_project_id: int
    _next_task_id: int

    def __init__(self) -> None:
        self._projects = {}
        self._tasks = {}
        self._next_project_id = 1
        self._next_task_id = 1

    def create_project(self, name: str, description: str) -> Project:
        project_id = ProjectId(self._next_project_id)
        project = Project(id=project_id, name=name, description=description)
        self._projects[project_id] = project
        self._next_project_id += 1
        return project

    def get_all_projects(self) -> list[Project]:
        return sorted(self._projects.values(), key=lambda p: p.created_at)
    
    def find_project_by_name(self, name: str) -> Project | None:
        for project in self._projects.values():
            if project.name == name:
                return project
        return None

    def delete_project(self, project_id: ProjectId) -> None:
        # Cascade Delete: Remove all tasks associated with the project.
        tasks_to_delete = [
            task_id for task_id, task in self._tasks.items() 
            if task.project_id == project_id
        ]
        for task_id in tasks_to_delete:
            del self._tasks[task_id]
        
        if project_id in self._projects:
            del self._projects[project_id]
    
    def create_task(self, project_id: ProjectId, title: str, description: str) -> Task:
        task_id = TaskId(self._next_task_id)
        task = Task(id=task_id, project_id=project_id, title=title, description=description)
        self._tasks[task_id] = task
        self._next_task_id += 1
        return task

    def get_tasks_by_project(self, project_id: ProjectId) -> list[Task]:
        tasks = [
            task for task in self._tasks.values() 
            if task.project_id == project_id
        ]
        return sorted(tasks, key=lambda t: t.created_at)
    
    def delete_task(self, task_id: TaskId) -> bool:
        """Deletes a task by its ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True  # Return True on successful deletion
        return False  # Return False if task was not found
    
    