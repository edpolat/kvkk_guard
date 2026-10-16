from openai import OpenAI

from kvkk_guard import GuardedClient

client = GuardedClient(
    OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),
    model="qwen2.5:7b",
    system_prompt=(
        "Sen bir bankanın müşteri temsilcisisin. Müşteriden gelen şikâyete, "
        "müşteriye hitap eden kısa ve kibar bir yanıt yazarsın."
    ),
)

print(client.chat(
    "Merhaba, ben Selin Arslan. TC kimlik numaram 12345678950. "
    "Geçen ay TR33 0006 1005 1978 6457 8413 26 numaralı IBAN'ıma yapılması "
    "gereken iade hâlâ gelmedi. Bana 0532 123 45 67 numarasından ulaşabilirsiniz."
))

print("\n--- ikinci mesaj ---\n")

print(client.chat("Bir de eşim Ayten Kılıç adına açılmış hesapta da aynı sorun var."))

print("\n--- LLM'in gördüğü sohbet geçmişi ---\n")
for m in client.messages:
    print(f"[{m['role']}] {m['content']}\n")