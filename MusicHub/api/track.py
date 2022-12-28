from fastapi import Depends, BackgroundTasks, UploadFile, Form
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from MusicHub.api.depends import get_current_user, get_db
from MusicHub.models.user import User
from MusicHub.schemas.trackSchema import BaseTrack
from MusicHub.services import trackService

router = InferringRouter()


@cbv(router)
class TrackCBV:
    current_user: User = Depends(get_current_user)
    db: Session = Depends(get_db)

    @router.post("/upload-track")
    def upload_track(self, background_task: BackgroundTasks, file: UploadFile,
                     is_public: bool = Form()) -> BaseTrack:
        return trackService.create_track(self.db, file, background_task, created_by=self.current_user.email,
                                         is_public=is_public)
