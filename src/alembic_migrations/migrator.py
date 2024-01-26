import logging
import os

from alembic import command
from alembic.config import Config
from sqlalchemy_utils.functions import create_database, database_exists

from app.settings.db import DbConfig


class NoPathFound(Exception):
    """Raised when the path to file/folder isn't founded."""
    pass


class DBMigrator:
    def __init__(self):
        self.alembic_cfg = Config(self._find_path(os.getcwd(), "alembic.ini"))
        self.alembic_cfg.set_main_option("sqlalchemy.url", DbConfig.SERVICE_CONNECTION_SETTINGS["dsn"])

        current_path = os.getcwd()  # Get the current working directory
        if os.path.basename(current_path) == "src":  # if current folder is '/src'
            self.alembic_cfg.set_main_option("script_location", "alembic_migrations")
        else:
            self.alembic_cfg.set_main_option("script_location", "src/alembic_migrations")

    def start_migrate(self) -> None:
        self._create_database(DbConfig.SERVICE_CONNECTION_SETTINGS["dsn"].replace("+asyncpg", ""))
        command.upgrade(self.alembic_cfg, "head")
        logging.info("Migration has been finished")

    def generate_migration(self, description: str) -> None:
        """Generate a new migration with autogenerate."""
        self._create_database(DbConfig.SERVICE_CONNECTION_SETTINGS["dsn"].replace("+asyncpg", ""))
        command.revision(self.alembic_cfg, autogenerate=True, message=description, head="head")
        logging.info("Generating migration has been finished")

    @staticmethod
    def _find_path(root_dir: str, target_name: str, is_file=True) -> str:
        """
        Recursively find the path (either file or folder) with the specified name in the specified directory and its
        subdirectories, there are ignoring folders.

        :param root_dir: The root directory to start the search from.
        :param target_name: The name of the file or folder to search for.
        :param is_file: If True, search for files; if False, search for folders.
        :return: The path of the target file or folder if found, otherwise an empty string.
        :raises: NoPathFound: There is no target_name in root_dir.
        """

        ignore_folders = ['.mypy_cache']

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_folders]  # remove folders for local debugging
            items = files if is_file else dirs
            if target_name in items:
                return os.path.join(root, target_name)

        raise NoPathFound(f"There is no {target_name} inside of {root_dir}")

    @staticmethod
    def find_src_directory(target_directory: str, starting_directory=os.getcwd()) -> str:
        """Find the absolute path to the 'target_directory' directory in the parent hierarchy."""
        current_directory = os.path.abspath(starting_directory)

        while os.path.basename(current_directory) != target_directory:
            parent_directory = os.path.dirname(current_directory)  # Move up to the parent directory
            # If moving up has no effect, the target directory is not found
            if parent_directory == current_directory:
                raise FileNotFoundError(f"Directory '{target_directory}' not found in the path hierarchy.")
            current_directory = parent_directory  # Update current directory to the parent directory

        return current_directory

    @staticmethod
    def _create_database(url: str):
        """Create target database if it doesn't exist, otherwise do nothing."""
        if not database_exists(url):
            create_database(url)
        assert database_exists(url)
