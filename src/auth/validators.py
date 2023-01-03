from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.auth.crud import get_code_for_user
from src.auth.models import Code
from src.common.constants import CodeType
from src.exceptions.codeException import CodeException
from src.users.models import User


def validate_code(code: Code) -> None:
    time = code.created_at + timedelta(days=1)
    if time < datetime.now():
        raise CodeException("Code has expired")


async def check_if_code_already_exists(db: Session, user: User, code_type: CodeType) -> None:
    if await get_code_for_user(db, user, code_type):
        raise CodeException("Code was already sent, check your email")
