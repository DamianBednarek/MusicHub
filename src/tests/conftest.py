from unittest.mock import patch, MagicMock

from src.tests.test_tracks.trackFactory import TrackFactory


class MockClass(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(MockClass, self).__call__(*args, **kwargs)


patch('src.emailProvider.emailService.send_email_with_code', lambda *x, **y: lambda f: f).start()
patch('src.AntivirusProvider.client.AntivirusScan.scan_for_malicious_content', new_callable=MockClass).start()

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from src.common.dependecies import get_db, get_current_user
from src.core.config import settings
from src.database import Base
from src.main import app
from src.tests.test_user.userFactory import UserFactory


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    connection.begin()

    db = Session(bind=connection)
    app.dependency_overrides[get_db] = lambda: db
    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
async def client(db):
    app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(app=app, base_url="http://localhost:8000") as c:
        yield c


@pytest.fixture(autouse=True)
def provide_session_to_factories(db):
    for factory in [UserFactory, TrackFactory]:
        factory._meta.sqlalchemy_session = db


@pytest.fixture()
def get_user():
    return UserFactory()


@pytest.fixture(scope="function")
def get_auth_user(db):
    user = UserFactory()
    db.flush()
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    app.dependency_overrides = {}
