from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.auth.router import router as auth_router
from src.common import models
from src.core.config import settings
from src.database import engine
from src.exceptions.handler import CustomException, user_exception_handler
from src.exceptions.jwtException import JwtException, jwt_exception_handler
from src.logger import LoggerMiddleware
from src.tracks.router import router as track_router
from src.users.router import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_KEY)
app.add_middleware(LoggerMiddleware, info_file="info.log", error_file="errors.log")

app.add_exception_handler(CustomException, user_exception_handler)
app.add_exception_handler(JwtException, jwt_exception_handler)

app.include_router(auth_router, tags=["authentication and registration"])
app.include_router(user_router, tags=["user"])
app.include_router(track_router, tags=["track"])
