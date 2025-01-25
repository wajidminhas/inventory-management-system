# app/routers/supplier.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.models import Supplier
from app.schemas import SupplierCreate, SupplierResponse
from app.database import session

router = APIRouter()

# Create Supplier
@router.post("/suppliers/", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate):
    db_supplier = Supplier(**supplier.dict())
    session.add(db_supplier)
    try:
        session.commit()
        session.refresh(db_supplier)
        return db_supplier
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get all Suppliers
@router.get("/suppliers/", response_model=list[SupplierResponse])
async def get_suppliers():
    suppliers = session.query(Supplier).all()
    return suppliers

# Get Supplier by ID
@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: int):
    db_supplier = session.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

# Update Supplier
@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(supplier_id: int, supplier: SupplierCreate):
    db_supplier = session.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in supplier.dict().items():
        setattr(db_supplier, key, value)
    try:
        session.commit()
        session.refresh(db_supplier)
        return db_supplier
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete Supplier
@router.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: int):
    db_supplier = session.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    try:
        session.delete(db_supplier)
        session.commit()
        return {"message": "Supplier deleted successfully"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
