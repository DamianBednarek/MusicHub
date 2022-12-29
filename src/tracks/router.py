from fastapi import Depends, BackgroundTasks, UploadFile, Form, APIRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from src.common.dependecies import get_current_user, get_db
from src.tracks.schemas import BaseTrack
from src.users.models import User
from .services import upload_track

router = APIRouter()


@cbv(router)
class TrackCBV:
    current_user: User = Depends(get_current_user)
    db: Session = Depends(get_db)

    @router.post("/upload-track")
    async def upload_track(self, bg_task: BackgroundTasks, file: UploadFile, is_public: bool = Form()) -> BaseTrack:
        return await upload_track(
            self.db,
            file, bg_task,
            created_by=self.current_user.email,
            is_public=is_public)
