from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from MusicHub.db.db import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(30), unique=True)
    password = Column(String, nullable=False)
    profile_avatar = Column(String)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
