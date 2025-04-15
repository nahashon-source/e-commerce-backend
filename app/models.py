from sqlalchemy import ForeignKey, DateTime, Column, Float, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Product(Base):  # Ensure this exists, otherwise create it if not
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # Links this order to a product
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("Product")  # Corrected to match 'Product'

class Payment(Base):  # Capitalized to follow Python class naming convention
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method = Column(String, nullable=False)
    amount_paid = Column(Float, nullable=False)
    status = Column(String, default="pending")
    
    order = relationship("Order")  # Corrected to match 'Order'
