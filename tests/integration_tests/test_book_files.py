import logging

import pytest
from pytest_aiohttp.plugin import AiohttpClient

from app.create_app import create_app
from app.routes import API_V1_ROOT


logging.basicConfig(level=logging.DEBUG)

# TODO: add fixture that returns test client


class TestBookFiles:

    @pytest.mark.asyncio
    async def test_get_book_file_200(self, aiohttp_client):
        # TODO: add yield fixture with self-clean to add book to s3
        client = await aiohttp_client(create_app())
        resp = await client.get(API_V1_ROOT.format("book_files/0"))
        assert resp.status == 200

    @pytest.mark.asyncio
    async def test_get_book_file_404(self, aiohttp_client):
        client = await aiohttp_client(create_app())
        resp = await client.get(API_V1_ROOT.format("book_files/99"))
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_post_book_file_201(self, aiohttp_client: AiohttpClient):
        # TODO: add fixture with self-cleaning
        client = await aiohttp_client(create_app())
        with open("test_data/test_book.txt", 'rb') as f:
            files = {'file': f}
            resp = await client.post(API_V1_ROOT.format("book_files/6"), data=files)
        assert resp.status == 201

    @pytest.mark.asyncio
    async def test_post_book_file_409(self, aiohttp_client: AiohttpClient):
        # TODO: add fixture that add book_file before test func start
        client = await aiohttp_client(create_app())
        with open("test_data/test_book.txt", 'rb') as f:
            files = {'file': f}
            resp = await client.post(API_V1_ROOT.format("book_files/6"), data=files)
        assert resp.status == 409
