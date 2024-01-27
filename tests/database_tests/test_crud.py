import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import Book, BookFile, Genre


@pytest.mark.asyncio
async def test_insert(tmp_database_engine):
    new_book = Book(
        title="Master and Margarita",
        author="Mikhail Bulgakov",
        published_date=datetime.date(1966, 12, 15),
    )

    # Associate BookFile's with the Book
    new_book.files.append(BookFile(file_size=30, file_format="epub"))
    new_book.files.append(BookFile(file_size=100, file_format="pdf"))

    # Associate Genre's with the Book
    new_book.genres.append(Genre(genre_name="Fantasy"))
    new_book.genres.append(Genre(genre_name="Satire"))


    async_session = async_sessionmaker(tmp_database_engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            session.add(new_book)

    async with tmp_database_engine.begin() as conn:
        await conn.execute(
            Book.__table__.insert().values(new_book),
        )  # At this point, the changes will be committed to the database

    # Perform additional assertions to verify the insertion

    async with tmp_database_engine.connect() as conn:
        result = await conn.execute(select(Book).where(Book.title == "Master and Margarita"))
        inserted_book = await result.fetchone()

    # Assertions based on the retrieved book or any other validation
        # Assertions based on the retrieved book or any other validation
        assert inserted_book is not None
        assert inserted_book.title == "Master and Margarita"
        assert inserted_book.author == "Mikhail Bulgakov"
        assert inserted_book.published_date == datetime.date(1966, 12, 15)
        assert inserted_book.files[0].file_format == "pdf"

