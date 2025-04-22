from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal
from typing import List
from .schemas import ProductResponse

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
@router.get("/products", response_model=List[ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


# GET /products/{id} - Get single product
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
   
# POST /products - Create a product
@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
            return crud.create_product(db, product)  # fixed from create_products
        
        
# PUT /products/{id}/status - Mark as sold
@router.put("/products/{product_id}/status", response_model=ProductResponse)
def mark_sold(product_id: int, db: Session = Depends(get_db)):
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or already sold")
    return product

# POST /order - Place an order
@router.post("/order", response_model=schemas.OrderRespose, status_code=201)
def place_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order_data)


# POST /payment - Verify payment
@router.post("/payment", response_model=schemas.PaymentResponse)
def process_payment(payment: schemas.PaymentRequest):
    result = crud.verify_payment(
        order_id=payment.order_id,
        amount=payment.amount
    )
    return result