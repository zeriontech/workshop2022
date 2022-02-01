import asyncio
from abc import ABCMeta, abstractmethod
from typing import ClassVar


class BaseTask(metaclass=ABCMeta):
    retry_time: ClassVar[int] = 5

    @abstractmethod
    async def task(self) -> None:
        raise NotADirectoryError('Implement me')

    async def run(self) -> None:
        while True:
            try:
                await self.task()
            except NotImplementedError:
                break
            except Exception as exc:
                print(f'Got exception: {exc}:{type(exc)}. Restarting task after {self.retry_time} seconds...')
                await asyncio.sleep(self.retry_time)
                continue
            else:
                print('Task successfuly finished')
                break



class LoadMissingLogsTask(BaseTask):
    async def task(self) -> None:
        print('Load missing')
        while True:
            await asyncio.sleep(5)
            print('ok')


class TrackNewLogsTask(BaseTask):
    async def task(self) -> None:
        print('Track new tasks')
        while True:
            await asyncio.sleep(2)
            print('ggwp')
