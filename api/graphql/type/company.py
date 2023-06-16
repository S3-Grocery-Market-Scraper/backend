import strawberry

from model import Company


@strawberry.experimental.pydantic.type(model=Company)
class CompanyType:
    id: str
    code: str
    name: str
    created_on: strawberry.auto
    last_modified: strawberry.auto
