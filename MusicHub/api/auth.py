from fastapi import BackgroundTasks, Depends, Request, status

from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from MusicHub.api.depends import get_db, authenticate_user
from MusicHub.core.config import settings
from MusicHub.core.oauth2.oauth import oauth
from MusicHub.core.security import create_token
from MusicHub.crud import codeCrud, userCrud
from MusicHub.crud.codeCrud import confirm_user
from MusicHub.emailProvider.emailService import send_email_with_code
from MusicHub.exceptions.codeException import CodeException
from MusicHub.schemas import tokenSchema, userSchema
from MusicHub.models.user import User

router = InferringRouter()


@cbv(router)
class AuthCBV:

    db: Session = Depends(get_db)

    @router.post("/sign-up", status_code=status.HTTP_201_CREATED)
    @send_email_with_code("register")
    def register(
        self,
        user: userSchema.CreateUser,
        background_task: BackgroundTasks,
    ) -> dict[str, str]:
        """Register new user"""
        user = userCrud.create_user(
            self.db,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        code = codeCrud.create_code(self.db, user, "verify")
        return {"link": f"{settings.LINK}signup-verify?code={code}"}

    @router.get("/signup-verify")
    def verify_signup(self, code: str) -> dict[str, str]:
        """Verify user account from link sent by email"""
        confirm_user(self.db, code)
        return {"message": "Youe have successfully verified your account"}

    @router.post("/login")
    def login(self, user: User = Depends(authenticate_user)) -> dict[str, str]:
        """Login to obtain jwt access token"""

        return {
            "access_token": create_token({"sub": user.email}),
            "token_type": "Bearer",
        }

    @router.get("/auth", include_in_schema=False)
    async def auth(self, request: Request) -> userSchema.BaseUser | tokenSchema.Token:
        """Handle creating or loging in a user from google sign page"""

        token = await oauth.google.authorize_access_token(request)
        google_user = token.get("userinfo")
        if userCrud.get_user_by_email(self.db, google_user["email"]):
            return {
                "access_token": create_token({"sub": google_user["email"]}),
                "token_type": "Bearer",
            }
        else:

            user = userCrud.create_user(
                self.db,
                email=google_user["email"],
                first_name=google_user["given_name"],
                last_name=google_user["family_name"],
            )
            userCrud.make_user_active(self.db, user)
            return user

    @router.post("/password-recovery")
    def password_recovery(
        self, code: str, password_form: userSchema.NewPasswordForm
    ) -> dict[str, str]:
        userCrud.reset_password(self.db, code, password_form.dict().get("password"))
        return {"message": "Password changed successfully"}

    @router.post("/reset-password")
    @send_email_with_code("password_reset")
    def reset_password(
        self,
        user: userSchema.ForgotPasswordUser,
        background_task: BackgroundTasks,
    ) -> dict[str, str]:
        db_user = userCrud.get_user_by_email(self.db, user.email)
        if db_user:
            code = codeCrud.create_code(self.db, db_user, "reset_password")
            return {"link": f"{settings.LINK}password-recovery?code={code}"}
        else:
            raise CodeException("No accout with given email")


@router.get("/google-signup")
async def google_sign(request: Request) -> None:
    """This endpoint redirects you to the Google signin page,
    it will not work on OpenAPI documentation, open this uri in browser instead.
    Create a new user or return token if user is already registered"""

    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)
