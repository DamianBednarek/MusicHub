from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.database import SessionLocal
from src.exceptions.jwtException import JwtException
from src.users.crud import get_user_by_email
from src.users.exceptions import UserException
from src.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise JwtException()
    except JWTError:
        raise JwtException()
    user = await get_user_by_email(db, email)
    if user is None:
        raise JwtException()
    return user


async def user_exists(email: str | dict, db: Session = Depends(get_db)) -> User:
    if user := await get_user_by_email(db, email["email"] if type(email) is dict else email):
        return user
    raise UserException("User not found")
