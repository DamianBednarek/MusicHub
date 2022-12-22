import re

NAME_REGEX = "^[a-zA-Z][a-zA-Z\-\s]*$"
PASSWORD_REGEX = "^.{8,64}$"


def validate_names(value: str) -> str:
    assert re.match(
        NAME_REGEX, value
    ), "name must start and ends with letter and can contain only ' ' or '-' special characters"
    return value


def validate_password(value: str):
    assert re.match(
        PASSWORD_REGEX, value
    ), "Password must be beetween 8-64 characters and can include Upper/lower cases, digits and special characters"
    return value


def validate_confirm_password(value: str, values: dict):
    confirm_password = values.get("password")
    assert value == confirm_password, "Password and confirm_password must be the same"
    return value
