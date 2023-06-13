import strawberry

from model import Category
from ..type.category import CategoryType


@strawberry.type
class CategoryQueries:
    category_by_id: CategoryType | None = strawberry.field(resolver=Category.try_get_by_id)
    categories: list[CategoryType] = strawberry.field(resolver=Category.read_all)