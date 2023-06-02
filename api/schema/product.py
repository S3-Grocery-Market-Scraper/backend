from pydantic import BaseModel, Field


class ProductCreateSchema(BaseModel):
    name: str = Field("Name of the product", min_length=1, max_length=64)
    price: float = Field("Price of the product")


class ProductUpdateSchema(ProductCreateSchema):
    pass