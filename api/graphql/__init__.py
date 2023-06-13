import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .queries import Query
from .mutations import Mutations


def init_graphql(app: FastAPI):

    schema = strawberry.Schema(query=Query)

    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/api/graphql")
