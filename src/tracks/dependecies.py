from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from src.common.dependecies import get_db
from src.exceptions.trackException import TrackException
from src.tracks.crud import get_track_by_uuid
from src.tracks.models import Track


async def get_track_by_id(uuid: UUID, db: Session = Depends(get_db)) -> Track:
    if track := await get_track_by_uuid(db, uuid):
        return track
    raise TrackException("Track not found with given uuid")
