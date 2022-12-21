from .handler import CustomException
from fastapi import Request, status
from fastapi.responses import JSONResponse


class JwtException(CustomException):
    def __init__(self, value: str = "Could not validate credentials"):
        self.value = value


async def jwt_exception_handler(request: Request, exc: JwtException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exc.value},
    )
