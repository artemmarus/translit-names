"""Names in the machine-readable zone (MRZ) of passports and ID cards.

Implements ICAO Doc 9303 (8th edition) Part 3 §4.6 and Parts 4/5:

- only ``A``–``Z`` and the filler ``<``; no digits, no diacritics;
- national characters are transliterated (Section 6 tables, or the issuing
  country's own table — e.g. KMU 2010 for Ukraine);
- apostrophes are deleted without a filler (``O'CONNOR`` → ``OCONNOR``);
  hyphens, spaces and commas inside an identifier become one ``<``;
- primary identifier (surname) ``<<`` secondary identifier (given names);
- the field is padded with ``<`` to 39 characters (TD3 passport) or
  30 (TD1 ID card), or truncated so that it ends with a letter.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from ._fold import fold
from ._registry import default_scheme_id, get_scheme
from .core import SchemeLike, resolve_scheme
from .detect import detect_language, detect_script
from .normalize import normalize

__all__ = ["TD1", "TD2", "TD3", "mrz_name", "mrz_text", "parse_mrz_name"]

TD3 = 39  #: passport (line 1, positions 6–44)
TD2 = 31  #: TD2 cards and MRV-B visas
TD1 = 30  #: ID cards (line 3)

_APOSTROPHES = "'\u2019\u02bc\u02bb\u2018`\u00b4\u02b9"
_SEP_RE = re.compile(r"[\s\-\u2010-\u2015,]+")
_FILLERS_RE = re.compile(r"<+")


def mrz_text(
    text: str, *, scheme: Optional[SchemeLike] = None, language: Optional[str] = None, german: bool = False
) -> str:
    """Convert one identifier (surname *or* given names) to MRZ characters.

    >>> mrz_text("Щербаков")
    'SHCHERBAKOV'
    >>> mrz_text("Smith-Jones")
    'SMITH<JONES'
    >>> mrz_text("D'Artagnan")
    'DARTAGNAN'
    """
    text = normalize(text)
    if not text:
        return ""
    if scheme is not None or detect_script(text) != "Latn":
        sch = resolve_scheme(text, scheme, language=language, purpose="mrz")
        if sch is not None:
            text = sch.transliterate(text)
    elif not german:
        # Latin-script languages with national letters (Azerbaijani Ə, Uzbek Oʻ/X …)
        lang = language or detect_language(text).language
        sid = default_scheme_id(lang, "mrz", "Latn")
        if sid:
            text = get_scheme(sid).transliterate(text)
    text = "".join(c for c in text if c not in _APOSTROPHES)
    text = fold(text, german=german).upper()
    text = _SEP_RE.sub("<", text)
    text = "".join(c for c in text if "A" <= c <= "Z" or c == "<")
    return _FILLERS_RE.sub("<", text).strip("<")


def _fit(primary: List[str], secondary: List[str], length: int, strategy: str) -> str:
    def build(p: List[str], s: List[str]) -> str:
        head = "<".join(x for x in p if x)
        tail = "<".join(x for x in s if x)
        return head + ("<<" + tail if tail else "")

    full = build(primary, secondary)
    if len(full) <= length:
        return full

    sec = list(secondary)
    if strategy == "initials":
        # Reduce secondary components (last first) to initials, keeping the first one.
        for k in range(len(sec) - 1, 0, -1):
            sec[k] = sec[k][:1]
            if len(build(primary, sec)) <= length:
                return build(primary, sec)
    elif strategy != "cut":
        raise ValueError(f"unknown truncation strategy {strategy!r}")

    prim = list(primary)
    # Make room for "<<" and at least the first letter of the secondary identifier.
    need = sum(len(x) for x in prim) + max(0, len(prim) - 1) + (3 if sec and sec[0] else 0)
    while need > length:
        k = max(range(len(prim)), key=lambda i: len(prim[i]))
        if len(prim[k]) <= 1:
            break
        prim[k] = prim[k][:-1]
        need -= 1
    out = build(prim, sec)[:length]
    while out.endswith("<"):
        # A truncated field must end with a letter: drop one more primary letter.
        k = max(range(len(prim)), key=lambda i: len(prim[i]))
        if len(prim[k]) <= 1:
            out = out.rstrip("<")
            break
        prim[k] = prim[k][:-1]
        out = build(prim, sec)[:length]
    return out


def mrz_name(
    surname: str,
    given_names: str = "",
    *,
    length: int = TD3,
    scheme: Optional[SchemeLike] = None,
    language: Optional[str] = None,
    strategy: str = "cut",
    pad: bool = True,
) -> str:
    """Build the MRZ name field.

    >>> mrz_name("Щербаков", "Юрий")
    'SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<'
    >>> mrz_name("Eriksson", "Anna Maria")
    'ERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<'
    >>> mrz_name("al-Basri", "Huda Muhammad Jawad")
    'AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<<<<<<<'

    ``length`` is 39 for passports (TD3), 31 for TD2, 30 for ID cards (TD1).
    ``strategy`` decides how over-long names are shortened: ``"cut"``
    (truncate, the field then ends with a letter) or ``"initials"`` (first
    reduce later given names to initials).  Patronymics are not part of the
    MRZ of Russian passports — pass only the given name.
    """
    p = mrz_text(surname, scheme=scheme, language=language)
    s = mrz_text(given_names, scheme=scheme, language=language) if given_names else ""
    primary = [x for x in p.split("<") if x]
    secondary = [x for x in s.split("<") if x]
    field = _fit(primary, secondary, length, strategy)
    if not secondary and pad:
        field = field + "<<" if len(field) + 2 <= length else field
    return field.ljust(length, "<") if pad else field


def parse_mrz_name(field: str) -> Tuple[str, str]:
    """Split an MRZ name field into (surname, given names) with spaces.

    >>> parse_mrz_name("AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<")
    ('AL BASRI', 'HUDA MUHAMMAD JAWAD')
    """
    field = field.strip().rstrip("<")
    primary, _, secondary = field.partition("<<")
    return primary.replace("<", " ").strip(), secondary.replace("<", " ").strip()
