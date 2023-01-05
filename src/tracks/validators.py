import re

from .constants import TRACK_NAME_REGEX


def validate_track_name(value: str):
    if re.match(TRACK_NAME_REGEX, value) is None:
        raise ValueError("invalid file name")
    return value
