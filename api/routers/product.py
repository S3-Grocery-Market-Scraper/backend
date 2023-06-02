from fastapi import APIRouter, HTTPException
from model import Company, Product
from ..schema import ProductCreateSchema, ProductUpdateSchema

router = APIRouter()


@router.get("/company/{company_id}/product")
async def product_read_all(company_id: str) -> list[Product]:
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found.")

    return await Product.read_all_by_company(company)


@router.post("/company/{company_id}/product")
async def product_create(company_id: str, product_schema: ProductCreateSchema) -> Product:
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found.")

    return await Product.create_new(company=company, **product_schema.dict())


@router.get("/company/{company_id}/product/{product_id}")
async def product_get(company_id: str, product_id: str) -> Product:
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found.")

    product = await Product.try_get_by_id(company, product_id)

    if product is None:
        raise HTTPException(404, "Product not found")

    return product


@router.put("/company/{company_id}/product/{product_id}")
async def product_update(company_id: str, product_id: str, product_schema: ProductUpdateSchema) -> Product:
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found.")

    product = await Product.try_get_by_id(company, product_id)

    if product is None:
        raise HTTPException(404, "Product not found")

    await product.update_self(**product_schema.dict())

    return product


@router.delete("/company/{company_id}/product/{product_id}")
async def product_delete(company_id: str, product_id: str):
    company = await Company.try_get_by_id(company_id)

    if company is None:
        raise HTTPException(404, "Company not found.")

    product = await Product.try_get_by_id(company, product_id)

    if product is None:
        raise HTTPException(404, "Product not found")

    await product.delete_self()

    return {"detail": f"Product {product.name} has been deleted."}
