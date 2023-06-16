from fastapi import FastAPI
from .config import config
from model import init_database


def init_db(app: FastAPI):
    @app.on_event("startup")
    async def startup_db_client():
        app.db = await init_database(config.mongo_url, config.mongo_database, config.use_mock)

    @app.on_event("shutdown")
    async def shutdown_db_client():
        app.db.close()
