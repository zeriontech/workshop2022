from http import HTTPStatus

from pydantic import BaseModel, Field


class Status(BaseModel):
    id: int
    author_address: str
    text: str
    block_number: int


class NodeLog(BaseModel):
    address: str
    removed: bool
    topics: list[str]
    data: str
    block_hash: str = Field(alias='blockHash')
    block_number: str = Field(alias='blockNumber')
    log_index: str = Field(alias='logIndex')
    transaction_hash: str = Field(alias='transactionHash')
    transaction_index: str = Field(alias='transactionIndex')

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


class AddressPortfolio(BaseModel):
    address: str
    assets_value: float
    borrowed_value: float
    deposited_value: float
    locked_value: float
    staked_value: float
    total_value: float


class ResponseSchema(BaseModel):
    code: HTTPStatus
    status: str


class SuccessResponseSchema(ResponseSchema):
    code: HTTPStatus = Field(HTTPStatus.OK)
    status: str = Field('success')


class FeedSuccessResponseSchema(SuccessResponseSchema):
    data: list[Status]
