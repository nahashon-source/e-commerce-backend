from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

# ---------------------------- Product CRUD ---------------------------- #

def create_product(db: Session, product: schemas.ProductCreate):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product

def update_product(db: Session, product_id: int, product_data: schemas.ProductCreate):
    product = get_product(db, product_id)
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def mark_product_sold(db: Session, product_id: int):
    product = get_product(db, product_id)
    product.status = "Sold"
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return

# ---------------------------- Order CRUD ---------------------------- #

def create_order(db: Session, order: schemas.OrderCreate):
    product = get_product(db, order.product_id)
    if product.status == "Sold":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is already sold.")

    new_order = models.Order(**order.dict())
    product.status = "Sold"
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_all_orders(db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return order

# ---------------------------- Payment CRUD ---------------------------- #

def verify_payment(db: Session, payment_data: schemas.PaymentRequest):
    order = get_order(db, payment_data.order_id)
    # Mock payment verification logic
    if payment_data.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payment amount.")

    # Assume success for demo
    response = {
        "order_id": payment_data.order_id,
        "amount": payment_data.amount,
        "status": "Payment Verified"
    }
    return response
