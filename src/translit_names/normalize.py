"""Unicode clean-up for personal names before transliteration or matching."""

from __future__ import annotations

import re
import unicodedata
from typing import Dict, Literal

__all__ = [
    "arabic_key",
    "fix_mixed_script",
    "latin_key",
    "normalize",
    "normalize_arabic",
    "script_of",
    "strip_arabic_diacritics",
    "unify_apostrophes",
]

_SPACES_RE = re.compile(r"[\s\u00a0\u2000-\u200b\u202f\u205f\u3000]+")
_DASHES = "\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe58\ufe63\uff0d"
_APOSTROPHE_LIKE = "'\u2019\u02bc\u02bb\u2018`\u00b4\u02b9\u02bd\u2032"

# Latin ↔ Cyrillic look-alikes (lower and upper case).
_LAT_TO_CYR: Dict[str, str] = {
    "a": "а",
    "c": "с",
    "e": "е",
    "o": "о",
    "p": "р",
    "x": "х",
    "y": "у",
    "i": "і",
    "j": "ј",
    "A": "А",
    "B": "В",
    "C": "С",
    "E": "Е",
    "H": "Н",
    "K": "К",
    "M": "М",
    "O": "О",
    "P": "Р",
    "T": "Т",
    "X": "Х",
    "Y": "У",
    "I": "І",
    "J": "Ј",
}
_CYR_TO_LAT: Dict[str, str] = {v: k for k, v in _LAT_TO_CYR.items()}
# Only unambiguous lower-case look-alikes may be swapped inside Latin words.
_CYR_TO_LAT_SAFE = {k: v for k, v in _CYR_TO_LAT.items() if k in "аеорсухіјАВЕКМНОРСТХУІЈ"}

_ARABIC_MARKS_RE = re.compile("[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06dc\u06df-\u06e8\u06ea-\u06ed]")
_TATWEEL = "ـ"
_ARABIC_DIGITS = {ord(c): str(i) for i, c in enumerate("٠١٢٣٤٥٦٧٨٩")}
_ARABIC_DIGITS.update({ord(c): str(i) for i, c in enumerate("۰۱۲۳۴۵۶۷۸۹")})
_ALEF_FORMS = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ٲ": "ا", "ٳ": "ا"})
# Fold Persian/Urdu letter shapes onto Arabic ones (matching keys only).
_ARABIC_KEY_MAP = str.maketrans(
    {
        "ی": "ي",
        "ى": "ي",
        "ې": "ي",
        "ۍ": "ي",
        "ے": "ي",
        "ئ": "ي",
        "ۓ": "ي",
        "ک": "ك",
        "ڪ": "ك",
        "ہ": "ه",
        "ھ": "ه",
        "ۀ": "ه",
        "ۃ": "ه",
        "ة": "ه",
        "ە": "ه",
        "ؤ": "و",
        "ۆ": "و",
        "ۇ": "و",
        "ۈ": "و",
        "ۋ": "و",
        "ء": "",
        "\u0654": "",
    }
)


def normalize(text: str, *, form: Literal["NFC", "NFD", "NFKC", "NFKD"] = "NFC") -> str:
    """Basic, lossless clean-up: Unicode normalisation, spaces, dashes, digits.

    - NFC composition (``е`` + U+0308 → ``ё``);
    - all space-like characters (NBSP, thin space, ZWSP …) → one space;
    - typographic dashes between letters → ``-``;
    - Arabic-Indic and Persian digits → ASCII;
    - tatweel (kashida) removed, Arabic presentation forms expanded.
    """
    if not text:
        return ""
    text = _expand_presentation_forms(text)
    text = unicodedata.normalize(form, text)
    text = text.replace(_TATWEEL, "").replace("\u200d", "")
    text = text.translate(_ARABIC_DIGITS)
    text = "".join("-" if c in _DASHES else c for c in text)
    # ZWNJ is meaningful in Persian; keep it but never as the only separator.
    text = _SPACES_RE.sub(" ", text).strip()
    return text


def _expand_presentation_forms(text: str) -> str:
    if not any("ﭐ" <= c <= "﷿" or "ﹰ" <= c <= "\ufeff" for c in text):
        return text
    return "".join(unicodedata.normalize("NFKC", c) if ("ﭐ" <= c <= "﷿" or "ﹰ" <= c <= "\ufeff") else c for c in text)


def unify_apostrophes(text: str, to: str = "'") -> str:
    """Replace every apostrophe-like character (’ \u02bc \u02bb \u2018 ` \u00b4 \u2032) with ``to``."""
    return "".join(to if c in _APOSTROPHE_LIKE else c for c in text)


