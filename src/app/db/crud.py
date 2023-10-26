import logging

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text


async def check_database_connection(engine: AsyncEngine) -> bool:
    try:
        async with engine.connect() as conn:
            statement = text('SELECT 1')
            await conn.execute(statement)
            return True
    except Exception as ex:
        logging.error(f"Database connection error: {ex}", exc_info=True)
        return False
