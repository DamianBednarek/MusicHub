from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .meta import Meta


class User(Meta):
    __tablename__ = "users"

    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String)
    profile_avatar = Column(String)

    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    code = relationship("Code", back_populates="user")
