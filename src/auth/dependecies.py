from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.crud import get_code
from src.auth.models import Code
from src.auth.schemas import Token
from src.common.constants import CodeType
from src.common.dependecies import get_db, user_exists
from src.core.security import check_passwords_match, create_token
from src.exceptions.codeException import CodeException
from src.users.exceptions import UserException


class GetValidCode:

    def __init__(self, code_type: CodeType):
        self.code_type = code_type

    async def __call__(self, code: str, db: Session = Depends(get_db)) -> Code:
        if db_code := await get_code(db, code, self.code_type):
            return db_code
        raise CodeException("Invalid code")


async def authenticate_user(credentials: OAuth2PasswordRequestForm = Depends(),
                            db: Session = Depends(get_db), ) -> Token:
    user = await user_exists(credentials.username, db)
    if not check_passwords_match(credentials.password, user.password):
        raise UserException("Passwords does not match")
    if not user.is_active:
        raise UserException("User is not active")

    return Token(access_token=create_token({"sub": user.email}), token_type="Bearer")
