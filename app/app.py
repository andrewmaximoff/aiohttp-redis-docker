import logging

from pathlib import Path
from functools import partial

import aioredis
import yaml

from aiohttp import web

from app.routes import init_routes


PATH = Path(__file__).parent

log = logging.getLogger(__name__)


async def init_redis(app: web.Application) -> None:
    """
    This is signal for success creating connection with redis
    """
    config = app['config']['redis']

    sub = await aioredis.create_redis(
        f'redis://{config["host"]}:{config["port"]}'
    )
    pub = await aioredis.create_redis(
        f'redis://{config["host"]}:{config["port"]}'
    )

    create_redis = partial(
        aioredis.create_redis,
        f'redis://{config["host"]}:{config["port"]}'
    )

    app['redis_sub'] = sub
    app['redis_pub'] = pub
    app['create_redis'] = create_redis


async def close_redis(app: web.Application) -> None:
    """
    This is signal for success closing connection with redis before shutdown
    """
    app['redis_sub'].close()
    app['redis_pub'].close()


def init_app() -> web.Application:
    app = web.Application()
    with open(PATH / '..' / 'config.yml', 'r') as stream:
        conf = yaml.load(stream)

    init_routes(app)
    app['config'] = conf

    logging.basicConfig(level=logging.DEBUG)
    log.debug(app['config'])

    app.on_startup.extend([init_redis])
    app.on_cleanup.extend([close_redis])

    return app
