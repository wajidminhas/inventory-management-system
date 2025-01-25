# app/schemas/category.py
from typing import Optional
from pydantic import BaseModel

# Base Category Schema
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

# Schema for creating a category
class CategoryCreate(CategoryBase):
    pass

# Schema for category response
class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
