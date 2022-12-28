from fastapi import UploadFile


def validate_file(file: UploadFile, allowed_extensions):
    assert (
            file.filename.split(".")[-1] in allowed_extensions
    ), "File extension is not allowed"
