

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import  engine, SQLModel
from app.database import create_db_table
from app.routers import (
    product,
#     stock,
#     employee,
#     order,
#     auth,
#     vendor,
#     supplier,
#     purchase_order,
    category
)

# Create all tables in the database
SQLModel.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Inventory Management System",
    description="An API for managing inventory, employees, orders, vendors, suppliers, and more.",
    version="1.0.0",
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    create_db_table()
    yield
    print("Closing database connection...")

app = FastAPI(lifespan=lifespan, title="Inventry Service API")
# CORS settings (Adjust origins as per your frontend requirements)
origins = ["http://localhost:3000", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(product.router, prefix="/api/products", tags=["Products"])
# app.include_router(stock.router, prefix="/api/stocks", tags=["Stocks"])
# app.include_router(employee.router, prefix="/api/employees", tags=["Employees"])
# app.include_router(order.router, prefix="/api/orders", tags=["Orders"])
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(vendor.router, prefix="/api/vendors", tags=["Vendors"])
# app.include_router(supplier.router, prefix="/api/suppliers", tags=["Suppliers"])
# app.include_router(purchase_order.router, prefix="/api/purchase-orders", tags=["Purchase Orders"])
app.include_router(category.router, prefix="/api/categories", tags=["Categories"])

# Health check endpoint
@app.get("/", tags=["Health Check"])
async def health_check():
    return {"message": "Inventory Management System API is running!"}
