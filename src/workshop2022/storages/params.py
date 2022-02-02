from typing import Optional

from workshop2022.context import CONTEXT


class PostgresParamsStroage:
    async def get(self, name: str) -> Optional[str]:
        query = '''SELECT * FROM params WHERE name = $1 LIMIT 1'''

        async with CONTEXT.db_pool.get().acquire() as connection:
            record = await connection.fetchrow(query, name)
            return record['value'] if record else None

    async def set(self, name: str, value: str) -> str:
        query = '''
        INSERT INTO params (name, value, updated_at)
        VALUES ($1, $2, NOW())
        ON CONFLICT (name) DO UPDATE
        SET
            value = $2,
            updated_at = NOW()
        RETURNING value
        '''

        async with CONTEXT.db_pool.get().acquire() as connection:
            record = await connection.fetchrow(query, name, value)
            return record['value']
