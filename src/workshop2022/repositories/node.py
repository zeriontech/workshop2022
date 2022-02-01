from typing import Any, ClassVar, Optional, Type

import httpx

from workshop2022.entities import NodeLog
from workshop2022.settings import ETHEREUM_NODE_URL, MESSAGE_STORAGE_CONTRACT_ADDRESS


class EthereumNodeRepository:
    Client: ClassVar[Type[httpx.AsyncClient]] = httpx.AsyncClient

    async def eth_new_filter(self) -> int:
        async with self.Client() as client:
            response = await client.post(
                url=ETHEREUM_NODE_URL,
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_newFilter',
                    'params': [{
                        'address': MESSAGE_STORAGE_CONTRACT_ADDRESS
                    }]
                }
            )
            return int(response.json()['result'], 16)

    async def eth_get_filter_changes(self, filter_id: int) -> list[NodeLog]:
        async with self.Client() as client:
            response = await client.post(
                url=ETHEREUM_NODE_URL,
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_getFilterChanges',
                    'params': [hex(filter_id)]
                }
            )
            return self._deserialize_node_logs(response.json()['result'])

    async def eth_get_logs(
            self,
            from_block: Optional[int] = None,
            to_block: Optional[int] = None,
            address: Optional[str] = None,
            topics: Optional[list[Optional[str]]] = None,
            block_hash: Optional[str] = None
    ) -> list[NodeLog]:
        data = {
            'jsonrpc': '2.0',
            'method': 'eth_getLogs',
            'params': []
        }
        params = {}
        if from_block is not None:
            params['fromBlock'] = hex(from_block)
        if to_block is not None:
            params['toBlock'] = hex(to_block)
        if address is not None:
            params['address'] = address
        if block_hash is not None:
            params['blockHash'] = block_hash
        if topics:
            params['topics'] = topics

        if params:
            data['params'].append(params)

        async with self.Client() as client:
            response = await client.post(
                url=ETHEREUM_NODE_URL,
                json=data
            )
            return self._deserialize_node_logs(response.json()['result'])

    def _deserialize_node_logs(self, node_logs_data: list[dict[str, Any]]) -> list[NodeLog]:
        return [
            self._deserialize_node_log(node_log_data) for node_log_data in node_logs_data
        ]

    @staticmethod
    def _deserialize_node_log(node_log_data: dict[str, Any]) -> NodeLog:
        return NodeLog(
            address=node_log_data['address'],
            block_hash=node_log_data['blockHash'],
            block_number=int(node_log_data['blockNumber'], 16),
            data=node_log_data['data'],
            log_index=int(node_log_data['logIndex'], 16),
            removed=node_log_data['removed'],
            topics=node_log_data['topics'],
            transaction_hash=node_log_data['transactionHash'],
            transaction_index=int(node_log_data['transactionIndex'], 16)
        )
