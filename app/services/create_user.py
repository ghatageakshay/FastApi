from app.schemas.patient_models import patient_data
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.patient import Patient
class Create_user:
    def __init__(self,db: Session = Depends(get_db)) -> None:
        self.db = db

    def create_user(self,patient:patient_data):
        db_patient = Patient(
            first_name = patient.name.first_name,
            middle_name = patient.name.middle_name,
            last_name = patient.name.last_name,
            age = patient.age,
            email = patient.email,
            weight = patient.weight,
            height = patient.height
        )
    
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)

        return db_patient