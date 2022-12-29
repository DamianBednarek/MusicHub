from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.common.constants import CodeType
from src.common.models import Meta


class Code(Meta):
    __tablename__ = "codes"

    code = Column(String(40))
    code_type = Column(Enum(CodeType))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="code")
