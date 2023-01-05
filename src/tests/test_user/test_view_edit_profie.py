import json

import pytest
from httpx import AsyncClient

from src.tests.common import make_get_request, make_patch_request
from src.users.models import User


@pytest.mark.profile
class TestUserProfile:

    async def test_get_user_info(self, client: AsyncClient, get_auth_user: User):
        await make_get_request(client, 200, url="/my-profile")

    async def test_get_info_unauthorized(self, client: AsyncClient):
        await make_get_request(client, 401, url="/my-profile")

    async def test_update_info(self, client: AsyncClient, get_auth_user: User):
        updated_data = {"first_name": "NewName", "last_name": "NewLastName"}
        await make_patch_request(client, 200, url="/my-profile/update", content=json.dumps(updated_data))

    async def test_update_info_unauthorized(self, client: AsyncClient):
        updated_data = {"first_name": "NewName", "last_name": "NewLastName"}
        await make_patch_request(client, 401, url="/my-profile/update", content=json.dumps(updated_data))
