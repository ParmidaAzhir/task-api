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


# AI vs Me

## Prompt

```text
Build a REST API using Python and FastAPI.

Store all data in memory using a Python list. Do not use a database, ORM, SQLAlchemy, or Pydantic models.

Each task should have:
- id (integer)
- title (string)
- done (boolean)

Initialize the API with these three tasks:

[
  {"id": 1, "title": "Study FastAPI", "done": false},
  {"id": 2, "title": "Buy groceries", "done": true},
  {"id": 3, "title": "Go to the gym", "done": false}
]

Implement the following endpoints:

GET /
- Return:
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks"]
}

GET /health
- Return:
{
  "status": "ok"
}

GET /tasks
- Return all tasks.
- Support these optional query parameters:
  - done (boolean): filter tasks by completion status.
  - search (string): perform a case-insensitive search on the task title.
- If both query parameters are provided, apply both filters.

GET /tasks/{id}
- Return the task with the given ID.
- If the task does not exist, return HTTP 404 with:
{
  "error": "Task {id} not found"
}

POST /tasks
- Accept a JSON body containing:
{
  "title": "..."
}
- If the title is missing or empty, return HTTP 400 with:
{
  "error": "Title cannot be empty"
}
- Create a new task with:
  - id = len(tasks) + 1
  - title from the request
  - done = false
- Return HTTP 201 Created.

PUT /tasks/{id}
- Accept a JSON body.
- Allow updating:
  - title
  - done
- If the body is empty, return HTTP 400:
{
  "error": "Request body cannot be empty"
}
- If the task does not exist, return HTTP 404.

DELETE /tasks/{id}
- Delete the task.
- Return HTTP 204 No Content.
- If the task is not found, return HTTP 404.

GET /stats
- Return:
{
  "total": number of tasks,
  "done": number of completed tasks,
  "open": number of incomplete tasks
}

POST /reset
- Restore the original three example tasks.
- Return a success message together with the restored task list.

Additional requirements:
- Use FastAPI's automatic Swagger UI.
- Use proper HTTP status codes (200, 201, 204, 400, 404).
- Use JSONResponse for custom error responses.
- Keep the implementation in a single file named main.py.
- Do not add authentication, databases, Docker, or any extra features that were not requested.
- Write clean, readable code with comments explaining the important parts.
```

---

## What the AI Did Better

- Created a reusable `find_task()` helper function instead of repeating the same search loop in multiple endpoints.
- Stored the original tasks in a separate `DEFAULT_TASKS` list, making the reset endpoint cleaner and safer.
- Organized the code with section headings, docstrings, and clearer function names.
- Converted the search text to lowercase once before filtering.

---

## What the AI Got Wrong

- Returned a `JSONResponse` for HTTP 204, even though a 204 response should not contain a body.
- Used raw `Request` objects for POST and PUT, which made the request-body format less clear in Swagger.
- Accepted unknown fields and invalid values in PUT requests without extra validation.

---

## What My Prompt Forgot to Specify

- Whether PUT should reject unknown fields.
- Whether an empty title should also be rejected during updates.
- Whether `done` must strictly be a boolean.
- That a successful DELETE response must contain no body.
- Whether the endpoint functions should be synchronous or asynchronous.

---

## Rematch

I improved my prompt by adding stricter validation rules for PUT requests and by specifying that DELETE must return a completely empty HTTP 204 response. The second version matched the intended behavior more closely.

I improved the prompt by adding strict validation requirements for PUT and by specifying that DELETE must return a completely empty 204 response. The regenerated version handled invalid updates more carefully and returned the correct empty DELETE response.

