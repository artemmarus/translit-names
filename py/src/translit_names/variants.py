"""Generation of plausible Latin spellings of a name.

A single Cyrillic or Arabic-script name ends up with many spellings in real
documents: every passport generation used another table (``Юрий`` →
``Yuriy`` 1997–2010, ``Iurii`` since 2013), newspapers use yet another
(``Yuri``), and foreign registries add their own (``Jurij``, ``Iouri``).
:func:`variants` lists them, ranked, for search and record linkage.

Sources, in decreasing weight:

1. every applicable bundled scheme (current passport system first);
2. the name lexicon: conventional English spelling, per-country spellings
   and attested variants (``Mohammed``, ``Mohamed``, ``Mehmet`` …);
3. rewrite rules for systematic alternations (``-iy/-y/-ii``, ``ks/x``,
   ``yu/iu/ju``, ``ou/u``, doubled consonants …), applied to the above.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

from ._data import data_path
from ._engine import Scheme
from ._fold import fold
from ._registry import list_schemes
from .detect import detect_language, detect_script
from .lexicon import NameEntry, get_lexicon
from .normalize import fix_mixed_script, normalize

__all__ = ["Variant", "scheme_weight", "variants", "variants_detailed"]

_ARABIC_SCRIPT_LANGS = {"ar", "fa", "ur", "ps"}
_STRIP_MARKS = re.compile('[\u2019\u201d\u02b9\u02ba\u02bb\u02bc\u02bf\u02be"`\u00b4\u02b9]')


@dataclass(frozen=True)
class Variant:
    """A candidate spelling with a heuristic plausibility score in (0, 1]."""

    text: str
    score: float
    sources: Tuple[str, ...]

    def __str__(self) -> str:
        return self.text


def scheme_weight(scheme: Scheme) -> float:
    """How likely a scheme's output is to appear in real-world records."""
    base = {
        "passport": 1.0,
        "practical": 0.93,
        "official": 0.85,
        "geographic": 0.82,
        "ascii": 0.85,
        "legacy": 0.7,
        "library": 0.6,
        "scholarly": 0.45,
    }.get(scheme.kind, 0.5)
    if scheme.status == "superseded":
        base *= 0.9
    elif scheme.status == "draft":
        base *= 0.75
    elif scheme.status == "informal":
        base *= 0.97
    return base


_rules_cache: Optional[Dict[str, List[Tuple[re.Pattern[str], Tuple[str, ...], float]]]] = None


def _rules() -> Dict[str, List[Tuple[re.Pattern[str], Tuple[str, ...], float]]]:
    global _rules_cache
    if _rules_cache is None:
        path = data_path() / "variant_rules.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        _rules_cache = {
            fam: [(re.compile(r["pattern"], re.IGNORECASE), tuple(r["alts"]), float(r["weight"])) for r in rules]
            for fam, rules in data.items()
            if isinstance(rules, list)
        }
    return _rules_cache


def _clean(text: str, ascii_only: bool) -> str:
    text = _STRIP_MARKS.sub("", text)
    text = text.replace("\u0361", "").replace("\u00b7", "")
    if ascii_only:
        text = fold(text)
        text = "".join(c for c in text if c.isalnum() or c in " -'")
    text = re.sub(r"\s+", " ", text).strip(" -")
    return _fix_word_case(text)


def _fix_word_case(text: str) -> str:
    """``IUrii`` (from ALA-LC I͡Uriĭ) → ``Iurii``; ``MUHAMMAD`` → ``Muhammad``."""

    def fix(word: str) -> str:
        letters = [c for c in word if c.isalpha()]
        if len(letters) > 1 and all(c.isupper() for c in letters):
            return word[:1] + word[1:].lower()
        if len(word) > 2 and word[0].isupper() and word[1].isupper() and word[2:].islower():
            return word[0] + word[1:].lower()
        return word

    return " ".join("-".join(fix(p) for p in w.split("-")) for w in text.split(" "))


def _match_case(template: str, text: str) -> str:
    if template.isupper() and len(template) > 1:
        return text.upper()
    if template[:1].isupper():
        return text[:1].upper() + text[1:]
    return text


