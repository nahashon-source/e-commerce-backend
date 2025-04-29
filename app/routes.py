from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency — DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------
# Base API Root Route
# ------------------------------------------------------

@router.get("/")
def root():
    return {"message": "Welcome to the E-commerce API"}

# ------------------------------------------------------
# Product Routes
# ------------------------------------------------------

# Get all products
@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

# Get one product by ID
@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# Create a new product
@router.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

# Update product details
@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated_product = crud.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product

# Mark product as sold
@router.put("/products/{product_id}/status", response_model=schemas.ProductResponse)
def mark_product_sold(product_id: int, db: Session = Depends(get_db)):
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or already sold")
    return product

# Delete a product
@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = crud.delete_product(db, product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return

# ------------------------------------------------------
# Order Routes
# ------------------------------------------------------

# Place a new order
@router.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order_data)

# Get all orders
@router.get("/orders", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)

# Get one order by ID
@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

# ------------------------------------------------------
# Payment Routes
# ------------------------------------------------------

# Process payment
@router.post("/payments", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment(payment: schemas.PaymentRequest):
    result = crud.verify_payment(
        order_id=payment.order_id,
        amount=payment.amount
    )
    return result
