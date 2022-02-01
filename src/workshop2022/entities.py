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


@dataclass
class ZerionAddressPortfolio:
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
