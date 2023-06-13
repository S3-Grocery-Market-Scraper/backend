import strawberry

from model import ProductItem
from .company import CompanyType
from .product_model import ProductModelType


@strawberry.experimental.pydantic.type(model=ProductItem)
class ProductItemType:
    id: str
    company: CompanyType
    product_model: ProductModelType
    price: strawberry.auto
    created_on: strawberry.auto
    last_modified: strawberry.auto
