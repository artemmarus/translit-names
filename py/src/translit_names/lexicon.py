"""Name lexicon: clusters of spellings of the same personal name across scripts.

Each entry groups the native-script spellings of a name (``Александр``,
``Олександр``, ``محمد``, ``Мухаммад``), its conventional Latin spellings per
language and an open list of attested variants.  The lexicon drives
vocalisation of Arabic-script names, practical English spellings, variant
generation and cross-script matching.
"""

from __future__ import annotations

import json
import threading
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from ._data import data_path
from .normalize import arabic_key, latin_key

__all__ = ["Lexicon", "NameEntry", "get_lexicon"]


@dataclass(frozen=True)
class NameEntry:
    """One name cluster."""

    id: str
    kind: str = "given"
    gender: str = "u"
    origin: str = ""
    english: str = ""
    native: Mapping[str, Tuple[str, ...]] = field(default_factory=dict)
    latin: Mapping[str, Tuple[str, ...]] = field(default_factory=dict)
    variants: Tuple[str, ...] = ()
    equivalents: Tuple[str, ...] = ()
    short: Tuple[str, ...] = ()
    vocalized: str = ""
    related: Tuple[str, ...] = ()
    source: str = ""

    def latin_for(self, languages: Sequence[str]) -> Optional[str]:
        """First conventional Latin spelling for the first matching language key.

        ``"ar_eg"`` falls back to ``"ar"``; ``"en"`` means :attr:`english`.
        """
        for lang in languages:
            if lang == "en" and self.english:
                return self.english
            for key in (lang, lang.split("_")[0]):
                forms = self.latin.get(key)
                if forms:
                    return forms[0]
        return None

    def all_latin(self) -> List[str]:
        """Every Latin spelling known for this cluster, most canonical first."""
        seen: Dict[str, None] = {}
        if self.english:
            seen[self.english] = None
        for forms in self.latin.values():
            for f in forms:
                seen.setdefault(f, None)
        for f in self.variants:
            seen.setdefault(f, None)
        return list(seen)

    def all_native(self) -> List[str]:
        seen: Dict[str, None] = {}
        for forms in self.native.values():
            for f in forms:
                seen.setdefault(f, None)
        return list(seen)


def _tuple(v: Any) -> Tuple[str, ...]:
    if v is None:
        return ()
    if isinstance(v, str):
        return (v,)
    return tuple(v)


def _entry(raw: Mapping[str, Any], source: str) -> NameEntry:
    return NameEntry(
        id=raw["id"],
        kind=raw.get("kind", "given"),
        gender=raw.get("gender", "u"),
        origin=raw.get("origin", ""),
        english=raw.get("english", ""),
        native={k: _tuple(v) for k, v in raw.get("native", {}).items()},
        latin={k: _tuple(v) for k, v in raw.get("latin", {}).items()},
        variants=_tuple(raw.get("variants")),
        equivalents=_tuple(raw.get("equivalents")),
        short=_tuple(raw.get("short")),
        vocalized=unicodedata.normalize("NFC", raw.get("vocalized", "")),
        related=_tuple(raw.get("related")),
        source=source,
    )


