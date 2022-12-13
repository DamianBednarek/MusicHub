from fastapi import FastAPI
from MusicHub.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)
