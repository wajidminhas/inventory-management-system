# app/schemas/supplier.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Base Supplier Schema
class SupplierBase(BaseModel):
    name: str
    contact_person: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
from pydantic import BaseModel

# Supplier Schemas
class SupplierCreate(BaseModel):
    name: str
    contact_email: str
    contact_phone: str
    company_name: str
    address: str


class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_email: str
    contact_phone: str
    company_name: str
    address: str

    class Config:
        orm_mode = True

