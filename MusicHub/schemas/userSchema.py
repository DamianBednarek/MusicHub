from pydantic import BaseModel, validator, EmailStr, FileUrl
from MusicHub.schemas.validators.userValidator import (
    validate_names,
    validate_password,
    validate_confirm_password,
)

MIN_STR_LENGTH = 1
MAX_STR_LENGTH = 30


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


class CreateUser(BaseUser):

    password: str
    confirm_password: str

    _validate_password = validator("password")(validate_password)
    _validate_confrim_password = validator("confirm_password")(
        validate_confirm_password
    )
