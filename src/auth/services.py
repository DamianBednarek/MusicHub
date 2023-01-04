from sqlalchemy.orm import Session

from src.common.constants import CodeType
from src.users import crud as user_crud
from src.users import schemas as user_schema
from src.users.crud import make_user_active
from .crud import create_code, delete_code
from .models import Code
from .schemas import Token
from .validators import validate_code
from ..core.security import create_token


async def register_user(db: Session, user: user_schema.CreateUser) -> str:
    user = await user_crud.create_user(
        db,
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    return await create_code(db, user, CodeType.VERIFY)


async def confirm_user(db: Session, code: Code) -> None:
    validate_code(code)
    await make_user_active(db, code.user)
    await delete_code(db, code)


async def register_and_login_google(db: Session, google_user: dict) -> Token:
    if not await user_crud.get_user_by_email(db, google_user["email"]):
        user = await user_crud.create_user(
            db,
            email=google_user["email"],
            first_name=google_user["given_name"],
            last_name=google_user["family_name"],
        )
        await user_crud.make_user_active(db, user)
    return Token(access_token=create_token({"sub": google_user["email"]}), token_type="Bearer")
