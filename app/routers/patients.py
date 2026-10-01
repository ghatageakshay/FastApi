from fastapi import APIRouter,HTTPException,Depends
import json
from fastapi.responses import JSONResponse
from app.schemas.patient_models import patient_data,Name,patient_update,Search_data
from app.schemas.patient_response import PatientResponse
from app.database import SessionLocal,get_db
from app.models.patient import Patient
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter()

def load_data():
    with open("patients_data.json" , "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients_data.json" , "w") as f:
        json.dump(data , f)


@router.post("/create",summary="Creates A new Patient!!")
def create(patient:patient_data,db:Session = Depends(get_db)):
    

    db_patient = Patient(
        first_name = patient.name.first_name,
        middle_name = patient.name.middle_name,
        last_name = patient.name.last_name,
        age = patient.age,
        email = patient.email,
        weight = patient.weight,
        height = patient.height
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient
@router.post("/search_patient",response_model=list[PatientResponse])
def search_patient(name:str,db:Session = Depends(get_db)):
    stmt = select(Patient).where(Patient.first_name == name)

    result = db.execute(stmt)
    patient = result.scalars().all()

    return patient
    

    
            
  
    raise HTTPException(status_code=400 , detail = "patient not found!")
       
@router.get("/view_patients",tags=["Patient"])
def view_patients(db:Session = Depends(get_db)):
    result = db.execute(select(Patient))

    patients = result.scalars().all()

    return patients
    
    

@router.put("/update_patient/{patient_id}")
def update_patient(patient_id:str,update_patient:patient_data,db:Session = Depends(get_db)):

    stmt = select(Patient).where(Patient.id == patient_id)

    result = db.execute(stmt)

    existing_patient = result.scalar_one_or_none()

    if existing_patient is None:
        raise HTTPException(status_code=400,detail="Patient Not Found!!")

    existing_patient.first_name = update_patient.name.first_name
    existing_patient.middle_name = update_patient.name.middle_name
    existing_patient.last_name = update_patient.name.last_name
    existing_patient.age = update_patient.age
    existing_patient.email = update_patient.email
    existing_patient.weight = update_patient.weight
    existing_patient.height = update_patient.height

    db.commit()
    db.refresh(existing_patient)

    return existing_patient




    
@router.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id : str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient Not found!!")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200 , content={"message":"patient deleted!"})