"""Generate golden outputs of the Python implementation for the TypeScript port.

The TypeScript package (``js/``) must reproduce these results exactly; CI
regenerates this file and fails if it differs from the committed copy, then
runs the TypeScript parity tests against it.

Usage: python scripts/gen_parity_fixtures.py [--out js/test/fixtures/parity.json]
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List

from translit_names import (
    compare,
    detect_language,
    fix_mixed_script,
    fold,
    get_lexicon,
    get_scheme,
    list_schemes,
    mrz_name,
    mrz_text,
    name_key,
    name_keys,
    normalize,
    split_name,
    transliterate,
    variants_detailed,
)
from translit_names._registry import scheme_specs
from translit_names.arabic import vocalize_word
from translit_names.detect import detect_script
from translit_names.matching import jaro_winkler

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "js" / "test" / "fixtures" / "parity.json"))
    args = ap.parse_args()
    rnd = random.Random(20261007)
    lex = get_lexicon()
    entries = sorted(lex, key=lambda e: e.id)
    specs = scheme_specs()

    natives: Dict[str, List[str]] = {}
    latins: List[str] = []
    for e in entries:
        for lang, forms in e.native.items():
            natives.setdefault(lang, []).extend(forms)
        latins.extend(f for f in e.all_latin() if detect_script(f) == "Latn")
    for lang in natives:
        natives[lang] = sorted(set(natives[lang]))
    latins = sorted(set(latins))

    out: Dict[str, Any] = {}

    # 1. Every scheme: its samples, its alphabet, and names of its language.
    rows = []
    for s in list_schemes():
        inputs = [src for src, _ in s.samples]
        alpha = specs[s.id].get("alphabet", "")
        if alpha:
            inputs += [alpha, alpha.upper(), alpha.title()]
        pool = natives.get(s.language, [])
        pool = [x for x in pool if detect_script(x) == s.script] if s.script != "Latn" else pool
        if s.script == "Latn":
            pool = [x for x in latins if not x.isascii()]
        inputs += rnd.sample(pool, min(40, len(pool)))
        for text in dict.fromkeys(inputs):
            rows.append([s.id, text, s.transliterate(text)])
    out["scheme"] = rows

    # 2. Auto transliteration, detection.
    mixed = []
    for lang in sorted(natives):
        mixed += rnd.sample(natives[lang], min(15, len(natives[lang])))
    mixed += rnd.sample(latins, 60)
    mixed += [
        "Щербаков Юрий",
        "Иванoв",
        "Олександр Згурський",
        "محمد بن سلمان",
        "عبد الرحمن",
        "Нұрсұлтан Назарбаев",
        "John Smith",
        "",
    ]
    out["auto"] = [[t, transliterate(t)] for t in dict.fromkeys(mixed)]
    out["detect"] = [
        [t, d.language, d.script, d.confidence, [list(c) for c in d.candidates]]
        for t in dict.fromkeys(mixed)
        for d in [detect_language(t)]
    ]

    # 3. Clean-up helpers.
    samples = list(
        dict.fromkeys(
            [
                *mixed,
                "  Анна\xa0\u2013\xa0Мария  ",
                "Е\u0308лкин",
                "١٢٣",
                "ﻻ",
                "محـــمد",
                "Аlexey",
                "Łódź Ærø Þór Məmmədov İstanbul",
                "ÆSIR",
                "GROß",
                "Ǆokić",
            ]
        )
    )
    out["normalize"] = [[t, normalize(t), fix_mixed_script(t)] for t in samples]
    out["fold"] = [[t, fold(t), fold(t, german=True)] for t in samples]
    out["split"] = [[t, split_name(t)] for t in samples]

    # 4. Lexicon lookups.
    probes = (
        rnd.sample(latins, 150)
        + rnd.sample([x for xs in natives.values() for x in xs], 150)
        + ["Саша", "John", "Мамедов", "Jurij"]
    )
    out["lookup"] = [
        [
            t,
            [e.id for e in lex.lookup(t)],
            [e.id for e in lex.lookup_short(t)],
            [e.id for e in lex.lookup_equivalents(t)],
        ]
        for t in dict.fromkeys(probes)
    ]

    # 5. Keys and Jaro–Winkler.
    words = rnd.sample(latins, 300) + rnd.sample([x for xs in natives.values() for x in xs if " " not in x], 200)
    out["keys"] = [[w, sorted(name_keys(w))] for w in dict.fromkeys(words)]
    out["name_key"] = [[t, name_key(t)] for t in dict.fromkeys(mixed)]
    out["jaro"] = [[a, b, jaro_winkler(a.lower(), b.lower())] for a, b in zip(words[:150], words[150:300])]

    # 6. Arabic template vocaliser.
    arabic_words = [x for x in natives.get("ar", []) if " " not in x]
    out["vocalize"] = [[w, vocalize_word(w)] for w in arabic_words]

    # 7. Matching.
    pairs = []
    for e in rnd.sample(entries, 250):
        forms = [f for f in e.all_native()[:2] + e.all_latin()[:4] if f]
        if len(forms) >= 2:
            a, b = rnd.sample(forms, 2)
            pairs.append((a, b))
    for _ in range(150):
        e1, e2 = rnd.sample(entries, 2)
        pairs.append((e1.english or e1.id, (e2.all_native() or [e2.english])[0]))
    pairs += [
        ("Мухаммед Али", "Mohammed Ali"),
        ("Ivanov Ivan Ivanovich", "IVAN IVANOV"),
        ("Abd al-Rahman", "Abdurrahman"),
        ("Саша Иванов", "Aleksandr Ivanov"),
        ("Michael", "Михаил"),
        ("Ivanov I. I.", "Ivan Ivanov"),
        ("Muhammad bin Salman", "محمد بن سلمان"),
    ]
    rows = []
    for a, b in pairs:
        for use_lexicon in (True, False):
            r = compare(a, b, use_lexicon=use_lexicon)
            rows.append(
                [
                    a,
                    b,
                    use_lexicon,
                    r.score,
                    [[p.left, p.right, p.score, p.reason] for p in r.pairs],
                    list(r.unmatched_left),
                    list(r.unmatched_right),
                ]
            )
    out["compare"] = rows

    # 8. Variants.
    names = [*rnd.sample(mixed, 80), "Юрий", "Евгений Щербаков", "محمد", "عبد الرحمن", "Хусейн", "Олександр"]
    rows = []
    for t in dict.fromkeys(names):
        for use_lexicon in (True, False):
            vs = variants_detailed(t, limit=15, use_lexicon=use_lexicon)
            rows.append([t, use_lexicon, [[v.text, v.score, list(v.sources)] for v in vs]])
    out["variants"] = rows

    # 9. MRZ.
    rows = []
    mrz_inputs = [
        ("ERIKSSON", "ANNA MARIA"),
        ("NILAVADHANANANDA", "CHAYAPA DEJTHAMRONG KRASUANG"),
        ("BENNELONG WOOLOOMOOLOO WARRANDYTE WARNAMBOOL", "DINGO POTOROO"),
        ("O'Connor", "Enya Siobhan"),
        ("Əliyev", "İlham"),
        ("Müller", ""),
    ]
    for t in rnd.sample([x for x in mixed if x], 60):
        parts = t.split()
        mrz_inputs.append((parts[-1], " ".join(parts[:-1])))
    for sur, given in mrz_inputs:
        for length in (39, 30):
            for strategy in ("cut", "initials"):
                rows.append([sur, given, length, strategy, mrz_name(sur, given, length=length, strategy=strategy)])
    out["mrz"] = rows
    out["mrz_text"] = [[t, mrz_text(t), mrz_text(t, german=True)] for t in samples if t.strip()]

    # Sanity: every fixture must be JSON-serialisable and deterministic.
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(out, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    Path(args.out).write_text(text + "\n", encoding="utf-8")
    counts = {k: len(v) for k, v in out.items()}
    print(f"wrote {args.out} ({len(text) // 1024} KB): {counts}")
    _ = get_scheme  # re-exported for interactive use


if __name__ == "__main__":
    main()