def script_of(ch: str) -> str:
    """Rough script of a character: ``Latn``, ``Cyrl``, ``Arab`` or ``Zyyy``."""
    if not ch.isalpha():
        if "\u0600" <= ch <= "ۿ" and unicodedata.category(ch) == "Mn":
            return "Arab"
        return "Zyyy"
    cp = ord(ch)
    if cp < 0x250 or 0x1E00 <= cp <= 0x1EFF or 0x2C60 <= cp <= 0x2C7F or 0xA720 <= cp <= 0xA7FF:
        return "Latn"
    if 0x0400 <= cp <= 0x052F or 0x1C80 <= cp <= 0x1C8F or 0x2DE0 <= cp <= 0x2DFF or 0xA640 <= cp <= 0xA69F:
        return "Cyrl"
    if 0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F or 0x08A0 <= cp <= 0x08FF or 0xFB50 <= cp <= 0xFEFF:
        return "Arab"
    if 0x0370 <= cp <= 0x03FF:
        return "Grek"
    return "Zyyy"


_WORD_RE = re.compile(r"[^\W\d_]+(?:['\u2019\u02bc][^\W\d_]+)*", re.UNICODE)


def fix_mixed_script(text: str) -> str:
    """Repair words that mix Latin and Cyrillic look-alike letters.

    ``"Аlexey"`` (Cyrillic А) → ``"Alexey"``; ``"Иванoв"`` (Latin o) → ``"Иванов"``.
    A word is converted to whichever script has the majority of its letters.
    The Chechen palochka (Ӏ) written as Latin I/l or digit 1 is restored
    inside Cyrillic words.
    """

    def fix(m: re.Match[str]) -> str:
        word = m.group(0)
        counts = {"Latn": 0, "Cyrl": 0}
        for c in word:
            s = script_of(c)
            if s in counts:
                counts[s] += 1
        if counts["Latn"] and counts["Cyrl"]:
            if counts["Cyrl"] >= counts["Latn"]:
                word = "".join(_LAT_TO_CYR.get(c, c) if script_of(c) == "Latn" else c for c in word)
                word = _fix_palochka(word)
            else:
                word = "".join(_CYR_TO_LAT_SAFE.get(c, c) if script_of(c) == "Cyrl" else c for c in word)
        return word

    return _WORD_RE.sub(fix, text)


_PALOCHKA_RE = re.compile(r"(?<=[гкхпт])[Ii1lІ]|(?<=[ГКХПТ])[Ii1lІ]")


def _fix_palochka(word: str) -> str:
    # In Caucasian orthographies the palochka follows г к х п т (гӀ, кӀ, хӀ …).
    return _PALOCHKA_RE.sub("Ӏ", word) if any(c in word for c in "Ii1lІ") else word


def strip_arabic_diacritics(text: str) -> str:
    """Remove harakat, shadda, sukun, tanwin, dagger alif and Quranic marks."""
    return _ARABIC_MARKS_RE.sub("", text)


def normalize_arabic(text: str, *, strip_diacritics: bool = False, fold_alef: bool = False) -> str:
    """Normalise Arabic-script text without losing information needed for
    romanisation (unless ``strip_diacritics``/``fold_alef`` are set)."""
    text = normalize(text)
    if strip_diacritics:
        text = strip_arabic_diacritics(text)
    if fold_alef:
        text = text.translate(_ALEF_FORMS)
    return text


def arabic_key(text: str) -> str:
    """Aggressive Arabic-script key for dictionary lookup and matching.

    Strips vowel marks and tatweel, folds hamza seats and alef forms, and
    unifies Persian/Urdu/Pashto letter shapes with their Arabic counterparts
    (ی/ى/ي, ک/ك, ہ/ه/ة …).  Spaces are collapsed.
    """
    text = normalize(text)
    text = strip_arabic_diacritics(text)
    text = text.translate(_ALEF_FORMS).translate(_ARABIC_KEY_MAP)
    text = text.replace("\u200c", "")
    return " ".join(text.split())


def latin_key(text: str) -> str:
    """Case-, diacritic- and punctuation-insensitive key for Latin spellings.

    ``"Hüseyin"`` → ``"huseyin"``; ``"Abd al-Rahman"`` → ``"abdalrahman"``.
    """
    from ._fold import fold

    folded = fold(normalize(text)).lower()
    return "".join(c for c in folded if c.isalnum())
