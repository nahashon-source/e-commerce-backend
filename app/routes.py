from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal
from typing import List

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def root():
    return {"message": "Welcome to the E-commerce API"}

# Get all products
@router.get("/products", response_model=List[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

# Get one product
@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Create product
@router.post("/products", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

# Mark product as sold
@router.put("/products/{product_id}/status", response_model=schemas.ProductResponse)
def mark_sold(product_id: int, db: Session = Depends(get_db)):
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or already sold")
    return product

# Place an order
@router.post("/order", response_model=schemas.OrderResponse, status_code=201)
def place_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order_data)

# Process payment
@router.post("/payment", response_model=schemas.PaymentResponse)
def process_payment(payment: schemas.PaymentRequest):
    result = crud.verify_payment(
        order_id=payment.order_id,
        amount=payment.amount
    )
    return result


#PRODUCT ROUTES
@router.put("/products/{product_id}")
def update_product_details(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, product)

@router.delete("/products/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, product_id)

@router.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)

@router.get("/orders/{order_id}")
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)
