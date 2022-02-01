from http import HTTPStatus
from typing import Optional

import pydantic
from pydantic import BaseModel, Field

from workshop2022.entities import Status


class ResponseSchema(BaseModel):
    code: HTTPStatus
    status: str


class SuccessResponseSchema(ResponseSchema):
    code: HTTPStatus = Field(HTTPStatus.OK)
    status: str = Field('success')


class PaginationSchema(BaseModel):
    next_offset: Optional[int]


class FeedSuccessResponseSchema(SuccessResponseSchema):
    data: list[pydantic.dataclasses.dataclass(Status)]
    pagination: PaginationSchema
