from pydantic import BaseModel,EmailStr,Field,field_validator,model_validator,computed_field
from typing import Annotated,Dict,Optional

class Name(BaseModel):
    first_name:str
    middle_name:str
    last_name:str

class patient_data(BaseModel ):
   
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    name:Annotated[Name,Field(...,description="Name of the patient")]
    email: Annotated[EmailStr,Field(description="Email Of patient")]
    weight:Annotated[float, Field(gt=0)]
    height:Annotated[float,Field(gt=0,description="Height Of patient in meters")]

    @field_validator("email")
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

class Search_data(BaseModel):
    name:Annotated[str , Field(...,description="Enter the name to search for...")]
