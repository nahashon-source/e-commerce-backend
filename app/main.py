from fastapi import FastAPI
from app.models import models
from app.database import  engine
from app.routes import router  as products, orders, payments

#create tables in the DB
models.Base.metadata.create_all(bind=engine)


#initalize FastAPI app
app = FastAPI(
    title = "E-commerce API",
    version = "1.0.0"
)

#include product-related routes
app.include_router(products)
app.include_router(orders)
app.include_router(payments)
