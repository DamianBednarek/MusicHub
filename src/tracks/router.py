from fastapi import Depends, BackgroundTasks, UploadFile, Form
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from src.common.dependecies import get_current_user, get_db
from src.tracks.schemas import BaseTrack
from src.users.models import User
from .crud import get_all_tracks
from .dependecies import get_track_by_id
from .models import Track
from .services import upload_track, change_track_to_public_or_private

router = InferringRouter()


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

    @router.get("/tracks")
    async def list_tracks(self) -> list[BaseTrack]:
        return await get_all_tracks(self.db)

    @router.get("/info/{uuid}")
    async def get_track_info_by_id(self, track: Track = Depends(get_track_by_id)) -> BaseTrack:
        return track

    @router.patch("/make-public/{uuid}")
    async def make_track_public_or_private(self, is_public: bool,
                                           track: Track = Depends(get_track_info_by_id)) -> BaseTrack:
        return await change_track_to_public_or_private(self.db, track, is_public)
