import asyncio
from typing import Any, ClassVar

from workshop2022.background.tasks import (
    BaseTask, OnReceivedAddressPortfolioTask, RequestAddressDataTask, TrackNewLogsTask
)
from workshop2022.context import CONTEXT
from workshop2022.db import create_pool
from workshop2022.storages import (
    EthereumNodeStorage, PostgresAddressPortfolioStorage, PostgresParamsStroage, PostgresStatusStorage, ZerionAPIStorage
)


class BackgroundApplication:
    tasks: ClassVar[list[BaseTask]] = [
        TrackNewLogsTask(),
        RequestAddressDataTask()
    ]
    on_events_tasks: ClassVar[dict[tuple[str, str], BaseTask]] = {
        ('/address', 'received address portfolio'): OnReceivedAddressPortfolioTask()
    }

    async def run(self) -> None:
        await self._startup()
        await self._run_tasks()
        await self._shutdown()

    async def _startup(self) -> None:
        print('Startup application')

        pg_pool = await create_pool()
        pg_address_portfolio_storage = PostgresAddressPortfolioStorage()
        pg_status_storage = PostgresStatusStorage()
        pg_params_storage = PostgresParamsStroage()
        eth_node_stroage = EthereumNodeStorage()

        zerion_api_storage = ZerionAPIStorage()
        await zerion_api_storage.connect()
        for (namespace, event), task in self.on_events_tasks.items():
            async def handler(data: Any):
                await task.run(data)
            zerion_api_storage.on(namespace, event, handler)

        CONTEXT.db_pool.set(pg_pool)
        CONTEXT.zerion_api_storage.set(zerion_api_storage)
        CONTEXT.pg_address_portfolio_storage.set(pg_address_portfolio_storage)
        CONTEXT.pg_status_storage.set(pg_status_storage)
        CONTEXT.pg_params_storage.set(pg_params_storage)
        CONTEXT.eth_node_stroage.set(eth_node_stroage)

    async def _shutdown(self) -> None:
        print('Shutdown application')
        await CONTEXT.db_pool.get().close()
        await CONTEXT.zerion_api_storage.get().disconnect()

    async def _run_tasks(self) -> None:
        print('Run tasks')
        await asyncio.gather(*(task.run() for task in self.tasks))
        print('Done')
