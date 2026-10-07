"""Cross-script, transliteration-aware comparison of personal names.

Three signals are combined:

1. **Lexicon clusters** — ``Магомед``, ``محمد``, ``Mohammed`` and ``Mehmet``
   belong to the same cluster, so they match even though they look different.
   Two *different* known names (``Hasan`` vs ``Husayn``) are kept apart.
2. **Skeleton keys** — a consonant skeleton that folds the usual
   transliteration alternations: ``kh/h/x/g`` (Khalid, Halid, Xalid, Gasan),
   ``sh/ch/sch/sz/cz`` (Shamil, Chamil), ``zh/j/dj/dzh`` (Zhamal, Jamal,
   Djamal), ``ks/x`` (Aleksandr, Alexander), ``v/w``, ``q/k/c``, endings
   ``-iy/-ii/-y/-ij``, article forms ``al-/el-/ul-/ad-``, ``-uddin/-eddine``,
   ``-ullah/-allah``.  Ambiguous letters (``j``, ``ch``, ``x``, ``c``,
   ``th``, ``dh``) yield several keys.
3. **Jaro–Winkler** similarity of the folded Latin spellings, for unknown
   names and typos.

Multi-part names are aligned part by part regardless of order, so
``"Ivanov Ivan Ivanovich"`` matches ``"IVAN IVANOV"`` (the missing
patronymic costs little).
"""

from __future__ import annotations

import itertools
import re
import unicodedata
from dataclasses import dataclass
from typing import FrozenSet, List, Optional, Sequence, Set, Tuple

from ._fold import fold
from .core import resolve_scheme
from .detect import detect_language, detect_script
from .normalize import fix_mixed_script, normalize

__all__ = [
    "PARTICLES",
    "MatchResult",
    "PartMatch",
    "compare",
    "is_match",
    "jaro_winkler",
    "name_key",
    "name_keys",
    "similarity",
    "split_name",
    "to_match_latin",
]

#: Name particles ignored when aligning name parts.
PARTICLES: FrozenSet[str] = frozenset(
    {
        "al",
        "el",
        "ul",
        "al-",
        "el-",
        "ad",
        "ar",
        "as",
        "ash",
        "at",
        "az",
        "an",
        "ad-",
        "ud",
        "ud-",
        "bin",
        "ibn",
        "ben",
        "bint",
        "binti",
        "bte",
        "bt",
        "b",
        "von",
        "van",
        "der",
        "de",
        "da",
        "di",
        "du",
        "la",
        "le",
        "dos",
        "das",
        "del",
        "oglu",
        "ogly",
        "ugli",
        "uly",
        "uulu",
        "ogli",
        "kizi",
        "kyzy",
        "qizi",
        "gyzy",
        "kizy",
        "ogh",
        "kyzi",
    }
)

# Diacritics → phonetic ASCII before keying (ICAO folding would lose č→ch, ş→sh …).
_PHONETIC_FOLD = {
    "č": "ch",
    "ć": "ch",
    "ç": "ch",
    "ĉ": "ch",
    "š": "sh",
    "ś": "sh",
    "ş": "sh",
    "ș": "sh",
    "ŝ": "shch",
    "ž": "zh",
    "ź": "zh",
    "ż": "zh",
    "đ": "dj",
    "ǆ": "dzh",
    "ǉ": "lj",
    "ǌ": "nj",
    "ğ": "gh",
    "ġ": "gh",
    "ı": "i",
    "ə": "a",
    "ä": "a",
    "ö": "o",
    "ü": "u",
    "ł": "l",
    "ř": "rzh",
    "ñ": "n",
    "ň": "n",
    "ŋ": "ng",
    "ß": "ss",
    "þ": "th",
    "ð": "d",
    "ø": "o",
    "æ": "ae",
    "œ": "oe",
    "ẖ": "kh",
    "ḫ": "kh",
    "ḥ": "h",
    "ṣ": "s",
    "ṭ": "t",
    "ḍ": "d",
    "ẓ": "z",
    "ẕ": "z",
    "ṯ": "th",
    "ḏ": "dh",
    "ġ\u0323": "gh",
}
_DROP_MARKS = set("'\u2019\u02bc\u02bb\u2018`\u00b4\u02b9\u02ba\u02bf\u02be\"")

_VOWELS = set("aeiouy")


@dataclass(frozen=True)
class _G:
    """A grapheme in the key with its alternative token strings (first = primary)."""

    alts: Tuple[str, ...]


