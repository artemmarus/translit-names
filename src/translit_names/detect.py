"""Guess the script and language of a personal name from its letters.

Names are short, so statistical language identification does not work; the
letters themselves are the evidence.  ``ґ є ї`` mean Ukrainian, ``ў`` with
``і`` Belarusian, ``ұ`` Kazakh, ``ҷ ӣ ӯ`` Tajik, ``ٹ ڈ ڑ ں ے`` Urdu, ``پ چ ژ گ``
with ``ی ک`` Persian, ``ł ą ę`` Polish, ``ə`` Azerbaijani, and so on.  When
nothing distinguishes the candidates, the most widespread language of the
script wins (Russian, Arabic).
"""

from __future__ import annotations

import unicodedata
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from .normalize import script_of

__all__ = ["Detection", "detect_language", "detect_script"]

_RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
_CYRILLIC: Dict[str, Tuple[str, float]] = {
    # language: (alphabet, prior)
    "ru": (_RU, 3.0),
    "uk": ("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'\u2019\u02bc", 2.0),
    "be": ("абвгдеёжзійклмнопрстуўфхцчшыьэюя'\u2019\u02bc", 1.5),
    "bg": ("абвгдежзийклмнопрстуфхцчшщъьюя", 1.5),
    "sr": ("абвгдђежзијклљмнњопрстћуфхцчџш", 1.2),
    "mk": ("абвгдѓежзѕијклљмнњопрстќуфхцчџш", 1.0),
    "kk": (_RU + "әғқңөұүһі", 1.0),
    "ky": (_RU + "ңөү", 0.8),
    "uz": ("абвгдеёжзийклмнопрстуфхцчшъьэюяўқғҳ", 0.8),
    "tg": ("абвгғдеёжзиӣйкқлмнопрстуӯфхҳчҷшъэюя", 0.8),
    "tt": (_RU + "әөүҗңһ", 0.7),
    "ba": (_RU + "әөүғҡңҙҫһ", 0.6),
    "ce": (_RU + "ӏ", 0.6),
}
# Letters that point strongly at one language (bonus on top of coverage).
_CYRILLIC_MARKERS: Dict[str, Dict[str, float]] = {
    "ґ": {"uk": 3},
    "є": {"uk": 3},
    "ї": {"uk": 3},
    "ў": {"be": 3, "uz": 1},
    "ы": {"ru": 0.5, "be": 0.5},
    "і": {"uk": 1, "be": 1, "kk": 0.5},
    "ъ": {"ru": 0.3, "bg": 0.6},
    "ђ": {"sr": 3},
    "ћ": {"sr": 3},
    "ѓ": {"mk": 3},
    "ќ": {"mk": 3},
    "ѕ": {"mk": 3},
    "љ": {"sr": 1, "mk": 1},
    "њ": {"sr": 1, "mk": 1},
    "џ": {"sr": 1, "mk": 1},
    "ј": {"sr": 1, "mk": 1},
    "ұ": {"kk": 4},
    "ә": {"kk": 2, "tt": 1.5, "ba": 1.2},
    "ғ": {"kk": 1.5, "uz": 1.5, "tg": 1.5, "ba": 1},
    "қ": {"kk": 2, "uz": 1.5, "tg": 1.5},
    "ң": {"kk": 1.5, "ky": 1.5, "tt": 1, "ba": 1},
    "ө": {"kk": 1.5, "ky": 1.5, "tt": 1, "ba": 1},
    "ү": {"kk": 1.5, "ky": 1.5, "tt": 1, "ba": 1},
    "һ": {"kk": 1, "tt": 1, "ba": 1},
    "ҳ": {"uz": 2, "tg": 2},
    "ҷ": {"tg": 4},
    "ӣ": {"tg": 4},
    "ӯ": {"tg": 4},
    "җ": {"tt": 4},
    "ҡ": {"ba": 4},
    "ҙ": {"ba": 4},
    "ҫ": {"ba": 4},
    "ӏ": {"ce": 4},
}

