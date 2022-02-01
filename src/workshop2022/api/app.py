from typing import Any, Callable, Dict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from workshop2022.api.routers import feed_router
from workshop2022.context import CONTEXT
from workshop2022.db import create_pool

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
    CONTEXT.db_pool = APP_CONTEXT['db_pool']
    return await call_next(request)


@app.on_event('startup')
async def startup_event() -> None:
    APP_CONTEXT['db_pool'] = await create_pool()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    if 'db_pool' in APP_CONTEXT:
        await APP_CONTEXT['db_pool'].close()
