from fastapi.security import OAuth2PasswordBearer
from MusicHub.db.db import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
