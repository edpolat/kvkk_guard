import pytest

from kvkk_guard import Guard, GuardedClient, LeakError
from tests.test_client import FakeLLM


def test_kelime_icindeki_ayni_harfler_degismez():
    guard = Guard()
    tag = guard._get_tag("KISI", "Can")
    sonuc = guard._replace("Can'a ve Canan'a söyle.", "Can", tag)
    assert sonuc == "[KISI_1]'a ve Canan'a söyle."


def test_sadece_kelime_icinde_geciyorsa_yine_maskelenir():
    guard = Guard()
    tag = guard._get_tag("KISI", "Can")
    assert "Can" not in guard._replace("Canan aradı.", "Can", tag)


def test_sizinti_kontrolu_temiz_metinde_bos():
    guard = Guard()
    assert guard.find_leaks("[TC_1] numaralı müşteri [TELEFON_1] ile aradı.") == []


def test_sizinti_kontrolu_kalan_veriyi_bulur():
    guard = Guard()
    assert guard.find_leaks("[KISI_1] 12345678950") == ["12345678950"]


def test_sizinti_varsa_hata_firlatir(monkeypatch):
    guard = Guard()
    # Maskelemeyi bilerek bozuyoruz: değiştirme hiçbir şey yapmasın
    monkeypatch.setattr(guard, "_replace", lambda text, value, tag: text)
    with pytest.raises(LeakError):
        guard.mask("TC no 12345678950")


def test_bilinmeyen_etiketleri_bulur():
    guard = Guard()
    guard.mask("TC no 12345678950")
    metin = "[TC_1] ve [TC_2] numaraları, [Şirket İsmi] adına"
    assert guard.find_unknown_tags(metin) == ["[TC_2]"]


def test_uydurma_etikette_uyari_verir():
    class HallucinatingLLM(FakeLLM):
        def _create(self, model, messages):
            response = super()._create(model, messages)
            response.choices[0].message.content += " [TC_2]"
            return response

    client = GuardedClient(HallucinatingLLM(), model="test")
    with pytest.warns(UserWarning, match=r"\[TC_2\]"):
        client.chat("TC no 12345678950")