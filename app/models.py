from sqlalchemy import ForeignKey, DateTime, Column, Float, Integer, String, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum


class PaymentStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="product", cascade="all, delete")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="orders")
    payments = relationship("Payment", back_populates="order", cascade="all, delete")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method = Column(String, nullable=False)
    amount_paid = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="payments")
