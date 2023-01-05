import json

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.auth.crud import get_code_for_user, create_code
from src.tests.common import make_post_request
from src.users.models import User


@pytest.mark.resetPassword
class TestUserPasswordReset:

    async def test_reset_password(self, client: AsyncClient, get_user: User, db: Session):
        await make_post_request(client, 200, url="/reset-password", content=json.dumps({"email": get_user.email}))

        reset_code = await get_code_for_user(db, get_user, "reset_password")

        await make_post_request(client, 200, url="/password-recovery",
                                content=json.dumps(
                                    {"password": "newPassword123", "confirm_password": "newPassword123"}),
                                params={"code": reset_code.code})

    async def test_reset_password_multiple_request(self, client: AsyncClient, get_user):
        await make_post_request(client, 200, url="/reset-password", content=json.dumps({"email": get_user.email}))
        await make_post_request(client, 400, url="/reset-password", content=json.dumps({"email": get_user.email}))

    async def test_reset_password_wrong_email(self, client: AsyncClient):
        await make_post_request(client, 400, url="/reset-password", content=json.dumps({"email": "wrong@example.com"}))

    async def test_reset_password_wrong_code(self, client: AsyncClient):
        await make_post_request(client, 400, url="/password-recovery",
                                content=json.dumps(
                                    {"password": "newPassword123", "confirm_password": "newPassword123"}),
                                params={"code": "invalidCode"})

    @pytest.mark.parametrize("password, confirm_password",
                             [("abcABC123*", "abcABC123*"), ("newPassword123", "NotTheSame")])
    async def test_reset_password_invalid_password(self, client: AsyncClient, db: Session, get_user: User, password,
                                                   confirm_password):
        reset_code = await create_code(db, get_user, "reset_password")
        await make_post_request(client, 422, url="/password-recovery",
                                content=json.dumps({"password": password, "confirm_password": confirm_password}),
                                params={"code": reset_code})
