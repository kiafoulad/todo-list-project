# cli/main.py

# --- IMPORT STATEMENTS ---
# We need to import all the classes and types we use from other files.
from core.services import ProjectService, TaskService
from storage.in_memory import InMemoryStorage
from core.models import ProjectId, TaskId  # This import was missing for the IDs

# --- HELPER FUNCTIONS ---
def print_projects(projects: list):
    """Prints a formatted list of projects."""
    if not projects:
        print("No projects found.")
        return
    
    print("Projects List:")
    for p in projects:
        print(f"  ID: {p.id}, Name: {p.name}, Description: {p.description}")


def print_tasks(tasks: list):
    """Prints a formatted list of tasks."""
    if not tasks:
        print("This project has no tasks.")
        return
        
    print("Tasks List:")
    for t in tasks:
        # Format deadline nicely if it exists
        deadline_str = t.deadline.strftime('%Y-%m-%d') if t.deadline else "No deadline"
        print(f"  ID: {t.id}, Title: {t.title}, Status: {t.status}, Deadline: {deadline_str}")

# --- MAIN APPLICATION LOGIC ---
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
        print("6. Edit a project")
        print("7. Delete a task")
        print("8. Edit a task")
        print("9. Change task status")
        print("10. Exit")
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
        elif choice == "3": # Add a task
            try:
                project_id = ProjectId(int(input("Enter the project ID: ")))
                title = input("Enter task title: ")
                desc = input("Enter task description: ")
                deadline_str = input("Enter deadline (YYYY-MM-DD) or leave empty: ")
                # Pass the deadline string to the service layer
                task = task_service.add_task_to_project(project_id, title, desc, deadline_str or None)
                print(f"Task '{task.title}' added successfully.")
            except (ValueError, KeyError) as e:
                print(f"Error: {e}")
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
            try:
                project_id = ProjectId(int(input("Enter the ID of the project to edit: ")))
                new_name = input("Enter the new project name: ")
                new_desc = input("Enter the new project description: ")
                updated_project = project_service.edit_project(project_id, new_name, new_desc)
                print(f"Project '{updated_project.name}' updated successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "7":
            try:
                task_id = TaskId(int(input("Enter the ID of the task to delete: ")))
                task_service.delete_task(task_id)
                print(f"Task with ID {task_id} deleted successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "8": # Edit a task
            try:
                task_id = TaskId(int(input("Enter the ID of the task to edit: ")))
                new_title = input("Enter the new task title: ")
                new_desc = input("Enter the new task description: ")
                new_deadline_str = input("Enter new deadline (YYYY-MM-DD) or leave empty: ")
                # Pass the new deadline string to the service layer
                updated_task = task_service.edit_task(task_id, new_title, new_desc, new_deadline_str or None)
                print(f"Task '{updated_task.title}' updated successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "9":
            try:
                task_id = TaskId(int(input("Enter the task ID: ")))
                new_status = input("Enter the new status (todo, doing, done): ")
                updated_task = task_service.change_task_status(task_id, new_status)
                print(f"Status of task '{updated_task.title}' changed to '{updated_task.status}'.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()