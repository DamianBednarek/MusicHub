from enum import Enum

ALLOWED_PICTURE_EXTENSIONS = ["jpg", "jpeg", "png"]
ALLOWED_MUSIC_EXTENSIONS = ["mp3", "wave", "aac"]


class CodeType(str, Enum):
    VERIFY = "verify"
    PASSWORD_RESET = "reset_password"
