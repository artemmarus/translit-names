from __future__ import annotations

import pytest

from translit_names._engine import Scheme
from translit_names._registry import _hooks
from translit_names.arabic import has_harakat, vocalize_word

_DEMO = {
    "id": "t_ar",
    "hook": "arabic",
    "options": {"vocalize": True, "lexicon": False},
    "geminate": "\u0651",
    "titlecase": True,
    "lowercase_words": ["al-"],
    "map": {
        "ا": "a",
        "أ": "",
        "إ": "",
        "ب": "b",
        "ت": "t",
        "ث": "th",
        "ج": "j",
        "ح": "h",
        "خ": "kh",
        "د": "d",
        "ذ": "dh",
        "ر": "r",
        "ز": "z",
        "س": "s",
        "ش": "sh",
        "ص": "s",
        "ض": "d",
        "ط": "t",
        "ظ": "z",
        "ع": "",
        "غ": "gh",
        "ف": "f",
        "ق": "q",
        "ك": "k",
        "ل": "l",
        "م": "m",
        "ن": "n",
        "ه": "h",
        "و": "w",
        "ي": "y",
        "ة": "",
        "\u064e": "a",
        "\u064f": "u",
        "\u0650": "i",
        "\u0652": "",
    },
    "rules": [
        {"from": "\u064fو", "to": "u"},
        {"from": "\u0650ي", "to": "i"},
        {"from": "\u064eا", "to": "a"},
        {"from": "ال", "to": "al-", "start": True},
    ],
}


@pytest.mark.parametrize(
    "word,expected",
    [
        ("خالد", "Khalid"),
        ("كريم", "Karim"),
        ("محمود", "Mahmud"),
        ("أحمد", "Ahmad"),
        ("فاطمة", "Fatima"),
        ("خديجة", "Khadija"),
        ("زينب", "Zaynab"),
        ("حسن", "Hasan"),
        ("علي", "Ali"),
        ("زيد", "Zayd"),
        ("نور", "Nur"),
        ("جعفر", "Jafar"),
        ("جمال", "Jamal"),
        ("الرشيد", "Al-Rashid"),
        ("هارون الرشيد", "Harun al-Rashid"),
    ],
)
def test_template_vocalisation(word: str, expected: str) -> None:
    assert Scheme(_DEMO, hooks=_hooks()).transliterate(word) == expected


def test_vocalize_word_edge_cases() -> None:
    assert vocalize_word("") is None
    assert vocalize_word("م\u064fح\u064eم\u064e\u0651د") is None  # already vocalised
    assert vocalize_word("ابراهيم") is None  # no template: left to the lexicon
    assert has_harakat(vocalize_word("سالم") or "")


def test_existing_harakat_are_respected() -> None:
    s = Scheme(_DEMO, hooks=_hooks())
    assert s.transliterate("ح\u064fس\u064eي\u0652ن") == "Husayn"
