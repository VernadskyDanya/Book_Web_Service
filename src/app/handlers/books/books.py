from typing import List

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_pydantic import PydanticView
from pydantic import BaseModel, ValidationError
from aiohttp_pydantic.oas.typing import r200, r201, r404


# Use pydantic BaseModel to validate request body
class Book(BaseModel):
    id: int
    name: str
    author: str
    date_published: str  # TODO: change to date
    genre: str


class Error(BaseModel):
    error: str


class BookView(PydanticView):

    async def get(
            self,
            id: int | None = None,
            name: str | None = None,
            author: str | None = None,
            date_published: str | None = None,
            genre: str | None = None
    ) -> r200[List[Book]] | r404[Error]:
        """
        Find books

        Tags: book
        Status Codes:
            200: Successful operation
            404: Book not found
        """
        try:
            view_data = [Book(id=1, name='Aiohttp', author='Danya', date_publushed="15.04.2017", genre="Bestseller")]
        except ValidationError as e:
            raise HTTPBadRequest(text=f'Data is invalid: {e}')
        else:
            return web.json_response(view_data[0].model_dump_json())

    async def post(self, book: Book) -> r201[Book]:
        """
        Add the new book

        Tags: book
        Status Codes:
            201: The book is created
        """
        pass

