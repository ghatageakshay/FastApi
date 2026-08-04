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

@app.get("/students/{student_id}")
def students(student_id : int , subject_name:str="All"):
    return{
        "student":student_id,
        "subject":subject_name
    }

@app.get("/products/{product_id}")
def products(product_id:int):
    return{
        "product_id":product_id,
        "status":"Avilable"
    }

@app.get("/users/{username}")
def users(username:str):
    return{
        "username":{username}
    }

#Query Parameter
@app.get("/search")
def serach(keyword:str):
    return{
        "KeyWord":keyword
    }

@app.get("/get_products")
def get_products(category:str,price:int):
    return{
        "category":category,
        "price":price
    }

@app.get("/branch")
def get_branch(branch:str="All"):
    return{
        "branch":branch
    }