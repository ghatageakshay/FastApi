from fastapi import FastAPI
from pydantic import BaseModel , Field , field_validator , EmailStr , model_validator , computed_field
from typing import List,Dict , Optional , Annotated 

class Name(BaseModel):
    first_name:str
    middle_name:str
    last_name:str

    @model_validator(mode="after")
    def name_transform(cls , model):
        return model.first_name.upper() , model.middle_name.upper() , model.last_name.upper()

class patient_data(BaseModel ):
    age:int
    name:Name
    email: EmailStr
    weight:float = Field(gt=50)
    height:float
    allergies:Optional[List[str]] = None
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validate(cls , value):
        domains = ["hdfc.com" , "icici,com" , "sbi.com"]
        value_domain = value.split("@")[-1]
        if value_domain not in domains:
            raise ValueError('Enter valid email')

        else:
            return value

   

    @model_validator(mode="after")
    def validate_emergency_contact(cls , model):
        if len(model.allergies) > 3 and "emergency_contact" not in model.contact_details:
            raise ValueError("You have more than 3 allergies please kindly add your emergency contact!!")

        else:
            return model

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2) , 2)
        return bmi

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

def patient(patient:patient_data):
    print(patient.age)
    print(patient.name)
    print(patient.contact_details)
    print(patient.allergies)
    print("BMI" ,patient.bmi)
    print("Inserted")
    print(patient.name[0])


name_dict = {"first_name" : "Akshay" , "middle_name":"Praveen" , "last_name":"Ghatage"}

n1 = Name(**name_dict)

patient_dict = {"age":12 , "name":n1 ,"email":"akshay@hdfc.com", "weight":52.5 ,"height":1.77, "allergies": ["pollen" , "dust" , "height" , "fire"] , "contact_details":{"email":"ghatageakshay96@gmail.com" , "phn no":"9156940632" , "emergency_contact":"9673134582"}}
p1 = patient_data(**patient_dict)
patient(p1)