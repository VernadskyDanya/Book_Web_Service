import typing

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r201, r404
from multidict import MultiDict
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Books as BookSQL


# Use pydantic BaseModel to validate request body
class Book(BaseModel):
    id: int | None = None
    name: str
    author: str
    date_published: str  # TODO: change to date type or add validation
    genre: str | None = None

    class Config:
        from_attributes = True


class Error(BaseModel):
    error: str


class BookKeyError(Exception):
    """Error for keys that are not valid."""


def _build_conditions(**kwargs: typing.Any) -> list:
    """Build SQL conditions for a query."""
    conditions = []
    for key, value in kwargs.items():
        if value is not None:
            conditions.append(getattr(BookSQL, key) == value)
    return conditions


def _validate_fields(parameters: dict | MultiDict[str], valid_values: tuple) -> None:
    for key in parameters.keys():
        if key not in valid_values:
            raise BookKeyError(f"{key}")


class BookView(PydanticView):

    async def get(  # noqa: WPS211 (needed for support swagger)
            self,
            id: int | None = None,  # noqa: WPS125
            name: str | None = None,
            author: str | None = None,
            date_published: str | None = None,
            genre: str | None = None,
    ) -> r200[list[Book]] | r404[Error]:
        """
        Find books.

        Tags: book
        Status Codes:
            200: Successful operation
            404: Book not found
        """
        try:
            _validate_fields(self.request.rel_url.query, tuple(Book.__annotations__.keys()))
        except BookKeyError as key:
            return web.json_response(
                Error(error="Invalid query parameter key '{key}'".format(key=str(key))).model_dump_json(),
                status=400,
            )

        conditions = _build_conditions(id=id, name=name, author=author, date_published=date_published, genre=genre)

        async with AsyncSession(self.request.app["db"]) as session:
            stmt = select(BookSQL).where(*conditions)
            retrieved_books = (await session.execute(stmt)).scalars().all()
            if not retrieved_books:
                return web.json_response({"error": "Books not found"}, status=404)
        return web.json_response([Book.model_validate(book.__dict__).model_dump_json() for book in retrieved_books])

    async def post(self, book: Book) -> r201:
        """
        Add the new book.

        Tags: book
        Status Codes:
            201: The book is created
        """
        try:
            _validate_fields(await self.request.json(), tuple(Book.__annotations__.keys()))
        except BookKeyError as key:
            return web.json_response(
                Error(error="Invalid body key '{key}'".format(key=str(key))).model_dump_json(),
                status=400,
            )

        async with AsyncSession(self.request.app["db"]) as session:
            book_instance = BookSQL(**book.model_dump())
            session.add(book_instance)
            await session.commit()
            await session.refresh(book_instance)
            book_id = book_instance.book_id

        return web.json_response({"message": f"Book with ID {book_id} has been created"}, status=201)
