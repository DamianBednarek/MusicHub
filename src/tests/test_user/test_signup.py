import json
from datetime import timedelta

import factory
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.auth.crud import create_code, get_code
from src.users.models import User
from .common import make_post_request, make_get_request, init_db_with_test_user
from .userFactory import UserFactory, UserRegisterFactory


async def create_code_for_user(db: Session, user: User) -> str:
    return await create_code(db, user, "verify")


@pytest.mark.signup
class TestUserRegistration:
    user = factory.build(dict, FACTORY_CLASS=UserRegisterFactory)
    random_user = factory.build(dict, FACTORY_CLASS=UserFactory)

    @pytest.fixture()
    async def create_verify_code(self, db: Session) -> str:
        user = await init_db_with_test_user(db, email=self.user.get("email"))
        return await create_code_for_user(db, user)

    async def test_sign_up(self, client: AsyncClient):
        await make_post_request(client, 200, url="/sign-up", content=json.dumps(self.user))

    async def test_signup_email_exists(self, client: AsyncClient, db: Session):
        await init_db_with_test_user(db, email=self.user.get("email"))
        await make_post_request(client, 400, url="/sign-up", content=json.dumps(self.user))

    @pytest.mark.parametrize("password", ["abc", "          ", "",
                                          "thispasswordiswaytolongandthisisatestmesssagetocheckhifitworksornot"])
    async def test_wrong_password(self, client: AsyncClient, password: str):
        self.user["password"] = password
        self.user["confirm_password"] = password
        await make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    async def test_passwords_does_not_match(self, client: AsyncClient):
        self.user["confirm_password"] = "notTheSamePassword"
        await make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    @pytest.mark.parametrize("email", ["notValidEmail", "", "      ", "alsonotvalid.com", "test@.test@.mail"])
    async def test_wrong_email(self, client: AsyncClient, email: str):
        self.user["email"] = email
        await make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    @pytest.mark.parametrize("first_name, last_name", [(1, 2), ("!!Sadasd", "@#$%%"), ("", ""), ("12345", "43123")])
    async def test_wrong_name(self, client: AsyncClient, first_name: str, last_name: str):
        self.user["first_name"] = first_name
        self.user["last_name"] = last_name
        await make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    async def test_verify_code(self, client: AsyncClient, create_verify_code):
        await make_get_request(client, 200, url="/signup-verify", params={"code": create_verify_code})

    @pytest.mark.parametrize("code", ["badCode", "", ])
    async def test_bad_verify_code(self, client: AsyncClient, db: Session, code):
        await init_db_with_test_user(db, email=self.user.get("email"))
        await make_get_request(client, 400, url="/signup-verify", params={"code": code})

    async def test_verify_code_expired(self, client: AsyncClient, db: Session, create_verify_code):
        code = await get_code(db, create_verify_code, "verify")
        code.created_at += timedelta(days=1)
        db.add(code)
        db.commit()
        await make_get_request(client, 400, url="/signup-verify", params={"code": code})
