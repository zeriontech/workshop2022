from typing import Optional

from asyncpg import Connection

from workshop2022.entities import Status


class FeedService:
    _connection: Connection

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_statuses(
            self,
            offset: Optional[int] = None,
            limit: int = 10,
            address: Optional[str] = None
    ) -> tuple[Optional[int], list[Status]]:
        # todo:
        return None, []
