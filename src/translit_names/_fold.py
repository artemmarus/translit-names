"""Folding of Latin letters with diacritics to plain ASCII.

The base table is ICAO Doc 9303 Part 3, Section 6.A ("Transliteration of
multinational Latin-based characters").  Where ICAO offers alternatives
(Ä → AE or A, Ö → OE or O, Ü → UE/UXX/U, Å → AA or A, Ñ → N or NXX) the
single-letter form is the default; ``german=True`` selects the digraphs.
Letters ICAO does not list (Azerbaijani Ə, Romanian Ș/Ț, Serbo-Croatian
digraph code points, modifier apostrophes) are added explicitly, because
Unicode decomposition alone cannot handle Ł, Đ, Ø, Þ, Ħ, Ŧ, Ŋ or ı.
"""

from __future__ import annotations

import unicodedata
from typing import Dict

__all__ = ["ICAO_LATIN", "fold", "fold_char"]

#: ICAO Doc 9303 Part 3 §6.A, upper case, first (preferred) option.
ICAO_LATIN: Dict[str, str] = {
    "À": "A",
    "Á": "A",
    "Â": "A",
    "Ã": "A",
    "Ä": "AE",
    "Å": "AA",
    "Æ": "AE",
    "Ç": "C",
    "È": "E",
    "É": "E",
    "Ê": "E",
    "Ë": "E",
    "Ì": "I",
    "Í": "I",
    "Î": "I",
    "Ï": "I",
    "Ð": "D",
    "Ñ": "N",
    "Ò": "O",
    "Ó": "O",
    "Ô": "O",
    "Õ": "O",
    "Ö": "OE",
    "Ø": "OE",
    "Ù": "U",
    "Ú": "U",
    "Û": "U",
    "Ü": "UE",
    "Ý": "Y",
    "Þ": "TH",
    "Ā": "A",
    "Ă": "A",
    "Ą": "A",
    "Ć": "C",
    "Ĉ": "C",
    "Ċ": "C",
    "Č": "C",
    "Ď": "D",
    "Đ": "D",
    "Ē": "E",
    "Ĕ": "E",
    "Ė": "E",
    "Ę": "E",
    "Ě": "E",
    "Ĝ": "G",
    "Ğ": "G",
    "Ġ": "G",
    "Ģ": "G",
    "Ĥ": "H",
    "Ħ": "H",
    "Ĩ": "I",
    "Ī": "I",
    "Ĭ": "I",
    "Į": "I",
    "İ": "I",
    "I": "I",
    "Ĳ": "IJ",
    "Ĵ": "J",
    "Ķ": "K",
    "Ĺ": "L",
    "Ļ": "L",
    "Ľ": "L",
    "Ŀ": "L",
    "Ł": "L",
    "Ń": "N",
    "Ņ": "N",
    "Ň": "N",
    "Ŋ": "N",
    "Ō": "O",
    "Ŏ": "O",
    "Ő": "O",
    "Œ": "OE",
    "Ŕ": "R",
    "Ŗ": "R",
    "Ř": "R",
    "Ś": "S",
    "Ŝ": "S",
    "Ş": "S",
    "Š": "S",
    "Ţ": "T",
    "Ť": "T",
    "Ŧ": "T",
    "Ũ": "U",
    "Ū": "U",
    "Ŭ": "U",
    "Ů": "U",
    "Ű": "U",
    "Ų": "U",
    "Ŵ": "W",
    "Ŷ": "Y",
    "Ÿ": "Y",
    "Ź": "Z",
    "Ż": "Z",
    "Ž": "Z",
    "ẞ": "SS",
}

#: ICAO entries that offer a one-letter alternative.
_SHORT_FORMS = {"Ä": "A", "Å": "A", "Ö": "O", "Ü": "U"}

#: Letters outside the ICAO table.
_EXTRA: Dict[str, str] = {
    "Ə": "A",  # Azerbaijani schwa: Məmmədov → Mammadov (dominant practice)
    "Ș": "S",
    "Ț": "T",  # comma-below (Romanian, Gagauz)
    "Ǆ": "DZ",
    "ǅ": "Dz",
    "ǆ": "dz",
    "Ǉ": "LJ",
    "ǈ": "Lj",
    "ǉ": "lj",
    "Ǌ": "NJ",
    "ǋ": "Nj",
    "ǌ": "nj",
    "Ǵ": "G",
    "Ḱ": "K",
    "Ḩ": "H",
    "Ḥ": "H",
    "Ṣ": "S",
    "Ṭ": "T",
    "Ḍ": "D",
    "Ẓ": "Z",
    "Ẕ": "Z",
    "Ḏ": "D",
    "Ṯ": "T",
    "Ḫ": "H",
    "Ẏ": "Y",
    "Ḟ": "F",
    "Ṡ": "S",
    "Ṅ": "N",
    "ß": "ss",
    "ı": "i",
    "ĸ": "q",
    "ſ": "s",
}

#: Apostrophe-like marks (Uzbek oʻ/gʻ, tutuq ʼ, Arabic ʿayn/hamza in scholarly
#: romanisations, soft/hard sign primes) and how they fold.
_MARKS: Dict[str, str] = {
    "\u02bb": "'",
    "\u02bc": "'",
    "\u2018": "'",
    "\u2019": "'",
    "\u02b9": "'",
    "\u02bd": "'",
    "\u02be": "'",
    "\u02bf": "'",
    "\u02ba": '"',
    "\u201c": '"',
    "\u201d": '"',
    "\u00b4": "'",
    "\u2032": "'",
    "\u2033": '"',
    "\u00b7": "",
    "\u0361": "",
    "\u035c": "",
}


def _build(german: bool) -> Dict[str, str]:
    table: Dict[str, str] = {}
    for up, val in ICAO_LATIN.items():
        if not german and up in _SHORT_FORMS:
            val = _SHORT_FORMS[up]
        table[up] = val
        low = up.lower()
        if len(low) == 1 and low != up:
            table.setdefault(low, val.lower())
    for k, v in _EXTRA.items():
        table[k] = v
        low = k.lower()
        if len(low) == 1 and low not in _EXTRA:
            table.setdefault(low, v.lower())
    table["ı"] = "i"
    table["İ"] = "I"
    table.update(_MARKS)
    return table


_TABLE = _build(german=False)
_TABLE_GERMAN = _build(german=True)


def fold_char(ch: str, german: bool = False) -> str:
    """Fold one character to ASCII (empty string if nothing sensible exists)."""
    if ch.isascii():
        return ch
    table = _TABLE_GERMAN if german else _TABLE
    if ch in table:
        return table[ch]
    decomposed = unicodedata.normalize("NFKD", ch)
    base = "".join(c for c in decomposed if not unicodedata.combining(c))
    if base and all(c.isascii() for c in base):
        return base
    if base and base != ch:
        return "".join(fold_char(c, german) for c in base)
    return ""


def fold(text: str, german: bool = False, keep: str = "") -> str:
    """Fold ``text`` to ASCII using the ICAO §6.A table plus extensions.

    ``keep`` lists non-ASCII characters to leave untouched.
    """
    text = unicodedata.normalize("NFC", text)
    out = []
    for i, ch in enumerate(text):
        if ch in keep:
            out.append(ch)
            continue
        if unicodedata.combining(ch):
            continue
        res = fold_char(ch, german)
        if len(res) > 1 and res.isupper():
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if nxt.islower():  # Æsir → Aesir, Þór → Thor, but ÆSIR → AESIR
                res = res.capitalize()
        out.append(res)
    return "".join(out)
