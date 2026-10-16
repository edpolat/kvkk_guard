import re


def is_valid_iban(iban: str) -> bool:
    iban = iban.replace(" ", "").upper()
    if len(iban) != 26 or not iban.startswith("TR") or not iban[2:].isdigit():
        return False
    rearranged = iban[4:] + iban[:4]
    digits = ""
    for c in rearranged:
        digits += str(int(c, 36))
    return int(digits) % 97 == 1


def find_iban(text: str) -> list[str]:
    candidates = re.findall(r"\bTR\d{2}(?:\s?\d{4}){5}\s?\d{2}\b", text, re.IGNORECASE)
    result = []
    for candidate in candidates:
        if is_valid_iban(candidate):
            result.append(candidate)
    return result
