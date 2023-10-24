from aiohttp import web
from aiohttp.hdrs import METH_GET as GET, METH_POST as POST

from app.handlers.book_files import book_files
from app.handlers.default.methods import liveness, readiness

from app.handlers.books.books import BookView

API_V1_ROOT = "/api/v1/{}"  # noqa: P103

routes = (
    web.route(GET, "/readiness", readiness),
    web.route(GET, "/liveness", liveness),
    web.view(API_V1_ROOT.format("books"), BookView),
    web.route(GET, API_V1_ROOT.format("book_files/{id}"), book_files.handle_download),
    web.route(POST, API_V1_ROOT.format("book_files/{id}"), book_files.handle_upload),
)
