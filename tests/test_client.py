from types import SimpleNamespace

from kvkk_guard import GuardedClient


class FakeLLM:
    """Gerçek LLM yerine geçen sahte istemci.

    Kendisine gönderilen mesajları kaydeder ve son kullanıcı mesajını
    'Alındı: ' önekiyle geri döndürür.
    """

    def __init__(self):
        self.sent = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, model, messages):
        self.sent.append([dict(m) for m in messages])
        reply = "Alındı: " + messages[-1]["content"]
        message = SimpleNamespace(content=reply)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_llm_kisisel_veri_gormez():
    fake = FakeLLM()
    client = GuardedClient(fake, model="test")
    client.chat("TC no 12345678950, tel 0532 123 45 67")
    gonderilen = str(fake.sent)
    assert "12345678950" not in gonderilen
    assert "0532 123 45 67" not in gonderilen


def test_kullanici_gercek_degerleri_gorur():
    fake = FakeLLM()
    client = GuardedClient(fake, model="test")
    cevap = client.chat("TC no 12345678950")
    assert cevap == "Alındı: TC no 12345678950"


def test_sohbet_boyunca_ayni_etiket():
    fake = FakeLLM()
    client = GuardedClient(fake, model="test")
    client.chat("Müşteri 12345678950 aradı.")
    client.chat("12345678950 tekrar aradı.")
    son_istek = fake.sent[-1]
    assert son_istek[-1]["content"] == "[TC_1] tekrar aradı."


def test_gecmis_mesajlar_da_maskeli_kalir():
    fake = FakeLLM()
    client = GuardedClient(fake, model="test")
    client.chat("TC no 12345678950")
    client.chat("Teşekkürler")
    assert "12345678950" not in str(fake.sent[-1])


def test_system_prompt_etiket_talimatini_icerir():
    fake = FakeLLM()
    client = GuardedClient(fake, model="test", system_prompt="Sen bir asistansın.")
    client.chat("Merhaba")
    system = fake.sent[0][0]
    assert system["role"] == "system"
    assert system["content"].startswith("Sen bir asistansın.")
    assert "[KISI_1]" in system["content"]