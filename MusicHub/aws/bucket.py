from fastapi import UploadFile
from MusicHub.core.config import settings
import boto3


def upload_to_bucket(file: UploadFile) -> None:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3.upload_fileobj(file.file, settings.AWS_STORAGE_BUCKET_NAME, file.filename)
