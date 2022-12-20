from MusicHub.core.security import check_passwords_match, get_password_hash
from MusicHub.exceptions.userException import UserException
from MusicHub.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


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


def autenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not check_passwords_match(password, user.password):
        return None
    return user
