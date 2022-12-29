from fastapi import Request, status
from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, value: str,
                 status_code: int = status.HTTP_400_BAD_REQUEST):
        self.value = value
        self.status_code = status_code


async def user_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.value},
    )
