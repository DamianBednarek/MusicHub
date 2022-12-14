from pydantic import BaseModel, EmailStr

from src.core.config import settings


class EmailSchema(BaseModel):
    email: list[EmailStr]


def register_template_body(recipient: str, link: str, hours: int = 24) -> str:
    return f"""<p>Welcome {recipient}!<p> 
Please follow the link to finish the registration process. 
Please note that the link is valid only for {hours}h. 
<br> {link} <br>
<i>Sincerely your {settings.PROJECT_NAME} team.</i>"""


def password_reset_template_body(recipient: str, link: str, hours: int = 24) -> str:
    return f"""<p>Hello {recipient}!<p> 
Seems like you are having trouble with password, use link below to reset your password. 
Please note that the link is valid only for {hours}h. 
<br> {link} <br>
<i>Sincerely your {settings.PROJECT_NAME} team.</i>"""
