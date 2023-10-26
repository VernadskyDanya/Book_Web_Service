from __future__ import annotations

from logging import getLogger

import ujson
from aiohttp import web_exceptions
from aiohttp.typedefs import Handler
from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse, json_response

logger = getLogger(__name__)


def _represent_errors(errors: str | None) -> str | dict:
    errors_str = "" if errors is None else errors
    try:
        return ujson.loads(errors_str)
    except ValueError:
        return errors_str


@middleware
async def error_handler(request: Request, handler: Handler) -> StreamResponse:
    try:
        return await handler(request)
    except web_exceptions.HTTPClientError as ex:
        errors = _represent_errors(ex.text)
        return json_response({"errors": errors}, status=ex.status_code)
    except (  # noqa: WPS329
            web_exceptions.HTTPRedirection,
            web_exceptions.HTTPSuccessful,
    ):
        raise
    except Exception as ex:
        logger.exception(ex)
        return json_response(
            {"errors": "Unknown server error"},
            status=web_exceptions.HTTPInternalServerError.status_code,
        )
