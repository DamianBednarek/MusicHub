from functools import wraps

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from MusicHub.core.config import settings
from MusicHub.emailProvider.email import register_template_body

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
)


templates = {"register": ["Finish your registration", register_template_body]}


async def send_email(
    subject: str,
    recipents: list[str],
    body: str,
    subtype: MessageType = MessageType.html,
) -> bool:
    message = MessageSchema(
        subject=subject,
        recipients=recipents,
        body=body,
        subtype=subtype,
    )

    fm = FastMail(conf)
    await fm.send_message(message)


def send_email_with_code(template: str):
    """Decorator for sending email with verification or password reset code

    Args:
        template (str): template to be used, choices are 'register', 'password-reset'
    """

    def wraper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            response = func(*args, **kwargs)
            verification_code = response.get("signup-token")
            email = kwargs.get("user").email
            bg_task = kwargs.get("background_task")
            bg_task.add_task(
                send_email,
                templates[template][0],
                [email],
                templates[template][1](
                    email, f"{settings.LINK}signup-verify?code={verification_code}"
                ),
            )
            return {
                "message": "You have successfully registred, check you email to verify your account"
            }

        return decorator

    return wraper
