import uuid
from datetime import datetime

from MusicHub.db.db import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class Meta(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now())
