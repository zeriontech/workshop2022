import asyncio

import click
import uvicorn
import uvloop

from workshop2022.api.app import app as api_app
from workshop2022.background import BackgroundApplication


@click.group()
def cli() -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@cli.command()
def run_background() -> None:
    asyncio.get_event_loop().run_until_complete(BackgroundApplication().run())


@cli.command()
@click.option('--host', type=str, default='0.0.0.0')
@click.option('--port', type=int, default=8000)
def run_api(host: str, port: int) -> None:
    uvicorn.run(api_app, host=host, port=port)


if __name__ == '__main__':
    cli()
