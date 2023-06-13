from fastapi import FastAPI

from .test import router as test_router

api_url = "/api/v1"


def init_router(app: FastAPI):
    app.include_router(test_router, prefix=api_url, tags=['Testing'])
