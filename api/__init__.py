from fastapi import FastAPI
from model import init_db
from .routers import init_router
from .cors import init_cors
from .config import config


app = FastAPI(
    title="Grocery shopper API",
    version="0.1",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs"
)

# Initialize modules
init_db(app, config.mongo_url, config.mongo_database)
init_router(app)
init_cors(app)