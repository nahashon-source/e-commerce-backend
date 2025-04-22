from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared product fields
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

# Product creation request
class ProductCreate(ProductBase):
    pass

# Product response
class ProductResponse(ProductBase):
    id: int
    status: str

    class Config:
        orm_mode = True


# Order creation request
class OrderCreate(BaseModel):
    product_id: int
    quantity: int

# Order response
class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True


# Payment
class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    payment_method: str


class PaymentResponse(BaseModel):
    status: str  # "success" or "failed"
    message: str
    order_id: Optional[int] = None
    amount: Optional[float] = None
