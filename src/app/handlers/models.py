import datetime as dt

from pydantic import BaseModel, ConfigDict, constr


class Genre(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    genre_id: int | None = None
    genre_name: constr(max_length=50) | None = None


class BookFile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_id: int | None = None
    book_id: int | None = None
    file_size: int | None = None
    file_format: constr(max_length=20) | None = None


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int | None = None
    title: constr(max_length=100) | None = None
    author: constr(max_length=30) | None = None
    published_date: dt.date | None = None

    genres: list[Genre] = []
    files: list[BookFile] = []


class Error(BaseModel):
    error: str
