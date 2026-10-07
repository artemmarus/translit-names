from __future__ import annotations

import json

import pytest

from translit_names import default_scheme_id, get_scheme, list_schemes, transliterate
from translit_names._registry import defaults_config
from translit_names.cli import main


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Щербаков Юрий", "Shcherbakov Iurii"),
        ("Сергій Корольов", "Serhii Korolov"),
        ("Нұрсұлтан Назарбаев", "Nursultan Nazarbayev"),
        ("Эмомалӣ Раҳмон", "Emomali Rahmon"),
        ("Новак Ђоковић", "Novak Đoković"),
        ("John Smith", "John Smith"),
    ],
)
def test_transliterate_auto(text: str, expected: str) -> None:
    assert transliterate(text) == expected


def test_transliterate_with_scheme_and_language() -> None:
    assert transliterate("Щербаков Юрий", "ru_bgn_pcgn") == "Shcherbakov Yuriy"
    assert transliterate("Щербаков Юрий", "ru-wikipedia") == "Shcherbakov Yury"
    assert transliterate("Христо Стоичков", language="bg") == "Hristo Stoichkov"
    assert transliterate("Олександр Згурський", language="uk") == "Oleksandr Zghurskyi"


def test_transliterate_repairs_mixed_script() -> None:
    assert transliterate("Иванoв") == "Ivanov"  # Latin "o" inside a Cyrillic word


def test_unknown_scheme() -> None:
    with pytest.raises(KeyError):
        get_scheme("xx_nope")


def test_every_default_points_to_an_existing_scheme() -> None:
    ids = {s.id for s in list_schemes()}
    for purpose, table in defaults_config().items():
        if not isinstance(table, dict):
            continue
        for lang, sid in table.items():
            assert sid in ids, f"{purpose}.{lang} -> {sid}"


def test_default_scheme_id_respects_script() -> None:
    assert default_scheme_id("az", "mrz", "Latn") == "az_ascii"
    assert default_scheme_id("ru") == "ru_icao"
    assert default_scheme_id("xx") is None


def test_list_schemes_filters() -> None:
    assert all(s.language == "uk" for s in list_schemes("uk"))
    assert all(s.kind == "passport" for s in list_schemes(kind="passport"))
    assert len(list_schemes()) >= 80


def test_cli_translit(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Щербаков", "Юрий"]) == 0
    assert capsys.readouterr().out.strip() == "Shcherbakov Iurii"
    assert main(["translit", "-s", "ru_bgn_pcgn", "Юрий"]) == 0
    assert capsys.readouterr().out.strip() == "Yuriy"


def test_cli_all_schemes(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["translit", "--all", "Юрий"]) == 0
    out = capsys.readouterr().out
    assert "ru_icao" in out and "ru_bgn_pcgn" in out


def test_cli_variants_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["variants", "--json", "-n", "5", "Юрий"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data[0]["text"] == "Iurii" and len(data) == 5


def test_cli_match_exit_code(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["match", "Мухаммед", "Mohammed"]) == 0
    assert "MATCH" in capsys.readouterr().out
    assert main(["match", "Hasan", "Husayn"]) == 1


def test_cli_mrz_detect_schemes(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["mrz", "Щербаков", "Юрий"]) == 0
    assert capsys.readouterr().out.strip() == "SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<"
    assert main(["detect", "Олександр Їжакевич"]) == 0
    assert capsys.readouterr().out.startswith("uk")
    assert main(["schemes", "-l", "uk"]) == 0
    assert "uk_kmu_2010" in capsys.readouterr().out


def test_cli_unknown_scheme(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["translit", "-s", "nope", "x"]) == 2
    assert "unknown scheme" in capsys.readouterr().err
