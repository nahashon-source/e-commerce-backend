from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal


router = APIRouter()

#Dependancy to get the DB session fo each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        #GET/ products
@router.get("/products", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

#GET / products/{id},
@router.get("products/{product_id}", response_model=schemas.product)
def read_product(product_id: int, db:Session = Depends(get_db)):
 product = crud.get_product(db, product_id)
 if not product:
     raise HTTPException(status_code=404, detail="Product not found")
 return product

#POST /products
@router.post("/products, response_model=schemas.Product")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

# PUT /products/{id}/status
@router.put("/products/{product_id}/status", response_model=schemas.Product)
def mark_sold(product_id: int, db: Session = Depends(get_db)):
    product = crud.mark_product_sold(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/order", response_model=schemas.Order)
def place_order(order_data: schemas.orderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order_data)