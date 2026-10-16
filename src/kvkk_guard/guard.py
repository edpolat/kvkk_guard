import re

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

# Sızıntı kontrolünde tekrar çalıştırılacak hızlı dedektörler (NER hariç)
LEAK_CHECKERS = DETECTORS[:4]

LABELS = "|".join(label for label, _ in DETECTORS)
TAG_PATTERN = re.compile(rf"\[(?:{LABELS})_\d+\]")


class LeakError(Exception):
    pass


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

    def _replace(self, text: str, value: str, tag: str) -> str:
        pattern = rf"(?<!\w){re.escape(value)}(?!\w)"
        new_text, count = re.subn(pattern, lambda m: tag, text)
        if count == 0:
            # Değer sadece başka bir kelimenin içinde geçiyorsa bile maskele:
            # fazladan maskelemek, sızdırmaktan iyidir.
            new_text = text.replace(value, tag)
        return new_text

    def mask(self, text: str) -> str:
        for label, find in DETECTORS:
            for value in find(text):
                tag = self._get_tag(label, value)
                text = self._replace(text, value, tag)
        leaks = self.find_leaks(text)
        if leaks:
            raise LeakError(f"Maskeleme sonrası metinde hâlâ {len(leaks)} kişisel veri bulundu.")
        return text

    def find_leaks(self, text: str) -> list[str]:
        leaks = []
        for _, find in LEAK_CHECKERS:
            leaks.extend(find(text))
        return leaks

    def find_unknown_tags(self, text: str) -> list[str]:
        unknown = []
        for tag in TAG_PATTERN.findall(text):
            if tag not in self.mapping and tag not in unknown:
                unknown.append(tag)
        return unknown

    def unmask(self, text: str) -> str:
        for tag, value in self.mapping.items():
            text = text.replace(tag, value)
        return text