import binascii
import os

from sqlalchemy.orm import Session

from src.auth.models import Code
from src.users.models import User


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode("utf-8")


async def get_code(db: Session, code: str, code_type: str):
    return (
        db.query(Code)
        .filter(Code.code == code)
        .filter(Code.code_type == code_type)
        .first()
    )


async def get_code_for_user(db: Session, user: User, code_type: str):
    return (
        db.query(Code)
        .filter(Code.user_id == user.id)
        .filter(Code.code_type == code_type)
        .first()
    )


async def create_code(db: Session, user: User, code_type: str):
    db_code = Code(code=_generate_code(), user=user, code_type=code_type)
    db.add(db_code)
    db.commit()

    return db_code.code


async def delete_code(db: Session, code: Code):
    db.delete(code)
    db.commit()
