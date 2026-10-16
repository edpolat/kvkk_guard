import pytest

from kvkk_guard.detectors.phone import find_phone


@pytest.mark.parametrize("text, expected", [
    ("Beni 0532 123 45 67 numarasından ara.", ["0532 123 45 67"]),
    ("Tel: +90 532 123 45 67", ["+90 532 123 45 67"]),
    ("Tel: +905321234567", ["+905321234567"]),
    ("Numaram 05321234567", ["05321234567"]),
    ("Ofis: (0212) 555 12 34", ["(0212) 555 12 34"]),
    ("Ofis: 0212-555-12-34", ["0212-555-12-34"]),
    ("Cep 0532 123 45 67, ev 0216 444 55 66", ["0532 123 45 67", "0216 444 55 66"]),
    ("TC no 12345678950", []),            # 1 ile başlıyor, telefon değil
    ("Toplam 1.250 TL ödendi.", []),
    ("Bu metinde numara yok.", []),
])
def test_find_phone(text, expected):
    assert find_phone(text) == expected