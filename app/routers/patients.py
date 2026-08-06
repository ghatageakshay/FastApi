from fastapi import APIRouter,HTTPException
import json
from fastapi.responses import JSONResponse
from app.schemas.patient_models import patient_data,Name,patient_update,Search_data

router = APIRouter()

def load_data():
    with open("patients_data.json" , "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients_data.json" , "w") as f:
        json.dump(data , f)


@router.post("/create")
def create(patient:patient_data):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400 ,detail="Patient ALready Exists!!")

    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)

    return JSONResponse(status_code=200 , content={"messagae":"patient added successfully!"})
    
@router.post("/search_patient")
def search_patient(search:Search_data):
    data = load_data()

    for patient_id , patient in data.items():
        if patient["name"]["first_name"].lower() == search.name.lower():
            return{
                "id":patient_id,
                "patient":patient
            }
  
    raise HTTPException(status_code=400 , detail = "patient not found!")
       
@router.get("/view_patients")
def view_patients():
    with open("patients_data.json","r") as f:
        data = json.load(f)

    return data

@router.put("/update_patient/{patient_id}")
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

@router.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id : str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient Not found!!")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200 , content={"message":"patient deleted!"})