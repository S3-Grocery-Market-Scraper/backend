import strawberry

from model import ProductModel
from .category import CategoryType
from .company import CompanyType


@strawberry.experimental.pydantic.type(model=ProductModel)
class ProductModelType:
    id: str
    name: str

    @strawberry.field
    async def categories(self: ProductModel) -> list[CategoryType]:
        return await self.fetch_category()

    @strawberry.field
    async def cheapest_at_company(self: ProductModel) -> CompanyType | None:
        return await self.cheapest_at_company()

    @strawberry.field
    async def cheapest_at_price(self: ProductModel) -> float | None:
        return await self.cheapest_at_price()


    created_on: strawberry.auto
    last_modified: strawberry.auto