def _family(language: Optional[str], script: str) -> str:
    if script == "Arab" or language in _ARABIC_SCRIPT_LANGS:
        return "arabic"
    return "cyrillic"


class _Pool:
    def __init__(self) -> None:
        self.items: Dict[str, Tuple[str, float, Set[str]]] = {}
        self.base: Dict[str, float] = {}

    def add(self, text: str, score: float, source: str) -> None:
        if not text:
            return
        key = text.lower()
        if key in self.items:
            old_text, _, sources = self.items[key]
            sources.add(source)
            # Several independent sources make a spelling a bit more plausible,
            # but never outrank the current passport standard (score 1.0).
            base = max(self.base[key], score)
            self.base[key] = base
            bonus = 0.01 * min(len(sources) - 1, 3)
            self.items[key] = (old_text, base if base >= 1.0 else min(base + bonus, 0.995), sources)
        else:
            self.base[key] = score
            self.items[key] = (text, score, {source})

    def ranked(self) -> List[Variant]:
        """Candidates by decreasing score (unrounded), then alphabetically."""
        return sorted(
            (Variant(t, s, tuple(sorted(src))) for t, s, src in self.items.values()),
            key=lambda v: (-v.score, v.text),
        )


def _lexicon_entries(part: str, language: Optional[str]) -> List[NameEntry]:
    lex = get_lexicon()
    found = lex.lookup(part, language)
    if not found and part.lower().startswith(("al-", "el-")):
        found = lex.lookup(part[3:], language)
    return found


def _part_variants(
    part: str,
    language: Optional[str],
    script: str,
    *,
    ascii_only: bool,
    include_short: bool,
    use_lexicon: bool,
    schemes: Sequence[Scheme],
) -> List[Variant]:
    pool = _Pool()
    if script != "Latn":
        for sch in schemes:
            if sch.case_mode == "preserve":
                continue
            out = _clean(sch.transliterate(part), ascii_only)
            pool.add(out, scheme_weight(sch), sch.id)
    else:
        pool.add(_clean(part, ascii_only) if ascii_only else part, 1.0, "input")

    lang_key = language or "en"
    for n, entry in enumerate(_lexicon_entries(part, language) if use_lexicon else []):
        damp = 1.0 if n == 0 else 0.85
        own = entry.latin.get(lang_key, ())
        for k, form in enumerate(own):
            pool.add(_clean(form, ascii_only), 0.97 * damp * (0.97**k), f"lexicon:{entry.id}")
        if entry.english:
            pool.add(_clean(entry.english, ascii_only), 0.95 * damp, f"lexicon:{entry.id}")
        for lang, forms in entry.latin.items():
            if lang == lang_key:
                continue
            for k, form in enumerate(forms):
                pool.add(_clean(form, ascii_only), 0.78 * damp * (0.97**k), f"lexicon:{entry.id}:{lang}")
        for k, form in enumerate(entry.variants):
            pool.add(_clean(form, ascii_only), 0.72 * damp * (0.995**k), f"lexicon:{entry.id}")
        if include_short:
            for form in entry.short:
                if detect_script(form) == "Latn":
                    pool.add(_clean(form, ascii_only), 0.4 * damp, f"lexicon:{entry.id}:short")

    # Rewrite rules on the strongest candidates (one or two steps).
    rules = _rules()
    family = _family(language, script)
    rule_list = rules.get("all", []) + rules.get(family, [])
    seeds = pool.ranked()[:8]
    frontier = [(v.text, v.score) for v in seeds]
    for _depth in range(2):
        nxt: List[Tuple[str, float]] = []
        for text, score in frontier:
            for pattern, alts, weight in rule_list:
                low = text.lower()
                if not pattern.search(low):
                    continue
                for alt in alts:
                    new = pattern.sub(alt, low, count=1)
                    new = _clean(_match_case(text, new), ascii_only)
                    if new and new.lower() != low:
                        s = score * weight
                        if s >= 0.35:
                            pool.add(new, s, "rule")
                            nxt.append((new, s))
        frontier = sorted(nxt, key=lambda t: -t[1])[:12]
    return pool.ranked()


_SEP_RE = re.compile(r"(\s+|-)")


