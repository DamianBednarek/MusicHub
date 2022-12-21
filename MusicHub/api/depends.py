from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from MusicHub.db.db import SessionLocal
from MusicHub.core.config import settings
from jose import jwt, JWTError
from MusicHub.exceptions.jwtException import JwtException
from sqlalchemy.orm import Session
from MusicHub.crud.userCrud import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
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
