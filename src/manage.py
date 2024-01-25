import click
from aiohttp import web
from aiohttp_pydantic import oas

from alembic_migrations.migrator import DBMigrator
from app.create_app import create_app
from app.settings.app import AppConfig


@click.group()
def cli() -> None:
    """Init event loop, logging config etc."""
    # TODO: setup Sentry
    # TODO: setup logging


@cli.command(short_help="start app")
def start() -> None:
    """Start REST API application."""
    app = create_app()
    oas.setup(app, url_prefix="/api/docs", title_spec="Book Web Service", version_spec=AppConfig.VERSION)
    web.run_app(app, port=AppConfig.PORT)


@cli.command(short_help="migrate database")
def migrate() -> None:
    DBMigrator().start_migrate()


@cli.command(short_help="generate migration")
@click.option("--description", "-d", help="Description for the migration")
def generate_migration(description: str) -> None:
    DBMigrator().generate_migration(description)


if __name__ == "__main__":
    cli()
