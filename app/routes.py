from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route
@router.get("/")
def root():
    return {"message": "Welcome to the E-commerce API"}

# GET /products - Get all products
@router.get("/products")
def read_products(db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return {
        "status": "success",
        "message": "Products retrieved successfully",
        "data": {"products": products}
    }

# GET /products/{id} - Get single product
@router.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status": "success",
        "message": "Product retrieved successfully",
        "data": {"product": product}
    }

# POST /products - Create a product
@router.post("/products")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    created_product = crud.create_product(db, product)  # fixed from create_products
    return {
        "status": "success",
        "message": "Product created successfully",
        "data": {"product": created_product}
    }

# PUT /products/{id}/status - Mark as sold
@router.put("/products/{product_id}/status")
def mark_sold(product_id: int, db: Session = Depends(get_db)):
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or already sold")
    return {
        "status": "success",
        "message": "Product marked as sold",
        "data": {"product": product}
    }

# POST /order - Place an order
@router.post("/order")
def place_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    order = crud.create_order(db, order_data)
    return {
        "status": "success",
        "message": "Order placed successfully",
        "data": {"order": order}
    }

# POST /payment - Verify payment
@router.post("/payment")
def process_payment(payment: schemas.PaymentRequest):
    result = crud.verify_payment(
        order_id=payment.order_id,
        amount=payment.amount
    )
    return {
        "status": "success" if result["verified"] else "failed",
        "message": result["message"],
        "data": result if result["verified"] else {}
    }
