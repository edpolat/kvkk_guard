import pytest

from kvkk_guard.detectors.email import find_email


@pytest.mark.parametrize("text, expected", [
    ("Bana ayse.yilmaz@firma.com.tr adresinden ulaşın.", ["ayse.yilmaz@firma.com.tr"]),
    ("İletişim: info@ornek.com.", ["info@ornek.com"]),           # sondaki nokta dahil değil
    ("a_b+test@mail.co ve x@y.io", ["a_b+test@mail.co", "x@y.io"]),
    ("Kullanıcı adı @ayse", []),                                 # sosyal medya etiketi
    ("Bu metinde e-posta yok.", []),
])
def test_find_email(text, expected):
    assert find_email(text) == expected