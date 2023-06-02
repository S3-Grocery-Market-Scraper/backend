from fastapi import FastAPI

from .company import router as company_router
from .product import router as product_router

api_url = "/api/v1"


def init_router(app: FastAPI):
    app.include_router(company_router, prefix=api_url, tags=['Company'])
    app.include_router(product_router, prefix=api_url, tags=['Product'])
