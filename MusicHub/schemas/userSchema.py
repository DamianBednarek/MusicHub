from pydantic import BaseModel, validator, EmailStr
from MusicHub.schemas.validators.userValidator import (
    check_max_length,
    validate_first_last_name,
    validate_password,
    validate_confirm_password,
)


class BaseUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    profile_avatar: str | None = None

    _check_max_length = validator("first_name", "last_name", allow_reuse=True)(
        check_max_length
    )
    _check_first_last_name = validator("first_name", "last_name", allow_reuse=True)(
        validate_first_last_name
    )

    class Config:
        orm_mode = True


class CreateUser(BaseUser):

    password: str
    confirm_password: str

    _validate_password = validator("password")(validate_password)
    _validate_confrim_password = validator("confirm_password")(
        validate_confirm_password
    )
