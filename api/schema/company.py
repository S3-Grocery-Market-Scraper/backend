from pydantic import BaseModel, Field


class CompanyCreateSchema(BaseModel):
    name: str = Field("Name of the company", min_length=1, max_length=64)


class CompanyUpdateSchema(CompanyCreateSchema):
    pass