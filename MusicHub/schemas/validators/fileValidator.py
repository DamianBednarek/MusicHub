from fastapi import UploadFile
import re

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]


def validate_file(file: UploadFile):
    assert (
        file.filename.split(".")[-1] in ALLOWED_EXTENSIONS
    ), "File extension is not allowed"
