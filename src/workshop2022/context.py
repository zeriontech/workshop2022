from contextvars import ContextVar

import asyncpg
import socketio


class Context:
    db_pool: ContextVar[asyncpg.pool.Pool] = ContextVar('db_pool')
    zerion_sio: ContextVar[socketio.AsyncClient] = ContextVar('zerion_sio')


CONTEXT = Context()
