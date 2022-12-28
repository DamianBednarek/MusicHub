from sqlalchemy.orm import Session

from MusicHub.models.track import Track


def create_track(db: Session, data: dict) -> Track:
    track = Track(**data)
    db.add(track)
    db.commit()
    return track
