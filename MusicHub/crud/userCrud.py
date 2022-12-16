from MusicHub.schemas.userSchema import CreateUser
from MusicHub.models.user import User
from sqlalchemy.orm import Session
from MusicHub.core.security import get_password_hash, check_passwords_match


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(user: CreateUser, db: Session):
    user_dict = user.dict()
    user_dict.pop("confirm_password")
    user_dict["password"] = get_password_hash(user_dict["password"])
    if get_user_by_email(db, user_dict["email"]):
        return None
    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def autenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not check_passwords_match(password, user.password):
        return None
    return user
