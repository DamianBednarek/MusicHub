from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.orm import Session

from src.auth.models import Code
from src.aws.bucket import upload_to_bucket
from src.common.constants import ALLOWED_PICTURE_EXTENSIONS, StorageDirectories
from src.core.config import settings
from src.core.security import check_passwords_match, get_password_hash
from src.tracks.validators import validate_file
from src.users import crud
from src.users.exceptions import UserException
from src.users.models import User


async def upload_picture(file: UploadFile, bg_task: BackgroundTasks, current_user: User, db: Session) -> User:
    validate_file(file, ALLOWED_PICTURE_EXTENSIONS)
    bg_task.add_task(upload_to_bucket, file, StorageDirectories.PROFILE_AVATAR)
    return await crud.update_user(
        current_user, db, profile_avatar=f"{settings.STORAGE_LINK}/pictures/{file.filename}"
    )


async def reset_password(db: Session, password: str, db_code: Code) -> None:
    user = db_code.user
    if check_passwords_match(password, user.password):
        raise UserException("New password must be different from old", 422)
    user.password = get_password_hash(password)
    await crud.reset_password(db, db_code)
