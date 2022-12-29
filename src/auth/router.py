from fastapi import BackgroundTasks, Depends, Request, APIRouter, Body
from fastapi_utils.cbv import cbv
# from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.auth.oauth2.oauth import oauth
from src.common.dependecies import get_db, user_exists
from src.core.config import settings
from src.core.security import create_token
from src.emailProvider.emailService import send_email_with_code
from src.users import schemas as user_schema
from src.users.models import User
from src.users.services import reset_password
from .crud import create_code
from .dependecies import authenticate_user, get_valid_code, get_valid_reset_code
from .models import Code
from .services import register_user, register_or_login_google, confirm_user
from .validators import check_if_code_already_exists
from ..common.constants import CodeType

router = APIRouter()


@cbv(router)
class AuthCBV:
    db: Session = Depends(get_db)

    @router.post("/sign-up")
    @send_email_with_code("register")
    async def register(self, user: user_schema.CreateUser, bg_task: BackgroundTasks) -> dict[str, str]:
        code = await register_user(self.db, user)
        return {"link": f"{settings.LINK}signup-verify?code={code}"}

    @router.get("/signup-verify")
    async def verify_signup(self, db_code: Code = Depends(get_valid_code)) -> JSONResponse:
        await confirm_user(self.db, db_code)
        return JSONResponse(content={"message": "You have successfully verified your account"})

    @router.post("/login")
    def login(self, user: User = Depends(authenticate_user)) -> JSONResponse:

        return JSONResponse(content={
            "access_token": create_token({"sub": user.email}),
            "token_type": "Bearer",
        })

    @router.get("/auth", include_in_schema=False)
    async def auth(self, request: Request) -> user_schema.BaseUser | JSONResponse:

        token = await oauth.google.authorize_access_token(request)

        result = await register_or_login_google(self.db, token.get("userinfo"))
        if isinstance(result, User):
            return result
        else:
            return JSONResponse(content={"access_token": result, "token_type": "Bearer"})

    @router.post("/password-recovery")
    async def password_recovery(
            self, password_form: user_schema.NewPasswordForm, db_code: Code = Depends(get_valid_reset_code)
    ) -> dict[str, str]:
        await reset_password(self.db, password_form.password, db_code)
        return {"message": "Password changed successfully"}

    @router.post("/reset-password")
    @send_email_with_code("password_reset")
    async def reset_password(self, bg_task: BackgroundTasks, email: str = Body(embed=True),
                             db_user: User = Depends(user_exists)) -> dict[str, str]:

        await check_if_code_already_exists(self.db, db_user, CodeType.PASSWORD_RESET)
        code = await create_code(self.db, db_user, "reset_password")
        return {"link": f"{settings.LINK}password-recovery?code={code}"}


@router.get("/google-signup")
async def google_sign(request: Request) -> None:
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)
