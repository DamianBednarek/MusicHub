from fastapi import Depends, UploadFile, BackgroundTasks
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from src.common.dependecies import get_current_user, get_db
from src.core.defaultResponse import DefaultResponse
from src.users import crud
from src.users.models import User
from src.users.schemas import BaseUser, UpdateUser
from src.users.services import upload_picture

router = InferringRouter()


@cbv(router)
class UserCBV:
    current_user: User = Depends(get_current_user)
    db: Session = Depends(get_db)

    @router.get("/my-profile")
    async def my_profile_info(self) -> BaseUser:
        return self.current_user

    @router.patch("/my-profile/update")
    async def update_profile_info(self, user: UpdateUser) -> BaseUser:
        return await crud.update_user(self.current_user, self.db, **user.dict())

    @router.post("/upload-photo")
    async def upload_photo(self, file: UploadFile, bg_task: BackgroundTasks) -> DefaultResponse:
        user = await upload_picture(file, bg_task, self.current_user, self.db)
        return DefaultResponse(msg="Successful action", details={"link": user.profile_avatar})
