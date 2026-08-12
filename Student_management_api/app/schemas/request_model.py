from typing import Annotated, List , Optional
from pydantic import BaseModel, EmailStr, Field, field_validator,computed_field


class Student_request(BaseModel):
    id: Annotated[int, Field(gt=0, description="Student Id")]
    name: Annotated[str, Field(description="Enter full name of student")]
    age: Annotated[int, Field(gt=0, lt=35)]
    email: Annotated[EmailStr, Field(description="Enter email: ")]
    marks: Annotated[List[int], Field(description="Enter three subjects marks")]

    @field_validator("marks")
    @classmethod
    def validate_marks(cls, marks):
        if len(marks) != 3:
            raise ValueError("Only send marks of 3 subjects!!")
        return marks

    @computed_field()
    @property

    def average(self) -> float:
        total = sum(self.marks)
        avg = total / 3

        return avg

class Student_Update(BaseModel):
    name:Annotated[Optional[str],Field(default=None,description="Update Student Name!")]
    age:Annotated[Optional[int],Field(default=None,gt=16,lt=35,description="Update Student Age Name!!")]
    email:Annotated[Optional[EmailStr],Field(default=None,description="Update Email!")]
    marks:Annotated[Optional[List[int]],Field(default=None,max_length=3,min_length=3,description="Update Marks Of Three Subjects")]