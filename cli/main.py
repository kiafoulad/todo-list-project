# cli/main.py
from core.services import ProjectService, TaskService
from storage.in_memory import InMemoryStorage
from core.models import ProjectId

def print_projects(projects: list):
    if not projects:
        print("No projects found.")
        return
    
    print("Projects List:")
    for p in projects:
        print(f"  ID: {p.id}, Name: {p.name}, Description: {p.description}")

def print_tasks(tasks: list):
    if not tasks:
        print("This project has no tasks.")
        return
        
    print("Tasks List:")
    for t in tasks:
        print(f"  ID: {t.id}, Title: {t.title}, Status: {t.status}")


def main():
    # Initialize the application layers.
    storage = InMemoryStorage()
    project_service = ProjectService(storage)
    task_service = TaskService(storage)

    print("Welcome to the ToDoList App!")

    while True:
        print("\n" + "="*20)
        print("1. Create a new project")
        print("2. List all projects")
        print("3. Add a task to a project")
        print("4. List tasks of a project")
        print("5. Delete a project")
        print("6. Exit")
        print("="*20)
        
        choice = input("Please select an option: ")

        if choice == "1":
            name = input("Enter project name: ")
            desc = input("Enter project description: ")
            try:
                project = project_service.create_project(name, desc)
                print(f"Project '{project.name}' created successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            projects = project_service.get_all_projects()
            print_projects(projects)

        elif choice == "3":
            try:
                project_id = ProjectId(int(input("Enter the project ID: ")))
                title = input("Enter task title: ")
                desc = input("Enter task description: ")
                task = task_service.add_task_to_project(project_id, title, desc)
                print(f"Task '{task.title}' added successfully.")
            except (ValueError, KeyError):
                print("Error: Invalid input or project not found.")

        elif choice == "4":
            try:
                project_id = ProjectId(int(input("Enter the project ID: ")))
                tasks = task_service.get_project_tasks(project_id)
                print_tasks(tasks)
            except ValueError:
                print("Error: Project ID must be a number.")
        
        elif choice == "5":
            try:
                project_id = ProjectId(int(input("Enter the ID of the project to delete: ")))
                project_service.delete_project(project_id)
                print(f"Project with ID {project_id} and all its tasks have been deleted.")
            except ValueError:
                print("Error: Project ID must be a number.")

        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()