def to_match_latin(name: str, language: Optional[str] = None) -> str:
    """Bring a name to lower-case ASCII Latin suitable for keys and comparison."""
    name = fix_mixed_script(normalize(name))
    if detect_script(name) not in ("Latn", "Zyyy"):
        sch = resolve_scheme(name, None, language=language, purpose="match")
        if sch is not None:
            name = sch.transliterate(name)
    name = unicodedata.normalize("NFC", name).lower()
    name = "".join(_PHONETIC_FOLD.get(c, c) for c in name)
    name = "".join(c for c in name if c not in _DROP_MARKS)
    return fold(name).lower()


# Ordered grapheme table: (pattern, alternatives).  Longest patterns first.
_GRAPHEMES: List[Tuple[str, Tuple[str, ...]]] = [
    ("schtsch", ("X",)),
    ("shtsh", ("X",)),
    ("chtch", ("X",)),
    ("shch", ("X",)),
    ("szcz", ("X",)),
    ("tsch", ("X",)),
    ("dzsh", ("J",)),
    ("dzh", ("J",)),
    ("dsch", ("J",)),
    ("sch", ("X",)),
    ("tch", ("X",)),
    ("sht", ("XT",)),
    ("kh", ("H",)),
    ("gh", ("H",)),
    ("zh", ("J",)),
    ("dj", ("J",)),
    ("dz", ("J", "DZ")),
    ("dg", ("J",)),
    ("sh", ("X",)),
    ("sz", ("X",)),
    ("cz", ("X",)),
    ("ch", ("X", "H")),
    ("ph", ("F",)),
    ("th", ("S", "T")),
    ("dh", ("Z", "D")),
    ("ts", ("C",)),
    ("tz", ("C",)),
    ("tc", ("C",)),
    ("ck", ("K",)),
    ("qu", ("K",)),
    ("gu", ("H",)),
    ("ks", ("KS",)),
    ("cs", ("KS",)),
    ("x", ("KS", "H")),
    ("q", ("K",)),
    ("k", ("K",)),
    ("c", ("K", "C")),
    ("g", ("H",)),
    ("h", ("H",)),
    ("w", ("V",)),
    ("v", ("V",)),
    ("j", ("J", "")),
    ("z", ("Z",)),
    ("s", ("S",)),
    ("f", ("F",)),
    ("b", ("B",)),
    ("p", ("P",)),
    ("d", ("D",)),
    ("t", ("T",)),
    ("l", ("L",)),
    ("r", ("R",)),
    ("m", ("M",)),
    ("n", ("N",)),
]
_GRAPHEME_RE = re.compile("|".join(re.escape(p) for p, _ in _GRAPHEMES) + "|[aeiouy]|.")
_GRAPHEME_ALTS = dict(_GRAPHEMES)

_ARABIC_COMPOUND = [
    (re.compile(r"^abd(?:ul|ol|al|el|il|ur|ar|ad|ud|as|us|ash|ush|an|un|az|uz|at|ut|u|e|o)?(?=[^aeiou])"), "abd"),
    (re.compile(r"(?<=[a-z]{3})(?:ud|ad|ed|id|od|al|el|ul|ol)-?din(?:e)?$"), "din"),
    (re.compile(r"(?:ul|ol|al|el|il|u)?lah?$"), "lah"),
]
_ENDINGS = [
    (re.compile(r"(?:iyy|iy|ij|ii|yi|yy|ie)$"), "i"),
    (re.compile(r"(?<=[aeiou])h$"), ""),
    (re.compile(r"(?<=[^aeiou])y$"), "i"),
    (re.compile(r"^(?:ye|je|ie|yo|jo|io|ё)(?=[^aeiou])"), "e"),
]


def _word_graphemes(word: str) -> List[_G]:
    for pattern, repl in _ARABIC_COMPOUND:
        if len(word) > 5:
            word = pattern.sub(repl, word)
    for pattern, repl in _ENDINGS:
        word = pattern.sub(repl, word)
    out: List[_G] = []
    pos = 0
    for m in _GRAPHEME_RE.finditer(word):
        g = m.group(0)
        if g in _VOWELS:
            out.append(_G(("_",)))  # vowel placeholder
        elif g in _GRAPHEME_ALTS:
            alts = _GRAPHEME_ALTS[g]
            # Word-initial j/y/i before a vowel is a glide (Yuri, Jurij, Iurii).
            if g == "j" and pos == 0:
                alts = ("Y", "J")
            out.append(_G(alts))
        pos = m.end()
    # Word-initial y/i before a/o/u is a glide (Yana, Iana, Yusuf, Iurii).
    if len(out) >= 2 and word[:1] in "yi" and word[1:2] in "aou":
        out[0] = _G(("Y",))
    return out


