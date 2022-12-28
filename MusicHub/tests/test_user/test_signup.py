import json
from datetime import timedelta

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from MusicHub.crud import codeCrud
from MusicHub.models.user import User
from .common import make_post_request, make_get_request, init_db_with_test_user
from .userFactory import UserFactory, UserRegisterFactory


def create_code_for_user(db: Session, user: User) -> str:
    return codeCrud.create_code(db, user, "verify")


@pytest.mark.signup
class TestUserRegistration:
    user = factory.build(dict, FACTORY_CLASS=UserRegisterFactory)
    random_user = factory.build(dict, FACTORY_CLASS=UserFactory)

    @pytest.fixture()
    def create_verify_code(self, db: Session) -> str:
        user = init_db_with_test_user(db, email=self.user.get("email"))
        return create_code_for_user(db, user)

    def test_sign_up(self, client: TestClient):
        make_post_request(client, 201, url="/sign-up", content=json.dumps(self.user))

    def test_signup_email_exists(self, client: TestClient, db: Session):
        init_db_with_test_user(db, email=self.user.get("email"))
        make_post_request(client, 400, url="/sign-up", content=json.dumps(self.user))

    @pytest.mark.parametrize("password", ["abc", "          ", "",
                                          "thispasswordiswaytolongandthisisatestmesssagetocheckhifitworksornot"])
    def test_wrong_password(self, client: TestClient, password: str):
        self.user["password"] = password
        self.user["confirm_password"] = password
        make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    def test_passwords_does_not_match(self, client: TestClient):
        self.user["confirm_password"] = "notTheSamePassword"
        make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    @pytest.mark.parametrize("email", ["notValidEmail", "", "      ", "alsonotvalid.com", "test@.test@.mail"])
    def test_wrong_email(self, client: TestClient, email: str):
        self.user["email"] = email
        make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    @pytest.mark.parametrize("first_name, last_name", [(1, 2), ("!!Sadasd", "@#$%%"), ("", ""), ("12345", "43123")])
    def test_wrong_name(self, client: TestClient, first_name: str, last_name: str):
        self.user["first_name"] = first_name
        self.user["last_name"] = last_name
        make_post_request(client, url="/sign-up", content=json.dumps(self.user))

    def test_verify_code(self, client: TestClient, create_verify_code):
        make_get_request(client, 200, url="/signup-verify", params={"code": create_verify_code})

    @pytest.mark.parametrize("code", ["badCode", "", ])
    def test_bad_verify_code(self, client: TestClient, db: Session, code):
        init_db_with_test_user(db, email=self.user.get("email"))
        make_get_request(client, 400, url="/signup-verify", params={"code": code})

    def test_verify_code_expired(self, client: TestClient, db: Session, create_verify_code):
        code = codeCrud.get_code(db, create_verify_code, "verify")
        code.created_at += timedelta(days=1)
        db.add(code)
        db.commit()
        make_get_request(client, 400, url="/signup-verify", params={"code": code})
