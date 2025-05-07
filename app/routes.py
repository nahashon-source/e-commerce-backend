from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

# ------------------------------------------------------
# Dependency — DB session per request
# ------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------
# Base API Root Route
# ------------------------------------------------------
@router.get("/", tags=["Root"])
def root():
    """Welcome endpoint."""
    return {"message": "Welcome to the E-commerce API"}

# ------------------------------------------------------
# Product Routes
# ------------------------------------------------------
@router.get("/products", response_model=List[schemas.ProductResponse], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    """Retrieve all available products."""
    return crud.get_all_products(db)

@router.get("/products/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a product by its ID."""
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    return product

@router.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""
    return crud.create_product(db, product)

@router.put("/products/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Update an existing product."""
    updated_product = crud.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    return updated_product

@router.put("/products/{product_id}/status", response_model=schemas.ProductResponse, tags=["Products"])
def mark_product_sold(product_id: int, db: Session = Depends(get_db)):
    """Mark a product as sold."""
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    return product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product."""
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    return

# ------------------------------------------------------
# Order Routes
# ------------------------------------------------------
@router.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create a new order."""
    return crud.create_order(db, order_data)

@router.get("/orders", response_model=List[schemas.OrderResponse], tags=["Orders"])
def get_orders(db: Session = Depends(get_db)):
    """Retrieve all orders."""
    return crud.get_all_orders(db)

@router.get("/orders/{order_id}", response_model=schemas.OrderResponse, tags=["Orders"])
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve an order by its ID."""
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found.")
    return order

# ------------------------------------------------------
# Payment Routes
# ------------------------------------------------------
@router.post("/payments", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED, tags=["Payments"])
def process_payment(payment: schemas.PaymentRequest, db: Session = Depends(get_db)):
    """Process a payment request."""
    response = crud.verify_payment(db, payment)
    if not response:
        raise HTTPException(status_code=400, detail="Payment verification failed.")
    return response
