from sqlalchemy import Column, String, Integer, ForeignKey, Boolean

from src.common.models import Meta


class Track(Meta):
    __tablename__ = "tracks"

    filename = Column(String(100), nullable=False)
    file = Column(String)
    track_length = Column(Integer)
    is_public = Column(Boolean, default=True)
    created_by = Column(String, ForeignKey("users.email"))
