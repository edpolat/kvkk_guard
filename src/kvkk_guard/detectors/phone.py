import re

PHONE_PATTERN = re.compile(
    r"(?<!\d)"                  # öncesinde rakam olmasın
    r"(?:\+?90[\s-]?)?"         # isteğe bağlı +90 / 90
    r"\(?0?[2-5]\d{2}\)?"       # alan/operatör kodu: 532, 0532, (0212) ...
    r"[\s-]?\d{3}"              # 3 hane
    r"[\s-]?\d{2}"              # 2 hane
    r"[\s-]?\d{2}"              # 2 hane
    r"(?!\d)"                   # sonrasında rakam olmasın
)


def find_phone(text: str) -> list[str]:
    return PHONE_PATTERN.findall(text)