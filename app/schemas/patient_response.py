from pydantic import BaseModel,Field
from typing import Dict
from app.schemas.patient_models import Name,patient_data

class PatientResponse(BaseModel):
    id:str
    name:Name
    age:int
    weight:float
    height:float

