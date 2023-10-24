import logging

from aiohttp.abc import Application
from sqlalchemy.sql import text


async def check_database_connection(app: Application) -> bool:
    try:
        async with app['db'].connect() as conn:
            statement = text('SELECT 1')
            await conn.execute(statement)
            return True
    except Exception as ex:
        logging.error(f"Database connection error: {ex}", exc_info=True)
        return False
