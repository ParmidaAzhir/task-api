from fastapi import FastAPI
app = FastAPI()
@app.get("/") #If someone sends a GET request to the path /, execute the function below.
def root():
    return {"message": "Hello World"}