import datetime as dt

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.db.models import Book, BookFile, Genre


@pytest_asyncio.fixture  # TODO: add 'class' scope
async def insert_book(tmp_database_engine: AsyncEngine):
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

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Book).options(
                    selectinload(Book.files),
                    selectinload(Book.genres),
                ).where(Book.title == "Master and Margarita"),
            )
            return result.scalar_one()
