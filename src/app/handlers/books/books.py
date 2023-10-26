from typing import List, Optional

from aiohttp import web
from aiohttp_pydantic import PydanticView
from pydantic import BaseModel
from aiohttp_pydantic.oas.typing import r200, r201, r404
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Book as BookSQL


# Use pydantic BaseModel to validate request body
class Book(BaseModel):
    id: Optional[int] = None
    name: str
    author: str
    date_published: str  # TODO: change to date type or add validation
    genre: str

    class Config:
        orm_mode = True


class Error(BaseModel):
    error: str


def _build_conditions(**kwargs) -> List:
    """Build SQL conditions for a query."""
    conditions = []
    for key, value in kwargs.items():
        if value is not None:
            conditions.append(getattr(BookSQL, key) == value)
    return conditions


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
        conditions = _build_conditions(id=id, name=name, author=author, date_published=date_published, genre=genre)

        async with AsyncSession(self.request.app["db"]) as session:
            stmt = select(BookSQL).where(*conditions)
            result = await session.execute(stmt)
            retrieved_books = result.scalars().all()
            if not retrieved_books:
                return web.json_response({"error": "Books not found"}, status=404)
        return web.json_response([Book.model_validate(b.__dict__).model_dump_json() for b in retrieved_books])

    async def post(self, book: Book) -> r201:
        """
        Add the new book

        Tags: book
        Status Codes:
            201: The book is created
        """
        async with AsyncSession(self.request.app["db"]) as session:
            book_instance = BookSQL(**book.model_dump())
            session.add(book_instance)
            await session.commit()

        return web.Response(status=201)
