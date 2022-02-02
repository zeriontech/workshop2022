from typing import Optional

from workshop2022.entities import NodeLog, Status


class FeedService:
    async def get_statuses(self) -> list[Status]:
        # todo:
        return []

    async def create_status_from_log(
            self,
            log: NodeLog
    ) -> None:
        # todo:
        pass
