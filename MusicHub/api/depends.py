from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from MusicHub.db.db import SessionLocal
from MusicHub.core.config import settings
from jose import jwt, JWTError
from MusicHub.exceptions.jwtException import JwtException
from sqlalchemy.orm import Session
from MusicHub.crud.userCrud import get_user_by_email
from MusicHub.exceptions.userException import UserException
from MusicHub.models.user import User
from MusicHub.core.security import check_passwords_match

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
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
    user = get_user_by_email(db, email)
    if user is None:
        raise JwtException()
    return user


def user_exists(email: str, db: Session = Depends(get_db)) -> User:
    user = get_user_by_email(db, email)
    if not user:
        raise UserException("User not found")
    return user


def authenticate_user(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> User:
    user = user_exists(credentials.username, db)
    if not check_passwords_match(credentials.password, user.password):
        raise UserException("User is not active")
    if not user.is_active:
        raise UserException("User is not active")
    return user
