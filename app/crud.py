from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import get_db

router = APIRouter()


# ---------------------------- Product Routes ---------------------------- #

@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.get("/products", response_model=List[schemas.ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product_data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, product_data)


@router.patch("/products/{product_id}/mark-sold", response_model=schemas.ProductResponse)
def mark_product_sold(product_id: int, db: Session = Depends(get_db)):
    return crud.mark_product_sold(db, product_id)


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, product_id)


# ---------------------------- Order Routes ---------------------------- #

@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.get("/orders", response_model=List[schemas.OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)


@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)


# ---------------------------- Payment Routes ---------------------------- #

@router.post("/payments/verify", response_model=schemas.PaymentVerifyResponse)
def verify_payment(payment_data: schemas.PaymentRequest, db: Session = Depends(get_db)):
    return crud.verify_payment(db, payment_data)