class Lexicon:
    """In-memory index over name entries."""

    def __init__(self, entries: Iterable[NameEntry]) -> None:
        self.entries: Dict[str, NameEntry] = {}
        self._native: Dict[str, List[Tuple[str, NameEntry]]] = {}
        self._arabic: Dict[str, List[Tuple[str, NameEntry]]] = {}
        self._latin: Dict[str, List[NameEntry]] = {}
        self._short: Dict[str, List[NameEntry]] = {}
        self._equiv: Dict[str, List[NameEntry]] = {}
        for e in entries:
            if e.id in self.entries:
                e = _merge(self.entries[e.id], e)
            self.entries[e.id] = e
        for e in self.entries.values():
            self._index(e)

    def _index(self, e: NameEntry) -> None:
        for lang, forms in e.native.items():
            for form in forms:
                key = _native_key(form)
                self._native.setdefault(key, []).append((lang, e))
                if _is_arabic_script(form):
                    akey = arabic_key(form)
                    self._arabic.setdefault(akey, []).append((lang, e))
                    if " " in akey:
                        self._arabic.setdefault(akey.replace(" ", ""), []).append((lang, e))
        for form in e.all_latin():
            if _script_of_text(form) != "Latn":
                continue
            key = latin_key(form)
            if key:
                bucket = self._latin.setdefault(key, [])
                if e not in bucket:
                    bucket.append(e)
        for form in e.equivalents:
            key = latin_key(form)
            if key:
                bucket = self._equiv.setdefault(key, [])
                if e not in bucket:
                    bucket.append(e)
        for form in e.short:
            for key in {_native_key(form), latin_key(form) if _script_of_text(form) == "Latn" else ""}:
                if key:
                    bucket = self._short.setdefault(key, [])
                    if e not in bucket:
                        bucket.append(e)

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(self.entries.values())

    def get(self, entry_id: str) -> Optional[NameEntry]:
        return self.entries.get(entry_id)

    def lookup_native(self, text: str, language: Optional[str] = None) -> List[NameEntry]:
        """Entries with ``text`` among their native-script spellings."""
        hits = self._native.get(_native_key(text), [])
        if not hits and _is_arabic_script(text):
            hits = self._arabic.get(arabic_key(text), [])
        return _rank(hits, language)

    def lookup_arabic(self, text: str, language: Optional[str] = None) -> List[NameEntry]:
        """Entries whose Arabic-script spelling matches ``text`` ignoring
        vowel marks, hamza seats and Persian/Arabic letter variants."""
        return _rank(self._arabic.get(arabic_key(text), []), language)

    def lookup_latin(self, text: str) -> List[NameEntry]:
        """Entries with a Latin spelling equal to ``text`` (case/diacritics-insensitive)."""
        key = latin_key(text)
        return list(self._latin.get(key, [])) if key else []

    def lookup_short(self, text: str) -> List[NameEntry]:
        """Entries for which ``text`` is a diminutive or short form (Саша, Sasha)."""
        found: List[NameEntry] = []
        for key in (_native_key(text), latin_key(text)):
            for e in self._short.get(key, []) if key else []:
                if e not in found:
                    found.append(e)
        return found

    def lookup_equivalents(self, text: str) -> List[NameEntry]:
        """Entries for which ``text`` is a translation equivalent, not a
        transliteration (John for Иван, Michael for Михаил, Cyrus for کوروش)."""
        key = latin_key(text)
        return list(self._equiv.get(key, [])) if key else []

    def lookup(self, text: str, language: Optional[str] = None, *, include_short: bool = False) -> List[NameEntry]:
        """Look a single name up in any script.

        Native-script matches come first, then Latin-spelling matches
        (``Jurij`` is both Slovene for George and a German rendering of
        Юрий).  Diminutives are included only with ``include_short``.
        """
        found = self.lookup_native(text, language)
        if _script_of_text(text) == "Latn":
            for e in self.lookup_latin(text):
                if e not in found:
                    found.append(e)
        if include_short:
            for e in self.lookup_short(text):
                if e not in found:
                    found.append(e)
        return found


def _merge(a: NameEntry, b: NameEntry) -> NameEntry:
    def merge_map(x: Mapping[str, Tuple[str, ...]], y: Mapping[str, Tuple[str, ...]]) -> Dict[str, Tuple[str, ...]]:
        out = {k: tuple(v) for k, v in x.items()}
        for k, v in y.items():
            out[k] = tuple(dict.fromkeys(out.get(k, ()) + tuple(v)))
        return out

    return NameEntry(
        id=a.id,
        kind=a.kind,
        gender=a.gender if a.gender != "u" else b.gender,
        origin=a.origin or b.origin,
        english=a.english or b.english,
        native=merge_map(a.native, b.native),
        latin=merge_map(a.latin, b.latin),
        variants=tuple(dict.fromkeys(a.variants + b.variants)),
        equivalents=tuple(dict.fromkeys(a.equivalents + b.equivalents)),
        short=tuple(dict.fromkeys(a.short + b.short)),
        vocalized=a.vocalized or b.vocalized,
        related=tuple(dict.fromkeys(a.related + b.related)),
        source=a.source,
    )


def _rank(hits: List[Tuple[str, NameEntry]], language: Optional[str]) -> List[NameEntry]:
    seen: Dict[str, NameEntry] = {}
    if language:
        for lang, e in hits:
            if lang == language:
                seen.setdefault(e.id, e)
    for _, e in hits:
        seen.setdefault(e.id, e)
    return list(seen.values())


def _native_key(text: str) -> str:
    return unicodedata.normalize("NFC", text).strip().lower().replace("ё", "е")


def _script_of_text(text: str) -> str:
    from .detect import detect_script

    return detect_script(text)


def _is_arabic_script(text: str) -> bool:
    return any("\u0600" <= c <= "ۿ" or "ݐ" <= c <= "ݿ" for c in text)


_lock = threading.Lock()
_lexicon: Optional[Lexicon] = None


def get_lexicon() -> Lexicon:
    """The bundled lexicon (loaded once, lazily)."""
    global _lexicon
    if _lexicon is None:
        with _lock:
            if _lexicon is None:
                entries: List[NameEntry] = []
                folder = data_path() / "names"
                for path in sorted(folder.iterdir(), key=lambda p: p.name):
                    if not path.name.endswith(".json"):
                        continue
                    data = json.loads(path.read_text(encoding="utf-8"))
                    for raw in data.get("names", []):
                        entries.append(_entry(raw, path.name))
                _lexicon = Lexicon(entries)
    return _lexicon
