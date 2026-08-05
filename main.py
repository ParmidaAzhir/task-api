from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
import sqlite3
from repository import initialize_database

initialize_database()

app = FastAPI()

@app.get("/", summary="Get API information") #If someone sends a GET(get reads data) request to the path /, execute the function below. 
def root():
    return {
    "name": "Task API",
    "version": "1.0",
    "endpoints": ["/tasks"]
}
@app.get("/health", summary="Check API health") #When someone requests /health (give me health), FastAPI runs the health() function and returns the status.
def health():
    return {"status": "ok"}

@app.get("/tasks", summary="Get all tasks")
def get_tasks(
    done: bool | None = None,
    search: str | None = None
):
    db = sqlite3.connect("tasks.db")
    cursor = db.cursor()

    query = "SELECT * FROM tasks"
    conditions = []
    values = []

    if done is not None:
        conditions.append("done = ?")
        values.append(done)

    if search is not None:
        conditions.append("title LIKE ?")
        values.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, values)
    rows = cursor.fetchall()
    db.close()

    return [
        {"id": row[0], "title": row[1], "done": bool(row[2])}
        for row in rows
    ]

@app.get("/tasks/{id}", summary="Get a task by ID")
def get_task(id: int):
    db = sqlite3.connect("tasks.db")
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()
    db.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(task=Body()):
    title = task.get("title")

    if title is None or title == "":
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    db = sqlite3.connect("tasks.db")
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, False)
    )

    new_id = cursor.lastrowid
    db.commit()
    db.close()

    return {
        "id": new_id,
        "title": title,
        "done": False
    }

@app.put("/tasks/{id}", summary="Update a task")
def update_task(id: int, task=Body()):

    if task == {}:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    db = sqlite3.connect("tasks.db")
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )
    row = cursor.fetchone()

    if row is None:
        db.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    title = row[1]
    done = bool(row[2])

    if "title" in task:
        if task["title"] is None or task["title"] == "":
            db.close()
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        title = task["title"]

    if "done" in task:
        done = task["done"]

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (title, done, id)
    )

    db.commit()
    db.close()

    return {
        "id": id,
        "title": title,
        "done": done
    }

@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
def delete_task(id: int):

    db = sqlite3.connect("tasks.db")
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    if cursor.fetchone() is None:
        db.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    db.commit()
    db.close()

@app.get("/stats", summary="Get task statistics")
def get_stats():
    total = len(tasks)
    done = 0

    for task in tasks:
        if task["done"]:
            done += 1
    
    open_tasks = total - done

    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }

@app.post("/reset", summary="Reset tasks")
def reset_tasks():

    tasks.clear()

    tasks.extend([
        {"id": 1, "title": "Study FastAPI", "done": False},
        {"id": 2, "title": "Buy groceries", "done": True},
        {"id": 3, "title": "Go to the gym", "done": False},
    ])

    return {
        "message": "Tasks reset successfully",
        "tasks": tasks
    }