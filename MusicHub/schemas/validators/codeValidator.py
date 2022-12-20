from datetime import datetime, timedelta

from MusicHub.exceptions.codeException import CodeException
from MusicHub.models.code import Code


def validate_code(code: Code):
    time = code.created_at + timedelta(days=1)
    assert time >= datetime.now(), "Code has expired"
