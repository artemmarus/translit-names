/**
 * Parity with the Python reference implementation.
 *
 * `test/fixtures/parity.json` is produced by `scripts/gen_parity_fixtures.py`
 * (Python).  Every case must give the same result in TypeScript.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

import {
  compare,
  detectLanguage,
  fixMixedScript,
  fold,
  getLexicon,
  getScheme,
  jaroWinkler,
  mrzName,
  mrzText,
  nameKey,
  nameKeys,
  normalize,
  splitName,
  transliterate,
  variantsDetailed,
  vocalizeWord,
} from "../src/index.js";

const here = dirname(fileURLToPath(import.meta.url));
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const F: Record<string, any[]> = JSON.parse(readFileSync(join(here, "fixtures", "parity.json"), "utf8"));

function check<T extends unknown[]>(name: string, rows: T[], fn: (row: T) => [unknown, unknown]): void {
  it(`${name} (${rows.length} cases)`, () => {
    const bad: string[] = [];
    for (const row of rows) {
      const [got, want] = fn(row);
      if (JSON.stringify(got) !== JSON.stringify(want)) {
        bad.push(`${JSON.stringify(row.slice(0, 4))}\n   got:  ${JSON.stringify(got)}\n   want: ${JSON.stringify(want)}`);
      }
    }
    expect(bad.slice(0, 15).join("\n"), `${bad.length} mismatches`).toBe("");
  });
}

describe("parity with Python", () => {
  check("scheme transliteration", F.scheme as [string, string, string][], ([sid, text, out]) => [
    getScheme(sid).transliterate(text),
    out,
  ]);
  check("auto transliteration", F.auto as [string, string][], ([text, out]) => [transliterate(text), out]);
  check("language detection", F.detect as [string, string, string, number, [string, number][]][], ([t, lang, script, conf, cands]) => {
    const d = detectLanguage(t);
    return [[d.language, d.script, d.confidence, d.candidates], [lang, script, conf, cands]];
  });
  check("normalize / fixMixedScript", F.normalize as [string, string, string][], ([t, n, m]) => [
    [normalize(t), fixMixedScript(t)],
    [n, m],
  ]);
  check("fold", F.fold as [string, string, string][], ([t, a, g]) => [
    [fold(t), fold(t, { german: true })],
    [a, g],
  ]);
  check("splitName", F.split as [string, string[]][], ([t, parts]) => [splitName(t), parts]);
  check("lexicon lookup", F.lookup as [string, string[], string[], string[]][], ([t, ids, short, eq]) => {
    const lex = getLexicon();
    return [
      [lex.lookup(t).map((e) => e.id), lex.lookupShort(t).map((e) => e.id), lex.lookupEquivalents(t).map((e) => e.id)],
      [ids, short, eq],
    ];
  });
  check("nameKeys", F.keys as [string, string[]][], ([w, keys]) => [nameKeys(w), keys]);
  check("nameKey", F.name_key as [string, string][], ([t, key]) => [nameKey(t), key]);
  check("jaroWinkler", F.jaro as [string, string, number][], ([a, b, s]) => [
    Math.abs(jaroWinkler(a.toLowerCase(), b.toLowerCase()) - s) < 1e-12,
    true,
  ]);
  check("vocalizeWord", F.vocalize as [string, string | null][], ([w, v]) => [vocalizeWord(w), v]);
  check(
    "compare",
    F.compare as [string, string, boolean, number, [string, string, number, string][], string[], string[]][],
    ([a, b, useLexicon, score, pairs, ul, ur]) => {
      const r = compare(a, b, { useLexicon });
      return [
        [r.score, r.pairs.map((p) => [p.left, p.right, p.score, p.reason]), r.unmatchedLeft, r.unmatchedRight],
        [score, pairs, ul, ur],
      ];
    },
  );
  check("variants", F.variants as [string, boolean, [string, number, string[]][]][], ([t, useLexicon, vs]) => [
    variantsDetailed(t, { limit: 15, useLexicon }).map((v) => [v.text, v.score, v.sources]),
    vs,
  ]);
  check("mrzName", F.mrz as [string, string, number, "cut" | "initials", string][], ([s, g, length, strategy, out]) => [
    mrzName(s, g, { length, strategy }),
    out,
  ]);
  check("mrzText", F.mrz_text as [string, string, string][], ([t, a, g]) => [
    [mrzText(t), mrzText(t, { german: true })],
    [a, g],
  ]);
});
