from datetime import datetime

from workshop2022.context import CONTEXT
from workshop2022.entities import Status


class PostgresStatusStorage:
    async def get_all(self) -> list[Status]:
        query = '''SELECT * FROM status ORDER BY posted_at DESC'''

        async with CONTEXT.db_pool.get().acquire() as connection:
            records = await connection.fetch(query)
            return [
                Status.parse_obj(record) for record in records
            ]

    async def insert(
            self,
            author_address: str,
            text: str,
            posted_at: datetime,
            block_number: int
    ) -> Status:
        query = '''
        INSERT INTO status (author_address, text, posted_at, block_number)
        VALUES ($1, $2, $3, $4)
        RETURNING *
        '''

        async with CONTEXT.db_pool.get().acquire() as connection:
            record = await connection.fetchrow(query, author_address, text, posted_at, block_number)
            return Status.parse_obj(record)
