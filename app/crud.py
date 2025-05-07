from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from . import models, schemas

# Constants
PRODUCT_STATUS_AVAILABLE = "available"
PRODUCT_STATUS_SOLD = "sold"

# ---------------------------- Product CRUD Operations ---------------------------- #

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        status=PRODUCT_STATUS_AVAILABLE
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_all_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).order_by(models.Product.id.desc()).all()


def get_product(db: Session, product_id: int) -> models.Product:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product


def mark_product_sold(db: Session, product_id: int) -> models.Product:
    product = get_product(db, product_id)
    if product.status.lower() == PRODUCT_STATUS_SOLD:
        raise HTTPException(status_code=400, detail="Product already sold")
    product.status = PRODUCT_STATUS_SOLD
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, updated_data: schemas.ProductCreate) -> models.Product:
    product = get_product(db, product_id)

    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.quantity = updated_data.quantity

    if product.quantity == 0:
        product.status = PRODUCT_STATUS_SOLD
    elif product.status.lower() == PRODUCT_STATUS_SOLD:
        product.status = PRODUCT_STATUS_AVAILABLE

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> dict:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"detail": f"Product with id {product_id} deleted successfully"}


# ---------------------------- Order CRUD Operations ---------------------------- #

def create_order(db: Session, order_data: schemas.OrderCreate) -> models.Order:
    product = get_product(db, order_data.product_id)

    if product.status.lower() == PRODUCT_STATUS_SOLD:
        raise HTTPException(status_code=400, detail="Cannot order a sold product")

    if order_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Order quantity must be at least 1")

    if product.quantity < order_data.quantity:
        raise HTTPException(
            status_code=400, detail=f"Insufficient stock. Available: {product.quantity}"
        )

    total_price = order_data.quantity * product.price

    new_order = models.Order(
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total_price
    )

    product.quantity -= order_data.quantity
    if product.quantity == 0:
        product.status = PRODUCT_STATUS_SOLD

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_all_orders(db: Session) -> List[models.Order]:
    return db.query(models.Order).order_by(models.Order.id.desc()).all()


def get_order(db: Session, order_id: int) -> models.Order:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order


# ---------------------------- Payment CRUD Operations ---------------------------- #

def verify_payment(db: Session, payment_data: schemas.PaymentRequest) -> schemas.PaymentVerifyResponse:
    order = get_order(db, payment_data.order_id)

    if payment_data.amount != order.total_price:
        raise HTTPException(status_code=400, detail="Incorrect payment amount")

    if payment_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be positive")

    new_payment = models.Payment(
        order_id=payment_data.order_id,
        payment_method=payment_data.payment_method,
        amount_paid=payment_data.amount,
        status=models.PaymentStatusEnum.completed  # <-- using Enum safely here
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return schemas.PaymentVerifyResponse(
        status="Success",
        message="Payment processed successfully.",
        order_id=order.id,
        amount=payment_data.amount,
        payment_id=new_payment.id
    )
