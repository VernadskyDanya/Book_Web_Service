import logging
from typing import Final

from minio import Minio

from app.settings.s3 import S3Config


_minio_config = S3Config()

bucket_name: Final[str] = _minio_config.S3_STORAGE_BUCKET_NAME
minio_client = Minio(
    "{host}:{port}".format(host=_minio_config.S3_HOST, port=_minio_config.S3_PORT),
    access_key=_minio_config.S3_ACCESS_KEY,
    secret_key=_minio_config.S3_SECRET_KEY,
    secure=False,
)


def check_minio_readiness() -> bool:
    """Try to list buckets to check if MinIO is ready."""
    try:
        minio_client.list_buckets()
    except Exception as err:
        logging.error(f"MinIO is not ready: {err}")
        return False
    return True
