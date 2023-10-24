from logging import getLogger

from aiohttp.web import Application

from app.middlewares.error import error_handler
from app.routes import routes
from app.settings.app import AppConfig

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.settings.db import DbConfig

logger = getLogger(__name__)


def create_app() -> Application:
    """Create REST application."""
    app = Application(client_max_size=AppConfig.CLIENT_MAX_SIZE)
    app.add_routes(routes)
    app.middlewares.append(error_handler)
    app.on_startup.append(init_db)
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
