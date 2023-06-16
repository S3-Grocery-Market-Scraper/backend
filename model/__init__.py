from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient
from .product_model import ProductModel
from .company import Company
from .category import Category
from .product_item import ProductItem

from beanie import init_beanie


async def init_database(mongo_url: str, mongo_database: str, use_mock: bool = False) -> AsyncIOMotorClient:
    client: AsyncIOMotorClient

    if use_mock:
        client = AsyncMongoMockClient()
    else:
        client = AsyncIOMotorClient(mongo_url)

    await init_beanie(database=client[mongo_database], document_models=[Company, Category, ProductModel, ProductItem])

    return client

