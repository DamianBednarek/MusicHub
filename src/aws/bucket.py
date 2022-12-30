import boto3
from fastapi import UploadFile

from src.core.config import settings


def upload_to_bucket(file: UploadFile, dir: str) -> None:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    s3.upload_fileobj(file.file, settings.AWS_STORAGE_BUCKET_NAME, f"{dir}/{file.filename}")
