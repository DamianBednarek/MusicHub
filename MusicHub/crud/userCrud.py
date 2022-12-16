from MusicHub.schemas.userSchema import CreateUser
from MusicHub.models.user import User
from sqlalchemy.orm import Session
from MusicHub.core.security import get_password_hash


def create_user(user: CreateUser, db: Session):
    user_dict = user.dict()
    user_dict.pop("confirm_password")
    user_dict["password"] = get_password_hash(user_dict["password"])
    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
