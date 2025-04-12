from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"
    
    id = column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) # Links this order to a product.
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
product = relationship("Product")
