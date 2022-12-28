import factory
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from MusicHub.crud import userCrud
from MusicHub.models.user import User
from .userFactory import UserFactory


def make_post_request(client: TestClient, response_status: int = 422, **kwargs):
    response = client.post(**kwargs)
    print(response.content)  # TODO remove
    assert response.status_code == response_status
    return response


def make_get_request(client: TestClient, response_status: int = 422, **kwargs):
    response = client.get(**kwargs)

    assert response.status_code == response_status
    return response


def make_patch_request(client: TestClient, response_status: int = 422, **kwargs):
    response = client.patch(**kwargs)
    print(response.content)  # TODO remove
    assert response.status_code == response_status
    return response


def init_db_with_test_user(db: Session, **kwargs) -> User:
    test_user = factory.build(dict, FACTORY_CLASS=UserFactory, **kwargs)
    return userCrud.create_user(db, **test_user)
