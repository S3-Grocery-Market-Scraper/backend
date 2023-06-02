from fastapi import APIRouter, HTTPException
from model import Company
from ..schema import CompanyCreateSchema, CompanyUpdateSchema

router = APIRouter()


@router.get("/company")
async def company_read_all() -> list[Company]:
    return await Company.find_all().to_list()


@router.post("/company")
async def company_create(company_schema: CompanyCreateSchema) -> Company:
    return await Company.create_new(**company_schema.dict())


@router.get("/company/{company_id}")
async def company_get(company_id: str) -> Company:
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found")

    return company


@router.put("/company/{company_id}")
async def company_update(company_id: str, company_schema: CompanyUpdateSchema) -> Company:
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found")

    await company.update_self(**company_schema.dict())

    return company


@router.delete("/company/{company_id}")
async def company_delete(company_id: str):
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found")

    await company.delete_self()

    return {"detail": f"Company {company.name} has been deleted."}
