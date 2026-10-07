from __future__ import annotations

import pytest

from translit_names import get_lexicon, variants, variants_detailed


def test_russian_name_variants_cover_all_passport_generations() -> None:
    out = variants("Юрий", limit=12)
    assert out[0] == "Iurii"  # current Russian passport (ICAO 9303)
    for expected in ("Yuriy", "Yuri", "Yury"):
        assert expected in out


def test_full_name_variants() -> None:
    out = variants("Евгений Щербаков", limit=30)
    assert out[0] == "Evgenii Shcherbakov"
    assert "Yevgeny Shcherbakov" in out
    assert all(v.isascii() for v in out)


def test_arabic_variants_use_lexicon() -> None:
    out = variants("محمد", limit=8)
    assert out[0] == "Muhammad"
    assert {"Mohammed", "Mohamed", "Mohammad"} <= set(out)


def test_arabic_compound_kept_together() -> None:
    out = variants("عبد الرحمن", limit=10)
    assert "Abdulrahman" in out or "Abdul Rahman" in out
    assert not any("Rhmn" in v for v in out)


def test_detailed_scores_sorted() -> None:
    vs = variants_detailed("Хусейн", limit=10)
    assert [v.score for v in vs] == sorted((v.score for v in vs), reverse=True)
    assert vs[0].sources


def test_variants_without_lexicon() -> None:
    out = variants("Юрий", use_lexicon=False, limit=10)
    assert "Iurii" in out and "Yuriy" in out


def test_unicode_variants_keep_diacritics() -> None:
    assert any(not v.isascii() for v in variants("Гусейн", ascii_only=False, limit=40))


@pytest.mark.parametrize(
    "text,entry_id",
    [
        ("Магомед", "muhammad"),
        ("محمد", "muhammad"),
        ("Mehmet", "muhammad"),
        ("Hossain", "husayn"),
        ("Олександр", "aleksandr"),
        ("Iurii", "yuriy"),
        ("Jewgeni", "yevgeniy"),
    ],
)
def test_lexicon_lookup(text: str, entry_id: str) -> None:
    assert entry_id in [e.id for e in get_lexicon().lookup(text)]


def test_lexicon_unknown_cyrillic_returns_nothing() -> None:
    assert get_lexicon().lookup("Вольдемарище") == []


def test_lexicon_short_and_equivalents_are_separate() -> None:
    lex = get_lexicon()
    assert lex.lookup("Саша") == []
    assert "aleksandr" in [e.id for e in lex.lookup_short("Саша")]
    assert "ivan" in [e.id for e in lex.lookup_equivalents("John")]
    assert "ivan" not in [e.id for e in lex.lookup("John")]


def test_lexicon_related_ids_resolve() -> None:
    lex = get_lexicon()
    missing = {(e.id, r) for e in lex for r in e.related if lex.get(r) is None}
    assert not missing, sorted(missing)[:20]
