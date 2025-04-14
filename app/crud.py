from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

#CREATE
def create_products(db: Session, product: schemas.ProductCreate): #create_prodct take a pydantic schema, converts it to a model, adds it to the DB
    new_product = models.product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


#READ ALL
def get_all_products(db: Session):# Returns a list of all products
    return db.querry(models.product).all()

#READ ONE BY ID
def get_product(db: Session, product_id: int): # Fetches a single product by ID
    return db.query(models.product).filter(models.Product.id == product_id).first()

#UPDATE STATUS TO "Sold"
def mark_product_sold(db:Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.status = "sold"
        db.commit()
        db.refresh(product)
        
        return product
    
    
def create_order(db: Session, order_data: schemas.ordercreate):
    product = db.query(models.product).filter(models.product.id == order_data.product_id).first()
    
    if not product:
        raise HTTPException(status_code =404, detail="Product nor found")
    
    if product.status == "Sold" or product.quantity < order_data.quantity:
        raise HTTPException(status_code=4000, detail="Not enough stock or product sold")
    
    total_price = order_data.quantity * product.price
    
    
    
    
#CREATE ORDER
new_order = models.product(
    product_id=order_data.product_id,
    quantity=order_data.quantity,
    total_price=total_price
)
db.add(new_order)


#UPDATE INVENTORY
product.quantity -= order_data.quantity
if product.quantity == 0:
    product.status = "sold"
    
    db.commit()
    db.refresh(new_order)
    return new_order