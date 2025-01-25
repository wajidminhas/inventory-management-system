# app/schemas/product.py
from pydantic import BaseModel
from typing import Optional

# Base Product Schema
class ProductBase(BaseModel):
    name: str
    barcode: str
    category: str
    price: float

# Schema for creating a product
class ProductCreate(ProductBase):
    supplier_id: Optional[int] = None

# Schema for product response
class ProductResponse(ProductBase):
    id: int
    supplier_id: Optional[int]

    class Config:
        orm_mode = True
