from pydantic import BaseModel


class SetupSchema(BaseModel):
    mongo_url: str
