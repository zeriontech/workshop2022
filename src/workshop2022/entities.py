from datetime import datetime
from http import HTTPStatus

from pydantic import BaseModel, Field


class Status(BaseModel):
    id: int
    author_address: str
    text: str
    posted_at: datetime
    block_number: int


class NodeLog(BaseModel):
    address: str
    block_hash: str
    block_number: int
    data: str
    log_index: int
    removed: bool
    topics: list[str]
    transaction_hash: str
    transaction_index: int


class ZerionAddressPortfolio(BaseModel):
    assets_value: float
    deposited_value: float
    borrowed_value: float
    locked_value: float
    staked_value: float
    arbitrum_assets_value: float
    bsc_assets_value: float
    polygon_assets_value: float
    optimism_assets_value: float
    total_value: float


class ResponseSchema(BaseModel):
    code: HTTPStatus
    status: str


class SuccessResponseSchema(ResponseSchema):
    code: HTTPStatus = Field(HTTPStatus.OK)
    status: str = Field('success')


class FeedSuccessResponseSchema(SuccessResponseSchema):
    data: list[Status]
