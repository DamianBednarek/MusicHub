from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from MusicHub.core.security import check_passwords_match, get_password_hash
from MusicHub.exceptions.userException import UserException
from MusicHub.models.user import User

from .codeCrud import get_code


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, **kwargs):
    try:

        if "password" in kwargs:
            kwargs["password"] = get_password_hash(kwargs["password"])
        db_user = User(**kwargs)
        db.add(db_user)
        db.commit()
        # db.refresh(db_user)
    except IntegrityError:
        raise UserException("This email address already exists")
    return db_user


def make_user_active(db: Session, user: User):
    user.is_active = True
    db.commit()


def reset_password(db: Session, code: str, password: str):
    db_code = get_code(db, code, "reset_password")
    if db_code:
        user = db_code.user
        if check_passwords_match(password, user.password):
            raise UserException("New password must be different from old")
        user.password = get_password_hash(password)
        db.delete(db_code)
        db.commit()
    else:
        raise UserException("Invalid code")
