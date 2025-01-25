# app/schemas/vendor.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Base Vendor Schema
class VendorBase(BaseModel):
    name: str
    contact_person: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

# Schema for creating a vendor
class VendorCreate(BaseModel):
    name: str
    contact_email: str
    contact_phone: str
    address: str


class VendorResponse(BaseModel):
    id: int
    name: str
    contact_email: str
    contact_phone: str
    address: str

    class Config:
        orm_mode = True
