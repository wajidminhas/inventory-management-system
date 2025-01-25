# app/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Employee Model
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100)
    role: str = Field(..., max_length=50)
    email: str = Field(..., unique=True)
    password: str = Field(..., max_length=255)  # Hashed

# Product Model
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100)
    barcode: str = Field(..., unique=True)
    category: str = Field(..., max_length=50)
    price: float = Field(..., ge=0)
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id")

    # Relationship with stock
    stock: List["Stock"] = Relationship(back_populates="product")

# Supplier Model
class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100)
    contact: str = Field(..., max_length=15)
    address: str = Field(..., max_length=255)

# Stock Model
class Stock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(..., foreign_key="product.id")
    quantity: int = Field(..., ge=0)
    location: str = Field(..., max_length=100)
    minimum_threshold: int = Field(default=10, ge=0)

    # Relationships
    product: Product = Relationship(back_populates="stock")

# Order Model
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(..., foreign_key="product.id")
    employee_id: int = Field(..., foreign_key="employee.id")
    quantity: int = Field(..., ge=1)
    total_price: float = Field(..., ge=0)
    order_date: str = Field(..., max_length=50)

# Vendor Model

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100)
    contact_person: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=15)
    email: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)


# Supplier Model
class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100)
    contact_person: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=15)
    email: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)

# Purchase Order Model
class PurchaseOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier_id: int = Field(..., foreign_key="supplier.id")
    total_cost: float = Field(..., ge=0)
    status: str = Field(..., max_length=50)  # Status (pending, received, canceled)

    # Relationships
    items: List["PurchaseOrderItem"] = Relationship(back_populates="purchase_order")

# Purchase Order Item Model
class PurchaseOrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    purchase_order_id: int = Field(..., foreign_key="purchaseorder.id")
    product_id: int = Field(..., foreign_key="product.id")
    quantity: int = Field(..., ge=1)

    # Relationships
    purchase_order: PurchaseOrder = Relationship(back_populates="items")


# Category Model
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)


