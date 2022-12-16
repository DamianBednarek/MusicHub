from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from MusicHub.schemas import userSchema, tokenSchema
from MusicHub.core.security import create_token
from MusicHub.api.depends import get_db
from MusicHub.crud import userCrud

router = APIRouter()


@router.post("/create-user", response_model=userSchema.BaseUser)
def create_user(user: userSchema.CreateUser, db: Session = Depends(get_db)):
    user = userCrud.create_user(user, db)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already in use",
        )


@router.post("/login", response_model=tokenSchema.Token)
def login(
    db: Session = Depends(get_db), credentials: OAuth2PasswordRequestForm = Depends()
):
    user = userCrud.autenticate_user(credentials.username, credentials.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not active",
        )

    return {
        "access_token": create_token({"sub": user.email}),
        "token_type": "Bearer",
    }
