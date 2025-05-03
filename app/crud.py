from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from . import models, schemas

# Status constants
PRODUCT_STATUS_AVAILABLE = "available"
PRODUCT_STATUS_SOLD = "sold"

#----------------------------- Product CRUD Operations ----------------------------#

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product and add it to the database."""
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
    """Retrieve all products from the database."""
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int) -> models.Product:
    """Retrieve a specific product by its ID."""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product


def mark_product_sold(db: Session, product_id: int) -> models.Product:
    """Mark a product as sold."""
    product = get_product(db, product_id)
    if product.status.lower() == PRODUCT_STATUS_SOLD:
        raise HTTPException(status_code=400, detail="Product already sold")
    product.status = PRODUCT_STATUS_SOLD
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, updated_data: schemas.ProductCreate) -> models.Product:
    """Update product details."""
    product = get_product(db, product_id)
    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.quantity = updated_data.quantity
    if product.quantity > 0 and product.status.lower() == PRODUCT_STATUS_SOLD:
        product.status = PRODUCT_STATUS_AVAILABLE
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> dict:
    """Delete a product from the database."""
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"detail": f"Product with id {product_id} deleted successfully"}


#----------------------------- Order CRUD Operations ----------------------------#

def create_order(db: Session, order_data: schemas.OrderCreate) -> models.Order:
    """Create a new order if stock is available."""
    product = get_product(db, order_data.product_id)
    if product.status.lower() == PRODUCT_STATUS_SOLD:
        raise HTTPException(status_code=400, detail="Cannot order a sold product")
    if product.quantity < order_data.quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock. Available: {product.quantity}")

    total_price = order_data.quantity * product.price
    new_order = models.Order(
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total_price
    )
    db.add(new_order)
    product.quantity -= order_data.quantity
    if product.quantity == 0:
        product.status = PRODUCT_STATUS_SOLD
    db.commit()
    db.refresh(new_order)
    return new_order


def get_all_orders(db: Session) -> List[models.Order]:
    """Retrieve all orders from the database."""
    return db.query(models.Order).all()


def get_order(db: Session, order_id: int) -> models.Order:
    """Retrieve a specific order by its ID."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order


#----------------------------- Payment CRUD Operations ----------------------------#

def verify_payment(db: Session, payment_data: schemas.PaymentRequest) -> dict:
    """Verify payment amount and record payment details."""
    order = get_order(db, payment_data.order_id)
    if payment_data.amount != order.total_price:
        raise HTTPException(status_code=400, detail="Incorrect payment amount")

    new_payment = models.Payment(
        order_id=payment_data.order_id,
        payment_method=payment_data.payment_method,
        amount_paid=payment_data.amount,
        status="completed"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {
        "status": "Success",
        "message": "Payment processed successfully",
        "order_id": order.id,
        "amount": payment_data.amount,
        "payment_id": new_payment.id
    }
