import datetime as dt

import pytest

from app.db.models import Book


class TestInsertedBook:
    @pytest.mark.asyncio
    async def test_inserted_book_attributes(self, insert_book: Book):
        assert insert_book is not None
        assert insert_book.title == "Master and Margarita"
        assert insert_book.author == "Mikhail Bulgakov"
        assert insert_book.published_date == dt.date(1966, 12, 15)

    @pytest.mark.asyncio
    async def test_inserted_book_files(self, insert_book: Book):
        files = insert_book.files
        assert files[0].file_format == "epub"
        assert files[1].file_format == "pdf"

    @pytest.mark.asyncio
    async def test_inserted_book_genres(self, insert_book: Book):
        genres = insert_book.genres
        assert genres[0].genre_name == "Fantasy"
        assert genres[1].genre_name == "Satire"
