from aiohttp import web
from aiohttp.hdrs import METH_GET as GET

from app.handlers.default.methods import liveness, readiness

from app.handlers.books.books import BookView

API_V1_ROOT = "/api/v1/{}"  # noqa: P103

routes = (
    web.route(GET, "/readiness", readiness),
    web.route(GET, "/liveness", liveness),
    web.view(
        API_V1_ROOT.format("books"),
        BookView,
    ),
)
