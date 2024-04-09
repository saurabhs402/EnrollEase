from fastapi import APIRouter, Response, HTTPException

from models.model import Student, CreateResponse,listStudentResponse, EmptyResponse
from schemas.schema import individual_serial,list_serial
from config.db import studentsCollection

from typing import Optional, List
from bson import ObjectId

endPoints=APIRouter()

@endPoints.get("/")
def home(country:str=None,age:int=0):
    return{
        "status":"ok",
        "message":"My fastapi is running.Please mention the endpoints such as /students or /docs",
        "country":country,
        "age":age
    }

# Create Students
@endPoints.post("/students",status_code=201,response_model=CreateResponse)
async def Create_student(student:Student):
    _id=studentsCollection.insert_one(student.dict())
    return  {"id":str(_id.inserted_id)}



#  Retrieve Students
@endPoints.get("/students",status_code=200,response_model=listStudentResponse)
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}

    # Apply country filter if provided
    if country:
        query["address.country"] = country

    # Apply age filter if provided
    if age is not None:
        query["age"] = {"$gt": age}
    students_cursor=studentsCollection.find(query)
    students = [{"name": student["name"], "age": student["age"]} for student in students_cursor]
     # Check if no students were found
    if not students:
        raise HTTPException(status_code=404, detail="No students found. Please insert some data.")
    return {"data":students}




# Fetch Particular Student
@endPoints.get("/students/{id}",status_code=200,response_model=Student)
async def Fetch_student(id:str):
    # Retrieve student from the database
    student = studentsCollection.find_one({"_id": ObjectId(id)})

    # Check if student is None (not found)
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id {id} not found")

    # Convert retrieved student data to model
    student_model = individual_serial(student)
    return student_model



# Update Student
@endPoints.patch("/students/{id}",status_code=204)
async def Update_student(id: str, updated_fields:Student):
   

    # Convert Pydantic model to dictionary excluding None values
    student_dict = student.dict(exclude_unset=True)

    # Perform partial update operation in MongoDB
    result = studentsCollection.update_one({"_id": ObjectId(id)}, {"$set": student_dict})


    # Check if the student record was found and updated
    if result is None:
        raise HTTPException(status_code=404, detail=f"Student with id {id} not found")

# Delete Student
@endPoints.delete("/students/{id}",status_code=200,response_model=EmptyResponse)
async def Delete_student(id:str):
    result=studentsCollection.find_one_and_delete({"_id":ObjectId(id)})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Student with id {id} not found")
    return {}
    
    
  
  
