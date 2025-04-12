from sqlalchemy import Column,Integer, String, Float, Boolean 
from database import  Base

class product :
    products = "Muchai stores"
    def __init__ (self,name, price, status="Available"):
        self.name = name
        self.price = price 
        self.status = status
        
        
    def sold(self):
        self.status = "sold"
        
        def __str__(self):
            return f"{self.name} - ${self.price} - {self.status}"
        
        
        class DiscountedProduct:
            def __init__(self):
                self
        
        
        product1 = product("T-shirt", 19.99)
        print(product1)