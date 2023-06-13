import strawberry

from model import Category


@strawberry.experimental.pydantic.type(model=Category)
class CategoryType:
    id: str
    name: str
    created_on: strawberry.auto
    last_modified: strawberry.auto
