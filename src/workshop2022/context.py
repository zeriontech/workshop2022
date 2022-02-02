from contextvars import ContextVar

import asyncpg


class Context:
    db_pool: ContextVar[asyncpg.pool.Pool] = ContextVar('db_pool')
    zerion_sio: ContextVar['ZerionAPIStorage'] = ContextVar('zerion_sio')


CONTEXT = Context()
