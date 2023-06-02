from __future__ import annotations

from datetime import datetime
from .company import Company
from beanie import Document, Indexed, DeleteRules, Link
from bson import ObjectId


class Product(Document):
    company: Link[Company]
    name: Indexed(str)
    price: Indexed(float)
    created_on: datetime
    last_modified: datetime

    @classmethod
    async def try_get_by_id(cls, company: Company, id: str) -> Product | None:
        return await cls.find_one(cls.id == ObjectId(id), cls.company.id == company.id, fetch_links=True)

    @classmethod
    async def get_by_id(cls, company: Company, id: str) -> Product:
        product = await cls.find_one(cls.id == id, cls.company == company)

        if product is None:
            raise Exception("Product not found")

        return product

    @classmethod
    async def read_all_by_company(cls, company: Company) -> list[Product]:
        return await cls.find(cls.company.id == company.id, fetch_links=True).to_list()

    @classmethod
    async def create_new(cls, company: Company, name: str, price: float) -> Product:
        current_datetime = datetime.now()

        new_product = cls(
            company=company,
            name=name,
            price=price,
            created_on=current_datetime,
            last_modified=current_datetime
        )

        await new_product.create()

        return new_product

    async def update_self(self, name: str, price: float):
        self.name = name
        self.price = price
        self.last_modified = datetime.now()

        await self.save()

    async def delete_self(self):
        await self.delete(link_rule=DeleteRules.DO_NOTHING)
