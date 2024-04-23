from app.settings.base import env


class AppConfig:
    HOST = env.str("HOST_ENV", default="localhost")
    PORT = env.int("PORT_ENV", default="8080")
    CLIENT_MAX_SIZE = env.int("CLIENT_MAX_SIZE", default=1024 * 1024 * 10)
    VERSION = "0.1.2"
    DEBUG = env.bool("DEBUG", default=False)
