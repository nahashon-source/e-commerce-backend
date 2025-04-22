from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# CREATE PRODUCT
def create_product(db: Session, product: schemas.ProductCreate):
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

# READ ALL PRODUCTS
def get_all_products(db: Session):
    return db.query(models.Product).all()

# READ PRODUCT BY ID
def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return product

# UPDATE STATUS TO "Sold"
def mark_product_sold(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    if product.status.lower() == "sold":
        raise HTTPException(status_code=400, detail="Product already sold")

    product.status = "sold"
    db.commit()
    db.refresh(product)
    return product

# CREATE ORDER
def create_order(db: Session, order_data: schemas.OrderCreate):
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

    # Save order
    db.add(new_order)

    # Update product quantity and status
    product.quantity -= order_data.quantity
    if product.quantity == 0:
        product.status = "sold"

    db.commit()
    db.refresh(new_order)
    return new_order