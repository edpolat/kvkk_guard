import pytest

from kvkk_guard.detectors.tckn import is_valid_tckn, find_tckn


@pytest.mark.parametrize("number, expected", [
    ("10000000146", True),
    ("12345678950", True),
    ("12345678951", False),   # 11. hane yanlış
    ("12345678940", False),   # 10. hane yanlış
    ("01234567890", False),   # 0 ile başlıyor
    ("1234567895", False),    # 10 hane
    ("123456789501", False),  # 12 hane
    ("1234567895a", False),   # harf içeriyor
    ("-1234567895", False),   # eksi işareti
    ("", False),              # boş metin
])
def test_is_valid_tckn(number, expected):
    assert is_valid_tckn(number) is expected


@pytest.mark.parametrize("text, expected", [
    (
        "Müşteri 12345678950 numarasıyla başvurdu.",
        ["12345678950"],
    ),
    (
        "Sipariş no 12345678901, TC no 12345678950.",
        ["12345678950"],
    ),
    (
        "Başvuranlar: 10000000146 ve 12345678950",
        ["10000000146", "12345678950"],
    ),
    (
        "Merhaba, bugün hava çok güzel.",
        [],
    ),
    (
        "Hesap no: 123456789501234",
        [],
    ),
    (
        "TC:12345678950.",
        ["12345678950"],
    ),
])
def test_find_tckn(text, expected):
    assert find_tckn(text) == expected