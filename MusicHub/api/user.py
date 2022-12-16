from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from MusicHub.schemas.userSchema import CreateUser, BaseUser
from MusicHub.api.depends import get_db
from MusicHub.crud import userCrud

router = APIRouter()


@router.post("/create-user", response_model=BaseUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user = userCrud.create_user(user, db)
    return user
