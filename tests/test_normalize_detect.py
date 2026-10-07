from __future__ import annotations

import pytest

from translit_names import detect_language, detect_script, fix_mixed_script, fold, normalize
from translit_names.normalize import arabic_key, latin_key, strip_arabic_diacritics, unify_apostrophes


def test_normalize() -> None:
    assert normalize("  Анна\u00a0\u2013\u00a0Мария  ") == "Анна - Мария"
    assert normalize("Е\u0308лкин") == "Ёлкин"
    assert normalize("١٢٣") == "123"
    assert normalize("ﻻ") == "لا"
    assert normalize("محـــمد") == "محمد"


def test_mixed_script() -> None:
    assert fix_mixed_script("Аlexey") == "Alexey"  # Cyrillic А in a Latin word
    assert fix_mixed_script("Иванoв") == "Иванов"  # Latin o in a Cyrillic word
    assert fix_mixed_script("Кадыров Рамзан") == "Кадыров Рамзан"
    assert fix_mixed_script("Мал1ик") == "Мал1ик"  # digits untouched outside palochka contexts


def test_apostrophes() -> None:
    assert unify_apostrophes("O\u2018zbek \u02bc") == "O'zbek '"


def test_arabic_keys() -> None:
    assert arabic_key("م\u064fح\u064eم\u064e\u0651د") == arabic_key("محمد")
    assert arabic_key("أحمد") == arabic_key("احمد")
    assert arabic_key("فاطمة") == arabic_key("فاطمه")
    assert arabic_key("علی") == arabic_key("علي")
    assert strip_arabic_diacritics("م\u064fح\u064eم\u064e\u0651د") == "محمد"


def test_latin_key_and_fold() -> None:
    assert latin_key("Hüseyin") == "huseyin"
    assert latin_key("Abd al-Rahman") == "abdalrahman"
    assert fold("Łódź Ærø Þór Məmmədov İstanbul") == "Lodz Aeroe Thor Mammadov Istanbul"
    assert fold("ÆSIR") == "AESIR"
    assert fold("Ä Ö Ü", german=True) == "AE OE UE"


@pytest.mark.parametrize(
    "text,lang",
    [
        ("Иван Петров", "ru"),
        ("Олександр Їжакевич", "uk"),
        ("Аляксандр Лукашэнка Ўладзімір", "be"),
        ("Нұрсұлтан Назарбаев", "kk"),
        ("Эмомалӣ Раҳмон", "tg"),
        ("Ђорђе Јовановић", "sr"),
        ("Ѓорѓе Петров", "mk"),
        ("Минтимер Шәймиев җ", "tt"),
        ("Христо Стоичков Ъгъл", "bg"),
        ("محمد بن سلمان", "ar"),
        ("محمود احمدی\u200cنژاد پژمان", "fa"),
        ("عمران خان ٹیپو", "ur"),
        ("ګلبدين حکمتيار ښه", "ps"),
        ("Łukasz Żółć", "pl"),
        ("Antonín Dvořák", "cs"),
        ("Recep Tayyip Erdoğan", "tr"),
        ("İlham Əliyev", "az"),
        ("Shavkat Mirziyoyev O\u02bbg\u02bbli", "uz"),
        ("Novak Đoković", "sh"),
        ("John Smith", "en"),
    ],
)
def test_detect_language(text: str, lang: str) -> None:
    assert detect_language(text).language == lang


def test_detect_script() -> None:
    assert detect_script("Иван") == "Cyrl"
    assert detect_script("محمد") == "Arab"
    assert detect_script("Ivan") == "Latn"
    assert detect_script("123") == "Zyyy"