def _group_arabic_phrases(tokens: List[str]) -> List[str]:
    """Re-join word tokens that form a compound name in the lexicon
    (عبد الرحمن, نور الدين) so that they are romanised as one unit."""
    lex = get_lexicon()
    out: List[str] = []
    i = 0
    while i < len(tokens):
        joined = None
        for span in (5, 3):  # 3 words (+2 separators) or 2 words (+1 separator)
            chunk = tokens[i : i + span]
            if len(chunk) == span and not any(_SEP_RE.fullmatch(t) for t in chunk[::2]):
                phrase = "".join(chunk)
                if all(t.isspace() for t in chunk[1::2]) and lex.lookup_arabic(" ".join(chunk[::2])):
                    joined = phrase
                    break
        if joined is not None:
            out.append(joined)
            i += span
        else:
            out.append(tokens[i])
            i += 1
    return out


def variants_detailed(
    name: str,
    language: Optional[str] = None,
    *,
    limit: int = 20,
    ascii_only: bool = True,
    include_short: bool = False,
    use_lexicon: bool = True,
) -> List[Variant]:
    """Like :func:`variants` but returns :class:`Variant` objects with
    scores and the schemes / lexicon entries that produced each spelling."""
    name = fix_mixed_script(normalize(name))
    if not name:
        return []
    script = detect_script(name)
    if language is None and script != "Latn":
        language = detect_language(name).language
    schemes: List[Scheme] = []
    if script != "Latn" and language:
        schemes = [
            s
            for s in list_schemes(language)
            if s.script == script
            and s.kind != "scholarly"
            and s.options.get("variants", True)
            # Reversible diacritic systems (ISO 9 …) fold into unrealistic spellings.
            and not (s.reversible and not s.ascii)
        ]
    tokens = _SEP_RE.split(name)
    if script == "Arab" and use_lexicon:
        tokens = _group_arabic_phrases(tokens)
    per_part: List[List[Variant]] = []
    for tok in tokens:
        if not tok or _SEP_RE.fullmatch(tok):
            per_part.append([Variant(" " if tok.isspace() else tok, 1.0, ())])
            continue
        vs = _part_variants(
            tok,
            language,
            script,
            ascii_only=ascii_only,
            include_short=include_short,
            use_lexicon=use_lexicon,
            schemes=schemes,
        )
        per_part.append(vs[: max(limit, 8)] or [Variant(tok, 0.5, ())])

    # Best-first combination of the parts.
    combos: List[Tuple[float, str, Set[str]]] = [(1.0, "", set())]
    for options in per_part:
        new: List[Tuple[float, str, Set[str]]] = []
        for score, text, srcs in combos:
            for v in options:
                new.append((score * v.score, text + v.text, srcs | set(v.sources)))
        new.sort(key=lambda t: -t[0])
        combos = new[: limit * 3]
    seen: Dict[str, Variant] = {}
    for score, text, srcs in combos:
        text = re.sub(r"\s+", " ", text).strip()
        key = text.lower()
        if key and key not in seen:
            seen[key] = Variant(text, round(score, 4), tuple(sorted(srcs)))  # rounded for display only
        if len(seen) >= limit:
            break
    return list(seen.values())


def variants(
    name: str,
    language: Optional[str] = None,
    *,
    limit: int = 20,
    ascii_only: bool = True,
    include_short: bool = False,
    use_lexicon: bool = True,
) -> List[str]:
    """Plausible Latin spellings of ``name``, most likely first.

    >>> variants("Юрий")[:4]  # doctest: +SKIP
    ['Iurii', 'Yuri', 'Yuriy', 'Yury']
    >>> "Mohammed" in variants("محمد")
    True

    ``language`` overrides detection (``"uk"`` for a Ukrainian name that has
    no Ukrainian-only letters).  ``include_short`` adds diminutives (Sasha
    for Aleksandr).  ``ascii_only=False`` keeps diacritics (Hüseyin).
    """
    return [
        v.text
        for v in variants_detailed(
            name, language, limit=limit, ascii_only=ascii_only, include_short=include_short, use_lexicon=use_lexicon
        )
    ]
