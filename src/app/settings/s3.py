from typing import Final

from minio import Minio
from pydantic.v1 import BaseSettings


class S3Config(BaseSettings):
    S3_HOST: str = "localhost"
    S3_PORT: str = "9000"
    S3_ACCESS_KEY: str = "ACCESS_KEY"
    S3_SECRET_KEY: str = "SECRET_KEY"
    S3_STORAGE_BUCKET_NAME: str = "books-bucket"


_minio_config = S3Config()

bucket_name: Final[str] = _minio_config.S3_STORAGE_BUCKET_NAME
minio_client = Minio(
    "{host}:{port}".format(host=_minio_config.S3_HOST, port=_minio_config.S3_PORT),
    access_key=_minio_config.S3_ACCESS_KEY,
    secret_key=_minio_config.S3_SECRET_KEY,
    secure=False
)
