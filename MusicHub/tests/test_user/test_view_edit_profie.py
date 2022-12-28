import json

import pytest
from fastapi.testclient import TestClient

from MusicHub.models.user import User
from .common import make_get_request, make_patch_request


@pytest.mark.profile
class TestUserProfile:

    def test_get_user_info(self, client: TestClient, get_auth_user: User):
        make_get_request(client, 200, url="/my-profile")

    def test_get_info_unauthorized(self, client: TestClient):
        make_get_request(client, 401, url="/my-profile")

    def test_update_info(self, client: TestClient, get_auth_user: User):
        updated_data = {"first_name": "NewName", "last_name": "NewLastName"}
        make_patch_request(client, 200, url="/my-profile/update", content=json.dumps(updated_data))

    def test_update_info_unauthorized(self, client: TestClient):
        updated_data = {"first_name": "NewName", "last_name": "NewLastName"}
        make_patch_request(client, 401, url="/my-profile/update", content=json.dumps(updated_data))