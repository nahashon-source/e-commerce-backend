from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


#--------------------------------Product Schemas-------------------------------
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0, description="Must be a positive number")
    quantity: int = Field(..., ge=1, description="Minimum quantity is 1")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    status: str

    class Config:
        orm_mode = True


#-------------------------------Order Schemas---------------------------------------
class OrderCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, description="Minimum order quantity is 1")

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True


#-------------------------------------Payment Schemas--------------------------
class PaymentRequest(BaseModel):
    order_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., min_length=3)

    @validator("payment_method")
    def validate_method(cls, v):
        if v.lower() not in ["paypal", "stripe", "mpesa"]:
            raise ValueError("Invalid payment method. Must be 'paypal', 'stripe', or 'mpesa'")
        return v.lower()


class PaymentResponse(BaseModel):
    status: str  # "success" or "failed"
    message: str
    order_id: Optional[int] = None
    amount: Optional[float] = None
