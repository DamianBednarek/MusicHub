from fastapi import BackgroundTasks
from fastapi import UploadFile
from mutagen import mp3, wave, aac
from sqlalchemy.orm import Session

from src.aws.bucket import upload_to_bucket
from src.common.constants import ALLOWED_MUSIC_EXTENSIONS, StorageDirectories
from src.common.validators import validate_file
from src.core.config import settings
from .crud import create_track, make_track_public
from .models import Track
from .validators import validate_track_name
from ..AntivirusProvider.client import AntivirusScan

length_extractor = {
    "wav": lambda file: int(wave.WAVE(file.file).info.length),
    "mp3": lambda file: int(mp3.MP3(file.file).info.length),
    "aac": lambda file: int(aac.AAC(file.file).info.length)
}


async def upload_track(db: Session, file: UploadFile, background_task: BackgroundTasks, **kwargs) -> Track:
    metadata = await extract_metadata_from_file(file)
    metadata |= kwargs
    background_task.add_task(upload_to_bucket, file, StorageDirectories.TRACK)
    return await create_track(db, metadata)


async def change_track_to_public_or_private(db: Session, track: Track, is_public: bool) -> Track:
    return await make_track_public(db, track, is_public)


@AntivirusScan
def extract_metadata_from_file(file: UploadFile) -> dict:
    validate_file(file, ALLOWED_MUSIC_EXTENSIONS)
    validate_track_name(file.filename)

    track_length = length_extractor[file.filename.split(".")[-1]](file)
    metadata = {"filename": file.filename,
                "track_length": track_length,
                "file": f"{settings.STORAGE_LINK}/tracks/{file.filename}"}
    return metadata
