"""Structural checks for the bundled name lexicon files."""

from __future__ import annotations

import json
import re
from importlib import resources

import pytest

NAMES_DIR = resources.files("translit_names") / "data" / "names"
FILES = sorted(p.name for p in NAMES_DIR.iterdir() if p.name.endswith(".json"))

KINDS = {"given", "family", "element", "compound"}
GENDERS = {"m", "f", "u"}
HARAKAT = re.compile("[\u064b-\u0652\u0670]")
ARABIC = re.compile("[\u0600-ۿݐ-ݿ]")
CYRILLIC = re.compile("[Ѐ-ԯ]")
ARABIC_LANGS = {"ar", "fa", "ur", "ps", "ug", "ckb", "sd", "ks"}
CYRILLIC_LANGS = {
    "ru",
    "uk",
    "be",
    "bg",
    "sr",
    "mk",
    "kk",
    "ky",
    "tg",
    "tt",
    "ba",
    "ce",
    "inh",
    "av",
    "cv",
    "sah",
    "kbd",
    "mn",
}
ID_RE = re.compile(r"^[a-z0-9_]+$")


def _load(name: str) -> dict:
    return json.loads((NAMES_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("fname", FILES)
def test_file_structure(fname: str) -> None:
    data = _load(fname)
    assert isinstance(data.get("names"), list) and data["names"], f"{fname}: empty 'names'"
    ids = [n["id"] for n in data["names"]]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"{fname}: duplicate ids {sorted(dupes)}"


@pytest.mark.parametrize("fname", FILES)
def test_entries(fname: str) -> None:
    problems = []
    for e in _load(fname)["names"]:
        eid = e.get("id", "?")
        if not ID_RE.match(eid):
            problems.append(f"{eid}: bad id")
        if e.get("kind", "given") not in KINDS:
            problems.append(f"{eid}: bad kind {e.get('kind')}")
        if e.get("gender", "u") not in GENDERS:
            problems.append(f"{eid}: bad gender {e.get('gender')}")
        if not e.get("english"):
            problems.append(f"{eid}: missing english")
        native = e.get("native", {})
        if not native:
            problems.append(f"{eid}: missing native")
        for lang, forms in native.items():
            forms = [forms] if isinstance(forms, str) else forms
            for f in forms:
                if lang in ARABIC_LANGS:
                    if not ARABIC.search(f):
                        problems.append(f"{eid}: native[{lang}] {f!r} is not Arabic script")
                    if HARAKAT.search(f):
                        problems.append(f"{eid}: native[{lang}] {f!r} must be unvocalized")
                if lang in CYRILLIC_LANGS and not CYRILLIC.search(f):
                    problems.append(f"{eid}: native[{lang}] {f!r} is not Cyrillic")
        has_arabic = any(lang in ARABIC_LANGS for lang in native)
        voc = e.get("vocalized", "")
        if has_arabic and e.get("kind") != "family" and not voc:
            problems.append(f"{eid}: Arabic-script name without 'vocalized'")
        if voc and not HARAKAT.search(voc):
            problems.append(f"{eid}: 'vocalized' has no harakat")
        for lang, forms in e.get("latin", {}).items():
            forms = [forms] if isinstance(forms, str) else forms
            for f in forms:
                if ARABIC.search(f) or CYRILLIC.search(f):
                    problems.append(f"{eid}: latin[{lang}] {f!r} is not Latin")
        for f in e.get("variants", []):
            if ARABIC.search(f) or CYRILLIC.search(f):
                problems.append(f"{eid}: variant {f!r} is not Latin")
    assert not problems, "\n".join(problems[:50])


def test_lexicon_loads() -> None:
    from translit_names.lexicon import get_lexicon

    lex = get_lexicon()
    assert len(lex) > 0 or not FILES
