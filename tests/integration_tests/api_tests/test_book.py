import logging
from datetime import date

import pytest
import pytest_asyncio
from aiohttp.test_utils import TestClient
from pytest_aiohttp.plugin import AiohttpClient

from app.create_app import create_app
from app.handlers.books.books import Book
from app.routes import API_V1_ROOT


logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture
async def http_client(aiohttp_client) -> TestClient:
    return await aiohttp_client(create_app())


@pytest.fixture
def book_json_data() -> dict:
    return {"title": "Math", "author": "Danya", "published_date": date(1999, 4, 15), "genres": ["Bestseller"]}


class TestBook:

    def test_validate_model(self, book_json_data: dict):
        book = Book(**book_json_data)
        assert book.title == "Math"

    @pytest.mark.asyncio
    async def test_get_book(self, http_client: TestClient, insert_book: None) -> None:  # noqa: WPS218
        resp = await http_client.get(
            path=API_V1_ROOT.format("books"),
            params={"title": "Master and Margarita", "author": "Mikhail Bulgakov"},
        )

        assert resp.status == 200
        books = await resp.json()
        assert len(books) == 1

        book_instance = Book.model_validate_json(books[0])

        # Assert primary book information
        assert book_instance.book_id == 1
        assert book_instance.title == "Master and Margarita"
        assert book_instance.author == "Mikhail Bulgakov"
        assert book_instance.published_date == date(1966, 12, 15)

        # Assert genre information
        assert len(book_instance.genres) == 2
        assert book_instance.genres[0].genre_name == "Fantasy"
        assert book_instance.genres[1].genre_name == "Satire"

        # Assert file information
        assert len(book_instance.files) == 2
        assert book_instance.files[0].file_size == 30
        assert book_instance.files[0].file_format == "epub"
        assert book_instance.files[1].file_size == 100
        assert book_instance.files[1].file_format == "pdf"

    @pytest.mark.asyncio
    async def test_post_book(self, aiohttp_client: AiohttpClient, book_json_data: dict):
        # TODO: Add yield fixture for cleaning database after test
        client = await aiohttp_client(create_app())
        resp = await client.post(API_V1_ROOT.format("books"), json=book_json_data)
        assert resp.status == 201

        # TODO: Add checking database directly for presence of book
