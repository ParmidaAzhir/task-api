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


## AI vs Me

### Prompt

"""
Task API
--------
A simple REST API built with FastAPI that stores tasks in memory using
a plain Python list (no database, no ORM, no Pydantic models).

Run with:
    uvicorn main:app --reload

Then open the automatic Swagger UI at:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API", version="1.0")


# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

# The "original" tasks, kept separate so /reset can restore them without
# being affected by later mutations of `tasks`.
DEFAULT_TASKS = [
    {"id": 1, "title": "Study FastAPI", "done": False},
    {"id": 2, "title": "Buy groceries", "done": True},
    {"id": 3, "title": "Go to the gym", "done": False},
]

# The live list of tasks. We copy the default tasks (as new dicts) so that
# mutating `tasks` never mutates DEFAULT_TASKS.
tasks = [task.copy() for task in DEFAULT_TASKS]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def find_task(task_id: int):
    """Return the task dict with the given id, or None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# ---------------------------------------------------------------------------
# Root & health endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    """Basic info about the API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Task endpoints
# ---------------------------------------------------------------------------

@app.get("/tasks")
def get_tasks(done: bool | None = None, search: str | None = None):
    """
    Return all tasks, optionally filtered by:
    - done: exact match on completion status
    - search: case-insensitive substring match on the title
    Both filters can be combined.
    """
    result = tasks

    if done is not None:
        result = [task for task in result if task["done"] == done]

    if search is not None:
        search_lower = search.lower()
        result = [task for task in result if search_lower in task["title"].lower()]

    return result


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return a single task by id, or a 404 error if it doesn't exist."""
    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )
    return task


@app.post("/tasks")
async def create_task(request: Request):
    """
    Create a new task from a raw JSON body: {"title": "..."}.
    No Pydantic model is used, so the body is parsed and validated manually.
    """
    try:
        body = await request.json()
    except Exception:
        body = None

    # Extract and validate the title
    title = None
    if isinstance(body, dict):
        title = body.get("title")

    if not title or not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"},
        )

    # Create the new task. id is simply len(tasks) + 1 as specified.
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
    }
    tasks.append(new_task)

    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    """
    Update an existing task's title and/or done status from a raw JSON body.
    """
    try:
        body = await request.json()
    except Exception:
        body = None

    # An empty body (or non-dict / dict with no keys) is rejected.
    if not body or not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"},
        )

    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    # Only update fields that were actually provided.
    if "title" in body:
        task["title"] = body["title"]
    if "done" in body:
        task["done"] = body["done"]

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by id. Returns 204 on success, 404 if not found."""
    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    tasks.remove(task)
    return JSONResponse(status_code=204, content=None)


# ---------------------------------------------------------------------------
# Stats endpoint
# ---------------------------------------------------------------------------

@app.get("/stats")
def get_stats():
    """Return counts of total, done, and open tasks."""
    total = len(tasks)
    done_count = sum(1 for task in tasks if task["done"])
    open_count = total - done_count

    return {
        "total": total,
        "done": done_count,
        "open": open_count,
    }


# ---------------------------------------------------------------------------
# Reset endpoint
# ---------------------------------------------------------------------------

@app.post("/reset")
def reset_tasks():
    """Restore the original three example tasks."""
    global tasks
    tasks = [task.copy() for task in DEFAULT_TASKS]

    return {
        "message": "Tasks have been reset to the default list",
        "tasks": tasks,
    }

### What the AI did better

The AI reduced repeated code by creating a reusable `find_task()` helper function. It also kept the original tasks in a separate `DEFAULT_TASKS` list, making the reset logic cleaner and safer. Its code was more organized through section headings, docstrings, and clearer names.

### What the AI got wrong or ignored

The DELETE endpoint returned a `JSONResponse` with `content=None` while using status code 204. A 204 response should contain no body, so returning an empty response would be more correct. The AI also used raw `Request` objects for POST and PUT, which made the expected JSON body less clearly documented in Swagger. In addition, PUT accepted unknown fields and invalid values without validation.

### What my prompt forgot to specify

My prompt did not specify whether PUT should reject unknown fields, empty titles, or non-boolean `done` values. It also did not clearly state that a successful DELETE response must contain no body. The AI therefore made these decisions itself.

### Rematch

I improved the prompt by adding strict validation requirements for PUT and by specifying that DELETE must return a completely empty 204 response. The regenerated version handled invalid updates more carefully and returned the correct empty DELETE response.

