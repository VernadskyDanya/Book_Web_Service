from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for ORM."""


class Books(Base):
    __tablename__ = "Books"
    book_id = Column(Integer, primary_key=True)
    title = Column(String(30))
    author = Column(String(30))
    published_date = Column(Date())

    # Define the relationship to the BookFiles table
    files = relationship("BookFiles", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        fields = tuple("{k}={v}".format(k=k, v=v) for k, v in self.__dict__.items())  # noqa: WPS221, WPS111
        return str(tuple(sorted(fields))).replace("\'", "")


class BookGenreAssociation(Base):
    __tablename__ = "BookGenres"
    book_id = Column(Integer, ForeignKey("Books.book_id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("Genres.genre_id"), primary_key=True)


class Genres(Base):
    __tablename__ = "Genres"
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(50))


class BookFiles(Base):
    __tablename__ = "BookFiles"
    file_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"))
    file_size = Column(Integer)
    file_format = Column(String(20))

    # Define the relationship to the Books table
    book = relationship("Books", back_populates="files", cascade="all, delete-orphan")
