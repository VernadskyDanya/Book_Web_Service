from aiohttp import web

from app.db.crud import check_database_connection


async def liveness(request) -> web.Response:
    return web.Response(text="Server is alive!", status=200)


async def readiness(request) -> web.Response:
    if await check_database_connection(request.app):
        return web.Response(text="Server is ready!", status=200)
    else:
        return web.Response(text="Server isn't ready (db failure)", status=500)
