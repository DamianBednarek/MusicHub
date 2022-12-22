from unittest.mock import patch

patch('MusicHub.emailProvider.emailService.send_email_with_code', lambda *x, **y: lambda f: f).start()

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from MusicHub.api.depends import get_db
from MusicHub.core.config import settings
from MusicHub.db.db import Base
from MusicHub.main import app


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
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c
