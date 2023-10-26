from logging import getLogger

from aiohttp.web import Application
from sqlalchemy.ext.asyncio import create_async_engine

from app.middlewares.error import error_handler
from app.routes import routes
from app.settings.app import AppConfig
from app.settings.db import DbConfig
from app.settings.s3 import bucket_name, minio_client

logger = getLogger(__name__)


def create_app() -> Application:
    """Create REST application."""
    app = Application(client_max_size=AppConfig.CLIENT_MAX_SIZE)
    app.add_routes(routes)
    app.middlewares.append(error_handler)
    app.on_startup.append(init_db)
    app.on_startup.append(init_s3)
    # app.on_cleanup.append()

    return app


async def init_db(app: Application) -> None:
    """Create an engine with a pool of connections."""
    db_url = DbConfig.SERVICE_CONNECTION_SETTINGS["dsn"]
    async_engine = create_async_engine(
        db_url,
        pool_size=10,
        max_overflow=5,
        echo=True,
    )
    app['db'] = async_engine


async def init_s3(app: Application) -> None:
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            logger.info(f"Bucket {bucket_name} created successfully.")
        else:
            logger.info(f"Bucket {bucket_name} already exists.")
    except Exception as err:
        logger.error(f"Error occurred: {err}", exc_info=True)
    else:
        app['s3'] = minio_client
        app['s3_bucket_name'] = bucket_name
