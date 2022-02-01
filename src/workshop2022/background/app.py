import asyncio
from typing import ClassVar

from workshop2022.background.tasks import BaseTask, LoadMissingLogsTask, TrackNewLogsTask


class BackgroundApplication:
    tasks: ClassVar[list[BaseTask]] = [
        LoadMissingLogsTask(),
        TrackNewLogsTask()
    ]

    async def run(self) -> None:
        await self._startup()
        await self._run_tasks()
        await self._shutdown()

    async def _startup(self) -> None:
        print('Startup application')

    async def _shutdown(self) -> None:
        print('Shutdown application')

    async def _run_tasks(self) -> None:
        print('Run tasks')
        await asyncio.gather(*(task.run() for task in self.tasks))
        print('Done')
