from fastapi import UploadFile


def validate_file(file: UploadFile, allowed_extensions) -> None:
    if extension := file.filename.split(".")[-1] not in allowed_extensions:
        raise ValueError(f"{extension} extension is not allowed")
