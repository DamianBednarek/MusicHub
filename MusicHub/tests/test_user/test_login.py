import pytest
from fastapi.testclient import TestClient

from MusicHub.models.user import User
from .common import make_post_request
from .userFactory import UserFactory


@pytest.mark.login
class TestUserLogin:

    def test_login(self, client: TestClient, get_user: User):
        make_post_request(client, 200, url="/login", data={"username": get_user.email, "password": "abcABC123*"})

    @pytest.mark.parametrize("username, password", [("wrong", "credentials"), ("", "")])
    def test_bad_credentials(self, client: TestClient, username, password):
        make_post_request(client, 422, url="/login", data={"username": username, "password": password})

    def test_bad_password(self, client: TestClient, get_user: User):
        make_post_request(client, 400, url="/login", data={"username": get_user.email, "password": "badPassword"})

    def test_inactive_user(self, client: TestClient):
        inactive_user = UserFactory(is_active=False)
        make_post_request(client, 400, url="/login", data={"username": inactive_user.email, "password": "abcABC123*"})
