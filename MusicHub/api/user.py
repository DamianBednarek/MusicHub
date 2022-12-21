from fastapi import Depends
from MusicHub.schemas.userSchema import BaseUser, UpdateUser
from MusicHub.crud import userCrud
from MusicHub.api.depends import get_current_user, get_db
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

router = InferringRouter()


@cbv(router)
class UserCBV:
    current_user: BaseUser = Depends(get_current_user)
    db: Session = Depends(get_db)

    @router.get("/my-profile")
    def my_profile_info(self) -> BaseUser:
        return self.current_user

    @router.patch("/myprofile/update")
    def update_profile_info(self, user: UpdateUser) -> BaseUser:
        return userCrud.update_user(self.current_user, self.db, **user.dict())
