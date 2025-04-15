from fastapi import FastAPI
from app.models import models
from app.database import  engine
from app.routes import router  as product_router

#create tables in the DB
models.Base.metadata.create_all(bind=engine)


#initalize FastAPI app
app = FastAPI(
    title = "E-commerce API",
    version = "1.0.0"
)

#include produuct-related routes
app.include_router(product_router)