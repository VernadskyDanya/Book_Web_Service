import json

from aiohttp import web
from aiohttp_pydantic.oas.typing import r201
from pydantic import ValidationError
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import selectinload

from app.db.models import Book as BookORM
from app.db.models import Genre as GenreORM
from app.handlers.models import Book


def _build_conditions(book: Book) -> Select[tuple[BookORM]]:
    """Build SQL conditions for a query."""
    # Build the base query
    query = select(BookORM).options(selectinload(BookORM.files), selectinload(BookORM.genres))  # noqa: WPS221

    if book.book_id:
        query = query.where(BookORM.book_id == book.id)
    if book.title:
        query = query.where(BookORM.title == book.title)
    if book.author:
        query = query.where(BookORM.author == book.author)
    if book.published_date:
        query = query.where(BookORM.published_date == book.published_date)
    if book.genres:
        query = query.where(BookORM.genres.any(GenreORM.genre_name.in_(book.genres)))  # noqa: WPS221

    return query


class BookView(web.View):

    async def get(self, content_type='application/json'):
        """
        Find books.

        Tags: book
        Status Codes:
            200: Successful operation
            400: Model validation error
            404: Book not found
        """
        try:
            pydantic_book = Book(**self.request.query)
        except ValidationError as e:
            error_message = {"error": "Validation error", "detail": str(e)}
            return web.Response(text=json.dumps(error_message), content_type=content_type, status=400)

        db_query = _build_conditions(pydantic_book)  # Build the database query

        async_session = async_sessionmaker(self.request.app["db"], expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(db_query)
                retrieved_books = result.fetchall()

        if not retrieved_books:
            return web.Response(text=json.dumps({"error": "No books found"}), content_type=content_type, status=404)

        pydantic_books = [Book.model_validate(book[0]) for book in retrieved_books]
        data = [model.model_dump_json() for model in pydantic_books]
        return web.Response(text=json.dumps(data), content_type=content_type)

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
