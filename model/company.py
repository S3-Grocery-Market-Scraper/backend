from __future__ import annotations

from datetime import datetime
from beanie import Document, Indexed, DeleteRules
import re


class Company(Document):
    code: Indexed(str)
    name: Indexed(str)
    created_on: datetime
    last_modified: datetime

    @classmethod
    async def read_all(cls, code: str | None = None, name: str | None = None, offset: int | None = None, limit: int | None = None,
                       sort: list[list[str, str]] | None = None) -> list[Company]:
        query = cls.find()

        if code is not None:
            query = query.find(
                cls.code == re.compile(code, flags=re.IGNORECASE)
            )

        if name is not None:
            query = query.find(
                cls.name == re.compile(name, flags=re.IGNORECASE)
            )

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
    async def try_get_by_id(cls, id: str) -> Company | None:
        return await cls.get(id)

    @classmethod
    async def get_by_id(cls, id: str) -> Company:
        company = await cls.get(id)

        if company is None:
            raise Exception("Company not found")

        return company

    @classmethod
    async def create_new(cls, code: str, name: str) -> Company:
        current_datetime = datetime.now()

        new_company = cls(
            code=code,
            name=name,
            created_on=current_datetime,
            last_modified=current_datetime
        )

        await new_company.create()

        return new_company

    async def update_self(self, code:str, name: str):
        self.code = code
        self.name = name
        self.last_modified = datetime.now()

        await self.save()

    async def delete_self(self):
        await self.delete(link_rule=DeleteRules.DELETE_LINKS)
