# app/schemas/employee.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Base Employee Schema
class EmployeeBase(BaseModel):
    name: str
    role: str
    email: EmailStr

# Schema for creating an employee
class EmployeeCreate(EmployeeBase):
    password: str  # For setting the initial password

# Schema for employee response
class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
