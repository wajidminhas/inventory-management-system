# app/routers/supplier.py
from sqlmodel import select
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.models import Supplier
from app.database import Session, get_session
from app.schemas.supplier import SupplierCreate, SupplierResponse

router = APIRouter()

# Create Supplier
@router.post("/suppliers/", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, session : Annotated[Session, Depends(get_session)]):
    db_supplier = Supplier(**supplier.exec())
    Session.add(db_supplier)
    try:
        Session.commit()
        Session.refresh(db_supplier)
        return db_supplier
    except SQLAlchemyError as e:
        Session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get all Suppliers
@router.get("/suppliers/", response_model=list[SupplierResponse])
async def get_suppliers(session : Annotated[Session, Depends(get_session)]):
    suppliers = Session.exec(Supplier).all()
    return suppliers

# Get Supplier by ID
@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: int, session : Annotated[Session, Depends(get_session)]):
    db_supplier = Session.exec(select(Supplier).filter(Supplier.id == supplier_id)).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

# Update Supplier
@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(supplier_id: int, supplier: SupplierCreate, session : Annotated[Session, Depends(get_session)]):
    db_supplier = Session.exec(select(Supplier).filter(Supplier.id == supplier_id)).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in supplier.dict().items():
        setattr(db_supplier, key, value)
    try:
        Session.commit()
        Session.refresh(db_supplier)
        return db_supplier
    except SQLAlchemyError as e:
        Session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete Supplier
@router.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: int, session : Annotated[Session, Depends(get_session)]):
    db_supplier = Session.exec(select(Supplier).filter(Supplier.id == supplier_id)).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    try:
        Session.delete(db_supplier)
        Session.commit()
        return {"message": "Supplier deleted successfully"}
    except SQLAlchemyError as e:
        Session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
