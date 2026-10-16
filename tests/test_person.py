from kvkk_guard import Guard
from kvkk_guard.detectors.person import find_person


def test_isim_bulma():
    assert find_person("Ayşe Yılmaz dün müşteri hizmetlerini aradı.") == ["Ayşe Yılmaz"]


def test_kesme_isareti_temiz_kesilir():
    assert find_person("Raporu Can'a gönderdim.") == ["Can"]


def test_isim_yoksa_bos_liste():
    assert find_person("Yarın Ankara ofisinde sunum yapılacak.") == []


def test_uzun_metnin_sonundaki_isim():
    dolgu = (
        "Bu dönem içerisinde operasyon süreçleri gözden geçirilmiş, "
        "raporlama adımları sadeleştirilmiştir. "
    )
    metin = dolgu * 40 + "Son olarak dosyayı Nihan Tekin'e iletiniz."
    assert "Nihan Tekin" in find_person(metin)


def test_soyadi_sizmaz():
    guard = Guard()
    sonuc = guard.mask("Cansu Erdem izin istedi. Cansu Hanım onaylandı.")
    assert "Cansu" not in sonuc
    assert "Erdem" not in sonuc


def test_isimli_metin_geri_acilir():
    guard = Guard()
    metin = "Selin Arslan'ın TC no 12345678950, telefonu 0532 123 45 67."
    assert guard.unmask(guard.mask(metin)) == metin