def _render(graphemes: Sequence[_G], choice: Sequence[str]) -> str:
    tokens: List[str] = []
    for k, (_g, tok) in enumerate(zip(graphemes, choice)):
        if tok == "_":
            if k == 0:
                tokens.append("A")
            continue
        tokens.append(tok)
    key = "".join(tokens)
    key = re.sub(r"(.)\1+", r"\1", key)
    if len(key) > 1 and key.endswith("D"):
        key = key[:-1] + "T"
    return key


def name_keys(word: str, language: Optional[str] = None, *, max_keys: int = 8) -> FrozenSet[str]:
    """Skeleton keys of one name part (a few when letters are ambiguous).

    >>> sorted(name_keys("Mohammed"))
    ['MHMT']
    >>> bool(name_keys("Alexander") & name_keys("Олександр"))
    True
    """
    latin = to_match_latin(word, language)
    latin = "".join(c for c in latin if c.isalpha())
    if not latin:
        return frozenset()
    graphemes = _word_graphemes(latin)
    ambiguous = [i for i, g in enumerate(graphemes) if len(g.alts) > 1]
    keys: List[str] = []
    primary = [g.alts[0] for g in graphemes]
    keys.append(_render(graphemes, primary))
    for combo in itertools.product(*[graphemes[i].alts for i in ambiguous[:3]]):
        choice = list(primary)
        for i, tok in zip(ambiguous[:3], combo):
            choice[i] = tok
        key = _render(graphemes, choice)
        if key not in keys:
            keys.append(key)
        if len(keys) >= max_keys:
            break
    return frozenset(k for k in keys if k)


def name_key(name: str, language: Optional[str] = None) -> str:
    """Primary skeleton key of a whole name (parts sorted, particles dropped).

    Useful as a blocking key in databases: equal keys → candidate match.
    """
    parts = [p for p in split_name(name) if p.lower() not in PARTICLES]
    keys = []
    for p in parts:
        latin = "".join(c for c in to_match_latin(p, language) if c.isalpha())
        if latin:
            graphemes = _word_graphemes(latin)
            keys.append(_render(graphemes, [g.alts[0] for g in graphemes]))
    return " ".join(sorted(k for k in keys if k))


_SPLIT_RE = re.compile(r"[\s,;/]+|(?<=\w)-(?=\w)")


def split_name(name: str) -> List[str]:
    """Split a full name into parts on spaces, commas and hyphens.

    Arabic article prefixes stay attached (``al-Rashid`` is one part).
    """
    name = normalize(name)
    parts: List[str] = []
    for chunk in re.split(r"[\s,;/]+", name):
        if not chunk:
            continue
        low = chunk.lower()
        if re.match(r"^(al|el|ul|ad|ar|as|ash|at|az|an|ud)-", low):
            parts.append(chunk)
            continue
        parts.extend(p for p in chunk.split("-") if p)
    return parts


