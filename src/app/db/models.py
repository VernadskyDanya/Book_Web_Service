from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for ORM."""


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    author = Column(String(30))
    date_published = Column(String(30))
    genre = Column(String(30), nullable=True)  # genre is optional

    def __repr__(self) -> str:
        fields = tuple("{k}={v}".format(k=k, v=v) for k, v in self.__dict__.items())  # noqa: WPS221, WPS111
        return str(tuple(sorted(fields))).replace("\'", "")
