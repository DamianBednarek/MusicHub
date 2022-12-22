import json

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from MusicHub.crud import userCrud
from .userFactory import UserFactory


@pytest.fixture
def init_db_with_user(db: Session):
    user = factory.build(dict, FACTORY_CLASS=UserFactory, email="test@example.com")
    userCrud.create_user(db, **user)


def make_request(client: TestClient, user: dict, response_status: int = 400, uri: str = "/sign-up"):
    response = client.post(uri, content=json.dumps(user))

    assert response.status_code == response_status
    return response


class TestUserRegistration:
    user = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testowy",
        "password": "abcABC123*",
        "confirm_password": "abcABC123*"
    }
    random_user = factory.build(dict, FACTORY_CLASS=UserFactory)

    def test_sign_up(self, client: TestClient):
        make_request(client, self.user, 201)

    def test_signup_email_exists(self, client, init_db_with_user):
        make_request(client, self.user)

    @pytest.mark.parametrize("password", ["abc", "          ", "",
                                          "thispasswordiswaytolongandthisisatestmesssagetocheckhifitworksornot"])
    def test_wrong_password(self, client: TestClient, password: str):
        self.user["password"] = password
        self.user["confirm_password"] = password
        make_request(client, self.user, 422)

    def test_passwords_does_not_match(self, client: TestClient):
        self.user["confirm_password"] = "notTheSamePassword"
        make_request(client, self.user, 422)

    @pytest.mark.parametrize("email", ["notValidEmail", "", "      ", "alsonotvalid.com", "test@.test@.mail"])
    def test_wrong_email(self, client: TestClient, email: str):
        self.user["email"] = email
        make_request(client, self.user, 422)

    @pytest.mark.parametrize("first_name, last_name", [(1, 2), ("!!Sadasd", "@#$%%"), ("", ""), ("12345", "43123")])
    def test_wrong_name(self, client: TestClient, first_name: str, last_name: str):
        self.user["first_name"] = first_name
        self.user["last_name"] = last_name
        make_request(client, self.user, 422)