def jaro_winkler(a: str, b: str, prefix_weight: float = 0.1) -> float:
    """Jaro–Winkler similarity in [0, 1] (pure Python, rapidfuzz if installed)."""
    if a == b:
        return 1.0 if a else 0.0
    if not a or not b:
        return 0.0
    try:  # pragma: no cover - optional speed-up
        from rapidfuzz.distance import JaroWinkler  # type: ignore[import-not-found,unused-ignore]

        return float(JaroWinkler.similarity(a, b, prefix_weight=prefix_weight))
    except ImportError:
        pass
    la, lb = len(a), len(b)
    window = max(0, max(la, lb) // 2 - 1)
    ma = [False] * la
    mb = [False] * lb
    matches = 0
    for i, ca in enumerate(a):
        lo, hi = max(0, i - window), min(lb, i + window + 1)
        for j in range(lo, hi):
            if not mb[j] and b[j] == ca:
                ma[i] = mb[j] = True
                matches += 1
                break
    if not matches:
        return 0.0
    t = 0
    j = 0
    for i in range(la):
        if ma[i]:
            while not mb[j]:
                j += 1
            if a[i] != b[j]:
                t += 1
            j += 1
    jaro = (matches / la + matches / lb + (matches - t / 2) / matches) / 3
    prefix = 0
    for ca, cb in zip(a[:4], b[:4]):
        if ca != cb:
            break
        prefix += 1
    return jaro + prefix * prefix_weight * (1 - jaro)


@dataclass(frozen=True)
class PartMatch:
    left: str
    right: str
    score: float
    reason: str


@dataclass(frozen=True)
class MatchResult:
    """Detailed outcome of :func:`compare`."""

    score: float
    pairs: Tuple[PartMatch, ...] = ()
    unmatched_left: Tuple[str, ...] = ()
    unmatched_right: Tuple[str, ...] = ()

    def __float__(self) -> float:
        return self.score


@dataclass
class _Part:
    raw: str
    latin: str
    keys: FrozenSet[str]
    clusters: FrozenSet[str]
    short_clusters: FrozenSet[str] = frozenset()
    equiv_clusters: FrozenSet[str] = frozenset()
    initial: bool = False


def _clusters(part: str, language: Optional[str]) -> Tuple[FrozenSet[str], FrozenSet[str], FrozenSet[str]]:
    """Lexicon clusters of a name part: (same name, diminutive of, translation of)."""
    from .lexicon import get_lexicon

    lex = get_lexicon()
    found = lex.lookup(part, language)
    if not found and "-" in part:
        found = lex.lookup(part.split("-", 1)[1], language)
    return (
        frozenset(e.id for e in found),
        frozenset(e.id for e in lex.lookup_short(part)),
        frozenset(e.id for e in lex.lookup_equivalents(part)),
    )


def _prepare(name: str, language: Optional[str], use_lexicon: bool = True) -> List[_Part]:
    if language is None and detect_script(name) not in ("Latn", "Zyyy"):
        language = detect_language(name).language
    parts = []
    for raw in split_name(name):
        bare = raw.rstrip(".")
        if bare.lower() in PARTICLES:
            continue
        if re.match(r"^(al|el|ul|ad|ar|as|ash|at|az|an|ud)-", bare.lower()):
            bare = bare.split("-", 1)[1]
        latin = "".join(c for c in to_match_latin(bare, language) if c.isalpha())
        if not latin or latin in PARTICLES:  # بن → bin
            continue
        initial = len(latin) == 1 or (raw.endswith(".") and len(latin) <= 3)
        empty: FrozenSet[str] = frozenset()
        lookup = use_lexicon and not initial
        clusters, short_clusters, equiv_clusters = _clusters(bare, language) if lookup else (empty, empty, empty)
        parts.append(
            _Part(
                raw=raw,
                latin=latin,
                keys=name_keys(bare, language) if not initial else frozenset(),
                clusters=clusters,
                short_clusters=short_clusters,
                equiv_clusters=equiv_clusters,
                initial=initial,
            )
        )
    return parts


_COARSE = str.maketrans({"Z": "S", "C": "S", "X": "S", "J": "S", "F": "V", "P": "B", "D": "T"})


def _coarse(key: str) -> str:
    """Second-tier key: German/Turkish-folded spellings (Sacharow, Schukow,
    Sirin, Ivanoff) collapse sibilants, v/f, b/p and d/t."""
    return re.sub(r"(.)\1+", r"\1", key.translate(_COARSE))


def _part_score(a: _Part, b: _Part) -> Tuple[float, str]:
    if a.initial or b.initial:
        if a.latin[:1] == b.latin[:1]:
            return 0.85, "initial"
        return 0.0, "initial-mismatch"
    if a.latin == b.latin:
        return 1.0, "exact"
    if a.clusters and b.clusters and a.clusters & b.clusters:
        return 0.98, "same-name"
    if (a.short_clusters & b.clusters) or (b.short_clusters & a.clusters):
        return 0.86, "diminutive"
    if (a.equiv_clusters & b.clusters) or (b.equiv_clusters & a.clusters):
        return 0.8, "equivalent"
    jw = jaro_winkler(a.latin, b.latin)
    if a.keys & b.keys:
        score = 0.9 + 0.08 * jw
        reason = "skeleton"
    elif {_coarse(k) for k in a.keys} & {_coarse(k) for k in b.keys}:
        score = 0.85 + 0.1 * jw
        reason = "skeleton-coarse"
    else:
        key_jw = max((jaro_winkler(x, y) for x in a.keys for y in b.keys), default=0.0)
        score = max(jw * 0.95, key_jw * 0.9)
        reason = "fuzzy"
    if a.clusters and b.clusters and not (a.clusters & b.clusters):
        # Both are known names but different ones (Hasan ≠ Husayn).
        score = min(score, 0.6)
        reason = "different-names"
    return round(score, 4), reason


def _merged(parts: List[_Part], language: Optional[str], use_lexicon: bool) -> List[List[_Part]]:
    """Alternative segmentations with one pair of adjacent parts joined
    (``Abdul Rahman`` ~ ``Abdulrahman``, ``Nur ad-Din`` ~ ``Nuruddin``)."""
    out = []
    for k in range(len(parts) - 1):
        a, b = parts[k], parts[k + 1]
        if a.initial or b.initial:
            continue
        joined = _prepare(re.sub(r"[-\s]", "", a.raw + b.raw), language, use_lexicon)
        if len(joined) != 1:
            continue
        part = joined[0]
        if use_lexicon:
            # The spaced form may be a compound in the lexicon ("Abd al-Rahman").
            spaced, _, _ = _clusters(f"{a.raw} {b.raw}", language)
            if spaced:
                part = _Part(
                    part.raw, part.latin, part.keys, part.clusters | spaced, part.short_clusters, part.equiv_clusters
                )
        out.append([*parts[:k], part, *parts[k + 2 :]])
    return out


def compare(
    a: str,
    b: str,
    *,
    language_a: Optional[str] = None,
    language_b: Optional[str] = None,
    use_lexicon: bool = True,
) -> MatchResult:
    """Compare two full names; returns a :class:`MatchResult` with details.

    Name parts are aligned in the best order.  Unmatched extra parts
    (patronymics, middle names) reduce the score only slightly.  Adjacent
    parts may be joined when that aligns better (``Abd al-Rahman`` vs
    ``Abdulrahman``).  ``use_lexicon=False`` relies on skeleton keys and
    string similarity only.
    """
    pa = _prepare(a, language_a, use_lexicon)
    pb = _prepare(b, language_b, use_lexicon)
    if not pa or not pb:
        return MatchResult(0.0)
    best = _compare_parts(pa, pb)
    if len(pa) != len(pb) and best.score < 0.97:
        longer_is_a = len(pa) > len(pb)
        lang = language_a if longer_is_a else language_b
        for alt in _merged(pa if longer_is_a else pb, lang, use_lexicon):
            res = _compare_parts(alt, pb) if longer_is_a else _compare_parts(pa, alt)
            if res.score > best.score:
                best = res
    return best


def _compare_parts(pa: List[_Part], pb: List[_Part]) -> MatchResult:
    swap = len(pa) > len(pb)
    small, big = (pb, pa) if swap else (pa, pb)
    matrix = [[_part_score(x, y) for y in big] for x in small]
    best_total = -1.0
    best_perm: Tuple[int, ...] = ()
    if len(big) <= 7:
        for perm in itertools.permutations(range(len(big)), len(small)):
            total = sum(matrix[i][j][0] for i, j in enumerate(perm))
            if total > best_total:
                best_total, best_perm = total, perm
    else:  # greedy for unusually long names
        used: Set[int] = set()
        perm_list = []
        for i in range(len(small)):
            j = max((j for j in range(len(big)) if j not in used), key=lambda j: matrix[i][j][0])
            used.add(j)
            perm_list.append(j)
        best_perm = tuple(perm_list)
        best_total = sum(matrix[i][j][0] for i, j in enumerate(best_perm))
    pairs = []
    for i, j in enumerate(best_perm):
        s, reason = matrix[i][j]
        left, right = (big[j], small[i]) if swap else (small[i], big[j])
        pairs.append(PartMatch(left.raw, right.raw, s, reason))
    extra = [big[j] for j in range(len(big)) if j not in best_perm]
    weights = [max(len(small[i].latin), 3) for i in range(len(small))]
    score = sum(matrix[i][j][0] * w for (i, j), w in zip(enumerate(best_perm), weights)) / sum(weights)
    # Each unmatched part (patronymic, second given name) costs 4%, capped at 15%.
    score *= 1 - min(0.15, 0.04 * len(extra))
    unmatched = tuple(p.raw for p in extra)
    return MatchResult(
        score=round(score, 4),
        pairs=tuple(pairs),
        unmatched_left=unmatched if swap else (),
        unmatched_right=() if swap else unmatched,
    )


def similarity(
    a: str,
    b: str,
    *,
    language_a: Optional[str] = None,
    language_b: Optional[str] = None,
    use_lexicon: bool = True,
) -> float:
    """Similarity of two names in [0, 1], across scripts and spellings.

    >>> similarity("Мухаммед Али", "Mohammed Ali") > 0.9
    True
    >>> similarity("Щербаков Юрий", "Yuri Scherbakov") > 0.9
    True
    """
    return compare(a, b, language_a=language_a, language_b=language_b, use_lexicon=use_lexicon).score


def is_match(
    a: str,
    b: str,
    threshold: float = 0.88,
    *,
    language_a: Optional[str] = None,
    language_b: Optional[str] = None,
    use_lexicon: bool = True,
) -> bool:
    """``True`` if :func:`similarity` is at least ``threshold`` (default 0.88)."""
    return similarity(a, b, language_a=language_a, language_b=language_b, use_lexicon=use_lexicon) >= threshold
