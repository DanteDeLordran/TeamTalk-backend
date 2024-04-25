import re


def email_validator(email: str) -> bool:
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    return re.match(regex, email) != None


def password_validator(password: str) -> bool:
    regex = r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}'
    return re.match(regex, password) != None
