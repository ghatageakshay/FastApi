from pydantic import BaseModel,Field,ConfigDict
from typing import Dict
from app.schemas.patient_models import Name,patient_data

class PatientResponse(BaseModel):
    id:int
    first_name:str
    middle_name:str
    last_name:str
    email:str
    age:int
    weight:float
    height:float

model_config = ConfigDict(from_attributes=True)
