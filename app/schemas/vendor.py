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
class VendorCreate(VendorBase):
    pass

# Schema for vendor response
class VendorResponse(VendorBase):
    id: int

    class Config:
        orm_mode = True
