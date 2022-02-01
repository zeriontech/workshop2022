from contextvars import ContextVar

import asyncpg


class Context:
    db_pool: ContextVar[asyncpg.pool.Pool] = ContextVar('db_pool')


CONTEXT = Context()
