from aiohttp import web

from app.views import index


def init_routes(app: web.Application) -> None:
    app.add_routes([web.route('GET', '/', index)])
