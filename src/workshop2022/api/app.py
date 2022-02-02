from typing import Any, Callable, Dict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from workshop2022.api.routers import feed_router
from workshop2022.context import CONTEXT
from workshop2022.db import create_pool
from workshop2022.storages import (
    EthereumNodeStorage, PostgresAddressPortfolioStorage, PostgresParamsStroage, PostgresStatusStorage
)

APP_CONTEXT: Dict[str, Any] = {}


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(feed_router)


@app.middleware('http')
async def copy_contexts(request: Request, call_next: Callable) -> Response:
    pg_address_portfolio_storage = PostgresAddressPortfolioStorage()
    pg_status_storage = PostgresStatusStorage()
    pg_params_storage = PostgresParamsStroage()
    eth_node_stroage = EthereumNodeStorage()

    CONTEXT.db_pool = APP_CONTEXT['db_pool']
    CONTEXT.pg_address_portfolio_storage.set(pg_address_portfolio_storage)
    CONTEXT.pg_status_storage.set(pg_status_storage)
    CONTEXT.pg_params_storage.set(pg_params_storage)
    CONTEXT.eth_node_stroage.set(eth_node_stroage)

    return await call_next(request)


@app.on_event('startup')
async def startup_event() -> None:
    APP_CONTEXT['db_pool'] = await create_pool()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    if 'db_pool' in APP_CONTEXT:
        await APP_CONTEXT['db_pool'].close()
