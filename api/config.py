from pydantic import BaseSettings
import json


class Config(BaseSettings):
    mongo_url: str
    mongo_database: str


config = Config()
