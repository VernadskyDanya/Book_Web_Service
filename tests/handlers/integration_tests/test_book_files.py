import logging
import pytest

from app.create_app import create_app
from app.handlers.books.books import Book
from app.routes import API_V1_ROOT

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def book_json_data() -> dict:
    return {"name": "Math", "author": "Danya", "date_published": "15.04.2017", "genre": "Bestseller"}


class TestBookFiles:

    def test_insert_file(self):


    def test_read_file(self):
        book = Book(**book_json_data)
        assert book.name == "Math"


    def test_validate_model(self, book_json_data):
        book = Book(**book_json_data)
        assert book.name == "Math"

    @pytest.mark.asyncio
    async def test_post_book(self, aiohttp_client, book_json_data):
        client = await aiohttp_client(create_app())
        resp = await client.post(API_V1_ROOT.format("books"), json=book_json_data)
        assert resp.status == 201

        # # Retrieve books from the table
        # result = await conn.execute(users.select())
        # rows = await result.fetchall()
        #

    @pytest.mark.asyncio
    async def test_get_book(self, aiohttp_client):
        client = await aiohttp_client(create_app())
        resp = await client.get(API_V1_ROOT.format("books"))
        assert resp.status == 200
