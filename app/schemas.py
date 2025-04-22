from pydantic import BaseModel
from typing import Optional
from datetime import datetime


#Base schema shared between create/update/read
class ProductBase(BaseModel):
    name:str
    description: Optional[str] = None
    price: float
    quantity: int
    
    
#schema for creating a new product(creation requests(POST/products))
class ProductCreate(ProductBase):
    pass

#schemas for response(includes ID and status)
class product(ProductBase):
    id : int
    status : str
    
    class config:
        orm_mode = True # allows SQLALCHEMY models to work with pydantic for auto serialization
        
        
        
    #Request: when placing an order
class OrderCreate(BaseModel): #is for incoming data when placing an order.
    product_id: int 
    quantity: int
    
class Order(BaseModel): #is for sending order data back (includes total_price, created_at).
    id : int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime
    
class Config: # allows FastAPI to return SQLAlchemy models as JSON
    orm_mode = True #to allow SQLAlchemy model -> pydantic model conversion
    
    
class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    payment_method: str