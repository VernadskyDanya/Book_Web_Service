from app.settings.base import env


class DbConfig:
    DB_USER = env.str("DB_USER", default="postgres")
    DB_PASSWORD = env.str("DB_PASSWORD", default="password")
    DB_NAME = env.str("DB_NAME", default="starlab")
    DB_HOST = env.str("DB_HOST", default="localhost")
    DB_PORT = env.str("DB_PORT", default="5432")
    DB_SCHEMA = env.str("DB_SCHEMA", default="public")

    SERVICE_CONNECTION_SETTINGS = {
        "dsn": (
            f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # NOQA: E501
        ),
        "min_size": env.int(
            "DB_SERVICE_POOL_MIN_SIZE",
            default=1,
        ),
        "max_size": env.int(
            "DB_SERVICE_POOL_MAX_SIZE",
            default=6,
        ),
        "timeout": env.int(
            "DB_SERVICE_TIMEOUT",
            default=60,
        ),
    }

