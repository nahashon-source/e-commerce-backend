from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging

from . import models
from .database import engine
from . import routes 

# Initializing logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Existing app initialization
app = FastAPI(
    title="E-commerce API",
    version="1.0.0"
)

# Include your routers
app.include_router(routes.product.router)
app.include_router(routes.order.router)

# HTTP Exception handler
@app.exception_handler(FastAPIHTTPException)
async def custom_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An unexpected error occurred. Please try again later."
            }
        }
    )

# DB Create Tables
models.Base.metadata.create_all(bind=engine)
