from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from MusicHub.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
)


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
