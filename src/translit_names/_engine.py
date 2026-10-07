"""Context-aware, rule-based transliteration engine.

A :class:`Scheme` is compiled from a JSON description (see ``docs/data-format.md``).
Matching is greedy longest-match over the lower-cased source; among rules of
equal length, contextual rules are tried in file order before the plain
``map`` entry.  Output case is restored from the source, so data files only
ever describe lower-case letters.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple

__all__ = ["APOSTROPHES", "Rule", "Scheme", "SchemeError", "Segment"]

#: Characters treated as part of a word when they sit between two letters
#: (Ukrainian/Belarusian apostrophe, Uzbek okina/tutuq, typographic quotes).
APOSTROPHES: FrozenSet[str] = frozenset("'\u2019\u02bc\u02bb\u2018`\u00b4\u02b9\u02bd")

_WORD_START = "^"
_WORD_END = "$"
_CLASS_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

#: A segment produced by a word hook: ``("src", text)`` is transliterated by the
#: rules, ``("lit", text)`` is copied to the output verbatim.
Segment = Tuple[str, str]
WordHook = Callable[["Scheme", str], List[Segment]]


class SchemeError(ValueError):
    """Raised for malformed scheme definitions."""


def _lower1(ch: str) -> str:
    """Lower-case a single character without changing the string length."""
    low = ch.lower()
    return low if len(low) == 1 else low[0]


def _is_letter(ch: str) -> bool:
    return ch.isalpha() or unicodedata.category(ch) in ("Mn", "Mc")


def _is_cased(ch: str) -> bool:
    return ch.lower() != ch.upper()


def _is_upperish(ch: str) -> bool:
    """Upper case or title case (ǅ ǈ ǋ count as capitals)."""
    return ch.isupper() or ch.istitle()


def _caps_relevant(ch: str) -> bool:
    """Cased letters that can signal an all-caps word (ß has no 1:1 capital)."""
    return _is_cased(ch) and len(ch.upper()) == 1


@dataclass(frozen=True)
class Rule:
    """One substitution: ``source`` (lower case) becomes ``target`` in context."""

    source: str
    target: str
    start: bool = False
    end: bool = False
    after: Optional[FrozenSet[str]] = None
    not_after: Optional[FrozenSet[str]] = None
    before: Optional[FrozenSet[str]] = None
    not_before: Optional[FrozenSet[str]] = None

    @property
    def contextual(self) -> bool:
        return bool(
            self.start
            or self.end
            or self.after is not None
            or self.not_after is not None
            or self.before is not None
            or self.not_before is not None
        )

    def applies(self, prev: str, nxt: str) -> bool:
        """Check the context. ``prev``/``nxt`` are neighbouring word characters
        (lower case) or ``"^"``/``"$"`` at a word boundary."""
        if self.start and prev != _WORD_START:
            return False
        if self.end and nxt != _WORD_END:
            return False
        if self.after is not None and prev not in self.after:
            return False
        if self.not_after is not None and prev in self.not_after:
            return False
        if self.before is not None and nxt not in self.before:
            return False
        return not (self.not_before is not None and nxt in self.not_before)


def _expand_set(spec: Any, classes: Mapping[str, str], where: str) -> Optional[FrozenSet[str]]:
    if spec is None:
        return None
    if isinstance(spec, list):
        spec = "".join(spec)
    if not isinstance(spec, str):
        raise SchemeError(f"{where}: context set must be a string, got {spec!r}")

    def repl(m: re.Match[str]) -> str:
        name = m.group(1)
        if name not in classes:
            raise SchemeError(f"{where}: unknown class {{{name}}}")
        return classes[name]

    expanded = _CLASS_RE.sub(repl, spec)
    return frozenset(_lower1(c) for c in unicodedata.normalize("NFC", expanded))


class Scheme:
    """A compiled transliteration scheme.

    Instances are normally obtained from :func:`translit_names.get_scheme`.
    """

    def __init__(self, spec: Mapping[str, Any], hooks: Optional[Mapping[str, WordHook]] = None) -> None:
        self.spec: Dict[str, Any] = dict(spec)
        try:
            self.id: str = spec["id"]
        except KeyError:
            raise SchemeError("scheme without 'id'") from None
        self.title: str = spec.get("title", self.id)
        self.language: str = spec.get("language", "")
        self.script: str = spec.get("script", "")
        self.target_script: str = spec.get("target_script", "Latn")
        self.kind: str = spec.get("kind", "other")
        self.status: str = spec.get("status", "current")
        self.year: Optional[int] = spec.get("year")
        self.authority: str = spec.get("authority", "")
        self.description: str = spec.get("description", "")
        self.sources: List[str] = list(spec.get("sources", []))
        self.notes: List[str] = list(spec.get("notes", []))
        self.ascii: bool = bool(spec.get("ascii", False))
        self.reversible: bool = bool(spec.get("reversible", False))
        self.samples: List[Tuple[str, str]] = [(s[0], s[1]) for s in spec.get("samples", [])]
        self.case_mode: str = spec.get("case", "auto")
        if self.case_mode not in ("auto", "preserve", "upper", "lower"):
            raise SchemeError(f"{self.id}: unknown case mode {self.case_mode!r}")
        self.titlecase: bool = bool(spec.get("titlecase", False))
        self.lowercase_words: Tuple[str, ...] = tuple(spec.get("lowercase_words", ()))
        self.geminate: Optional[str] = spec.get("geminate")
        self.options: Dict[str, Any] = dict(spec.get("options", {}))
        self.fallback: str = spec.get("fallback", "keep")
        if self.fallback not in ("keep", "drop", "ascii"):
            raise SchemeError(f"{self.id}: unknown fallback {self.fallback!r}")

        hook_name = spec.get("hook")
        self._hook: Optional[WordHook] = None
        if hook_name:
            if not hooks or hook_name not in hooks:
                raise SchemeError(f"{self.id}: unknown hook {hook_name!r}")
            self._hook = hooks[hook_name]

        self._aliases = self._compile_aliases(spec.get("aliases", {}))
        self._rules = self._compile_rules(spec)
        self._post = [(re.compile(p["pattern"]), p["replace"]) for p in spec.get("post", [])]

    # ------------------------------------------------------------------ compile
    def _compile_aliases(self, aliases: Mapping[str, str]) -> Dict[str, str]:
        table: Dict[str, str] = {}
        for k, v in aliases.items():
            k = unicodedata.normalize("NFC", k)
            v = unicodedata.normalize("NFC", v)
            table[k] = v
            up = k.upper()
            if up != k and len(up) == len(k) and up not in aliases:
                table[up] = v.upper()
        return table

    def _compile_rules(self, spec: Mapping[str, Any]) -> Dict[str, List[Rule]]:
        classes = {k: unicodedata.normalize("NFC", v) for k, v in spec.get("classes", {}).items()}
        ordered: List[Tuple[int, int, Rule]] = []
        for n, raw in enumerate(spec.get("rules", [])):
            where = f"{self.id}: rules[{n}]"
            if "from" not in raw or "to" not in raw:
                raise SchemeError(f"{where}: needs 'from' and 'to'")
            unknown = set(raw) - {"from", "to", "start", "end", "after", "not_after", "before", "not_before", "note"}
            if unknown:
                raise SchemeError(f"{where}: unknown keys {sorted(unknown)}")
            sources = raw["from"] if isinstance(raw["from"], list) else [raw["from"]]
            for src in sources:
                src = "".join(_lower1(c) for c in unicodedata.normalize("NFC", src))
                if not src:
                    raise SchemeError(f"{where}: empty 'from'")
                rule = Rule(
                    source=src,
                    target=unicodedata.normalize("NFC", raw["to"]),
                    start=bool(raw.get("start", False)),
                    end=bool(raw.get("end", False)),
                    after=_expand_set(raw.get("after"), classes, where),
                    not_after=_expand_set(raw.get("not_after"), classes, where),
                    before=_expand_set(raw.get("before"), classes, where),
                    not_before=_expand_set(raw.get("not_before"), classes, where),
                )
                ordered.append((-len(src), n, rule))
        base = len(ordered) + 1
        for n, (src, tgt) in enumerate(spec.get("map", {}).items()):
            src = "".join(_lower1(c) for c in unicodedata.normalize("NFC", src))
            if not src:
                raise SchemeError(f"{self.id}: empty key in map")
            ordered.append((-len(src), base + n, Rule(source=src, target=unicodedata.normalize("NFC", tgt))))
        ordered.sort(key=lambda t: (t[0], t[1]))
        index: Dict[str, List[Rule]] = {}
        for _, _, rule in ordered:
            index.setdefault(rule.source[0], []).append(rule)
        return index

    # ---------------------------------------------------------------- inspect
    @property
    def alphabet(self) -> FrozenSet[str]:
        """Single source characters this scheme knows how to transliterate."""
        return frozenset(r.source for rules in self._rules.values() for r in rules if len(r.source) == 1)

    def rules(self) -> Iterable[Rule]:
        for rules in self._rules.values():
            yield from rules

    def __repr__(self) -> str:
        return f"<Scheme {self.id!r}: {self.title}>"

    # ------------------------------------------------------------- transliterate
    def __call__(self, text: str) -> str:
        return self.transliterate(text)

    def preprocess(self, text: str) -> str:
        text = unicodedata.normalize("NFC", text)
        if self._aliases:
            text = "".join(self._aliases.get(c, c) for c in text)
        if self.geminate:
            text = self._move_gemination_marks(text)
        return text

    def transliterate(self, text: str) -> str:
        """Transliterate ``text`` with this scheme."""
        text = self.preprocess(text)
        all_caps = _text_is_all_caps(text)
        if self._hook:
            parts = []
            for kind, s in self._hook(self, text):
                parts.append(self._apply(self.preprocess(s), all_caps) if kind == "src" else s)
            out = "".join(parts)
        else:
            out = self._apply(text, all_caps)
        for pattern, repl in self._post:
            out = pattern.sub(repl, out)
        out = unicodedata.normalize("NFC", out)
        if self.titlecase:
            out = titlecase_name(out, self.lowercase_words)
        if self.case_mode == "upper":
            out = out.upper()
        elif self.case_mode == "lower":
            out = out.lower()
        return out

    def _move_gemination_marks(self, text: str) -> str:
        """Put the gemination mark (e.g. Arabic shadda) right after its base letter."""
        g = self.geminate
        assert g is not None
        chars = list(text)
        i = 0
        while i < len(chars):
            if unicodedata.category(chars[i]) == "Mn":
                j = i
                while j < len(chars) and unicodedata.category(chars[j]) == "Mn":
                    j += 1
                run = chars[i:j]
                if g in run:
                    run = [g] * run.count(g) + [c for c in run if c != g]
                    chars[i:j] = run
                i = j
            else:
                i += 1
        return "".join(chars)

    def _apply(self, text: str, text_all_caps: bool) -> str:
        if not text:
            return ""
        low = "".join(_lower1(c) for c in text)
        n = len(text)
        word_caps = _word_caps_map(text, text_all_caps)
        out: List[str] = []
        last_letter_target = ""
        i = 0
        while i < n:
            ch = low[i]
            if self.geminate and ch == self.geminate:
                out.append(last_letter_target)
                i += 1
                continue
            prev = _context_prev(low, i)
            matched: Optional[Rule] = None
            for rule in self._rules.get(ch, ()):
                j = i + len(rule.source)
                if j > n or low[i:j] != rule.source:
                    continue
                if rule.contextual and not rule.applies(prev, _context_next(low, j)):
                    continue
                matched = rule
                break
            if matched is None:
                out.append(self._fallback(text[i]))
                i += 1
                continue
            j = i + len(matched.source)
            target = matched.target
            if target:
                if self.case_mode == "auto":
                    target = _recase(text[i:j], target, word_caps[i])
                out.append(target)
                if _is_letter(text[i]):
                    last_letter_target = matched.target
            i = j
        return "".join(out)

    def _fallback(self, ch: str) -> str:
        if self.fallback == "keep" or ch.isspace() or ch.isascii():
            return ch
        if self.fallback == "drop":
            return ""
        from ._fold import fold_char  # local import: avoid a cycle at import time

        return fold_char(ch)


# ---------------------------------------------------------------------- helpers
def _context_prev(low: str, i: int) -> str:
    """Previous in-word character or ``^`` at a word start."""
    if i == 0:
        return _WORD_START
    p = low[i - 1]
    if _is_letter(p):
        return p
    if p in APOSTROPHES and i >= 2 and _is_letter(low[i - 2]):
        return p
    return _WORD_START


def _context_next(low: str, j: int) -> str:
    """Next in-word character or ``$`` at a word end."""
    if j >= len(low):
        return _WORD_END
    c = low[j]
    if _is_letter(c):
        return c
    if c in APOSTROPHES and j + 1 < len(low) and _is_letter(low[j + 1]):
        return c
    return _WORD_END


def _text_is_all_caps(text: str) -> bool:
    cased = [c for c in text if _is_cased(c)]
    cased = [c for c in cased if _caps_relevant(c)]
    return len(cased) >= 2 and all(c.isupper() for c in cased)


def _word_caps_map(text: str, text_all_caps: bool) -> List[bool]:
    """For each position: is the surrounding word written in capitals?"""
    result = [False] * len(text)
    i = 0
    n = len(text)
    while i < n:
        if not (_is_letter(text[i]) or text[i] in APOSTROPHES):
            i += 1
            continue
        j = i
        while j < n and (_is_letter(text[j]) or text[j] in APOSTROPHES):
            j += 1
        cased = [c for c in text[i:j] if _is_cased(c)]
        cased = [c for c in cased if _caps_relevant(c)]
        caps = all(c.isupper() for c in cased) and (len(cased) >= 2 or (len(cased) == 1 and text_all_caps))
        for k in range(i, j):
            result[k] = caps
        i = j
    return result


def _recase(source: str, target: str, word_is_caps: bool) -> str:
    first = next((c for c in source if _is_cased(c)), None)
    if first is None:
        return target
    if word_is_caps and not _caps_relevant(first):
        return target.upper()  # ß inside GROß
    if not _is_upperish(first):
        return target
    cased = [c for c in source if _caps_relevant(c)]
    if word_is_caps or (len(cased) >= 2 and all(c.isupper() for c in cased)):
        return target.upper()
    return _capitalize_first(target)


def _capitalize_first(s: str) -> str:
    for k, c in enumerate(s):
        if _is_cased(c):
            return s[:k] + c.upper() + s[k + 1 :]
    return s


_TITLE_WORD_RE = re.compile(r"[^\s]+")


def titlecase_name(text: str, lowercase_words: Sequence[str] = ()) -> str:
    """Capitalise each name part of a romanisation made from an uncased script.

    ``lowercase_words`` lists particles kept in lower case unless they open
    the string; an entry ending in ``-`` is a prefix (``"al-"`` keeps
    ``al-Rashid`` but still capitalises ``Rashid``).
    """
    prefixes = sorted((w for w in lowercase_words if w.endswith("-")), key=len, reverse=True)
    words = {w for w in lowercase_words if not w.endswith("-")}
    first = True

    def fix_part(part: str, is_first: bool) -> str:
        low = part.lower()
        for p in prefixes:
            if low.startswith(p) and len(part) > len(p):
                head = part[: len(p)]
                head = _capitalize_first(head) if is_first else head
                return head + _capitalize_first(part[len(p) :])
        if not is_first and low in words:
            return part
        return _capitalize_first(part)

    def repl(m: re.Match[str]) -> str:
        nonlocal first
        token = m.group(0)
        pieces = token.split("-")
        if len(pieces) > 1 and any(token.lower().startswith(p) for p in prefixes):
            fixed = fix_part(token, first)
        else:
            fixed = "-".join(fix_part(p, first and k == 0) if p else p for k, p in enumerate(pieces))
        first = False
        return fixed

    return _TITLE_WORD_RE.sub(repl, text)
