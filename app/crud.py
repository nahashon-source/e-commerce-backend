from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# CREATE PRODUCT
def create_products(db: Session, product: schemas.ProductCreate):
    new_product = models.Product(  # Fixed: Capitalized 'Product'
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        status="available"  # Optional: default status if needed
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# READ ALL PRODUCTS
def get_all_products(db: Session):
    return db.query(models.Product).all()  # Fixed: typo 'querry' -> 'query', capitalized Product


# READ PRODUCT BY ID
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


# UPDATE STATUS TO "Sold"
def mark_product_sold(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.status = "sold"
        db.commit()
        db.refresh(product)
        return product
    raise HTTPException(status_code=404, detail="Product not found")


# CREATE ORDER
def create_order(db: Session, order_data: schemas.OrderCreate):  # Fixed: Capitalized OrderCreate
    product = db.query(models.Product).filter(models.Product.id == order_data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.status.lower() == "sold" or product.quantity < order_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock or product is sold")

    total_price = order_data.quantity * product.price

    new_order = models.Order(  # Fixed: Use models.Order, not models.product
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total_price
    )
    db.add(new_order)

    # UPDATE INVENTORY
    product.quantity -= order_data.quantity
    if product.quantity == 0:
        product.status = "sold"

    db.commit()
    db.refresh(new_order)
    return new_order
