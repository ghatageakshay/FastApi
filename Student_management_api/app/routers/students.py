from fastapi import APIRouter, HTTPException
from app.schemas.request_model import Student_request,Student_Update
from app.schemas.response_student import Student_Response
import json
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter()


def load_data():
    with open("student_data.json", "r") as f:
        data = json.load(f)
        return data


def save_data(data):
    with open("student_data.json", "w") as f:
        json.dump(data, f)
    return data

@router.get("/view/{id}",response_model=Student_Response)
def view_student(id:str):
    data = load_data()
    
    if id not in data:
        raise HTTPException(status_code=400,detail="student not found")

    return data[id]

@router.get("/view_all",response_model=List[Student_Response])
def view_all():
    data =  load_data()
    return list(data.values())



@router.post("/student")
def create_student(student_details: Student_request):
    data = load_data()

    if student_details.id in data:
        raise HTTPException(status_code=400, detail="Student Already Exists!!")

    data[str(student_details.id)] = student_details.model_dump(exclude=["id"])
    save_data(data)

    return {"message": "Student Added Successfully!!"}

@router.patch("/student/{id}")
def update_student(id:str,student_details:Student_Update):
    data = load_data()

    if id not in data:
        raise HTTPException(status_code=404,detail="student not found!!")

    student_data = data[id]
    student_details = student_details.model_dump(exclude_unset=True)

    for key,values in student_details.items():
        student_data[key] = values


    data[id] = student_data

    save_data(data)

    return JSONResponse(status_code=200,content={"message":"student details updated!!"})

@router.put("/update/{id}")
def compl_update_student(id:str,student_details:Student_request):

    data = load_data()

    if id not in data:
        raise HTTPException(
            status_code = 404,
            details = "user not found!!"
        )

    existing_student_data = data[id]

    student_details = student_details.model_dump(exclude_unset = True)

    for key , values in student_details.items():
        existing_student_data[key] = values

    existing_student_data["id"] = id


    existing_student_data = Student_request(**existing_student_data)
    existing_student_data = existing_student_data.model_dump(exclude="id")

    updated_data = existing_student_data

    data[id] = updated_data

    save_data(data)
    return JSONResponse(
        status_code = 200,
        content = {
            "messgae":"Student Updated SuccessFully!"
        }
    )



@router.delete("/delete/{id}")
def delete_student(id:str):
    data = load_data()

    print("Received Ids",repr(id))
    print("Avilable IDs",data.keys())
    
    if id not in data:
        raise HTTPException(
            status_code=404,
            detail="student not found!!"
        )

    del data[id]
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message":"Student Details Deleted!"
        }
    )