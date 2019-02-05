from aiohttp import web


async def index(request: web.Request) -> web.Response:
    app = request.app
    redis = await app['create_redis']()
    count = await redis.incr('views')
    text = f'Hello from Docker! I have been seen {count} times.\n'
    return web.Response(text=text)
