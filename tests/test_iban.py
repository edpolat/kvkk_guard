import pytest

from kvkk_guard.detectors.iban import is_valid_iban, find_iban


@pytest.mark.parametrize("iban, expected", [
    ("TR330006100519786457841326", True),
    ("TR320010009999901234567890", True),
    ("TR33 0006 1005 1978 6457 8413 26", True),   # boşluklu yazım
    ("tr330006100519786457841326", True),          # küçük harf
    ("TR340006100519786457841326", False),         # kontrol hanesi yanlış
    ("TR33000610051978645784132", False),          # 25 karakter
    ("TR3300061005197864578413261", False),        # 27 karakter
    ("DE330006100519786457841326", False),         # başka ülke
    ("TR33000610051978645784132A", False),         # harf içeriyor
    ("", False),                                   # boş metin
])
def test_is_valid_iban(iban, expected):
    assert is_valid_iban(iban) is expected


@pytest.mark.parametrize("text, expected", [
    (
        "Ödeme için IBAN: TR330006100519786457841326",
        ["TR330006100519786457841326"],
    ),
    (
        "Hesabım TR33 0006 1005 1978 6457 8413 26, teşekkürler.",
        ["TR33 0006 1005 1978 6457 8413 26"],
    ),
    (
        "TR330006100519786457841326 ve TR320010009999901234567890",
        ["TR330006100519786457841326", "TR320010009999901234567890"],
    ),
    (
        "Yanlış IBAN: TR340006100519786457841326",
        [],
    ),
    (
        "Bu metinde IBAN yok.",
        [],
    ),
])
def test_find_iban(text, expected):
    assert find_iban(text) == expected