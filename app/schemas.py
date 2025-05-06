from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

#-------------------------------Product Schemas--------------------------------
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Classic T-Shirt")
    description: Optional[str] = Field(None, max_length=300, example="A comfortable cotton t-shirt.")
    price: float = Field(..., gt=0, description="Must be a positive number", example=19.99)
    quantity: int = Field(..., ge=1, description="Minimum quantity is 1", example=10)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


#-------------------------------Order Schemas-----------------------------------
class OrderCreate(BaseModel):
    product_id: int = Field(..., gt=0, example=1)
    quantity: int = Field(..., ge=1, description="Minimum order quantity is 1", example=2)


class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True


#------------------------------Payment Schemas----------------------------------
class PaymentRequest(BaseModel):
    order_id: int = Field(..., gt=0, example=5)
    amount: float = Field(..., gt=0, example=39.98)
    payment_method: str = Field(..., min_length=3, example="mpesa")

    @validator("payment_method")
    def validate_method(cls, v):
        if v.lower() not in ["paypal", "stripe", "mpesa"]:
            raise ValueError("Invalid payment method. Must be 'paypal', 'stripe', or 'mpesa'")
        return v.lower()


class PaymentResponse(BaseModel):
    id: int
    status: Literal["pending", "completed", "failed"]
    order_id: Optional[int] = None
    amount: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True


class PaymentVerifyResponse(BaseModel):
    status: str
    message: str
    order_id: int
    amount: float
    payment_id: int

    class Config:
        orm_mode = True
