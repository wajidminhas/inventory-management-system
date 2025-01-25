# app/schemas/order.py
from pydantic import BaseModel
from typing import Optional

# Base Order Schema
class OrderBase(BaseModel):
    product_id: int
    employee_id: int
    quantity: int
    total_price: float
    order_date: str

# Schema for creating an order
class OrderCreate(OrderBase):
    pass

# Schema for order response
class OrderResponse(OrderBase):
    id: int

    class Config:
        orm_mode = True
