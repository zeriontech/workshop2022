import asyncio
from typing import ClassVar

from workshop2022.background.tasks import BaseTask, TrackNewLogsTask
from workshop2022.context import CONTEXT
from workshop2022.db import create_pool


class BackgroundApplication:
    tasks: ClassVar[list[BaseTask]] = [
        TrackNewLogsTask()
    ]

    async def run(self) -> None:
        await self._startup()
        await self._run_tasks()
        await self._shutdown()

    async def _startup(self) -> None:
        print('Startup application')
        CONTEXT.db_pool.set(await create_pool())

    async def _shutdown(self) -> None:
        print('Shutdown application')
        await CONTEXT.db_pool.get().close()

    async def _run_tasks(self) -> None:
        print('Run tasks')
        await asyncio.gather(*(task.run() for task in self.tasks))
        print('Done')
