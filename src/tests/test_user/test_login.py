import pytest
from httpx import AsyncClient

from src.users.models import User
from .common import make_post_request
from .userFactory import UserFactory


@pytest.mark.login
class TestUserLogin:

    async def test_login(self, client: AsyncClient, get_user: User):
        await make_post_request(client, 200, url="/login", data={"username": get_user.email, "password": "abcABC123*"})

    @pytest.mark.parametrize("username, password", [("wrong", "credentials"), ("21313", "112313")])
    async def test_bad_credentials(self, client: AsyncClient, username, password):
        await make_post_request(client, 400, url="/login", data={"username": username, "password": password})

    async def test_bad_password(self, client: AsyncClient, get_user: User):
        await make_post_request(client, 400, url="/login", data={"username": get_user.email, "password": "badPassword"})

    async def test_inactive_user(self, client: AsyncClient):
        inactive_user = UserFactory(is_active=False)
        await make_post_request(client, 400, url="/login",
                                data={"username": inactive_user.email, "password": "abcABC123*"})
