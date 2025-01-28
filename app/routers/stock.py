from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models import Stock
from app.schemas import StockCreate, StockResponse
from typing import List

router = APIRouter(prefix="/stock", tags=["Stock"])

# Create Stock
@router.post("/", response_model=StockResponse)
def create_stock(stock: StockCreate, session : Annotated[Session, Depends(get_session)]):
    new_stock = Stock(**stock.dict())
    session.add(new_stock)
    session.commit()
    session.refresh(new_stock)
    return new_stock

# Get All Stock Items
@router.get("/", response_model=List[StockResponse])
def get_stock_items(session : Annotated[Session, Depends(get_session)]):
    stock_items = session.query(Stock).all()
    return stock_items

# Get Stock by ID
@router.get("/{stock_id}", response_model=StockResponse)
def get_stock(stock_id: int, session : Annotated[Session, Depends(get_session)]):
    stock = session.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

# Update Stock
@router.put("/{stock_id}", response_model=StockResponse)
def update_stock(stock_id: int, updated_stock: StockCreate, session : Annotated[Session, Depends(get_session)]):
    stock = session.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    for key, value in updated_stock.dict().items():
        setattr(stock, key, value)
    session.commit()
    session.refresh(stock)
    return stock

# Delete Stock
@router.delete("/{stock_id}")
def delete_stock(stock_id: int, session : Annotated[Session, Depends(get_session)]):
    stock = session.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    session.delete(stock)
    session.commit()
    return {"detail": "Stock deleted successfully"}
