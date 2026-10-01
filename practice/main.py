from fastapi import FastAPI
from pydantic import BaseModel

class student(BaseModel):
    name:str
    age:int

app = FastAPI()

@app.get("/hello")
def get_student():
    return {
        "message":"welcome guys!!"
    }

@app.get("/students/{student_id}")
def get_student_by_id(student_id:int):
    return {
        "student_id":student_id  
    }

@app.post("/student")
def create_student(data:student):
    return {
        "student added successfully!!"
    }