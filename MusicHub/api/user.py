from fastapi import APIRouter, Depends
from MusicHub.schemas.userSchema import BaseUser
from MusicHub.api.depends import get_current_user

router = APIRouter()


@router.get("/my-profile", response_model=BaseUser)
def my_profile_info(current_user: BaseUser = Depends(get_current_user)):
    return current_user


@router.patch("/myprofile/update", response_model=BaseUser)
def update_profile_info(current_user: BaseUser = Depends(get_current_user)):
    pass
