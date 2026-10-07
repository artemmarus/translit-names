"""Every bundled scheme must reproduce its own ``samples``."""

from __future__ import annotations

import pytest

from translit_names import get_scheme
from translit_names._registry import scheme_specs

SPECS = scheme_specs()
SAMPLES = [
    pytest.param(sid, src, expected, id=f"{sid}:{src}")
    for sid, spec in sorted(SPECS.items())
    for src, expected in spec.get("samples", [])
]


@pytest.mark.parametrize("sid,src,expected", SAMPLES)
def test_sample(sid: str, src: str, expected: str) -> None:
    assert get_scheme(sid).transliterate(src) == expected


@pytest.mark.parametrize("sid", sorted(SPECS))
def test_scheme_metadata(sid: str) -> None:
    spec = SPECS[sid]
    for key in ("id", "title", "language", "script", "kind", "status", "sources", "description"):
        assert spec.get(key), f"{sid}: missing {key}"
    assert spec["kind"] in {
        "passport",
        "official",
        "geographic",
        "library",
        "scholarly",
        "practical",
        "ascii",
        "legacy",
    }
    assert spec["status"] in {"current", "superseded", "draft", "informal"}
    assert len(spec.get("samples", [])) >= 3, f"{sid}: needs at least 3 samples"


@pytest.mark.parametrize("sid", sorted(SPECS))
def test_ascii_flag(sid: str) -> None:
    scheme = get_scheme(sid)
    if not scheme.ascii:
        return
    for src, _ in scheme.samples:
        out = scheme.transliterate(src)
        assert out.isascii(), f"{sid}: non-ASCII output {out!r} for {src!r}"


@pytest.mark.parametrize("sid", sorted(SPECS))
def test_full_alphabet_covered(sid: str) -> None:
    """Letters declared in ``alphabet`` must all have a mapping."""
    spec = SPECS[sid]
    alphabet = spec.get("alphabet")
    if not alphabet:
        return
    scheme = get_scheme(sid)
    known = scheme.alphabet
    missing = [c for c in alphabet.lower() if c not in known and c.strip()]
    assert not missing, f"{sid}: no mapping for {missing}"


@pytest.mark.parametrize("sid", sorted(SPECS))
def test_no_source_letters_left(sid: str) -> None:
    """Transliterating the whole alphabet (any case) leaves no source-script letters."""
    from translit_names.normalize import script_of

    spec = SPECS[sid]
    alphabet = spec.get("alphabet", "")
    if not alphabet or spec["script"] == "Latn":
        return
    out = get_scheme(sid).transliterate(" ".join([alphabet, alphabet.upper(), alphabet.title()]))
    left = sorted({c for c in out if script_of(c) == spec["script"]})
    assert not left, f"{sid}: untransliterated {left}"
