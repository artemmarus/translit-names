from __future__ import annotations

import pytest

from translit_names import Scheme, SchemeError
from translit_names._engine import titlecase_name

UK = {
    "id": "t_uk",
    "map": {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ю": "iu",
        "я": "ia",
        "'": "",
    },
    "aliases": {"\u2019": "'", "\u02bc": "'"},
    "rules": [
        {"from": "є", "to": "ye", "start": True},
        {"from": "ї", "to": "yi", "start": True},
        {"from": "й", "to": "y", "start": True},
        {"from": "ю", "to": "yu", "start": True},
        {"from": "я", "to": "ya", "start": True},
        {"from": "зг", "to": "zgh"},
    ],
}


@pytest.mark.parametrize(
    "src,expected",
    [
        ("Згорани", "Zghorany"),
        ("Розгон", "Rozghon"),
        ("Знам'янка", "Znamianka"),
        ("Знам\u2019янка", "Znamianka"),
        ("Їжакевич", "Yizhakevych"),
        ("Кадиївка", "Kadyivka"),
        ("Стрий", "Stryi"),
        ("Юрій", "Yurii"),
        ("Анна-Яна", "Anna-Yana"),
        ("ЄНАКІЄВЕ", "YENAKIIEVE"),
        ("ЮРІЙ ЩЕРБАК", "YURII SHCHERBAK"),
        ("Я", "Ya"),
        ("Ю. Щербак", "Yu. Shcherbak"),
    ],
)
def test_word_start_and_case(src: str, expected: str) -> None:
    assert Scheme(UK).transliterate(src) == expected


def test_after_before_and_classes() -> None:
    s = Scheme(
        {
            "id": "t",
            "classes": {"V": "аеиоуыэюяё"},
            "map": {"е": "e", "л": "l", "ь": "", "ц": "ts", "и": "i", "н": "n", "с": "s", "в": "v", "а": "a"},
            "rules": [
                {"from": "е", "to": "ye", "after": "^{V}ьъ"},
                {"from": "с", "to": "ss", "after": "{V}", "before": "{V}"},
            ],
        }
    )
    assert s("Ельцин") == "Yeltsin"
    assert s("Васильева") == "Vassilyeva"
    assert s("ЕЛЬЦИН") == "YELTSIN"


def test_not_after_not_before_end() -> None:
    s = Scheme(
        {
            "id": "t",
            "map": {"и": "i", "я": "ya", "й": "y", "к": "k", "о": "o", "с": "s", "ф": "f"},
            "rules": [
                {"from": "ия", "to": "ia", "end": True},
                {"from": "и", "to": "y", "not_after": "^", "not_before": "$кся"},
            ],
        }
    )
    assert s("София") == "Sofia"
    assert s("Сия") == "Sia"


def test_digraph_collapsing_keeps_case() -> None:
    s = Scheme(
        {
            "id": "t",
            "map": {"к": "k", "с": "s", "е": "e", "н": "n", "и": "i", "я": "ia"},
            "rules": [{"from": "кс", "to": "x"}],
        }
    )
    assert s("Ксения") == "Xeniia"
    assert s("КСЕНИЯ") == "XENIIA"


def test_longest_match_and_order() -> None:
    s = Scheme({"id": "t", "map": {"a": "1", "ab": "2", "abc": "3"}})
    assert s("abcab a") == "32 1"


def test_unknown_characters_fallback() -> None:
    keep = Scheme({"id": "t", "map": {"а": "a"}})
    drop = Scheme({"id": "t", "map": {"а": "a"}, "fallback": "drop"})
    fold = Scheme({"id": "t", "map": {"а": "a"}, "fallback": "ascii"})
    assert keep("аЖ 1") == "aЖ 1"
    assert drop("аЖ 1") == "a 1"
    assert fold("аé") == "ae"


def test_gemination() -> None:
    s = Scheme(
        {
            "id": "t",
            "geminate": "\u0651",
            "map": {"م": "m", "ح": "ḥ", "د": "d", "\u064e": "a", "\u064f": "u", "\u0652": ""},
            "titlecase": True,
        }
    )
    # shadda written after or before the vowel mark gives the same result
    assert s("م\u064fح\u064eم\u064e\u0651د") == "Muḥammad"
    assert s("م\u064fح\u064eم\u064e\u0651د".replace("\u064e\u0651", "\u0651\u064e")) == "Muḥammad"


def test_case_modes_and_post() -> None:
    upper = Scheme({"id": "t", "map": {"б": "b"}, "case": "upper"})
    preserve = Scheme({"id": "t", "map": {"ح": "H", "ب": "b"}, "case": "preserve"})
    post = Scheme({"id": "t", "map": {"б": "b"}, "post": [{"pattern": "bb", "replace": "b"}]})
    assert upper("бб") == "BB"
    assert preserve("حب") == "Hb"
    assert post("бб") == "b"


@pytest.mark.parametrize(
    "spec",
    [
        {"map": {}},
        {"id": "x", "rules": [{"from": "a"}]},
        {"id": "x", "rules": [{"from": "a", "to": "b", "bogus": 1}]},
        {"id": "x", "rules": [{"from": "a", "to": "b", "after": "{NOPE}"}]},
        {"id": "x", "case": "weird"},
        {"id": "x", "hook": "missing"},
    ],
)
def test_bad_specs(spec: dict) -> None:
    with pytest.raises(SchemeError):
        Scheme(spec)


def test_titlecase_particles() -> None:
    assert titlecase_name("muḥammad ibn \u02bbabd allāh", ["ibn"]) == "Muḥammad ibn \u02bbAbd Allāh"
    assert titlecase_name("al-rashīd", ["al-"]) == "Al-Rashīd"
    assert titlecase_name("hārūn al-rashīd", ["al-"]) == "Hārūn al-Rashīd"
    assert titlecase_name("nūr ad-dīn", ["ad-"]) == "Nūr ad-Dīn"


def test_alphabet_property() -> None:
    s = Scheme({"id": "t", "map": {"а": "a", "зг": "zgh"}, "rules": [{"from": "б", "to": "b", "start": True}]})
    assert s.alphabet == frozenset({"а", "б"})
