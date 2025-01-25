# app/routers/category.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.models import Category
from app.schemas import CategoryCreate, CategoryResponse
from app.database import session

router = APIRouter()

# Create Category
@router.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate):
    db_category = Category(**category.dict())
    session.add(db_category)
    try:
        session.commit()
        session.refresh(db_category)
        return db_category
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get all Categories
@router.get("/categories/", response_model=list[CategoryResponse])
async def get_categories():
    categories = session.query(Category).all()
    return categories

# Get Category by ID
@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int):
    db_category = session.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Update Category
@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryCreate):
    db_category = session.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    try:
        session.commit()
        session.refresh(db_category)
        return db_category
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete Category
@router.delete("/categories/{category_id}")
async def delete_category(category_id: int):
    db_category = session.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        session.delete(db_category)
        session.commit()
        return {"message": "Category deleted successfully"}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
