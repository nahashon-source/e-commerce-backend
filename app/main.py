from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging

from app import models
from app.database import engine
from app import routes

# ---------------------------- Logging Configuration ---------------------------- #
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ---------------------------- FastAPI App Initialization ---------------------------- #
app = FastAPI(
    title="E-commerce API",
    version="1.0.0"
)

# ---------------------------- Database Table Creation ---------------------------- #
models.Base.metadata.create_all(bind=engine)

# ---------------------------- Routers ---------------------------- #
app.include_router(routes.product.router, prefix="/api")
app.include_router(routes.order.router, prefix="/api")

# ---------------------------- Custom Exception Handlers ---------------------------- #
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
