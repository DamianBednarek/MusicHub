from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.crud import get_code
from src.common.constants import CodeType
from src.common.dependecies import get_db, user_exists
from src.core.security import check_passwords_match
from src.exceptions.codeException import CodeException
from src.users.exceptions import UserException
from src.users.models import User


class GetValidCode:

    def __init__(self, code_type: CodeType):
        self.code_type = code_type

    async def __call__(self, code: str, db: Session = Depends(get_db)):
        if db_code := await get_code(db, code, self.code_type):
            return db_code
        raise CodeException("Invalid code")


async def authenticate_user(
        credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
) -> User:
    user = await user_exists(credentials.username, db)
    if not check_passwords_match(credentials.password, user.password):
        raise UserException("Passwords does not match")
    if not user.is_active:
        raise UserException("User is not active")
    return user
