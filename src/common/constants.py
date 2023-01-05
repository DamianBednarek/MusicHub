from enum import Enum

ALLOWED_PICTURE_EXTENSIONS = ["jpg", "jpeg", "png"]
ALLOWED_MUSIC_EXTENSIONS = ["mp3", "wav", "aac"]


class StorageDirectories(str, Enum):
    PROFILE_AVATAR = "avatars"
    TRACK = "tracks"


class CodeType(str, Enum):
    VERIFY = "verify"
    PASSWORD_RESET = "reset_password"
