from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    author: Mapped[str] = mapped_column(String(30))  # TODO: (one-to-one), table of authors
    date_published: Mapped[int] = mapped_column(String(30))
    genre: Mapped[int] = mapped_column(String(30))  # TODO: (one-to-one), table of genres

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, name={self.name!r}, date_published={self.date_published!r})"
