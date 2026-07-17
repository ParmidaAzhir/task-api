from fastapi import FastAPI
app = FastAPI()
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