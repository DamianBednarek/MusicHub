import binascii
import os

from sqlalchemy.orm import Session

from MusicHub.exceptions.codeException import CodeException
from MusicHub.models.code import Code
from MusicHub.models.user import User
from MusicHub.schemas.validators.codeValidator import validate_code


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode("utf-8")


def get_code(db: Session, code: str, code_type: str):
    return (
        db.query(Code)
        .filter(Code.code == code)
        .filter(Code.code_type == code_type)
        .first()
    )


def get_code_for_user(db: Session, user: User, code_type: str):
    return (
        db.query(Code)
        .filter(Code.user_id == user.id)
        .filter(Code.code_type == code_type)
        .first()
    )


def create_code(db: Session, user: User, code_type: str):
    if get_code_for_user(db, user, code_type):
        raise CodeException("Code was already sent, check your email")
    db_code = Code(code=_generate_code(), user=user, code_type=code_type)
    db.add(db_code)
    db.commit()

    return db_code.code


def confirm_user(db: Session, code: str):

    if db_code := get_code(db, code, "verify"):
        validate_code(db_code)
        db_code.user.is_active = True
        db.delete(db_code)
        db.commit()
    else:
        raise CodeException("Invalid code")
