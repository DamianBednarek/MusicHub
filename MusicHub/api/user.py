from fastapi import Depends, UploadFile, BackgroundTasks

from MusicHub.models.user import User
from MusicHub.schemas.userSchema import BaseUser, UpdateUser
from MusicHub.crud import userCrud
from MusicHub.api.depends import get_current_user, get_db
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from MusicHub.aws.bucket import upload_to_bucket
from MusicHub.schemas.validators.fileValidator import validate_file
from MusicHub.exceptions.userException import UserException

router = InferringRouter()


@cbv(router)
class UserCBV:
    current_user: User = Depends(get_current_user)
    db: Session = Depends(get_db)

    @router.get("/my-profile")
    def my_profile_info(self) -> BaseUser:
        return self.current_user

    @router.patch("/my-profile/update")
    def update_profile_info(self, user: UpdateUser) -> BaseUser:
        return userCrud.update_user(self.current_user, self.db, **user.dict())

    @router.post("/upload-photo")
    def upload_photo(
            self, file: UploadFile, background_task: BackgroundTasks
    ) -> dict[str, str]:
        try:
            validate_file(file)
            background_task.add_task(upload_to_bucket(file))
            userCrud.update_user(
                self.current_user, self.db, profile_avatar=file.filename
            )
            return {"link": file.filename}
        except AssertionError as e:
            raise UserException(str(e))
