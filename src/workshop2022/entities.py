from dataclasses import dataclass
from datetime import datetime


@dataclass
class Status:
    author: str
    text: str
    posted_at: datetime



@dataclass
class NodeLog:
    address: str
    block_hash: str
    block_number: int
    data: str
    log_index: int
    removed: bool
    topics: list[str]
    transaction_hash: str
    transaction_index: int
