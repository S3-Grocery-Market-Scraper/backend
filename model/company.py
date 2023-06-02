from __future__ import annotations

from datetime import datetime
from beanie import Document, Indexed, DeleteRules


class Company(Document):
    name: Indexed(str)
    created_on: datetime
    last_modified: datetime


    @classmethod
    async def try_get_by_id(cls, id: str) -> Company | None:
        return await cls.get(id)

    @classmethod
    async def get_by_id(cls, id: str) -> Company:
        company = await cls.get(id)

        if company is None:
            raise Exception("Company not found")

        return company

    @classmethod
    async def create_new(cls, name: str) -> Company:
        current_datetime = datetime.now()

        new_company = cls(
            name=name,
            created_on=current_datetime,
            last_modified=current_datetime
        )

        await new_company.create()

        return new_company

    async def update_self(self, name: str):
        self.name = name
        self.last_modified = datetime.now()

        await self.save()

    async def delete_self(self):
        await self.delete(link_rule=DeleteRules.DELETE_LINKS)
