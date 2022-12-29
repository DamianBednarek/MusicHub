from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.crud import get_code
from src.auth.models import Code
from src.common.constants import CodeType
from src.common.dependecies import get_db, user_exists
from src.core.security import check_passwords_match
from src.exceptions.codeException import CodeException
from src.users.exceptions import UserException
from src.users.models import User


async def get_valid_code(code: str, db: Session = Depends(get_db)) -> Code:
    if db_code := await get_code(db, code, CodeType.VERIFY):
        return db_code
    else:
        raise CodeException("Invalid code")


async def get_valid_reset_code(code: str, db: Session = Depends(get_db)) -> Code:
    if db_code := await get_code(db, code, CodeType.PASSWORD_RESET):
        return db_code
    else:
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
