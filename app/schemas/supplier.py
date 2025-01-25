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

# Schema for creating a supplier
class SupplierCreate(SupplierBase):
    pass

# Schema for supplier response
class SupplierResponse(SupplierBase):
    id: int

    class Config:
        orm_mode = True
