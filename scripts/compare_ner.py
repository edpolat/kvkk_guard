from transformers import pipeline

MODELS = [
    "savasy/bert-base-turkish-ner-cased",
    "busecarik/berturk-sunlp-ner-turkish",
]

PERSON_LABELS = {"PER", "PERSON"}  # iki model kişiyi farklı adlandırıyor

# (metin, içinde geçen isimler)
TEXTS = [
    (
        """Merhaba Kerem Bey,

Dün Selin Hanım ile yaptığımız görüşmede sözleşmenin yenilenmesi konusunu
konuştuk. Fiyat güncellemesi için muhasebeden Okan Aydın'ın onayı gerekiyor.
Onay gelince size taslağı ileteceğim.

Saygılarımla,
Derya Koç""",
        ["Kerem", "Selin", "Okan Aydın", "Derya Koç"],
    ),
    (
        """Toplantı Notları - 14 Ekim

Katılımcılar: Hakan Öztürk, Gizem Yıldız, Emre Can

Yeni dönem bütçesi görüşüldü. Gizem'in önerisiyle pazarlama harcamaları
yüzde on azaltılacak. Emre sunumu cuma gününe kadar hazırlayacak. Hakan Bey
bir sonraki toplantıyı Ankara ofisinde yapmayı önerdi.""",
        ["Hakan Öztürk", "Gizem Yıldız", "Emre Can"],
    ),
    (
        """merhaba ben deniz aksoy geçen hafta sipariş verdim hala gelmedi kargo
takip numarası da çalışmıyor. dün kurye murat bey aradı adresi doğrulattı
ama yine gelmedi lütfen yardımcı olun""",
        ["deniz aksoy", "murat"],
    ),
    (
        """Temsilci (Büşra): Merhaba, size nasıl yardımcı olabilirim?
Müşteri: Merhaba, ben Serkan. Eşim Ayten Kılıç adına açılmış hesapta
bir sorun var, giriş yapamıyoruz.
Temsilci (Büşra): Anlıyorum Serkan Bey, hesabı kontrol ediyorum.""",
        ["Büşra", "Serkan", "Ayten Kılıç"],
    ),
    (
        """İnsan Kaynakları Bildirimi

Cansu Erdem'in yıllık izin talebi, yöneticisi Tolga Şen tarafından
onaylanmıştır. İzin süresince Cansu Hanım'ın görevlerini İzmir ekibinden
Onur Güler üstlenecektir.""",
        ["Cansu Erdem", "Tolga Şen", "Onur Güler"],
    ),
    (
        """Yeni şube açılışı nedeniyle Ankara ve İzmir ofislerinde çalışma
saatleri değişmiştir. Detaylar için insan kaynakları birimine başvurunuz.
Garanti Bankası ile yapılan anlaşma kapsamında maaş ödemeleri ayın
on beşinde yapılacaktır.""",
        [],  # kontrol metni: içinde hiç kişi yok
    ),
]

# Kesilme testi: uzun bir metnin en sonuna bir isim koyuyoruz
FILLER = (
    "Bu dönem içerisinde operasyon süreçleri gözden geçirilmiş, "
    "raporlama adımları sadeleştirilmiş ve ekipler arası iletişim "
    "güçlendirilmiştir. "
)
LONG_TEXT = FILLER * 40 + "Son olarak dosyayı Nihan Tekin'e iletiniz."
LONG_EXPECTED = ["Nihan Tekin"]


def find_persons(ner, text):
    return [e["word"] for e in ner(text) if e["entity_group"] in PERSON_LABELS]


def score(found, expected):
    hits = 0
    for name in expected:
        for word in found:
            if name.lower() in word.lower() or word.lower() in name.lower():
                hits += 1
                break
    extra = len(found) - hits if len(found) > hits else 0
    return hits, extra


for model_name in MODELS:
    print("=" * 70)
    print(model_name)
    print("=" * 70)

    ner = pipeline("ner", model=model_name, aggregation_strategy="simple")
    total_hits = 0
    total_expected = 0
    total_extra = 0

    for i, (text, expected) in enumerate(TEXTS, start=1):
        found = find_persons(ner, text)
        hits, extra = score(found, expected)
        total_hits += hits
        total_expected += len(expected)
        total_extra += extra
        print(f"\nMetin {i}: {hits}/{len(expected)} bulundu, {extra} fazladan")
        print(f"   Beklenen: {expected}")
        print(f"   Bulunan : {found}")

    print(f"\nTOPLAM: {total_hits}/{total_expected} isim bulundu "
          f"(recall = {total_hits / total_expected:.2f}), {total_extra} fazladan")

    print("\n--- Uzun metin testi ---")
    found = find_persons(ner, LONG_TEXT)
    print(f"Varsayılan ayar  : {found}")

    ner_long = pipeline("ner", model=model_name, aggregation_strategy="simple", stride=128)
    found = find_persons(ner_long, LONG_TEXT)
    print(f"stride=128 ile   : {found}")
    print()