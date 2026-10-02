from fastapi import FastAPI
from app.database import Base, engine
from app.models.patient import Patient
from .routers import patients

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(patients.router)

@app.get("/")
def welcome():
    return {
        "message": "Welcome to Patient Mangagement System!!"
    }




