# Task API

A simple REST API built with FastAPI for managing tasks. It supports creating, reading, updating, and deleting tasks (CRUD) and includes automatically generated Swagger UI documentation.

---

## Features

- Create a new task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task
- Interactive API documentation with Swagger UI

---

## Technologies

- Python
- FastAPI
- Uvicorn

---

## Installation

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

Activate the virtual environment (Windows):

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install fastapi uvicorn
```

Run the API:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Get API information |
| GET | /health | Check if the API is running |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get a task by ID |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

---

## Example Request

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

---

## Swagger UI

FastAPI automatically generates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Tasks are stored only in memory, so any new tasks or changes disappear when the server restarts. A database is needed to keep data permanently.
You can test every endpoint directly from your browser using the **Try it out** button.
<img width="884" height="548" alt="image" src="https://github.com/user-attachments/assets/29284eca-3a31-47d6-8021-22745c76c23a" />


