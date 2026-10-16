import warnings
from kvkk_guard.guard import Guard

TAG_INSTRUCTION = (
    "Metindeki [KISI_1], [TC_1], [IBAN_1] gibi köşeli parantezli ifadeler "
    "gizlenmiş kişisel verilerdir. Bunları değiştirmeden, köşeli parantezleriyle "
    "birlikte olduğu gibi kullan."
)


class GuardedClient:
    def __init__(self, client, model: str, system_prompt: str = ""):
        self.client = client
        self.model = model
        self.guard = Guard()
        full_prompt = (system_prompt + "\n\n" + TAG_INSTRUCTION).strip()
        self.messages = [{"role": "system", "content": full_prompt}]

    def chat(self, text: str) -> str:
        masked = self.guard.mask(text)
        self.messages.append({"role": "user", "content": masked})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        unknown = self.guard.find_unknown_tags(reply)
        if unknown:
            warnings.warn(
                f"LLM cevabında bilinmeyen etiketler var: {', '.join(unknown)}. "
                "Model bu bilgileri uydurmuş olabilir."
            )
        return self.guard.unmask(reply)