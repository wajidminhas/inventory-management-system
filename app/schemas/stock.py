# app/schemas/stock.py
from pydantic import BaseModel
from typing import Optional

# Base Stock Schema
class StockBase(BaseModel):
    quantity: int
    location: str
    minimum_threshold: Optional[int] = 10

# Schema for adding stock
class StockCreate(StockBase):
    product_id: int

# Schema for stock response
class StockResponse(StockBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True
