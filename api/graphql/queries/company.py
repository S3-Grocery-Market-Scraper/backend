import strawberry

from model import Company
from ..type.company import CompanyType


@strawberry.type
class CompanyQueries:
    company_by_id: CompanyType | None = strawberry.field(resolver=Company.try_get_by_id)
    companies: list[CompanyType] = strawberry.field(resolver=Company.read_all)