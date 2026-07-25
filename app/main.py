from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"Welcome To my FastApi Course"}

@app.get("/about")
def about():
    return{"name":"Akshay",
           "Role":"Python Backend Developer"
           }

@app.get("/health")
def health():
    return{"status":"okay!!"}

