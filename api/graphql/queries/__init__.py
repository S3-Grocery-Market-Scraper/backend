import strawberry
from .company import CompanyQueries
from .category import CategoryQueries
from .product_model import ProductModelQueries
from .product_item import ProductItemQueries


@strawberry.type
class Query(CompanyQueries, CategoryQueries, ProductModelQueries, ProductItemQueries):
    pass