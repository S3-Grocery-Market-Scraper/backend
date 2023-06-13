from __future__ import annotations

from datetime import datetime
from .category import Category
from .company import Company
from beanie import Document, Indexed, DeleteRules, Link


class ProductModel(Document):
    name: Indexed(str)
    categories: list[Link[Category]]
    created_on: datetime
    last_modified: datetime

    @classmethod
    async def try_get_by_id(cls, id: str) -> ProductModel | None:
        return await cls.get(id)

    async def cheapest_at_company(self) -> Company | None:
        from .product_item import ProductItem

        product_items = await ProductItem.read_all_by_product_model(self)

        if len(product_items) == 0:
            return None

        sorted_by_price = sorted(product_items, key=lambda x: x.price)

        return sorted_by_price[0].company

    async def cheapest_at_price(self) -> float | None:
        from .product_item import ProductItem

        product_items = await ProductItem.read_all_by_product_model(self)

        if len(product_items) == 0:
            return None

        sorted_by_price = sorted(product_items, key=lambda x: x.price)

        return sorted_by_price[0].price

    @classmethod
    async def get_by_id(cls, id: str) -> ProductModel:
        product = await cls.get(id)

        if product is None:
            raise Exception("ProductModel not found")

        return product

    async def fetch_category(self) -> list[Category]:
        await self.fetch_link(ProductModel.categories)

        return self.categories

    @classmethod
    async def read_all(cls, categories: str | None = None, offset: int | None = None, limit: int | None = None,
                       sort: list[list[str, str]] | None = None) -> list[ProductModel]:
        query = cls.find()

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
    async def create_new(cls, name: str, categories: list[Category]) -> ProductModel:
        current_datetime = datetime.now()

        new_product = cls(
            name=name,
            categories=categories,
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
