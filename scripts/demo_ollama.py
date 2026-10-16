from openai import OpenAI

from kvkk_guard import Guard

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
guard = Guard()

SYSTEM_PROMPT = (
    "Sen bir bankanın müşteri temsilcisisin. Müşteriden gelen şikâyete, "
    "müşteriye hitap eden kısa ve kibar bir yanıt yazarsın. "
    "Metindeki [KISI_1], [TC_1], [IBAN_1] gibi köşeli parantezli ifadeler "
    "gizlenmiş kişisel verilerdir. Bunları değiştirmeden, köşeli parantezleriyle "
    "birlikte olduğu gibi kullan."
)

metin = """Merhaba, ben Selin Arslan. TC kimlik numaram 12345678950.
Geçen ay TR33 0006 1005 1978 6457 8413 26 numaralı IBAN'ıma yapılması
gereken iade hâlâ gelmedi. Bana 0532 123 45 67 numarasından ulaşabilirsiniz."""

maskeli = guard.mask(metin)

response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Bu müşteri şikâyetine kısa ve kibar bir yanıt yaz:\n\n" + maskeli},
    ],
)
cevap = response.choices[0].message.content

print("=== LLM'E GİDEN METİN ===")
print(maskeli)
print("\n=== LLM'İN CEVABI (maskeli) ===")
print(cevap)
print("\n=== KULLANICIYA GÖSTERİLEN CEVAP ===")
print(guard.unmask(cevap))