"""Loading and lookup of the bundled transliteration schemes."""

from __future__ import annotations

import json
import threading
from importlib import resources
from typing import Any, Dict, List, Mapping, Optional, Tuple

from ._engine import Scheme, SchemeError, WordHook

__all__ = ["default_scheme_id", "get_scheme", "list_schemes", "scheme_specs"]

_lock = threading.Lock()
_specs: Optional[Dict[str, Dict[str, Any]]] = None
_compiled: Dict[str, Scheme] = {}
_defaults: Optional[Dict[str, str]] = None


def _data_dir() -> Any:
    return resources.files("translit_names") / "data"


def _hooks() -> Mapping[str, WordHook]:
    from .arabic import arabic_hook

    return {"arabic": arabic_hook}


def _load_specs() -> Dict[str, Dict[str, Any]]:
    global _specs
    if _specs is not None:
        return _specs
    with _lock:
        if _specs is not None:
            return _specs
        specs: Dict[str, Dict[str, Any]] = {}
        for entry in sorted((_data_dir() / "schemes").iterdir(), key=lambda p: p.name):
            if not entry.name.endswith(".json"):
                continue
            spec = json.loads(entry.read_text(encoding="utf-8"))
            sid = spec.get("id")
            if not sid:
                raise SchemeError(f"{entry.name}: missing 'id'")
            if entry.name != f"{sid}.json":
                raise SchemeError(f"{entry.name}: file name must be {sid}.json")
            specs[sid] = spec
        _specs = {sid: _resolve(sid, specs, ()) for sid in specs}
        return _specs


def _resolve(sid: str, raw: Mapping[str, Dict[str, Any]], chain: Tuple[str, ...]) -> Dict[str, Any]:
    """Apply ``extends`` inheritance (child keys win, child rules come first)."""
    if sid in chain:
        raise SchemeError(f"inheritance cycle: {' -> '.join((*chain, sid))}")
    spec = raw[sid]
    parent_id = spec.get("extends")
    if not parent_id:
        return dict(spec)
    if parent_id not in raw:
        raise SchemeError(f"{sid}: extends unknown scheme {parent_id!r}")
    parent = _resolve(parent_id, raw, (*chain, sid))
    merged: Dict[str, Any] = {
        k: v for k, v in parent.items() if k not in ("samples", "notes", "sources", "description")
    }
    for key, value in spec.items():
        if key in ("map", "aliases", "classes", "options"):
            combined = dict(parent.get(key, {}))
            combined.update(value)
            # ``null`` in a child map removes the parent's entry
            merged[key] = {k: v for k, v in combined.items() if v is not None}
        elif key == "rules":
            inherit = spec.get("inherit_rules", True)
            merged["rules"] = list(value) + (list(parent.get("rules", [])) if inherit else [])
        else:
            merged[key] = value
    if "rules" not in spec and not spec.get("inherit_rules", True):
        merged["rules"] = []
    merged.pop("inherit_rules", None)
    return merged


def _canon(sid: str) -> str:
    return sid.strip().lower().replace("-", "_").replace(" ", "_").replace(".", "_")


def scheme_specs() -> Dict[str, Dict[str, Any]]:
    """Resolved JSON specs of every bundled scheme, keyed by id."""
    return dict(_load_specs())


def get_scheme(scheme_id: str) -> Scheme:
    """Return a compiled :class:`Scheme` by id (``"ru_icao"``, ``"uk-kmu-2010"`` …).

    A bare language code (``"ru"``) returns that language's default scheme.
    """
    specs = _load_specs()
    sid = _canon(scheme_id)
    if sid not in specs:
        defaults = _load_defaults()
        if sid in defaults:
            sid = defaults[sid]
        else:
            raise KeyError(f"unknown scheme {scheme_id!r}; see translit_names.list_schemes()")
    scheme = _compiled.get(sid)
    if scheme is None:
        with _lock:
            scheme = _compiled.get(sid)
            if scheme is None:
                scheme = Scheme(specs[sid], hooks=_hooks())
                _compiled[sid] = scheme
    return scheme


def list_schemes(
    language: Optional[str] = None,
    *,
    kind: Optional[str] = None,
    status: Optional[str] = None,
    script: Optional[str] = None,
) -> List[Scheme]:
    """List bundled schemes, optionally filtered."""
    out = []
    for sid, spec in sorted(_load_specs().items()):
        if language and spec.get("language") != language:
            continue
        if kind and spec.get("kind") != kind:
            continue
        if status and spec.get("status", "current") != status:
            continue
        if script and spec.get("script") != script:
            continue
        out.append(get_scheme(sid))
    return out


_config: Optional[Dict[str, Any]] = None


def defaults_config() -> Dict[str, Any]:
    """Parsed ``data/defaults.json`` (cached)."""
    global _config
    if _config is None:
        path = _data_dir() / "defaults.json"
        data: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        _config = data
    return _config


def _load_defaults() -> Dict[str, str]:
    table: Dict[str, str] = defaults_config()["transliterate"]
    return table


def default_scheme_id(language: str, purpose: str = "transliterate", script: Optional[str] = None) -> Optional[str]:
    """Default scheme id for a language and purpose, or ``None``.

    ``purpose`` is ``"transliterate"``, ``"mrz"`` or ``"match"``.  With
    ``script`` (``"Latn"``, ``"Cyrl"``, ``"Arab"``) only a scheme for that
    source script is returned, e.g. ``("az", script="Latn")`` → ``az_ascii``.
    """
    specs = _load_specs()
    sections = [defaults_config().get(purpose, {})]
    if purpose != "transliterate":
        sections.append(defaults_config()["transliterate"])
    for table in sections:
        for key in (f"{language}-{script}", language) if script else (language,):
            sid = table.get(key)
            if sid and sid in specs and (script is None or specs[sid].get("script") == script):
                return str(sid)
    return None
