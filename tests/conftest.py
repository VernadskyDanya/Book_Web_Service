import asyncio
import datetime as dt
import logging
import os
import uuid
from unittest.mock import patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy_utils import drop_database

from alembic_migrations.migrator import DBMigrator
from app.db.models import Book, BookFile, Genre
from app.settings.db import DbConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["HOST_ENV"] = "localhost"
os.environ["PORT_ENV"] = "8080"
os.environ["ENVIRONMENT"] = "local"
os.environ["LOG_LEVEL"] = "DEBUG"

os.environ["DB_HOST"] = "localhost"
os.environ["DB_NAME"] = "starlab"
os.environ["DB_PORT"] = "5432"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "password"  # noqa: S105
os.environ["POSTGRES_PASSWORD"] = "password"  # noqa: S105


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
def random_database_url() -> str:
    """Generate a randomly generated database URL."""
    tmp_db_name = f"pytest.{uuid.uuid4().hex}"  # noqa: WPS237
    return DbConfig.SERVICE_CONNECTION_SETTINGS["dsn"] + "." + tmp_db_name  # noqa: WPS336


@pytest.fixture(scope='session')
def alembic_ini_folder() -> str:
    """Provide the path to the alembic.ini file."""
    root_dir = DBMigrator.find_src_directory("Book_Web_Service")
    return DBMigrator._find_path(root_dir, "src", is_file=False)  # noqa: WPS437


@pytest.fixture(scope='class')
def tmp_database_url(random_database_url: str, alembic_ini_folder: str) -> str:
    """Fixture to set up temporary database (create and make migrations)."""
    with patch('os.getcwd', return_value=alembic_ini_folder):
        with patch(
                'src.alembic_migrations.migrator.DbConfig.SERVICE_CONNECTION_SETTINGS',
                new={"dsn": random_database_url},
        ):
            migrator = DBMigrator()
            migrator.alembic_cfg.set_main_option("script_location", f"{alembic_ini_folder}/alembic_migrations")
            try:  # noqa: WPS229
                migrator.start_migrate()
                yield random_database_url
            finally:
                drop_database(random_database_url.replace("+asyncpg", ""))


@pytest_asyncio.fixture(scope='class')
async def tmp_database_engine(tmp_database_url: str) -> AsyncEngine:
    engine = create_async_engine(
        tmp_database_url,
        pool_size=10,
        max_overflow=5,
        # echo=True,  # noqa: E800
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="class")
async def insert_book(tmp_database_engine: AsyncEngine) -> None:
    """Fixture to insert a sample book record into the database.

    This fixture creates a new book with associated files and genres and inserts it into the database using
    the provided AsyncEngine.
    The book details include title, author, and published date. Multiple files and genres are associated with the book.
    """
    logger.info("Inserting a sample book into the database.")

    new_book = Book(
        title="Master and Margarita",
        author="Mikhail Bulgakov",
        published_date=dt.date(1966, 12, 15),
    )

    new_book.files.extend([
        BookFile(file_size=30, file_format="epub"),
        BookFile(file_size=100, file_format="pdf"),
    ])

    new_book.genres.extend([
        Genre(genre_name="Fantasy"),
        Genre(genre_name="Satire"),
    ])

    async_session = async_sessionmaker(tmp_database_engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            session.add(new_book)
    logger.info("Sample book inserted successfully.")

    yield

    # Delete inserted book
    async with async_session() as session:
        async with session.begin():
            await session.delete(new_book)
    logger.info("Sample book deleted successfully.")


