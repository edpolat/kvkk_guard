from kvkk_guard import Guard


def test_tek_tur_maskeleme():
    guard = Guard()
    assert guard.mask("TC no 12345678950") == "TC no [TC_1]"


def test_birden_fazla_tur():
    guard = Guard()
    metin = (
        "Müşteri 12345678950, tel 0532 123 45 67, "
        "mail ayse@firma.com, IBAN TR33 0006 1005 1978 6457 8413 26"
    )
    beklenen = "Müşteri [TC_1], tel [TELEFON_1], mail [EPOSTA_1], IBAN [IBAN_1]"
    assert guard.mask(metin) == beklenen


def test_ayni_deger_ayni_etiketi_alir():
    guard = Guard()
    metin = "12345678950 ile 10000000146 başvurdu, 12345678950 onaylandı."
    assert guard.mask(metin) == "[TC_1] ile [TC_2] başvurdu, [TC_1] onaylandı."


def test_iki_mesajda_ayni_etiket():
    guard = Guard()
    guard.mask("Müşteri 12345678950 aradı.")
    assert guard.mask("12345678950 tekrar aradı.") == "[TC_1] tekrar aradı."


def test_geri_acma():
    guard = Guard()
    guard.mask("Müşteri 12345678950, mail ayse@firma.com")
    cevap = "[TC_1] numaralı müşteriye [EPOSTA_1] adresinden dönüş yapılacak."
    assert guard.unmask(cevap) == (
        "12345678950 numaralı müşteriye ayse@firma.com adresinden dönüş yapılacak."
    )


def test_maskele_ve_geri_ac_ayni_metni_verir():
    guard = Guard()
    metin = "TC 12345678950, IBAN TR330006100519786457841326, tel +90 532 123 45 67"
    assert guard.unmask(guard.mask(metin)) == metin


def test_kisisel_veri_yoksa_metin_degismez():
    guard = Guard()
    metin = "Toplantı yarın saat 15:00'te."
    assert guard.mask(metin) == metin


def test_etiket_10_ve_1_karismaz():
    guard = Guard()
    for i in range(10):
        guard._get_tag("TC", f"deger{i}")
    assert guard.unmask("[TC_1] ve [TC_10]") == "deger0 ve deger9"