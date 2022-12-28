from fastapi import BackgroundTasks
from fastapi import UploadFile
from mutagen import mp3
from sqlalchemy.orm import Session

from MusicHub.aws.bucket import upload_to_bucket
from MusicHub.common.constants import ALLOWED_MUSIC_EXTENSIONS
from MusicHub.core.config import settings
from MusicHub.crud import trackCrud
from MusicHub.models.track import Track
from MusicHub.schemas.validators.fileValidator import validate_file


def create_track(db: Session, file: UploadFile, background_task: BackgroundTasks, **kwargs) -> Track:
    metadata = extract_metadata_from_file(file)
    metadata |= kwargs
    background_task.add_task(upload_to_bucket(file))
    return trackCrud.create_track(db, metadata)


def extract_metadata_from_file(file: UploadFile):
    validate_file(file, ALLOWED_MUSIC_EXTENSIONS)
    metadata = {"filename": file.filename,
                "track_length": int(mp3.MP3(file.file).info.length),
                "file": f"{settings.STORAGE_LINK}/tracks/{file.filename}"}
    return metadata
