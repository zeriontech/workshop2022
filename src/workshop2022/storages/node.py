from typing import Any, Optional

import aiohttp

from workshop2022.entities import NodeLog
from workshop2022.settings import ETHEREUM_NODE_URL, MESSAGE_STORAGE_CONTRACT_ADDRESS


class EthereumNodeStorage:
    async def eth_new_filter(self) -> int:
        async with aiohttp.ClientSession() as session:
            request = session.post(
                url=ETHEREUM_NODE_URL,
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_newFilter',
                    'params': [{
                        'address': MESSAGE_STORAGE_CONTRACT_ADDRESS
                    }]
                }
            )
            async with request as response:
                return int(response.json()['result'], 16)

    async def eth_get_filter_changes(self, filter_id: int) -> list[NodeLog]:
        async with aiohttp.ClientSession() as session:
            request = session.post(
                url=ETHEREUM_NODE_URL,
                json={
                    'jsonrpc': '2.0',
                    'method': 'eth_getFilterChanges',
                    'params': [hex(filter_id)]
                }
            )
            async with request as response:
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

        async with aiohttp.ClientSession() as session:
            request = session.post(
                url=ETHEREUM_NODE_URL,
                json=data
            )
            async with request as response:
                return self._deserialize_node_logs(response.json()['result'])

    def _deserialize_node_logs(self, node_logs_data: list[dict[str, Any]]) -> list[NodeLog]:
        return [
            self._deserialize_node_log(node_log_data) for node_log_data in node_logs_data
        ]

    @staticmethod
    def _deserialize_node_log(node_log_data: dict[str, Any]) -> NodeLog:
        return NodeLog.parse_obj(node_log_data)
