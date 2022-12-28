import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from MusicHub.crud import codeCrud
from MusicHub.models.user import User
from .common import make_post_request


@pytest.mark.resetPassword
class TestUserPasswordReset:

    def test_reset_password(self, client: TestClient, get_user: User, db: Session):
        make_post_request(client, 200, url="/reset-password", content=json.dumps({"email": get_user.email}))

        reset_code = codeCrud.get_code_for_user(db, get_user, "reset_password")

        make_post_request(client, 200, url="/password-recovery",
                          content=json.dumps({"password": "newPassword123", "confirm_password": "newPassword123"}),
                          params={"code": reset_code.code})

    def test_reset_password_multiple_request(self, client: TestClient, get_user):
        make_post_request(client, 200, url="/reset-password", content=json.dumps({"email": get_user.email}))
        make_post_request(client, 400, url="/reset-password", content=json.dumps({"email": get_user.email}))

    def test_reset_password_wrong_email(self, client: TestClient):
        make_post_request(client, 400, url="/reset-password", content=json.dumps({"email": "wrong@example.com"}))

    def test_reset_password_wrong_code(self, client: TestClient):
        make_post_request(client, 422, url="/password-recovery",
                          content=json.dumps({"password": "newPassword123", "confirm_password": "newPassword123"}),
                          params={"code": "invalidCode"})

    @pytest.mark.parametrize("password, confirm_password",
                             [("abcABC123*", "abcABC123*"), ("newPassword123", "NotTheSame")])
    def test_reset_password_invalid_password(self, client: TestClient, db: Session, get_user: User, password,
                                             confirm_password):
        reset_code = codeCrud.create_code(db, get_user, "reset_password")
        make_post_request(client, 422, url="/password-recovery",
                          content=json.dumps({"password": password, "confirm_password": confirm_password}),
                          params={"code": reset_code})
