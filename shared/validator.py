import re

from django.core.validators import validate_email


def phone_number_validator(mobile: str) -> bool:
    pattern = re.compile(r"(^[+0-9]{1,3})*([0-9]{10,11}$)")
    if len(mobile) == 10 and pattern.search(mobile):
        return True

def password_validator(password: str) -> bool:
    if len(password) < 7 and password.isdigit():
        return True

def email_validator(email: str) -> bool:
    try:
        validate_email(email)
    except Exception as e:
        return False
    else:
        return True