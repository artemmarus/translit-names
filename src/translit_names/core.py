"""High-level transliteration entry point."""

from __future__ import annotations

from typing import Optional, Union

from ._engine import Scheme
from ._registry import default_scheme_id, get_scheme
from .detect import detect_language, detect_script
from .normalize import fix_mixed_script, normalize

__all__ = ["resolve_scheme", "transliterate"]

SchemeLike = Union[str, Scheme]


def resolve_scheme(
    text: str,
    scheme: Optional[SchemeLike] = None,
    *,
    language: Optional[str] = None,
    purpose: str = "transliterate",
) -> Optional[Scheme]:
    """Pick the scheme for ``text``.

    ``purpose`` selects the section of ``defaults.json``: ``transliterate``
    (official/passport system), ``mrz`` (ICAO machine-readable zone) or
    ``match`` (stable ASCII form used for matching keys).  Returns ``None``
    when the text needs no transliteration (plain ASCII Latin).
    """
    if isinstance(scheme, Scheme):
        return scheme
    if scheme:
        return get_scheme(scheme)
    script = detect_script(text)
    lang = language or detect_language(text).language
    sid = default_scheme_id(lang, purpose, script)
    if sid is None:
        return None
    return get_scheme(sid)


def transliterate(
    text: str,
    scheme: Optional[SchemeLike] = None,
    *,
    language: Optional[str] = None,
    clean: bool = True,
) -> str:
    """Transliterate a name (or any short text) into Latin script.

    >>> transliterate("Щербаков Юрий")
    'Shcherbakov Iurii'
    >>> transliterate("Щербаков Юрий", "ru_bgn_pcgn")
    'Shcherbakov Yuriy'
    >>> transliterate("Олександр Згурський", language="uk")
    'Oleksandr Zghurskyi'

    Without ``scheme`` the language is detected from the letters and the
    default (official / passport) scheme for that language is used.
    ``clean`` normalises Unicode and repairs mixed Latin/Cyrillic look-alikes
    before transliteration.
    """
    if clean:
        text = fix_mixed_script(normalize(text))
    sch = resolve_scheme(text, scheme, language=language)
    if sch is None:
        return text
    return sch.transliterate(text)
