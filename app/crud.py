from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from fastapi.responses import JSONResponse


# Create a new product
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """
    Adds a new product to the database.
    """
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
def get_all_products(db: Session) -> list:
    """
    Returns a list of all products.
    """
    return db.query(models.Product).all()


# Get a product by ID
def get_product(db: Session, product_id: int) -> models.Product:
    """
    Fetch a single product by ID.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product


# Mark product as sold
def mark_product_sold(db: Session, product_id: int) -> models.Product:
    """
    Marks a product as sold.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    if product.status.lower() == "sold":
        raise HTTPException(status_code=400, detail="Product already sold")

    product.status = "sold"
    db.commit()
    db.refresh(product)
    return product


# Create a new order
def create_order(db: Session, order_data: schemas.OrderCreate) -> models.Order:
    """
    Places an order for a product.
    """
    product = db.query(models.Product).filter(models.Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {order_data.product_id} not found")

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

    # Save order and adjust product quantity
    db.add(new_order)
    product.quantity -= order_data.quantity
    if product.quantity == 0:
        product.status = "sold"

    db.commit()
    db.refresh(new_order)
    return new_order


# Verify payment (mocked)
def verify_payment(db: Session, order_id: int, amount: float) -> dict:
    """
    Mock payment verification.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")

    if amount != order.total_price:
        raise HTTPException(status_code=400, detail="Incorrect payment amount")

    return {
        "status": "Success",
        "message": "Payment processed successfully",
        "order_id": order.id,
        "amount": amount
    }


# Update product details
def update_product(db: Session, product_id: int, updated_data: schemas.ProductCreate) -> models.Product:
    """
    Updates an existing product's details.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    product.name = updated_data.name
    product.description = updated_data.description
    product.price = updated_data.price
    product.quantity = updated_data.quantity

    # If restocking, reset status to available
    if product.quantity > 0 and product.status.lower() == "sold":
        product.status = "available"

    db.commit()
    db.refresh(product)
    return product


# Delete a product
def delete_product(db: Session, product_id: int) -> dict:
    """
    Deletes a product from the database.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    db.delete(product)
    db.commit()
    return {"detail": f"Product with id {product_id} deleted successfully"}


# Get all orders
def get_all_orders(db: Session) -> list:
    """
    Returns a list of all orders.
    """
    return db.query(models.Order).all()


# Get an order by ID
def get_order(db: Session, order_id: int) -> models.Order:
    """
    Fetch a single order by ID.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order
