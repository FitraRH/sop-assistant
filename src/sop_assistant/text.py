"""Indonesian tokenisation: lowercase, stopwords, Sastrawi stemming, query synonyms."""
import re
from functools import lru_cache

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

STOPWORDS = set("""
yang dan di ke dari untuk pada dengan atau oleh dalam adalah itu ini tidak ada akan juga sebagai
dapat bisa harus boleh sudah telah masih saja lebih kepada karena jika apabila bila agar serta
antara tersebut setiap semua para apa apakah siapa kapan dimana bagaimana berapa mengapa kenapa
mana saya kami kita anda dia mereka lama waktu cara sih dong kah sekali
""".split())

# Informal/English query words mapped to the formal Indonesian used in the SOPs.
SYNONYMS = {
    "update": "pembaruan", "refund": "pengembalian dana", "password": "kata sandi",
    "ticket": "tiket", "incident": "insiden", "escalation": "eskalasi", "handover": "serah terima",
    "complaint": "keluhan", "komplain": "keluhan", "close": "penutupan", "closing": "penutupan",
}

stem = lru_cache(maxsize=None)(StemmerFactory().create_stemmer().stem)


def tokenize(text: str, stop: bool = True) -> list[str]:
    """Stemmed tokens. Codes like p1 / sev1 and numbers are kept as they are."""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    if stop:
        tokens = [t for t in tokens if t not in STOPWORDS]
    return [t if t.isdigit() or re.fullmatch(r"[a-z]{1,4}\d+", t) else stem(t) for t in tokens]


def query_terms(text: str) -> list[str]:
    extra = [SYNONYMS[w] for w in re.findall(r"[a-z]+", text.lower()) if w in SYNONYMS]
    return tokenize(" ".join([text, *extra]))