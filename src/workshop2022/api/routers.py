from typing import Optional

from fastapi import APIRouter

from workshop2022.entities import FeedSuccessResponseSchema
from workshop2022.services import FeedService


feed_router = APIRouter(
    prefix='/feed',
    tags=['feed']
)


@feed_router.get('/', response_model=FeedSuccessResponseSchema)
async def get_feed() -> FeedSuccessResponseSchema:
    """Get list of statuses with offset based pagination."""
    statuses = await FeedService().get_statuses()
    return FeedSuccessResponseSchema(
        data=statuses
    )
