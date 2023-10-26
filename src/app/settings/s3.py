from pydantic.v1 import BaseSettings


class S3Config(BaseSettings):
    S3_HOST: str = "localhost"
    S3_PORT: str = "9000"
    S3_ACCESS_KEY: str = "ACCESS_KEY"
    S3_SECRET_KEY: str = "SECRET_KEY"
    S3_STORAGE_BUCKET_NAME: str = "books-bucket"