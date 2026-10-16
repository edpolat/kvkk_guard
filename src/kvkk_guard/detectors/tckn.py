import re

def is_valid_tckn(number: str) -> bool:
    if len(number) != 11 or not number.isdigit() or number[0] == '0':
        return False
    i = 0
    even = 0
    odd = 0
    for c in number[:9]:
        if i % 2 == 0:
            odd += int(c)
        else:
            even += int(c)
        i += 1
    k = ((odd*7) - even) % 10
    l = (k + odd + even) % 10
    if k != int(number[9]) or l != int(number[10]):
        return False
    return True


def find_tckn(text: str) -> list[str]:
    candidates = re.findall(r"\b[1-9]\d{10}\b", text)
    result = []
    for candidate in candidates:
        if is_valid_tckn(candidate):
            result.append(candidate)
    return result