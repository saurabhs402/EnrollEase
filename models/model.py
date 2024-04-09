from pydantic import BaseModel, Field, validator
from fastapi import HTTPException
from typing import List

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name:str
    age:int
    address:Address
     

    @validator('name')
    def name_must_not_be_empty(cls, name):
        if not name.strip():
            raise HTTPException(status_code=400, detail='Name must not be empty')
        return name

    @validator('age')
    def age_must_be_positive(cls, age):
        if age <= 0:
             raise HTTPException(status_code=400, detail='Age must be a positive integer')
        return age

    @validator('address')
    def address_must_not_be_empty(cls, add):
        if not add.city.strip() or not add.country.strip():
            raise HTTPException(status_code=400, detail='Address must not be empty')
        return add


class CreateResponse(BaseModel):
    id: str

class nameAndAge(BaseModel):
    name:str
    age:int

class listStudentResponse(BaseModel):
    data:List[nameAndAge]
    
class EmptyResponse(BaseModel):
    pass
   