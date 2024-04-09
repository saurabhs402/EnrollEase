from fastapi import APIRouter, Response

from models.model import Student, CreateResponse,listStudentResponse, EmptyResponse
from schemas.schema import individual_serial,list_serial
from config.db import studentsCollection

from typing import Optional, List
from bson import ObjectId

endPoints=APIRouter()

# @endPoints.get("/")
# def home(country:str=None,age:int=0):
#     return{
#         "status":"ok",
#         "message":"My fastapi is running.Please mention the endpoints.",
#         "country":country,
#         "age":age
#     }

# Create Students
@endPoints.post("/students",status_code=201,response_model=CreateResponse)
async def Create_student(student:Student):
    _id=studentsCollection.insert_one(dict(student))
    return  {"_id":str(_id.inserted_id)}

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
    return students


# Fetch Particular Student
@endPoints.get("/students/{id}",status_code=200,response_model=Student)
async def Fetch_student(id:str):
    student= individual_serial(studentsCollection.find_one({"_id":ObjectId(id)}))
    return student


# Update Student
@endPoints.patch("/students/{id}",status_code=204)
async def Update_student(id:str,student:dict):
    studentsCollection.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(student)
    })
    return Response(status_code=204, content_type="text/plain", content="")
    
    

# Delete STudent
@endPoints.delete("/students/{id}",status_code=200,response_model=EmptyResponse)
async def Delete_student(id:str):
    studentsCollection.find_one_and_delete({"_id":ObjectId(id)})
    
  
  
