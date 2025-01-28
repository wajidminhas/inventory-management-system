# app/routers/purchase_order.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from app.models import PurchaseOrder, PurchaseOrderItem
from app.database import get_session, SQLModel
from app.schemas.order import PurchaseOrderCreate, PurchaseOrderResponse

router = APIRouter()



# Create Purchase Order
@router.post("/purchase-orders/", response_model=PurchaseOrderResponse)
async def create_purchase_order(purchase_order: PurchaseOrderCreate, session : Annotated[Session, Depends(get_session)]):
    db_purchase_order = PurchaseOrder(**purchase_order.dict())
    session.add(db_purchase_order)
    try:
        session.commit()
        session.refresh(db_purchase_order)
        for item in purchase_order.items:
            db_item = PurchaseOrderItem(**item, purchase_order_id=db_purchase_order.id)
            session.add(db_item)
        session.commit()
        return db_purchase_order
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get all Purchase Orders
@router.get("/purchase-orders/", response_model=list[PurchaseOrderResponse])
async def get_purchase_orders(session : Annotated[Session, Depends(get_session)]):
    purchase_orders = session.exec(select(PurchaseOrder)).all()
    return purchase_orders

# Get Purchase Order by ID
@router.get("/purchase-orders/{order_id}", response_model=PurchaseOrderResponse)
async def get_purchase_order(order_id: int, session : Annotated[Session, Depends(get_session)]):
    db_order = session.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return db_order

# Update Purchase Order
@router.put("/purchase-orders/{order_id}", response_model=PurchaseOrderResponse)
async def update_purchase_order(order_id: int, purchase_order: PurchaseOrderCreate, session : Annotated[Session, Depends(get_session)]):
    db_order = session.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    for key, value in purchase_order.dict().items():
        setattr(db_order, key, value)
    try:
        session.commit()
        session.refresh(db_order)
        return db_order
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete Purchase Order
@router.delete("/purchase-orders/{order_id}")
async def delete_purchase_order(order_id: int, session : Annotated[Session, Depends(get_session)]):
    db_order = session.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    try:
        session.delete(db_order)
        session.commit()
        return {"message": "Purchase Order deleted successfully"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