_AR_BASE = "ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىي"
_ARABIC: Dict[str, Tuple[str, float]] = {
    "ar": (_AR_BASE + "ٱ", 3.0),
    "fa": (_AR_BASE.replace("ك", "").replace("ي", "") + "پچژگکیۀ", 2.0),
    "ur": (_AR_BASE.replace("ك", "").replace("ي", "") + "پچژگکیٹڈڑںھہےۃ", 1.5),
    "ps": (_AR_BASE.replace("ك", "").replace("ي", "") + "پچژګگکیټډړږښځڅڼېۍ", 1.0),
}
_ARABIC_MARKERS: Dict[str, Dict[str, float]] = {
    "ك": {"ar": 1},
    "ي": {"ar": 1},
    "ة": {"ar": 1},
    "ى": {"ar": 0.5},
    "ی": {"fa": 1, "ur": 0.8, "ps": 0.6},
    "ک": {"fa": 1, "ur": 0.8, "ps": 0.4},
    "پ": {"fa": 1, "ur": 1},
    "چ": {"fa": 1, "ur": 1},
    "ژ": {"fa": 1.5},
    "گ": {"fa": 1, "ur": 1},
    "ٹ": {"ur": 4},
    "ڈ": {"ur": 4},
    "ڑ": {"ur": 4},
    "ں": {"ur": 4},
    "ھ": {"ur": 3},
    "ہ": {"ur": 3},
    "ے": {"ur": 4},
    "ۃ": {"ur": 2},
    "ټ": {"ps": 4},
    "ډ": {"ps": 4},
    "ړ": {"ps": 4},
    "ږ": {"ps": 4},
    "ښ": {"ps": 4},
    "ځ": {"ps": 4},
    "څ": {"ps": 4},
    "ڼ": {"ps": 4},
    "ې": {"ps": 4},
    "ۍ": {"ps": 4},
    "ګ": {"ps": 4},
    "ۀ": {"fa": 2},
}

_LATIN_MARKERS: Dict[str, Dict[str, float]] = {
    "ł": {"pl": 4},
    "ą": {"pl": 4},
    "ę": {"pl": 4},
    "ś": {"pl": 3},
    "ź": {"pl": 3},
    "ż": {"pl": 4},
    "ń": {"pl": 3},
    "ř": {"cs": 4},
    "ů": {"cs": 4},
    "ě": {"cs": 4},
    "ď": {"cs": 2, "sk": 2},
    "ť": {"cs": 2, "sk": 2},
    "ň": {"cs": 1.5, "sk": 1.5, "tk": 1},
    "ľ": {"sk": 4},
    "ĺ": {"sk": 4},
    "ŕ": {"sk": 4},
    "ô": {"sk": 2},
    "đ": {"sh": 4},
    "ć": {"sh": 2, "pl": 2},
    "č": {"sh": 1.5, "sl": 1.5, "cs": 1.5, "sk": 1.5},
    "š": {"sh": 1.5, "sl": 1.5, "cs": 1.5, "sk": 1.5},
    "ž": {"sh": 1.5, "sl": 1.5, "cs": 1.5, "sk": 1.5, "tk": 1},
    "ǆ": {"sh": 4},
    "ǉ": {"sh": 4},
    "ǌ": {"sh": 4},
    "ğ": {"tr": 2, "az": 2},
    "ı": {"tr": 2, "az": 2, "kk": 1},
    "ş": {"tr": 1.5, "az": 1.5, "tk": 1.5, "kk": 1},
    "ç": {"tr": 1.5, "az": 1.5, "tk": 1.5},
    "ə": {"az": 5},
    "ö": {"tr": 1, "az": 1, "tk": 1},
    "ü": {"tr": 1, "az": 1, "tk": 1},
    "ä": {"tk": 2, "sk": 1, "kk": 1},
    "ý": {"tk": 2, "cs": 1, "sk": 1},
    "ū": {"kk": 3},
    "ñ": {"kk": 2},
    "\u02bb": {"uz": 4},
    "\u2018": {"uz": 1},
    "â": {"tr": 0.5},
}
_LATIN_PRIOR = {
    "tr": 1.0,
    "pl": 1.0,
    "cs": 0.8,
    "sh": 0.8,
    "az": 0.8,
    "uz": 0.8,
    "sk": 0.6,
    "sl": 0.6,
    "tk": 0.5,
    "kk": 0.4,
}


@dataclass(frozen=True)
class Detection:
    """Result of :func:`detect_language`."""

    language: str
    script: str
    confidence: float
    candidates: Tuple[Tuple[str, float], ...] = ()

    def __str__(self) -> str:
        return self.language


