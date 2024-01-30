import datetime as dt
import logging

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.db.models import Book, BookFile, Genre


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="class")
async def insert_book(tmp_database_engine: AsyncEngine) -> None:
    """Fixture to insert a sample book record into the database.

    This fixture creates a new book with associated files and genres and inserts it into the database using
    the provided AsyncEngine.
    The book details include title, author, and published date. Multiple files and genres are associated with the book.
    """
    logger.info("Inserting a sample book into the database.")

    new_book = Book(
        title="Master and Margarita",
        author="Mikhail Bulgakov",
        published_date=dt.date(1966, 12, 15),
    )

    new_book.files.extend([
        BookFile(file_size=30, file_format="epub"),
        BookFile(file_size=100, file_format="pdf"),
    ])

    new_book.genres.extend([
        Genre(genre_name="Fantasy"),
        Genre(genre_name="Satire"),
    ])

    async_session = async_sessionmaker(tmp_database_engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            session.add(new_book)
    logger.info("Sample book inserted successfully.")


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
