from pydantic import BaseModel, Field, validator
from fastapi import HTTPException

class Student(BaseModel):
    name:str
    age:int
    address:dict

    @validator('name')
    def name_must_not_be_empty(cls, name):
        if not name.strip():
            HTTPException(status_code=400, detail='Name must not be empty')
        return name

    @validator('age')
    def age_must_be_positive(cls, age):
        if age <= 0:
             raise HTTPException(status_code=400, detail='Age must be a positive integer')
        return age

    @validator('address')
    def address_must_not_be_empty(cls, add):
        if not add or len(add) == 0:
            raise HTTPException(status_code=400, detail='Address must not be empty')
        return add