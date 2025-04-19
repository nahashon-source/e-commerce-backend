from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import router  # ✅ Correct import

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce API",
    version="1.0.0"
)

# Include all routes (products, orders, payments) from the router
app.include_router(router)
