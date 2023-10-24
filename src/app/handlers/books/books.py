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
        conditions = []
        if id:
            conditions.append(BookSQL.id == id)
        if name:
            conditions.append(BookSQL.name == name)
        if author:
            conditions.append(BookSQL.author == author)
        if date_published:
            conditions.append(BookSQL.date_published == date_published)
        if genre:
            conditions.append(BookSQL.genre == genre)

        async with AsyncSession(self.request.app["db"]) as session:
            stmt = select(BookSQL).where(*conditions)
            result = await session.execute(stmt)
            retrieved_book = result.scalars().all()
            print(retrieved_book)
        return web.json_response([Book.model_validate(b.__dict__).model_dump_json() for b in retrieved_book])

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
