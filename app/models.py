from sqlalchemy import Column, Integer,String, Float, Boolean
from.database import Base

class Production(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="Available")  #Available or sold