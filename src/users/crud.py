from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth.models import Code
from src.core.security import get_password_hash
from src.users.exceptions import UserException
from src.users.models import User


async def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(db: Session, **kwargs) -> User:
    try:
        if "password" in kwargs.keys():
            kwargs["password"] = get_password_hash(kwargs["password"])
        db_user = User(**kwargs)
        db.add(db_user)
        db.commit()
    except IntegrityError:
        raise UserException("This email address already exists")
    return db_user


async def make_user_active(db: Session, user: User) -> None:
    user.is_active = True
    db.commit()


async def reset_password(db: Session, db_code: Code) -> None:
    db.delete(db_code)
    db.commit()


async def update_user(user: User, db: Session, **kwargs) -> User:
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    return user
