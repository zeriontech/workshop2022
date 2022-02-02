from typing import Optional

from workshop2022.context import CONTEXT
from workshop2022.entities import AddressPortfolio


class PostgresAddressPortfolioStorage:
    async def upsert(
            self,
            address: str,
            assets_value: float,
            deposited_value: float,
            borrowed_value: float,
            locked_value: float,
            staked_value: float,
            total_value: float
    ) -> AddressPortfolio:
        query = '''
        INSERT INTO address_portfolio
        (address, assets_value, deposited_value, borrowed_value, locked_value, staked_value, total_value, updated_at)
        VALUES
        ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (address) DO UPDATE
        SET
            assets_value = $2,
            deposited_value = $3,
            borrowed_value = $4,
            locked_value = $5,
            staked_value = $6,
            total_value = $7
            updated_at = NOW()
        RETURNING *
        '''
        async with CONTEXT.db_pool.get().acquire() as connection:
            record = await connection.fetchrow(
                query, address, assets_value, deposited_value,
                borrowed_value, locked_value, staked_value, total_value
            )
            return AddressPortfolio.parse_obj(record)

    async def get(self, address: str) -> Optional[AddressPortfolio]:
        query = '''SELECT * FROM address_portfolio WHERE address = $1 LIMIT 1'''

        async with CONTEXT.db_pool.get().acquire() as connection:
            record = await connection.fetchrow(query, address)
            return AddressPortfolio.parse_obj(record) if record else None
