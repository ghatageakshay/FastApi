from fastapi import FastAPI
from .routers import patients

app = FastAPI()

app.include_router(patients.router)

@app.get("/")
def welcome():
    return{
        "message":"Welcome to Patient Mangagement System!!"
    }

