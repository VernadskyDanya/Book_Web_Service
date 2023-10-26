from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for ORM."""


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    author: Mapped[str] = mapped_column(String(30))  # TODO: (one-to-one), table of authors
    date_published: Mapped[int] = mapped_column(String(30))
    genre: Mapped[int] = mapped_column(String(30))  # TODO: (one-to-one), table of genres

    def __repr__(self) -> str:
        fields = tuple("{k}={v}".format(k=k, v=v) for k, v in self.__dict__.items())  # noqa: WPS221, WPS111
        return str(tuple(sorted(fields))).replace("\'", "")
