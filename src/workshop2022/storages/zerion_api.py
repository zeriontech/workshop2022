from uuid import uuid4

import socketio

from workshop2022.settings import ZERION_API_TOKEN, ZERION_API_TOKEN_ORIGIN, ZERION_API_URL


class ZerionAPIStorage:
    _sio: socketio.AsyncClient

    def __init__(self) -> None:
        self._sio = socketio.AsyncClient()

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

    async def get_address_portfolio(self, address: str) -> None:
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


    def on(self, namespace: str, event: str, handler) -> None:
        self._sio.on(event, handler, namespace)

    async def disconnect(self) -> None:
        if not self._sio.connected:
            return

        await self._sio.disconnect()
