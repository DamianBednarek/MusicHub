from sqlalchemy.orm import Session

from src.tracks.models import Track


async def create_track(db: Session, data: dict) -> Track:
    track = Track(**data)
    db.add(track)
    db.commit()
    return track
