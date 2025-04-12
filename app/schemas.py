from pydantic import BaseModel
from typing import Optional

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