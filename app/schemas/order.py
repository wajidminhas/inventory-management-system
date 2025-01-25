# app/schemas/order.py
from datetime import date
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
class PurchaseOrderCreate(BaseModel):
    order_date: date
    supplier_id: int
    product_id: int
    quantity: int
    total_price: float


class PurchaseOrderResponse(BaseModel):
    id: int
    order_date: date
    supplier_id: int
    supplier_name: str
    product_id: int
    product_name: str
    quantity: int
    total_price: float

    class Config:
        orm_mode = True
