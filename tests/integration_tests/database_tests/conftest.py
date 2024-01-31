import logging

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.db.models import Book


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="class")
async def inserted_book(insert_book: None, tmp_database_engine: AsyncEngine):
    """Fixture to retrieve the previously inserted book from the database.

    This fixture uses the 'insert_book' fixture to insert a sample book record into the database and then retrieves
    the inserted book using the provided AsyncEngine. The book is selected based on its title, 'Master and Margarita'.
    """
    logger.info("Retrieving the previously inserted book from the database.")

    async_session = async_sessionmaker(tmp_database_engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Book).options(
                    selectinload(Book.files),
                    selectinload(Book.genres),
                ).where(Book.title == "Master and Margarita"),
            )

            book = result.scalar_one()

    logger.info("Book retrieved successfully.")
    return book
