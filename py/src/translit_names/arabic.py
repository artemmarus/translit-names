"""Arabic-script support: vocalisation of names before romanisation.

Arabic, Persian, Urdu and Pashto are normally written without short vowels,
so ``محمد`` carries only the consonants m-ḥ-m-d.  Every romanisation standard
assumes the vowels are known.  The hook below supplies them, in order:

1. text that already has vowel marks (harakat) is used as is;
2. names found in the bundled lexicon are replaced by their vocalised form
   (or, for *practical* schemes, by their conventional English spelling);
3. optionally, common Arabic name patterns (فاعل Khalid, فعيل Karim,
   مفعول Mahmud, أفعل Ahmad …) are vocalised heuristically;
4. anything else is romanised letter by letter (consonant skeleton).
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, List, Optional, Sequence, Tuple

if TYPE_CHECKING:  # pragma: no cover
    from ._engine import Scheme, Segment
    from .lexicon import NameEntry

__all__ = ["ARTICLE", "arabic_hook", "has_harakat", "vocalize_word"]

FATHA, DAMMA, KASRA, SUKUN, SHADDA = "\u064e", "\u064f", "\u0650", "\u0652", "\u0651"
ARTICLE = "ال"
_HARAKAT_RE = re.compile("[\u064b-\u0652\u0670]")
_WORD_RE = re.compile("[ء-غف-ي\u064b-\u065fٮ-ۓەۮۯۺ-ۿݐ-ݿ\u0670\u200c]+")

_ALEFS = set("اآأإٱ")
_YEHS = set("يیىې")
_WAWS = set("وۇۆ")
_TA_MARBUTA = "ة"


def has_harakat(text: str) -> bool:
    return bool(_HARAKAT_RE.search(text))


def _is_cons(c: str) -> bool:
    return c not in _ALEFS and c not in _YEHS and c not in _WAWS and c != _TA_MARBUTA


def vocalize_word(word: str) -> Optional[str]:
    """Guess short vowels for a bare Arabic name using common templates.

    Returns ``None`` when no template fits.  The guesses follow classical
    name patterns and are right for most Arabic given names, but they are
    guesses: prefer the lexicon, or input with harakat, when accuracy matters.
    """
    if not word or has_harakat(word):
        return None
    fem = word.endswith(_TA_MARBUTA)
    stem = word[:-1] if fem else word
    L = list(stem)
    n = len(L)
    out: Optional[List[str]] = None

    def C(k: int) -> bool:
        return _is_cons(L[k])

    if n == 3:
        if C(0) and C(1) and C(2):
            out = [L[0], FATHA, L[1], FATHA, L[2]]  # فَعَل  Hasan
        elif C(0) and L[1] in _YEHS and C(2):
            out = [L[0], FATHA, L[1], SUKUN, L[2]]  # فَيْل  Zayd, Sayf
        elif C(0) and L[1] in _WAWS and C(2):
            out = [L[0], DAMMA, L[1], L[2]]  # فُول  Nur
        elif C(0) and C(1) and L[2] in _YEHS:
            out = [L[0], FATHA, L[1], KASRA, L[2]]  # فَعِي  Ali
        elif C(0) and L[1] in _ALEFS and C(2):
            out = [L[0], FATHA, L[1], L[2]]  # فال  Jad
    elif n == 4:
        if C(0) and L[1] in _ALEFS and C(2) and C(3):
            out = [L[0], FATHA, L[1], L[2], KASRA, L[3]]  # فاعِل  Khalid
        elif C(0) and C(1) and L[2] in _YEHS and C(3):
            out = [L[0], FATHA, L[1], KASRA, L[2], L[3]]  # فَعِيل  Karim
        elif C(0) and C(1) and L[2] in _WAWS and C(3):
            out = [L[0], FATHA, L[1], DAMMA, L[2], L[3]]  # فَعُول  Sabur
        elif C(0) and C(1) and L[2] in _ALEFS and C(3):
            out = [L[0], FATHA, L[1], FATHA, L[2], L[3]]  # فَعال  Jamal
        elif L[0] in _ALEFS and C(1) and C(2) and C(3):
            first = "إ" if L[0] == "إ" else "أ"
            vowel = KASRA if first == "إ" else FATHA
            out = [first, vowel, L[1], SUKUN, L[2], FATHA, L[3]]  # أَفْعَل  Ahmad
        elif C(0) and (L[1] in _YEHS or L[1] in _WAWS) and C(2) and C(3):
            out = [L[0], FATHA, L[1], SUKUN, L[2], FATHA, L[3]]  # فَيْعَل  Haydar, Zaynab
        elif C(0) and C(1) and C(2) and C(3):
            out = [L[0], FATHA, L[1], SUKUN, L[2], FATHA, L[3]]  # فَعْلَل  Jafar
        elif C(0) and C(1) and C(2) and L[3] in _YEHS:
            out = [L[0], FATHA, L[1], SUKUN, L[2], KASRA, L[3]]  # فَعْلِي  Ramzi, Zanki
    elif n == 5:
        if C(0) and L[1] in _ALEFS and C(2) and L[3] in _WAWS and C(4):
            out = [L[0], FATHA, L[1], L[2], DAMMA, L[3], L[4]]  # فاعُول  Harun, Faruq
        elif L[0] == "م" and C(1) and C(2) and L[3] in _WAWS and C(4):
            out = [L[0], FATHA, L[1], SUKUN, L[2], DAMMA, L[3], L[4]]  # مَفْعُول  Mahmud
        elif L[0] in _ALEFS and C(1) and C(2) and L[3] in _ALEFS and C(4):
            first = "إ" if L[0] in "إا" else L[0]
            out = [first, KASRA, L[1], SUKUN, L[2], FATHA, L[3], L[4]]  # إِفْعال  Ihsan
    if out is None:
        return None
    if fem:
        if out[-1] not in (FATHA, DAMMA, KASRA, SUKUN):
            out.append(FATHA)
        out.append(_TA_MARBUTA)
    return "".join(out)


def _tokenize(text: str) -> List[Tuple[bool, str]]:
    tokens: List[Tuple[bool, str]] = []
    pos = 0
    for m in _WORD_RE.finditer(text):
        if m.start() > pos:
            tokens.append((False, text[pos : m.start()]))
        tokens.append((True, m.group(0)))
        pos = m.end()
    if pos < len(text):
        tokens.append((False, text[pos:]))
    return tokens


def _phrase(tokens: Sequence[Tuple[bool, str]], i: int, words: int) -> Optional[Tuple[str, int]]:
    """Join ``words`` word tokens starting at ``i`` if separated only by spaces."""
    parts = []
    j = i
    for k in range(words):
        if j >= len(tokens) or not tokens[j][0]:
            return None
        parts.append(tokens[j][1])
        j += 1
        if k < words - 1:
            if j >= len(tokens) or tokens[j][0] or tokens[j][1].strip() not in ("", "-"):
                return None
            j += 1
    return " ".join(parts), j


def _lookup(scheme: Scheme, text: str) -> Optional[NameEntry]:
    from .lexicon import get_lexicon

    hits = get_lexicon().lookup_arabic(text, scheme.language)
    if not hits:
        joined = text.replace(" ", "")
        if joined != text:
            hits = get_lexicon().lookup_arabic(joined, scheme.language)
    for e in hits:
        return e
    return None


def _render(scheme: Scheme, entry: NameEntry, article: bool) -> Optional[Segment]:
    practical = scheme.options.get("practical")
    if practical:
        latin = entry.latin_for([*list(practical), "en"])
        if latin:
            prefix = scheme.options.get("article", "al-") if article else ""
            return ("lit", prefix + latin)
    if entry.vocalized:
        return ("src", (ARTICLE if article else "") + entry.vocalized)
    return None


def arabic_hook(scheme: Scheme, text: str) -> List[Segment]:
    """Word hook used by Arabic-script schemes (``"hook": "arabic"``).

    Scheme ``options``:

    - ``lexicon`` (default ``true``): use the bundled name lexicon;
    - ``practical``: list of lexicon language keys (``["ar", "ar_eg"]``); when
      set, known names are emitted in their conventional Latin spelling;
    - ``article``: literal used for the article in practical output (``"al-"``);
    - ``vocalize`` (default ``false``): guess vowels for unknown names.
    """
    use_lexicon = scheme.options.get("lexicon", True)
    guess = scheme.options.get("vocalize", False)
    tokens = _tokenize(text)
    segments: List[Segment] = []
    i = 0
    while i < len(tokens):
        is_word, tok = tokens[i]
        if not is_word or has_harakat(tok):
            segments.append(("src", tok))
            i += 1
            continue
        if use_lexicon:
            done = False
            for span in (3, 2):
                ph = _phrase(tokens, i, span)
                if ph is None:
                    continue
                entry = _lookup(scheme, ph[0])
                if entry is not None:
                    seg = _render(scheme, entry, article=False)
                    if seg is not None:
                        segments.append(seg)
                        i = ph[1]
                        done = True
                        break
            if done:
                continue
            seg = None
            entry = _lookup(scheme, tok)
            if entry is not None:
                seg = _render(scheme, entry, article=False)
            elif tok.startswith(ARTICLE) and len(tok) > 3:
                entry = _lookup(scheme, tok[2:])
                if entry is not None:
                    seg = _render(scheme, entry, article=True)
            if seg is not None:
                segments.append(seg)
                i += 1
                continue
        if guess:
            article = tok.startswith(ARTICLE) and len(tok) > 4
            stem = tok[2:] if article else tok
            voc = vocalize_word(stem)
            if voc is not None:
                segments.append(("src", (ARTICLE if article else "") + voc))
                i += 1
                continue
        segments.append(("src", tok))
        i += 1
    return segments
