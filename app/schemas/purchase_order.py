# app/schemas/purchase_order.py
from pydantic import BaseModel
from typing import List, Optional

# Base Purchase Order Schema
class PurchaseOrderBase(BaseModel):
    supplier_id: int
    total_cost: float
    status: str  # e.g., "pending", "received", "canceled"

# Schema for creating a purchase order
class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[dict]  # Each item contains product_id and quantity

# Schema for purchase order response
class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    items: List[dict]  # Detailed list of items in the purchase order

    class Config:
        orm_mode = True
