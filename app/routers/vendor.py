# app/routers/vendor.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.models import Vendor
from app.schemas import VendorCreate, VendorResponse
from app.database import session

router = APIRouter()

# Create Vendor
@router.post("/vendors/", response_model=VendorResponse)
async def create_vendor(vendor: VendorCreate):
    db_vendor = Vendor(**vendor.dict())
    session.add(db_vendor)
    try:
        session.commit()
        session.refresh(db_vendor)
        return db_vendor
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get all Vendors
@router.get("/vendors/", response_model=list[VendorResponse])
async def get_vendors():
    vendors = session.query(Vendor).all()
    return vendors

# Get Vendor by ID
@router.get("/vendors/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: int):
    db_vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

# Update Vendor
@router.put("/vendors/{vendor_id}", response_model=VendorResponse)
async def update_vendor(vendor_id: int, vendor: VendorCreate):
    db_vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    for key, value in vendor.dict().items():
        setattr(db_vendor, key, value)
    try:
        session.commit()
        session.refresh(db_vendor)
        return db_vendor
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete Vendor
@router.delete("/vendors/{vendor_id}")
async def delete_vendor(vendor_id: int):
    db_vendor = session.query(Vendor).filter(Vendor.id == vendor_id).first()
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    try:
        session.delete(db_vendor)
        session.commit()
        return {"message": "Vendor deleted successfully"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
