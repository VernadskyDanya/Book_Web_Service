import os
import uuid
from unittest.mock import patch
from unittest.mock import MagicMock

import pytest
from sqlalchemy_utils import drop_database

from alembic_migrations.migrator import DBMigrator
from app.settings.db import DbConfig

os.environ["HOST_ENV"] = "localhost"
os.environ["PORT_ENV"] = "8080"
os.environ["ENVIRONMENT"] = "local"
os.environ["LOG_LEVEL"] = "DEBUG"

os.environ["DB_HOST"] = "localhost"
os.environ["DB_NAME"] = "starlab"
os.environ["DB_PORT"] = "5432"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "password"
os.environ["POSTGRES_PASSWORD"] = "password"


@pytest.fixture(scope='session')
def tmp_db_url() -> str:
    """Provides URL for creating temporary databases."""
    tmp_db_name = f"pytest.{uuid.uuid4().hex}"
    return DbConfig.SERVICE_CONNECTION_SETTINGS["dsn"] + "." + tmp_db_name


@pytest.fixture(scope='session')
def alembic_ini_folder() -> str:
    """Returns path to alembic.ini file."""
    root_dir = DBMigrator.find_src_directory("Book_Web_Service")
    return DBMigrator._find_path(root_dir, "src", is_file=False)


@pytest.fixture
def tmp_database(tmp_db_url: str, alembic_ini_folder: str) -> str:
    try:
        with patch('os.getcwd', return_value=alembic_ini_folder):
            with patch('src.alembic_migrations.migrator.DbConfig.SERVICE_CONNECTION_SETTINGS', new={"dsn": tmp_db_url}):
                migrator = DBMigrator()
                migrator.alembic_cfg.set_main_option("script_location", f"{alembic_ini_folder}/alembic_migrations")
                migrator.start_migrate()
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url.replace("+asyncpg", ""))
