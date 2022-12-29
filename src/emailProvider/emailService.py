from functools import wraps

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.core.config import settings
from src.emailProvider.email import (
    password_reset_template_body,
    register_template_body,
)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
)

templates = {
    "register": ["Finish your registration", register_template_body],
    "password_reset": ["Password reset request", password_reset_template_body],
}


async def send_email(
        subject: str,
        recipients: list[str],
        body: str,
        subtype: MessageType = MessageType.html,
) -> bool:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=subtype,
    )

    fm = FastMail(conf)
    await fm.send_message(message)


def send_email_with_code(template: str):
    """Decorator for sending email with verification or password reset code

    Args:
        template (str): template to be used, choices are 'register', 'password_reset'
    """

    def wrapper(func):
        @wraps(func)
        async def decorator(*args, **kwargs):
            response = await func(*args, **kwargs)
            bg_task = kwargs.get("bg_task")
            email = kwargs.get("user").email

            bg_task.add_task(
                send_email,
                templates[template][0],
                [email],
                templates[template][1](email, response.get("link")),
            )
            return {"message": "Successful action, check your email to finish process"}

        return decorator

    return wrapper
