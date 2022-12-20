from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from MusicHub.api.user import router
from MusicHub.core.config import settings
from MusicHub.db.db import engine
from MusicHub.exceptions.handler import CustomException, user_exception_handler
from MusicHub.logger import LoggerMiddleware
from MusicHub.models import meta

meta.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)


app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_KEY)
app.add_middleware(LoggerMiddleware, info_file="info.log", error_file="errors.log")

app.add_exception_handler(CustomException, user_exception_handler)
app.include_router(router, tags=["authentication and registration"])
