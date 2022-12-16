import re

NAME_REGEX = "^[a-zA-Z][a-zA-Z\-\s]*$"
PASSWORD_REGEX = "^.{8,64}$"


def check_max_length(value: str, **kwargs) -> str:
    if "max_length" in kwargs:
        max_length = kwargs["max_length"]
    else:
        max_length = 30
    assert len(value) <= max_length, f"value must be less than {max_length} characters"
    return value


def validate_first_last_name(value: str) -> str:

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
