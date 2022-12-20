from MusicHub.core.config import settings
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: list[EmailStr]


def register_template_body(recipient: str, link: str, hours: int = 24) -> str:
    return f"""<p>Welcome {recipient}!<p> 
Please follow the link to finish the regstration process. 
Please note that the link is valid only for {hours}h. 
<br> {link} <br>
<i>Sincerly your {settings.PROJECT_NAME} team.</i>"""
