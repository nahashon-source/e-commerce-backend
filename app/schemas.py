from pydantic import BaseModel
from typing import Optional

# Product
class ProductBase(BaseModel):
    name: str
    price: float
    status: Optional[str] = "Available"

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

# Order
class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    class Config:
        orm_mode = True
