import datetime

import factory

from src.core.security import get_password_hash
from src.users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = get_password_hash("abcABC123*")
    is_active = True
    is_admin = False
    created_at = datetime.datetime.now()


class UserRegisterFactory(factory.Factory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = "abcABC123*"
    confirm_password = "abcABC123*"
