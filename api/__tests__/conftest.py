import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from model import init_database
from api import app


async def clear_database(server: FastAPI) -> None:
    """Empties the test database"""
    for collection in await server.db.list_collections():
        await server.db[collection["name"]].delete_many({})


@pytest.fixture()
async def test_client() -> AsyncClient:
    await init_database('mongodb://root:1234@localhost:27017', 'grocery-shopping-test', True)

    """Async server client that handles lifespan and teardown"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac