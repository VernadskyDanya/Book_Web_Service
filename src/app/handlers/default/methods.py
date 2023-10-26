from aiohttp import web
from pydantic import BaseModel

from app.db.crud import check_database_connection

from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r503

from app.s3_storage.s3_client import check_minio_readiness


class Readiness(BaseModel):
    status: str
    sql_database: bool
    s3_storage: bool


class ReadinessView(PydanticView):
    async def get(self) -> r200[Readiness] | r503[Readiness]:
        """
        Get readiness status.

        Tags: readiness
        """
        db_status = False
        s3_status = False

        if await check_database_connection(self.request.app["db"]):
            db_status = True

        if check_minio_readiness():
            s3_status = True

        server_status = db_status and s3_status
        server_status_str = "Server is ready!" if server_status else "Server isn't ready!"

        readiness_obj = Readiness(
            status=server_status_str,
            sql_database=db_status,
            s3_storage=s3_status,
        )

        return web.json_response(readiness_obj.model_dump(), status=200 if server_status else 503)


async def liveness(request) -> web.Response:
    return web.Response(text="Server is alive!", status=200)

