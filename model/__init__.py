from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient
from fastapi import FastAPI
from .product_model import ProductModel
from .company import Company
from .category import Category
from .product_item import ProductItem

from beanie import init_beanie


def init_db(app: FastAPI, mongo_url: str, mongo_database: str, use_mock: bool = False):
    @app.on_event("startup")
    async def startup_db_client():
        client: AsyncIOMotorClient

        if use_mock:
            client = AsyncMongoMockClient()
        else:
            client = AsyncIOMotorClient(mongo_url)
        app.db = client[mongo_database]

        await init_beanie(database=app.db, document_models=[Company, Category, ProductModel, ProductItem])

    @app.on_event("shutdown")
    async def shutdown_db_client():
        app.db.close()