def detect_script(text: str) -> str:
    """Dominant script of ``text``: ``Cyrl``, ``Arab``, ``Latn``, ``Grek`` or ``Zyyy``."""
    counts = Counter(script_of(c) for c in unicodedata.normalize("NFC", text))
    counts.pop("Zyyy", None)
    if not counts:
        return "Zyyy"
    return counts.most_common(1)[0][0]


def _score(
    letters: Counter[str], alphabets: Dict[str, Tuple[str, float]], markers: Dict[str, Dict[str, float]]
) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for lang, (alphabet, prior) in alphabets.items():
        missing = sum(n for ch, n in letters.items() if ch not in alphabet)
        scores[lang] = prior - 6.0 * missing
    for ch in letters:
        for lang, bonus in markers.get(ch, {}).items():
            if lang in scores:
                scores[lang] += bonus
    return scores


_UK_HINTS = ("ськ", "цьк", "зьк", "ньк", "ьо")


def _ukrainian_hint(text: str) -> float:
    """Ukrainian spellings without Ukrainian-only letters: -ський, -цький, ьо."""
    low = text.lower()
    return sum(1.5 for h in _UK_HINTS if h in low)


def _bulgarian_hint(text: str) -> float:
    """Bulgarian uses ъ as a vowel before consonants and at word ends; Russian
    only before е ё ю я.  It also lacks ы э ё."""
    low = text.lower()
    bonus = 0.0
    for i, ch in enumerate(low):
        if ch == "ъ":
            nxt = low[i + 1] if i + 1 < len(low) else " "
            if nxt not in "еёюя":
                bonus += 2.5
    return bonus


def detect_language(text: str, *, hint: Optional[str] = None) -> Detection:
    """Guess the language of a name.

    Returns a :class:`Detection` whose ``language`` is a code such as ``ru``,
    ``uk``, ``kk``, ``ar``, ``fa``, ``ur``, ``tr``, ``pl``.  For plain ASCII
    Latin text the language is ``"en"``; for Latin text with diacritics that
    match no profile it is ``"mul"``.  ``hint`` breaks ties in its favour.
    """
    text = unicodedata.normalize("NFC", text)
    script = detect_script(text)
    letters = Counter(c for c in text.lower() if c.isalpha() or c in "'\u2019\u02bc\u02bb\u2018")
    if script == "Cyrl":
        letters = Counter({c: n for c, n in letters.items() if script_of(c) == "Cyrl" or c in "'\u2019\u02bc"})
        scores = _score(letters, _CYRILLIC, _CYRILLIC_MARKERS)
        scores["bg"] += _bulgarian_hint(text)
        scores["uk"] += _ukrainian_hint(text)
    elif script == "Arab":
        letters = Counter({c: n for c, n in letters.items() if script_of(c) == "Arab"})
        scores = _score(letters, _ARABIC, _ARABIC_MARKERS)
    elif script == "Latn":
        scores = {lang: 0.0 for lang in _LATIN_PRIOR}
        for ch in letters:
            for lang, bonus in _LATIN_MARKERS.get(ch, {}).items():
                scores[lang] = scores.get(lang, 0.0) + bonus
        if (
            "o\u2018" in text.lower()
            or "g\u2018" in text.lower()
            or "o\u02bb" in text.lower()
            or "g\u02bb" in text.lower()
        ):
            scores["uz"] = scores.get("uz", 0.0) + 4
        if not any(v > 0 for v in scores.values()):
            lang = "en" if text.isascii() else "mul"
            return Detection(lang, script, 0.5 if lang == "en" else 0.3, ((lang, 1.0),))
        for lang, prior in _LATIN_PRIOR.items():
            if scores.get(lang, 0) > 0:
                scores[lang] += prior * 0.1
    else:
        return Detection("und", script, 0.0, ())
    if hint and hint in scores:
        scores[hint] += 1.5
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    best, best_score = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else best_score - 3
    margin = best_score - second
    confidence = max(0.05, min(0.99, 0.5 + margin / 6.0)) if best_score > -3 else 0.05
    return Detection(best, script, round(confidence, 3), tuple((k, round(v, 3)) for k, v in ranked[:5]))
