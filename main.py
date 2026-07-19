from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
app = FastAPI()
tasks = [
    {"id": 1, "title": "Study FastAPI", "done": False},
    {"id": 2, "title": "Buy groceries", "done": True},
    {"id": 3, "title": "Go to the gym", "done": False},
]
@app.get("/") #If someone sends a GET request to the path /, execute the function below. (get creates data)
def root():
    return {
    "name": "Task API",
    "version": "1.0",
    "endpoints": ["/tasks"]
}
@app.get("/health") #When someone requests /health (give me health), FastAPI runs the health() function and returns the status.
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks: #For each task in the tasks list... (search the task)
        if task["id"] == id:
            return task
    return JSONResponse(
    status_code=404,
    content={"error": f"Task {id} not found"}
)

@app.post("/tasks", status_code=status.HTTP_201_CREATED) #When someone sends a POST(create) request to /tasks, take the JSON from the request body, store it in the variable task, and run the create_task function. return HTTP status 201 (Created)
def create_task(task=Body()):
    title = task.get("title")

    if title is None or title == "":
        return JSONResponse(
        status_code=400,
        content={"error": "Title cannot be empty"}
    )

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}") ##When someone sends a PUT (update) request to /tasks/{id}, take the id from the URL, take the JSON from the request body, store it in the variable task, run the update_task function.
def update_task(id: int, task=Body()):

    if task == {}:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    for existing_task in tasks:
        if existing_task["id"] == id:

            if "title" in task:
                existing_task["title"] = task["title"]

            if "done" in task:
                existing_task["done"] = task["done"]

            return existing_task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT) ##When someone sends a DELETE request to /tasks/{id}, find the task with that id, run the delete_task function, and return HTTP status 204 (No Content) if successful.
def delete_task(id: int):
     for existing_task in tasks:
        if existing_task["id"] == id:
            tasks.remove(existing_task)
            return
     return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )