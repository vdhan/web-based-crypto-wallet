import re


def is_valid_email(email: str) -> bool:
    pattern = re.compile(r'[a-z0-9]+([._-]?[a-z0-9]+)*@[a-z0-9]+(\.[a-z0-9]+)+', re.I)
    if pattern.fullmatch(email):
        return True

    return False
