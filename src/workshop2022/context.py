from contextvars import ContextVar

import asyncpg


class Context:
    db_pool: ContextVar[asyncpg.pool.Pool] = ContextVar('db_pool')
    zerion_api_storage: ContextVar['ZerionAPIStorage'] = ContextVar('zerion_api_storage')
    pg_address_portfolio_storage: ContextVar['PostgresAddressPortfolioStorage'] \
        = ContextVar('pg_address_portfolio_storage')
    pg_status_storage: ContextVar['PostgresStatusStorage'] = ContextVar('pg_status_storage')
    pg_params_storage: ContextVar['PostgresParamsStroage'] = ContextVar('pg_params_storage')
    eth_node_stroage: ContextVar['EthereumNodeStorage'] = ContextVar('eth_node_stroage')


CONTEXT = Context()
