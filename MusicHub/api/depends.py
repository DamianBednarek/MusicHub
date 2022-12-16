from MusicHub.db.db import SessionLocal
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
