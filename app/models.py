from sqlalchemy import ForeignKey, DateTime, Column, Float, Integer, String, Foreignkey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) # Links this order to a product.
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
product = relationship("Product")


class payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, Foreignkey("orders.id"), nullable=False)
    payment_method = Column(String, nullable=False)
    amount_paid = Column(Float, nullable=False)
    status = Column(String, default="pending")
    
    order = relationship("order")
    