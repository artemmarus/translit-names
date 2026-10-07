"""Matching and variant-generation benchmark built from the bundled lexicon.

The lexicon groups attested spellings of the same name.  This script checks
how well the *lexicon-free* machinery (skeleton keys + string similarity)
generalises:

- recall: pairs of spellings of the same name that are recognised as a match
  without looking them up in the lexicon;
- false-positive rate: random pairs of *different* names that are wrongly
  recognised as a match (without the lexicon);
- cross-script recall: native spelling (Cyrillic / Arabic script) vs its
  conventional Latin spellings;
- variant coverage: share of conventional Latin spellings that
  ``variants(native_form)`` proposes.

Usage: python scripts/benchmark.py [--threshold 0.88] [--seed 1]
"""

from __future__ import annotations

import argparse
import random
import statistics
import time
from itertools import combinations

from translit_names import get_lexicon, similarity, variants
from translit_names.detect import detect_script
from translit_names.normalize import latin_key


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.88)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--pairs", type=int, default=3000)
    args = ap.parse_args()
    rnd = random.Random(args.seed)
    lex = get_lexicon()
    entries = [e for e in lex if e.kind in ("given", "family")]

    # 1. Same-name pairs, Latin vs Latin, no lexicon.
    same = []
    for e in entries:
        forms = [f for f in e.all_latin() if detect_script(f) == "Latn" and " " not in f]
        uniq = list({latin_key(f): f for f in forms}.values())
        same.extend(combinations(uniq, 2))
    rnd.shuffle(same)
    same = same[: args.pairs]
    t0 = time.perf_counter()
    scores = [similarity(a, b, use_lexicon=False) for a, b in same]
    dt = time.perf_counter() - t0
    recall = sum(s >= args.threshold for s in scores) / len(scores)

    # 2. Different-name pairs, no lexicon.
    diff = []
    while len(diff) < args.pairs:
        e1, e2 = rnd.sample(entries, 2)
        if set(e1.related) & {e2.id} or set(e2.related) & {e1.id}:
            continue
        a, b = e1.english or e1.all_latin()[0], e2.english or e2.all_latin()[0]
        if latin_key(a) != latin_key(b):
            diff.append((a, b))
    fp_scores = [similarity(a, b, use_lexicon=False) for a, b in diff]
    fpr = sum(s >= args.threshold for s in fp_scores) / len(fp_scores)

    # 3. Native script vs Latin, no lexicon.
    cross = []
    for e in entries:
        natives = [
            f for lang, fs in e.native.items() for f in fs if lang in ("ru", "uk", "ar", "fa", "kk") and " " not in f
        ]
        latins = [f for f in e.all_latin() if detect_script(f) == "Latn" and " " not in f][:4]
        for n in natives[:2]:
            for latin in latins:
                cross.append((n, latin))
    rnd.shuffle(cross)
    cross = cross[: args.pairs]
    cross_scores = [similarity(a, b, use_lexicon=False) for a, b in cross]
    cross_recall = sum(s >= args.threshold for s in cross_scores) / len(cross_scores)

    # 4. Variant coverage for Cyrillic names.
    cov = []
    for e in rnd.sample(entries, min(300, len(entries))):
        ru = e.native.get("ru")
        target = e.latin.get("ru")
        if not ru or not target:
            continue
        proposed = {latin_key(v) for v in variants(ru[0], "ru", limit=30, use_lexicon=False)}
        cov.append(sum(latin_key(t) in proposed for t in target) / len(target))

    print(f"lexicon entries            {len(lex)}")
    print(f"threshold                  {args.threshold}")
    print(f"same-name recall (no lex)  {recall:.3f}   n={len(same)}  median={statistics.median(scores):.3f}")
    print(f"false-positive rate        {fpr:.4f}  n={len(diff)}")
    print(f"cross-script recall        {cross_recall:.3f}   n={len(cross)}")
    print(
        f"variants coverage (ru)     {statistics.mean(cov):.3f}   n={len(cov)}  (schemes + rules, no lexicon, top 30)"
    )
    print(f"speed                      {len(same) / dt:.0f} comparisons/s (pure Python)")
    misses = [(a, b, s) for (a, b), s in zip(same, scores) if s < args.threshold]
    if misses:
        print("\nsample misses:")
        for a, b, s in misses[:15]:
            print(f"  {s:.3f}  {a} ~ {b}")


if __name__ == "__main__":
    main()
