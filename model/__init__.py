from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from .product import Product
from .company import Company
from api.config import config

from beanie import init_beanie

client: AsyncIOMotorClient


def init_db(app: FastAPI, mongo_url: str, mongo_database: str):
    @app.on_event("startup")
    async def startup_db_client():
        global client

        client = AsyncIOMotorClient(mongo_url)

        await init_beanie(database=client[mongo_database], document_models=[Company, Product])

    @app.on_event("shutdown")
    async def shutdown_db_client():
        global client

        client.close()
