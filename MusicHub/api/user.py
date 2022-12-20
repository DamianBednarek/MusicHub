from fastapi.security import OAuth2PasswordRequestForm
from MusicHub.api.depends import get_db
from MusicHub.core.oauth2.oauth import oauth
from MusicHub.core.security import create_token
from MusicHub.crud import codeCrud, userCrud
from MusicHub.crud.codeCrud import confirm_user
from MusicHub.emailProvider.emailService import send_email_with_code
from MusicHub.exceptions.userException import UserException
from MusicHub.schemas import tokenSchema, userSchema
from sqlalchemy.orm import Session

from fastapi import APIRouter, BackgroundTasks, Depends, Request, status

router = APIRouter()


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
@send_email_with_code("register")
def create_user(
    user: userSchema.CreateUser,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):

    user = userCrud.create_user(
        db,
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    code = codeCrud.create_code(db, user)
    return {"signup-token": code}


@router.get("/signup-verify")
def verify_signup(code: str, db: Session = Depends(get_db)):
    confirm_user(db, code)
    return {"message": "Youe have successfully verified your account"}


@router.post("/login", response_model=tokenSchema.Token)
def login(
    db: Session = Depends(get_db), credentials: OAuth2PasswordRequestForm = Depends()
):
    user = userCrud.autenticate_user(credentials.username, credentials.password, db)
    if not user:
        raise UserException("Invalid login or password")
    if not user.is_active:
        raise UserException("User is not active")

    return {
        "access_token": create_token({"sub": user.email}),
        "token_type": "Bearer",
    }


@router.get("/google-signup")
async def login(request: Request):
    """This endpoint redirects you to the Google signin page,
    it will not work on OpenAPI documentation, open this uri in browser instead."""

    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get(
    "/auth",
    response_model=userSchema.BaseUser | tokenSchema.Token,
    include_in_schema=False,
)
async def auth(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    google_user = token.get("userinfo")
    if userCrud.get_user_by_email(db, google_user["email"]):
        return {
            "access_token": create_token({"sub": google_user["email"]}),
            "token_type": "Bearer",
        }
    else:

        user = userCrud.create_user(
            db,
            email=google_user["email"],
            first_name=google_user["given_name"],
            last_name=google_user["family_name"],
        )
        userCrud.make_user_active(db, user)
        return user
