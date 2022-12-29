from pydantic import BaseModel, EmailStr, FileUrl, validator, Extra

from src.users.constants import MIN_STR_LENGTH, MAX_STR_LENGTH
from src.users.validators import (
    validate_confirm_password,
    validate_names,
    validate_password,
)


class BaseUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    profile_avatar: FileUrl | None = None

    _check_first_last_name = validator("first_name", "last_name", allow_reuse=True)(
        validate_names
    )

    class Config:
        orm_mode = True
        min_anystr_length = MIN_STR_LENGTH
        max_anystr_length = MAX_STR_LENGTH
        anystr_strip_whitespace = True


class NewPasswordForm(BaseModel):
    password: str
    confirm_password: str

    _validate_password = validator("password")(validate_password)
    _validate_confirm_password = validator("confirm_password")(
        validate_confirm_password
    )


class CreateUser(BaseUser, NewPasswordForm):
    pass


class UserEmailSchema(BaseModel):
    email: EmailStr


class UpdateUser(BaseModel):
    first_name: str
    last_name: str

    _check_first_last_name = validator("first_name", "last_name", allow_reuse=True)(
        validate_names
    )

    class Config:
        min_anystr_length = MIN_STR_LENGTH
        max_anystr_length = MAX_STR_LENGTH
        extra = Extra.forbid
