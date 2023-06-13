from __future__ import annotations

from datetime import datetime
from .product_model import ProductModel
from .company import Company
from beanie import Document, DeleteRules, Link


class ProductItem(Document):
    company: Link[Company]
    product_model: Link[ProductModel]
    price: float
    created_on: datetime
    last_modified: datetime

    @classmethod
    async def read_all_by_product_model(cls, product_model: ProductModel):
        return await cls.find_many(cls.product_model.id == product_model.id, fetch_links=True).to_list()

    @classmethod
    async def read_all_by_company(cls, company: Company):
        return await cls.find_many(cls.company == company).to_list()

    @classmethod
    async def read_all(cls, offset: int | None = None, limit: int | None = None,
                       sort: list[list[str, str]] | None = None) -> list[ProductItem]:
        query = cls.find(fetch_links=True)

        if offset is not None:
            query = query.skip(offset)

        if limit is not None:
            query = query.limit(limit)

        if sort is not None:
            for key, value in sort:
                if value == 'asc':
                    query = query.sort(+getattr(cls, key))
                elif value == 'desc':
                    query = query.sort(-getattr(cls, key))
                else:
                    raise Exception(f"Unknown order type '{value}'.")

        return await query.to_list()


    @classmethod
    async def try_get_by_id(cls, id: str) -> ProductItem | None:
        return await cls.get(id)

    @classmethod
    async def get_by_id(cls, id: str) -> ProductItem:
        company = await cls.get(id)

        if company is None:
            raise Exception("ProductItem not found")

        return company

    @classmethod
    async def create_new(cls, company: Company, product_model: ProductModel, price: float) -> ProductItem:
        current_datetime = datetime.now()

        new_company = cls(
            company=company,
            product_model=product_model,
            price=price,
            created_on=current_datetime,
            last_modified=current_datetime
        )

        await new_company.create()

        return new_company

    async def update_self(self, price: float):
        self.price = price
        self.last_modified = datetime.now()

        await self.save()

    async def delete_self(self):
        await self.delete(link_rule=DeleteRules.DELETE_LINKS)
