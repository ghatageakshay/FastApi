from pydantic import BaseModel,EmailStr

class Student_Response(BaseModel):
    name:str
    email:EmailStr
    age:int