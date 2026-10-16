import re

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def find_email(text: str) -> list[str]:
    return EMAIL_PATTERN.findall(text)