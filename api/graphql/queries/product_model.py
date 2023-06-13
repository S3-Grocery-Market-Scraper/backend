import strawberry

from model import ProductModel
from ..type.product_model import ProductModelType


@strawberry.type
class ProductModelQueries:
    product_model_by_id: ProductModelType | None = strawberry.field(resolver=ProductModel.try_get_by_id)
    product_models: list[ProductModelType] = strawberry.field(resolver=ProductModel.read_all)