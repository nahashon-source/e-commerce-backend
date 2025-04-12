from fastapi import FastAPI
from . import models
from .database import  engine
from .routes import router  as product_router

#create tables in the DB
models.Base.metadata.create_all(bind=engine)


#initalize FastAPI app
app = FastAPI(
    title = "E-commerce API",
    version = "1.0.0"
)

#include produuct-related routes
app.include_router(product_router)