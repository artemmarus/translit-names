from __future__ import annotations

import pytest

from translit_names import compare, is_match, jaro_winkler, name_key, name_keys, similarity, split_name


@pytest.mark.parametrize(
    "a,b",
    [
        # Cyrillic vs every passport generation and press spelling
        ("Щербаков Юрий", "Yuri Scherbakov"),
        ("Щербаков Юрий", "SHCHERBAKOV IURII"),
        ("Евгений", "Yevgeny"),
        ("Евгений", "Jewgeni"),
        ("Хрущёв", "Khrushchev"),
        ("Хрущёв", "Chruschtschow"),
        ("Чайковский", "Tchaikovsky"),
        ("Захаров", "Sacharow"),
        ("Жуков", "Schukow"),
        ("Иванов", "Ivanoff"),
        ("Ivanov Ivan Ivanovich", "IVAN IVANOV"),
        ("Олександр", "Aleksandr"),
        ("Аляксандр Лукашэнка", "Alexander Lukashenko"),
        # Arabic-origin names across languages and scripts
        ("Мухаммед Али", "Mohammed Ali"),
        ("محمد", "Mehmet"),
        ("Магомед", "Muhammad"),
        ("حسين", "Hüseyin"),
        ("Гусейн", "Hossein"),
        ("عبد الرحمن", "Abderrahmane"),
        ("Abdul Rahman", "Abdulrahman"),
        ("Abd al-Rahman", "Abdurrahman"),
        ("Nur ad-Din", "Noureddine"),
        ("Muhammad bin Salman", "محمد بن سلمان"),
        ("Нұрсұлтан Назарбаев", "Nursultan Nazarbayev"),
        ("Şirin", "Shirin"),
    ],
)
def test_same_person(a: str, b: str) -> None:
    assert similarity(a, b) >= 0.88, compare(a, b)


@pytest.mark.parametrize(
    "a,b",
    [
        ("Hasan", "Husayn"),
        ("Said", "Zayd"),
        ("Alexander Smith", "Alexandra Smith"),
        ("John Smith", "Ivan Petrov"),
        ("Ivan Petrov", "Igor Sokolov"),
        ("Fatima", "Fatih"),
    ],
)
def test_different_people(a: str, b: str) -> None:
    assert similarity(a, b) < 0.88, compare(a, b)


def test_weak_relations_are_explained() -> None:
    assert compare("Michael", "Михаил").pairs[0].reason == "equivalent"
    assert compare("Саша", "Александр").pairs[0].reason == "diminutive"
    assert 0.8 <= similarity("Саша Иванов", "Александр Иванов") < 0.97


def test_without_lexicon_skeleton_still_works() -> None:
    assert similarity("Mukhammed", "Mohamed", use_lexicon=False) >= 0.9
    assert similarity("Shcherbakov", "Szczerbakow", use_lexicon=False) >= 0.9
    assert compare("Mohammed", "Muhammad", use_lexicon=False).pairs[0].reason == "skeleton"


def test_initials() -> None:
    assert similarity("Ivanov I. I.", "Ivan Ivanov") >= 0.88
    assert similarity("Ivanov P.", "Ivan Ivanov") < 0.95


def test_order_independent() -> None:
    assert similarity("Ivanov Ivan", "Ivan Ivanov") == 1.0


def test_keys() -> None:
    assert name_keys("Mohammed") & name_keys("Мухаммед")
    assert name_keys("Aleksandr") & name_keys("Alexander")
    assert name_keys("Yuri") & name_keys("Jurij")
    assert name_key("Ivan Ivanov") == name_key("Иванов Иван")
    assert name_keys("") == frozenset()


def test_split_name() -> None:
    assert split_name("Анна-Мария Петрова") == ["Анна", "Мария", "Петрова"]
    assert split_name("Harun al-Rashid") == ["Harun", "al-Rashid"]


def test_jaro_winkler() -> None:
    assert jaro_winkler("martha", "marhta") == pytest.approx(0.9611, abs=1e-3)
    assert jaro_winkler("", "") == 0.0
    assert jaro_winkler("abc", "abc") == 1.0
    assert jaro_winkler("abc", "xyz") == 0.0


def test_is_match_threshold() -> None:
    assert is_match("Мухаммед", "Mohammed")
    assert not is_match("Мухаммед", "Mohammed", threshold=0.999)
