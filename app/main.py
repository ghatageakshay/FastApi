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

        elif self.bmi >= 18.5 and self.bmi <= 24.9:
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

class patient_update(BaseModel ):
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=120)]
    name:Annotated[Optional[Name],Field(default=None)]
    email: Annotated[Optional[EmailStr],Field(default=None)]
    weight:Annotated[Optional[float], Field(default=None, gt=0)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    contact_details:Annotated[Optional[Dict[str,str]],Field(default=None)]

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
       
@app.get("/view_patients")
def view_patients():
    with open("patients_data.json","r") as f:
        data = json.load(f)

    return data

@app.put("/update_patient/{patient_id}")
def update_patient(patient_id:str,update_patient:patient_update):
    data = load_data()
    #check if patient exist or not
    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="User not found!")

    existing_patient_info = data[patient_id]
    #covert update object to dict
    update_patient = update_patient.model_dump(exclude_unset=True)

    #iterate in update dict to replace the updated value in existing dict
    for key , values in update_patient.items():
        existing_patient_info[key] = values

    #add id field to existing dict
    existing_patient_info["id"] = patient_id
    patient_pydantic_object = patient_data(**existing_patient_info)

    #covert pydantic object back to dict excluding id we did to calculate those computed fields with updated values
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')

    #assign the  updated values to patient
    data[patient_id] = existing_patient_info 

    save_data(data) 

    return JSONResponse(status_code=200 , content={"message":"patient updated successfully!!"})  

@app.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id : str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient Not found!!")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200 , content={"message":"patient deleted!"})