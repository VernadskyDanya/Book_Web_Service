from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for ORM."""


association_book_genre = Table(
    'book_genre',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.book_id')),
    Column('genre_id', Integer, ForeignKey('genre.genre_id')),
)


class Book(Base):
    __tablename__ = "book"
    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(30))
    published_date: Mapped[Date] = mapped_column(Date())

    # Define the many-to-many relationship to "genre" through "book_genre"
    genres: Mapped[list["Genre"]] = relationship(
        secondary=association_book_genre, lazy="select", backref="books", cascade="all",
    )

    # Define the relationship to the BookFile table
    files: Mapped[list["BookFile"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        fields = tuple("{k}={v}".format(k=k, v=v) for k, v in self.__dict__.items())  # noqa: WPS221, WPS111
        return str(tuple(sorted(fields))).replace("\'", "")


class Genre(Base):
    __tablename__ = "genre"
    genre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    genre_name: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"Genre(genre_id={self.genre_id!r}, genre_name={self.genre_name!r})"


class BookFile(Base):
    __tablename__ = "book_file"
    file_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.book_id"))
    file_size: Mapped[int] = mapped_column()
    file_format: Mapped[str] = mapped_column(String(20))

    # Define the relationship to the Books table
    book: Mapped["Book"] = relationship(back_populates="files")

    def __repr__(self) -> str:
        return (
            f"BookFile(file_id={self.file_id!r}, book_id={self.book_id!r}, " +
            f"file_size={self.file_size!r}, file_format={self.file_format!r})"
        )
