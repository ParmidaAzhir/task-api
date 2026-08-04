# Task API

A REST API built with **FastAPI** and **SQLite** for managing tasks.

This project demonstrates the fundamental CRUD (Create, Read, Update, Delete) operations while introducing persistent data storage using SQLite. The API also provides automatically generated interactive documentation using Swagger UI.

---

# Features

- Create a new task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task
- Filter tasks by completion status
- Search tasks by title
- Store tasks permanently using SQLite
- Interactive Swagger UI documentation

---

# Technologies

- Python
- FastAPI
- Uvicorn
- SQLite
- Python `sqlite3`

---

# Database

This project uses **SQLite** because it is:

- Lightweight
- Requires no separate database server
- Stores data in a single file
- Keeps data after the server restarts

Database file:

```text
tasks.db
```

The application automatically:

- Creates `tasks.db` if it does not exist
- Creates the `tasks` table if it does not exist
- Inserts the three example tasks when the table is empty

Because `tasks.db` is ignored by Git, every new clone automatically creates a fresh database the first time the project is run.

SQLite stores Boolean values as:

| Value | Meaning |
|------|---------|
| 0 | False |
| 1 | True |

---

# Installation

Clone the repository:

```bash
git clone https://github.com/ParmidaAzhir/task-api.git
```

Go into the project folder:

```bash
cd task-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it (Windows):

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install fastapi uvicorn
```

Run the project:

```bash
uvicorn main:app --reload
```

The database is created automatically the first time the application starts.

---

# API URLs

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Get API information |
| GET | `/health` | Check API health |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks?done=true` | Filter completed tasks |
| GET | `/tasks?search=text` | Search tasks by title |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

---

# Example Request

Create a task:

```http
POST /tasks
```

Request body:

```json
{
  "title": "Study FastAPI"
}
```

Response:

```json
{
  "id": 4,
  "title": "Study FastAPI",
  "done": false
}
```

Status code:

```text
201 Created
```

---

# Example SQL Query

Return all completed tasks:

```sql
SELECT * FROM tasks WHERE done = 1;
```

This query was executed manually using **DB Browser for SQLite**.

---

# Database Screenshot

The database was explored using **DB Browser for SQLite**.


![SQLite Database](images/database-screenshot.png)

---

# Swagger UI

FastAPI automatically generates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Every endpoint can be tested directly from the browser using the **Try it out** button.

Save a screenshot of your Swagger page as:

```text
images/swagger.png
```

Then replace the line below with your actual image:

```markdown
![Swagger UI](images/swagger.png)
```

---

# Project Structure

```text
task-api/
│
├── main.py
├── README.md
├── .gitignore
├── tasks.db
└── images/
    ├── database-screenshot.png
    └── swagger.png
```

---

# Assignment Progress

## Assignment 1

- Built a REST API using FastAPI
- Implemented CRUD operations
- Added filtering and search
- Added Swagger UI documentation

## Week 3

- Replaced the in-memory task list with SQLite
- Created the database automatically
- Created the table automatically
- Inserted example tasks only on the first run
- Replaced CRUD operations with SQL queries
- Executed SQL queries manually using DB Browser for SQLite

---

# Author

**Parmida Azhir**
