from functools import wraps
from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.core.config import settings
from src.core.defaultResponse import DefaultResponse

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
)
subjects = {
    "register": "Finish your registration",
    "reset_password": "Password reset request"
}


async def send_email(template_name: str, recipients: list[str], body: dict) -> None:
    message = MessageSchema(
        subject=subjects[template_name],
        recipients=recipients,
        template_body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=f"{template_name}.html")


def send_email_with_code(template: str):
    """Decorator for sending email with verification or password reset code

    Args:
        template (str): template to be used, choices are 'register', 'password_reset'
    """

    def wrapper(func):
        @wraps(func)
        async def decorator(*args, **kwargs):
            response = await func(*args, **kwargs)
            user = kwargs["user"]
            bg_task = kwargs["bg_task"]
            body = {
                "link": response.msg,
                "recipient": user.email,
                "hours": settings.CODE_EXPIRATION_TIME_HOURS
            }
            bg_task.add_task(
                send_email,
                template,
                [user.email],
                body,
            )
            return DefaultResponse(msg="Successful action, check your email to finish process")

        return decorator

    return wrapper
