import asyncio
from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar

from workshop2022.services import FeedService


class BaseTask(metaclass=ABCMeta):
    retry_time: ClassVar[int] = 5

    @abstractmethod
    async def task(self, *args: Any, **kwargs: Any) -> None:
        raise NotADirectoryError('Implement me')

    async def run(self, *args: Any, **kwargs: Any) -> None:
        while True:
            try:
                await self.task(*args, **kwargs)
            except NotImplementedError:
                break
            except Exception as exc:
                print(f'Got exception: {exc}:{type(exc)}. Restarting task after {self.retry_time} seconds...')
                await asyncio.sleep(self.retry_time)
                continue
            else:
                print('Task successfuly finished')
                break


class TrackNewLogsTask(BaseTask):
    async def task(self) -> None:
        while True:
            await FeedService().process_updated_logs()
            await asyncio.sleep(5)


class RequestAddressDataTask(BaseTask):
    async def task(self) -> None:
        while True:
            await FeedService().request_address_data_from_zerion_api()
            await asyncio.sleep(10*60)


class OnReceivedAddressPortfolioTask(BaseTask):
    async def task(self, address_portfolio_data: dict[str, Any]) -> None:
        await FeedService().process_received_address_portfolio(address_portfolio_data)
