from fastapi import FastAPI , HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , field_validator , EmailStr , model_validator , computed_field 
from typing import List,Dict , Optional , Annotated
import json 

class Name(BaseModel):
    first_name:str
    middle_name:str
    last_name:str

class patient_data(BaseModel ):
    id:Annotated[str,Field(... , description="Patient Id" , examples=("P001","P002"))]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    name:Annotated[Name,Field(...,description="Name of the patient")]
    email: Annotated[EmailStr,Field(description="Email Of patient")]
    weight:Annotated[float, Field(gt=0)]
    height:Annotated[float,Field(gt=0,description="Height Of patient in meters")]
    contact_details:Annotated[Dict[str,str],Field(description="Contact Details of patient")]

    @field_validator('email')
    @classmethod
    def email_validate(cls , value):
        domains = ["hdfc.com" , "icici,com" , "sbi.com","gmail.com"]
        value_domain = value.split("@")[-1]
        if value_domain not in domains:
            raise ValueError('Enter valid email')

        else:
            return value

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2) , 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if  self.bmi < 18.5:
            verdict = "Underweight"

        elif 18.5> self.bmi < 24.9:
            verdict = "Healthy"

        else:
            verdict = "Overweight"

        return verdict

    @computed_field
    @property
    def age_category(self) -> str:
        if self.age < 10:
            return "kid"

        elif self.age < 20:
            return "teenager"

        elif self.age < 50:
            return "adult"

        else:
            return "aged"

class Search_data(BaseModel):
    name:Annotated[str , Field(...,description="Enter the name to search for...")]

app = FastAPI()

def load_data():
    with open("patients_data.json" , "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients_data.json" , "w") as f:
        json.dump(data , f)


@app.post("/create")
def create(patient:patient_data):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400 ,detail="Patient ALready Exists!!")

    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)

    return JSONResponse(status_code=200 , content={"messagae":"patient added successfully!"})
    
@app.post("/search_patient")
def search_patient(search:Search_data):
    data = load_data()

    for patient_id , patient in data.items():
        if patient["name"]["first_name"].lower() == search.name.lower():
            return{
                "id":patient_id,
                "patient":patient
            }
  
    raise HTTPException(status_code=400 , detail = "patient not found!")
       

    
