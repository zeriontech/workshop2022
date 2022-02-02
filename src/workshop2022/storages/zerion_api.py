import asyncio
from collections import defaultdict
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import socketio

from workshop2022.entities import ZerionAddressPortfolio
from workshop2022.settings import ZERION_API_TOKEN, ZERION_API_TOKEN_ORIGIN, ZERION_API_URL


@dataclass(frozen=True)
class QueueItem:
    message: str
    value: Any


class ZerionAPIStorage:
    _sio: socketio.AsyncClient
    _queues: asyncio.Queue()

    def __init__(self) -> None:
        self._sio = socketio.AsyncClient()
        self._queues = defaultdict(asyncio.Queue)
        self._register_handlers()

    async def connect(self) -> None:
        if self._sio.connected:
            return

        await self._sio.connect(
            f'{ZERION_API_URL}?api_token={ZERION_API_TOKEN}',
            headers={
                'Origin': ZERION_API_TOKEN_ORIGIN
            },
            namespaces=['/address'],
            transports=['websocket']
        )

    async def get_address_portfolio(self, address: str) -> 'hh':
        request_id = str(uuid4())

        await self._sio.emit(
            'get',
            {
                'scope': ['portfolio'],
                'payload': {
                    'address': address,
                    'currency': 'usd',
                    'request_id': request_id
                }

            },
            namespace='/address'
        )

        response = await asyncio.wait_for(
            self._read_reponse('received address portfolio', request_id),
            30
        )
        return ZerionAddressPortfolio.parse_obj(response.value['payload']['portfolio'])

    async def _read_reponse(self, message: str, request_id: str) -> QueueItem:
        while True:
            item = await self._queues[message].get()
            if item.value['meta'].get('request_id') == request_id:
                return item

            await self._queues[message].put(item)

    async def disconnect(self) -> None:
        if not self._sio.connected:
            return

        await self._sio.disconnect()

    def _register_handlers(self) -> None:
        @self._sio.on('received address portfolio', namespace='/address')
        async def _on_received_address_portfolio(data) -> None:
            await self._queues['received address portfolio'].put(QueueItem(
                message='received address portfolio',
                value=data
            ))
