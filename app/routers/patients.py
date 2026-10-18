from fastapi import APIRouter,HTTPException,Depends
import json
from fastapi.responses import JSONResponse
from app.schemas.patient_models import patient_data,Name,patient_update,Search_data
from app.schemas.patient_response import PatientResponse
from app.database import SessionLocal,get_db
from app.models.patient import Patient
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.services.create_user import Create_user

router = APIRouter()


@router.post("/create",summary="Creates A new Patient!!")
def create(patient:patient_data,service:Create_user = Depends(Create_user)):

    return service.create_user(patient)

    # db_patient = Patient(
    #     first_name = patient.name.first_name,
    #     middle_name = patient.name.middle_name,
    #     last_name = patient.name.last_name,
    #     age = patient.age,
    #     email = patient.email,
    #     weight = patient.weight,
    #     height = patient.height
    # )

    # db.add(db_patient)
    # db.commit()
    # db.refresh(db_patient)

    # return {db_patient}

@router.get("/search_patient",response_model=list[PatientResponse])
def search_patient(name:str,db:Session = Depends(get_db)):
    stmt = select(Patient).where(Patient.first_name == name)

    result = db.execute(stmt)
    patient = result.scalars().all()

    return patient
    
       
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
def delete_patient(patient_id : int,db:Session = Depends(get_db)):

    stmt = select(Patient).where(Patient.id == patient_id)
    result = db.execute(stmt)
    existing_patient = result.scalar_one_or_none()

    if existing_patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(existing_patient)

    db.commit()

    return{
        "message":"Patient Deleted Successfully!!"
    }

@router.patch("/update_patient/{patient_id}",response_model=PatientResponse)

def patch_patient(
    patient_id : int,
    update_patient : patient_update,
    db:Session = Depends(get_db)
):

    stmt = select(Patient).where(Patient.id == patient_id)

    result = db.execute(stmt)
    existing_patient = result.scalar_one_or_none()

    if existing_patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found!!"
        )

    update_data = update_patient.model_dump(exclude_unset=True)

    for key,value in update_data.items():

        if key == "name":
            existing_patient.first_name = value["first_name"]
            existing_patient.middle_name = value["middle_name"]
            existing_patient.last_name = value["last_name"]

        else:
            setattr(existing_patient,key,value)

    db.commit()
    db.refresh(existing_patient)

    return existing_patient