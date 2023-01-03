import factory
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.users.crud import create_user
from src.users.models import User
from .userFactory import UserFactory


async def make_post_request(client: AsyncClient, response_status: int = 422, **kwargs):
    response = await client.post(**kwargs)
    print(response.content)
    assert response.status_code == response_status
    return response


async def make_get_request(client: AsyncClient, response_status: int = 422, **kwargs):
    response = await client.get(**kwargs)
    print(response.content)
    assert response.status_code == response_status
    return response


async def make_patch_request(client: AsyncClient, response_status: int = 422, **kwargs):
    response = await client.patch(**kwargs)

    assert response.status_code == response_status
    return response


async def init_db_with_test_user(db: Session, **kwargs) -> User:
    test_user = factory.build(dict, FACTORY_CLASS=UserFactory, **kwargs)
    return await create_user(db, **test_user)
