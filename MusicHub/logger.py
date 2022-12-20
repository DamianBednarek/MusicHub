import sys

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, info_file: str, error_file: str):
        super().__init__(app)

        logger.add(
            error_file,
            level="WARNING",
            backtrace=False,
            diagnose=False,
            format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | {level} | <level>{message}</level>",
        )
        logger.add(
            info_file,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} |<level>{message}</level>",
            backtrace=False,
            diagnose=False,
        )
        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
            backtrace=False,
            diagnose=False,
        )

    async def dispatch(self, request: Request, call_next):
        try:

            response = await call_next(request)
            logger.info(
                f"{request.method} {request.url} | Response status: {response.status_code}"
            )
            return response
        except Exception as e:
            logger.error(f"{request.method} {request.url} | Error message: {str(e)}")
            raise Exception(e)
