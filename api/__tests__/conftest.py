"""
Pytest fixtures
"""

# pylint: disable=wrong-import-position

from typing import Iterator

import pytest
from asgi_lifespan import LifespanManager
from beanie import init_beanie
from fastapi import FastAPI
from httpx import AsyncClient

from api import app
from model import Company, Product


async def clear_database(server: FastAPI) -> None:
    """Empties the test database"""
    for collection in await server.db.list_collections():
        await server.db[collection["name"]].delete_many({})


@pytest.fixture()
async def test_client() -> Iterator[AsyncClient]:
    """Async server client that handles lifespan and teardown"""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as _client:
            yield _client