"""Command-line interface: ``translit-names`` (or ``python -m translit_names``)."""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional, Sequence

from . import __version__
from ._registry import list_schemes
from .core import transliterate
from .detect import detect_language
from .matching import compare
from .mrz import TD1, TD2, TD3, mrz_name
from .variants import variants_detailed


def _read_inputs(values: Sequence[str]) -> List[str]:
    if values:
        return [" ".join(values)]
    return [line.rstrip("\n") for line in sys.stdin if line.strip()]


def _cmd_translit(args: argparse.Namespace) -> int:
    for text in _read_inputs(args.text):
        if args.all:
            lang = args.language or detect_language(text).language
            for sch in list_schemes(lang):
                print(f"{sch.id:<24} {sch.transliterate(text)}")
        else:
            print(transliterate(text, args.scheme, language=args.language))
    return 0


def _cmd_variants(args: argparse.Namespace) -> int:
    for text in _read_inputs(args.text):
        vs = variants_detailed(
            text, args.language, limit=args.limit, ascii_only=not args.unicode, include_short=args.short
        )
        if args.json:
            print(
                json.dumps([{"text": v.text, "score": v.score, "sources": v.sources} for v in vs], ensure_ascii=False)
            )
        else:
            for v in vs:
                print(f"{v.score:.3f}  {v.text}" if args.scores else v.text)
    return 0


def _cmd_match(args: argparse.Namespace) -> int:
    res = compare(args.a, args.b)
    if args.json:
        print(
            json.dumps(
                {
                    "score": res.score,
                    "match": res.score >= args.threshold,
                    "pairs": [
                        {"left": p.left, "right": p.right, "score": p.score, "reason": p.reason} for p in res.pairs
                    ],
                    "unmatched": list(res.unmatched_left + res.unmatched_right),
                },
                ensure_ascii=False,
            )
        )
    else:
        print(f"score {res.score:.3f} -> {'MATCH' if res.score >= args.threshold else 'no match'}")
        for p in res.pairs:
            print(f"  {p.left!s:<20} ~ {p.right!s:<20} {p.score:.3f}  {p.reason}")
        for u in res.unmatched_left + res.unmatched_right:
            print(f"  (unmatched: {u})")
    return 0 if res.score >= args.threshold else 1


def _cmd_mrz(args: argparse.Namespace) -> int:
    length = {"td1": TD1, "td2": TD2, "td3": TD3}[args.format]
    print(
        mrz_name(
            args.surname,
            args.given or "",
            length=length,
            scheme=args.scheme,
            language=args.language,
            strategy=args.strategy,
        )
    )
    return 0


def _cmd_detect(args: argparse.Namespace) -> int:
    for text in _read_inputs(args.text):
        d = detect_language(text)
        cands = ", ".join(f"{k}:{v}" for k, v in d.candidates)
        print(f"{d.language}\t{d.script}\t{d.confidence}\t{cands}")
    return 0


def _cmd_schemes(args: argparse.Namespace) -> int:
    rows = list_schemes(args.language, kind=args.kind)
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "id": s.id,
                        "title": s.title,
                        "language": s.language,
                        "script": s.script,
                        "kind": s.kind,
                        "status": s.status,
                        "year": s.year,
                    }
                    for s in rows
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    for s in rows:
        year = s.year or ""
        print(f"{s.id:<24} {s.language:<4} {s.kind:<11} {s.status:<11} {year!s:<5} {s.title}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="translit-names",
        description="Transliterate, generate spelling variants of, and match Slavic and Muslim personal names.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command")

    t = sub.add_parser("translit", aliases=["t"], help="transliterate a name (default command)")
    t.add_argument("text", nargs="*", help="name to transliterate (reads stdin lines if omitted)")
    t.add_argument("-s", "--scheme", help="scheme id, e.g. ru_icao, uk_kmu_2010, ar_ala_lc")
    t.add_argument("-l", "--language", help="language code to skip auto-detection (ru, uk, kk, ar, fa …)")
    t.add_argument("-a", "--all", action="store_true", help="show the result of every scheme for the language")
    t.set_defaults(func=_cmd_translit)

    v = sub.add_parser("variants", aliases=["v"], help="list plausible Latin spellings")
    v.add_argument("text", nargs="*")
    v.add_argument("-l", "--language")
    v.add_argument("-n", "--limit", type=int, default=20)
    v.add_argument("--scores", action="store_true", help="print scores")
    v.add_argument("--short", action="store_true", help="include diminutives")
    v.add_argument("--unicode", action="store_true", help="keep diacritics")
    v.add_argument("--json", action="store_true")
    v.set_defaults(func=_cmd_variants)

    m = sub.add_parser("match", aliases=["m"], help="compare two names (exit code 0 if they match)")
    m.add_argument("a")
    m.add_argument("b")
    m.add_argument("-t", "--threshold", type=float, default=0.88)
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=_cmd_match)

    z = sub.add_parser("mrz", help="build the ICAO MRZ name field")
    z.add_argument("surname")
    z.add_argument("given", nargs="?")
    z.add_argument("-f", "--format", choices=["td1", "td2", "td3"], default="td3")
    z.add_argument("-s", "--scheme")
    z.add_argument("-l", "--language")
    z.add_argument("--strategy", choices=["cut", "initials"], default="cut")
    z.set_defaults(func=_cmd_mrz)

    d = sub.add_parser("detect", help="guess the language of a name")
    d.add_argument("text", nargs="*")
    d.set_defaults(func=_cmd_detect)

    s = sub.add_parser("schemes", help="list available schemes")
    s.add_argument("-l", "--language")
    s.add_argument("-k", "--kind")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=_cmd_schemes)
    return p


_COMMANDS = {"translit", "t", "variants", "v", "match", "m", "mrz", "detect", "schemes", "-h", "--help", "--version"}


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in _COMMANDS:
        argv.insert(0, "translit")
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except KeyError as exc:
        print(f"error: {exc.args[0] if exc.args else exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
