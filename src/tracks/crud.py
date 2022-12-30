from uuid import UUID

from sqlalchemy.orm import Session

from src.tracks.models import Track


async def create_track(db: Session, data: dict) -> Track:
    track = Track(**data)
    db.add(track)
    db.commit()
    return track


async def get_all_tracks(db: Session) -> list[Track]:
    return db.query(Track).all()


async def get_track_by_uuid(db: Session, uuid: UUID) -> Track:
    return db.query(Track).filter(Track.id == uuid).first()


async def make_track_public(db: Session, track: Track, is_public: bool) -> Track:
    track.is_public = is_public
    db.add(track)
    db.commit()
    return track
