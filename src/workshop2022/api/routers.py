from typing import Optional

from fastapi import APIRouter, Query

from workshop2022.api.schemas import FeedSuccessResponseSchema
from workshop2022.context import CONTEXT
from workshop2022.services import FeedService

feed_router = APIRouter(
    prefix='/feed',
    tags=['feed']
)


@feed_router.get('/', response_model=FeedSuccessResponseSchema)
async def get_feed(
        limit: int = Query(
            50,
            description='The number of statuses per page',
            gt=0,
            le=100
        ),
        offset: Optional[int] = Query(
            None,
            description='Start position of the requested page'
        ),
        address: Optional[str] = Query(
            None,
            description="Filter statuses by wallet's address"
        )
) -> FeedSuccessResponseSchema:
    """Get list of statuses with offset based pagination."""
    async with CONTEXT.db_pool.acquire() as connection:
        next_offset, statuses = await FeedService(connection).get_statuses(
            offset=offset,
            limit=limit,
            address=address
        )
        return FeedSuccessResponseSchema(
            data=statuses,
            pagination={
                'next_offset': next_offset
            }
        )
