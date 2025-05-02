from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# Create a new product
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        status="available"
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Get all products
def get_all_products(db: Session) -> list[models.Product]:
    return db.query(models.Product).all()

# Get a product by ID
def get_product(db: Session, product_id: int) -> models.Product:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product

# Mark product as sold
def mark_product_sold(db: Session, product_id: int) -> models.Product:
    product = get_product(db, product_id)
    if product.status.lower() == "sold":
        raise HTTPException(status_code=400, detail="Product already sold")
    product.status = "sold"
    db.commit()
    db.refresh(product)
    return product

# Update product details
def update_product(db: Session, product_id: int, updated_data: schemas.ProductCreate) -> models.Product:
    product = get_product(db, product_id)
    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.quantity = updated_data.quantity
    if product.quantity > 0 and product.status.lower() == "sold":
        product.status = "available"
    db.commit()
    db.refresh(product)
    return product

# Delete a product
def delete_product(db: Session, product_id: int) -> dict:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"detail": f"Product with id {product_id} deleted successfully"}

# Create a new order
def create_order(db: Session, order_data: schemas.OrderCreate) -> models.Order:
    product = get_product(db, order_data.product_id)
    if product.status.lower() == "sold":
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
        product.status = "sold"
    db.commit()
    db.refresh(new_order)
    return new_order

# Get all orders
def get_all_orders(db: Session) -> list[models.Order]:
    return db.query(models.Order).all()

# Get an order by ID
def get_order(db: Session, order_id: int) -> models.Order:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order

# Verify and record payment
def verify_payment(db: Session, order_id: int, amount: float) -> dict:
    order = get_order(db, order_id)
    if amount != order.total_price:
        raise HTTPException(status_code=400, detail="Incorrect payment amount")

    new_payment = models.Payment(
        order_id=order_id,
        payment_method="mock_method",
        amount_paid=amount,
        status="completed"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {
        "status": "Success",
        "message": "Payment processed successfully",
        "order_id": order.id,
        "amount": amount,
        "payment_id": new_payment.id
    }
