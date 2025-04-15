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
    
@router.get("/")
def root():
    return{"message": "Welcome to the E-commerce API"}

# GET /products - Get all products
@router.get("/products", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

# GET /products/{id} - Get single product
@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# POST /products - Create a product
@router.post("/products", response_model=schemas.Product)  # Fixed path and typo
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_products(db, product)

# PUT /products/{id}/status - Mark as sold
@router.put("/products/{product_id}/status", response_model=schemas.Product)
def mark_sold(product_id: int, db: Session = Depends(get_db)):
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# POST /order - Place an order
@router.post("/order", response_model=schemas.Order)
def place_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order_data)

# POST /payment - Verify payment (optional logic)
@router.post("/payment")
def process_payment(payment: schemas.PaymentRequest):
    result = crud.verify_payment(
        order_id=payment.order_id,
        amount=payment.amount
    )
    return result
