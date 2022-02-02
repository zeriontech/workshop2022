import asyncpg
from asyncpg import Pool

from workshop2022.settings import (
    POSTGRES_DB, POSTGRES_HOST, POSTGRES_MAX_SIZE, POSTGRES_MIN_SIZE, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
)


async def create_pool() -> Pool:
    return await asyncpg.create_pool(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        min_size=POSTGRES_MIN_SIZE,
        max_size=POSTGRES_MAX_SIZE,
    )
