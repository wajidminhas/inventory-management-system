# app/routers/products.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models import Product, Stock
from app.database import get_session
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

# Create a product
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

# Get all products
@router.get("/", response_model=list[ProductResponse])
def list_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

# Add stock to a product
@router.post("/{product_id}/stock/")
def add_stock(product_id: int, quantity: int, location: str, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    stock = Stock(product_id=product_id, quantity=quantity, location=location)
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return {"message": "Stock added successfully", "stock": stock}
