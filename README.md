# ToDoList CLI Application

A simple, command-line ToDoList application built with Python and Object-Oriented Programming (OOP) principles.

## Features ✨

This application allows users to manage their tasks and projects through a command-line interface. The main features include:

-   **Project Management:**
    -   Create new projects.
    -   Edit existing projects.
    -   [cite_start]Delete projects (with cascade deletion of all associated tasks)[cite: 398].
    -   List all created projects.
-   **Task Management:**
    -   Add tasks to a specific project.
    -   Delete a task from a project.
    -   Edit an existing task.
    -   [cite_start]Change a task's status (`todo`, `doing`, `done`)[cite: 411, 416].
    -   List all tasks within a specific project.

## Tech Stack & Tools 🛠️

-   **Language:** Python
-   **Core Principles:** Object-Oriented Programming (OOP)
-   [cite_start]**Dependency Management:** Poetry [cite: 513]
-   [cite_start]**Version Control:** Git & GitHub [cite: 492, 493]

## Setup and Installation ⚙️

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/kiafoulad/todo-list-project.git](https://github.com/kiafoulad/todo-list-project.git)
    cd todo-list-project
    ```

2.  **Install dependencies using Poetry:**
    (Ensure you have Poetry installed first)
    ```bash
    poetry install
    ```

## How to Run the Application ▶️

To run the application, use the following command from the project's root directory:

```bash
poetry run python -m cli.main
### 3. Save and Push the Changes
Now, let's commit this new `README.md` and push it to GitHub.

**Run these commands in PowerShell:**
```powershell
git add README.md
git commit -m "docs: create and populate README.md file"
git push -u origin docs/update-readme
