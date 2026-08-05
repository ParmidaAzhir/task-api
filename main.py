from fastapi import FastAPI, Body, status, Response
from fastapi.responses import JSONResponse
from repository import (
    initialize_database,
    get_all_tasks,
    get_task_by_id,
    create_task as create_task_in_db,
    update_task_by_id,
    delete_task_by_id,
)

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
    return get_all_tasks(done=done, search=search)

@app.get("/tasks/{id}", summary="Get a task by ID")
def get_task(id: int):
    task = get_task_by_id(id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return task

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

    return create_task_in_db(title)

@app.put("/tasks/{id}", summary="Update a task")
def update_task(id: int, task=Body()):

    if task == {}:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    existing_task = get_task_by_id(id)

    if existing_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    title = existing_task["title"]
    done = existing_task["done"]

    if "title" in task:
        if task["title"] is None or task["title"] == "":
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        title = task["title"]

    if "done" in task:
        done = task["done"]

    return update_task_by_id(id, title, done)

@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
def delete_task(id: int):
    deleted = delete_task_by_id(id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


