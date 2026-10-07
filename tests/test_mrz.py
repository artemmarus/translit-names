"""MRZ name field — examples from ICAO Doc 9303 Parts 3 and 4 (8th ed.)."""

from __future__ import annotations

import pytest

from translit_names import mrz_name, mrz_text, parse_mrz_name
from translit_names.mrz import TD1


@pytest.mark.parametrize(
    "surname,given,expected",
    [
        ("ERIKSSON", "ANNA MARIA", "ERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"),
        ("HENG", "DEBORAH MING LO", "HENG<<DEBORAH<MING<LO<<<<<<<<<<<<<<<<<<"),
        ("SMITH-JONES", "SUSIE MARGARET", "SMITH<JONES<<SUSIE<MARGARET<<<<<<<<<<<<"),
        ("O'CONNOR", "ENYA SIOBHAN", "OCONNOR<<ENYA<SIOBHAN<<<<<<<<<<<<<<<<<<"),
        ("VAN DER MUELLEN", "MARTIN", "VAN<DER<MUELLEN<<MARTIN<<<<<<<<<<<<<<<<"),
        ("AL-BASRI", "HUDA MUHAMMAD JAWAD", "AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<<<<<<<"),
        ("VILARCHAO FERNANDEZ", "JOSE RAMON", "VILARCHAO<FERNANDEZ<<JOSE<RAMON<<<<<<<<"),
        ("ARKFREITH", "", "ARKFREITH<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"),
        ("NILAVADHANANANDA", "ARNPOL PETCH CHARONGUANG", "NILAVADHANANANDA<<ARNPOL<PETCH<CHARONGU"),
        ("PAPANDROPOULOUS", "JONATHON WARREN TREVOR", "PAPANDROPOULOUS<<JONATHON<WARREN<TREVOR"),
    ],
)
def test_icao_examples(surname: str, given: str, expected: str) -> None:
    out = mrz_name(surname, given)
    assert out == expected
    assert len(out) == 39


def test_initials_strategy() -> None:
    out = mrz_name("NILAVADHANANANDA", "CHAYAPA DEJTHAMRONG KRASUANG", strategy="initials")
    assert out == "NILAVADHANANANDA<<CHAYAPA<DEJTHAMRONG<K"


def test_truncated_field_ends_with_letter() -> None:
    out = mrz_name("BENNELONG WOOLOOMOOLOO WARRANDYTE WARNAMBOOL", "DINGO POTOROO")
    assert len(out) == 39
    assert out[-1].isalpha()
    assert "<<D" in out
    td1 = mrz_name("BENNELONG WOOLOOMOOLOO WARRANDYTE WARNAMBOOL", "DINGO POTOROO", length=TD1)
    assert len(td1) == 30 and td1[-1].isalpha()


def test_diacritics_and_special_letters() -> None:
    assert mrz_text("Térèsa Cañon") == "TERESA<CANON"
    assert mrz_text("Wałęsa") == "WALESA"
    assert mrz_text("Gößmann") == "GOSSMANN"
    assert mrz_text("Müller", german=True) == "MUELLER"
    assert mrz_text("Đoković") == "DOKOVIC"


def test_cyrillic_uses_passport_scheme() -> None:
    assert mrz_name("Щербаков", "Юрий") == "SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<"
    assert mrz_text("Анна-Мария") == "ANNA<MARIIA"


def test_parse() -> None:
    assert parse_mrz_name("AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<") == ("AL BASRI", "HUDA MUHAMMAD JAWAD")
    assert parse_mrz_name("ARKFREITH<<<<<") == ("ARKFREITH", "")
