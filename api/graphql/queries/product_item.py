import strawberry

from model import ProductItem
from ..type.product_item import ProductItemType


@strawberry.type
class ProductItemQueries:
    product_item_by_id: ProductItemType | None = strawberry.field(resolver=ProductItem.try_get_by_id)
    product_items: list[ProductItemType] = strawberry.field(resolver=ProductItem.read_all)