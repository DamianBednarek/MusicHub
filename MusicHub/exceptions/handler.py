from fastapi import Request, status
from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, value: str):
        self.value = value


async def user_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": exc.value},
    )
