from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()
tasks = [
    {"id": 1, "title": "Study FastAPI", "done": False},
    {"id": 2, "title": "Buy groceries", "done": True},
    {"id": 3, "title": "Go to the gym", "done": False},
]
@app.get("/") #If someone sends a GET request to the path /, execute the function below.
def root():
    return {
    "name": "Task API",
    "version": "1.0",
    "endpoints": ["/tasks"]
}
@app.get("/health") #When someone requests /health, FastAPI runs the health() function and returns the status.
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