# ToDoList CLI Application

A simple, command-line ToDoList application built with Python and Object-Oriented Programming (OOP) principles.

## Features ✨

This application allows users to manage their tasks and projects through a command-line interface. The main features include:

-   **Project Management:**
    -   [cite_start]Create new projects[cite: 52, 53].
    -   [cite_start]Edit existing projects[cite: 61, 62].
    -   [cite_start]Delete projects (with cascade deletion of all associated tasks)[cite: 70, 73].
    -   [cite_start]List all created projects[cite: 111].
-   **Task Management:**
    -   [cite_start]Add tasks to a specific project[cite: 78].
    -   [cite_start]Delete a task from a project[cite: 105].
    -   [cite_start]Edit an existing task[cite: 97].
    -   [cite_start]List all tasks within a specific project[cite: 121].

## Tech Stack & Tools 🛠️

-   **Language:** Python
-   [cite_start]**Core Principles:** Object-Oriented Programming (OOP) [cite: 9]
-   [cite_start]**Dependency Management:** Poetry [cite: 188]
-   [cite_start]**Version Control:** Git & GitHub [cite: 167, 168]

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