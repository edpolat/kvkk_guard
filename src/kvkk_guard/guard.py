from kvkk_guard.detectors.email import find_email
from kvkk_guard.detectors.iban import find_iban
from kvkk_guard.detectors.phone import find_phone
from kvkk_guard.detectors.tckn import find_tckn
from kvkk_guard.detectors.person import find_person
# Sıra önemli: önce uzun/özel olanlar maskelenir, sonra genel olanlar.
DETECTORS = [
    ("EPOSTA", find_email),
    ("IBAN", find_iban),
    ("TC", find_tckn),
    ("TELEFON", find_phone),
    ("KISI", find_person),
]


class Guard:
    def __init__(self):
        self.mapping = {}    # "[TC_1]" -> "12345678950"
        self.reverse = {}    # "12345678950" -> "[TC_1]"
        self.counters = {}   # "TC" -> 1

    def _get_tag(self, label: str, value: str) -> str:
        if value in self.reverse:
            return self.reverse[value]
        self.counters[label] = self.counters.get(label, 0) + 1
        tag = f"[{label}_{self.counters[label]}]"
        self.mapping[tag] = value
        self.reverse[value] = tag
        return tag

    def mask(self, text: str) -> str:
        for label, find in DETECTORS:
            for value in find(text):
                tag = self._get_tag(label, value)
                text = text.replace(value, tag)
        return text

    def unmask(self, text: str) -> str:
        for tag, value in self.mapping.items():
            text = text.replace(tag, value)
        return text