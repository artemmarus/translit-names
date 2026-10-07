"""translit-names: transliteration of Slavic and Muslim personal names into Latin script.

Quick start::

    >>> from translit_names import transliterate, variants, similarity, mrz_name
    >>> transliterate("Щербаков Юрий")              # Russian passport (ICAO 9303)
    'Shcherbakov Iurii'
    >>> transliterate("Щербаков Юрий", "ru_bgn_pcgn")
    'Shcherbakov Yuriy'
    >>> mrz_name("Щербаков", "Юрий")[:20]
    'SHCHERBAKOV<<IURII<<'
"""

from __future__ import annotations

from ._engine import Rule, Scheme, SchemeError
from ._fold import fold
from ._registry import default_scheme_id, get_scheme, list_schemes
from .core import resolve_scheme, transliterate
from .detect import Detection, detect_language, detect_script
from .lexicon import NameEntry, get_lexicon
from .matching import MatchResult, compare, is_match, jaro_winkler, name_key, name_keys, similarity, split_name
from .mrz import mrz_name, mrz_text, parse_mrz_name
from .normalize import fix_mixed_script, normalize
from .variants import Variant, variants, variants_detailed

__version__ = "0.1.0"

__all__ = [
    "Detection",
    "MatchResult",
    "NameEntry",
    "Rule",
    "Scheme",
    "SchemeError",
    "Variant",
    "__version__",
    "compare",
    "default_scheme_id",
    "detect_language",
    "detect_script",
    "fix_mixed_script",
    "fold",
    "get_lexicon",
    "get_scheme",
    "is_match",
    "jaro_winkler",
    "list_schemes",
    "mrz_name",
    "mrz_text",
    "name_key",
    "name_keys",
    "normalize",
    "parse_mrz_name",
    "resolve_scheme",
    "similarity",
    "split_name",
    "transliterate",
    "variants",
    "variants_detailed",
]
