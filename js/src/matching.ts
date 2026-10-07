/**
 * Cross-script, transliteration-aware comparison of personal names (port of `matching.py`).
 *
 * Signals: lexicon clusters (Магомед = محمد = Mohammed = Mehmet), skeleton
 * keys that fold transliteration alternations (kh/h/x/g, sh/ch/sch/sz,
 * zh/j/dj, ks/x, -iy/-ii/-y, al-/el-/ul-, -uddin/-eddine …) and
 * Jaro–Winkler similarity.  Multi-part names are aligned in the best order.
 */

import { detectLanguage, detectScript } from "./detect.js";
import { fold } from "./fold.js";
import { getLexicon } from "./lexicon.js";
import { fixMixedScript, normalize } from "./normalize.js";
import { resolveScheme } from "./translit.js";
import { cps, isAlpha, pyRound } from "./unicode.js";

/** Name particles ignored when aligning name parts. */
export const PARTICLES: ReadonlySet<string> = new Set([
  "al", "el", "ul", "al-", "el-", "ad", "ar", "as", "ash", "at", "az", "an", "ad-", "ud", "ud-",
  "bin", "ibn", "ben", "bint", "binti", "bte", "bt", "b", "von", "van", "der", "de", "da", "di", "du",
  "la", "le", "dos", "das", "del", "oglu", "ogly", "ugli", "uly", "uulu", "ogli", "kizi", "kyzy", "qizi",
  "gyzy", "kizy", "ogh", "kyzi",
]);

const PHONETIC_FOLD: Readonly<Record<string, string>> = {
  č: "ch", ć: "ch", ç: "ch", ĉ: "ch", š: "sh", ś: "sh", ş: "sh", ș: "sh", ŝ: "shch", ž: "zh", ź: "zh", ż: "zh",
  đ: "dj", ǆ: "dzh", ǉ: "lj", ǌ: "nj", ğ: "gh", ġ: "gh", ı: "i", ə: "a", ä: "a", ö: "o", ü: "u", ł: "l",
  ř: "rzh", ñ: "n", ň: "n", ŋ: "ng", ß: "ss", þ: "th", ð: "d", ø: "o", æ: "ae", œ: "oe", ẖ: "kh", ḫ: "kh",
  ḥ: "h", ṣ: "s", ṭ: "t", ḍ: "d", ẓ: "z", ẕ: "z", ṯ: "th", ḏ: "dh",
};
const DROP_MARKS = new Set(["'", "\u2019", "\u02bc", "\u02bb", "\u2018", "`", "\u00b4", "\u02b9", "\u02ba", "\u02bf", "\u02be", '"']);
const VOWELS = new Set(["a", "e", "i", "o", "u", "y"]);

/** Bring a name to lower-case ASCII Latin suitable for keys and comparison. */
export function toMatchLatin(name: string, language?: string | null): string {
  let n = fixMixedScript(normalize(name));
  const script = detectScript(n);
  if (script !== "Latn" && script !== "Zyyy") {
    const sch = resolveScheme(n, null, { language: language ?? null, purpose: "match" });
    if (sch) n = sch.transliterate(n);
  }
  n = n.normalize("NFC").toLowerCase();
  n = cps(n)
    .map((c) => PHONETIC_FOLD[c] ?? c)
    .join("");
  n = cps(n)
    .filter((c) => !DROP_MARKS.has(c))
    .join("");
  return fold(n).toLowerCase();
}

const GRAPHEMES: readonly [string, readonly string[]][] = [
  ["schtsch", ["X"]], ["shtsh", ["X"]], ["chtch", ["X"]], ["shch", ["X"]], ["szcz", ["X"]], ["tsch", ["X"]],
  ["dzsh", ["J"]], ["dzh", ["J"]], ["dsch", ["J"]], ["sch", ["X"]], ["tch", ["X"]], ["sht", ["XT"]],
  ["kh", ["H"]], ["gh", ["H"]], ["zh", ["J"]], ["dj", ["J"]], ["dz", ["J", "DZ"]], ["dg", ["J"]],
  ["sh", ["X"]], ["sz", ["X"]], ["cz", ["X"]], ["ch", ["X", "H"]], ["ph", ["F"]], ["th", ["S", "T"]],
  ["dh", ["Z", "D"]], ["ts", ["C"]], ["tz", ["C"]], ["tc", ["C"]], ["ck", ["K"]], ["qu", ["K"]], ["gu", ["H"]],
  ["ks", ["KS"]], ["cs", ["KS"]], ["x", ["KS", "H"]], ["q", ["K"]], ["k", ["K"]], ["c", ["K", "C"]],
  ["g", ["H"]], ["h", ["H"]], ["w", ["V"]], ["v", ["V"]], ["j", ["J", ""]], ["z", ["Z"]], ["s", ["S"]],
  ["f", ["F"]], ["b", ["B"]], ["p", ["P"]], ["d", ["D"]], ["t", ["T"]], ["l", ["L"]], ["r", ["R"]],
  ["m", ["M"]], ["n", ["N"]],
];
const escapeRe = (s: string): string => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const GRAPHEME_RE = new RegExp(`${GRAPHEMES.map(([p]) => escapeRe(p)).join("|")}|[aeiouy]|.`, "gu");
const GRAPHEME_ALTS = new Map(GRAPHEMES);

const ARABIC_COMPOUND: readonly [RegExp, string][] = [
  [/^abd(?:ul|ol|al|el|il|ur|ar|ad|ud|as|us|ash|ush|an|un|az|uz|at|ut|u|e|o)?(?=[^aeiou])/u, "abd"],
  [/(?<=[a-z]{3})(?:ud|ad|ed|id|od|al|el|ul|ol)-?din(?:e)?$/u, "din"],
  [/(?:ul|ol|al|el|il|u)?lah?$/u, "lah"],
];
const ENDINGS: readonly [RegExp, string][] = [
  [/(?:iyy|iy|ij|ii|yi|yy|ie)$/u, "i"],
  [/(?<=[aeiou])h$/u, ""],
  [/(?<=[^aeiou])y$/u, "i"],
  [/^(?:ye|je|ie|yo|jo|io|ё)(?=[^aeiou])/u, "e"],
];

type G = readonly string[];

function wordGraphemes(word0: string): G[] {
  let word = word0;
  for (const [re, repl] of ARABIC_COMPOUND) if (cps(word).length > 5) word = word.replace(re, repl);
  for (const [re, repl] of ENDINGS) word = word.replace(re, repl);
  const out: G[] = [];
  let pos = 0;
  for (const m of word.matchAll(GRAPHEME_RE)) {
    const g = m[0];
    if (VOWELS.has(g)) out.push(["_"]);
    else {
      const alts = GRAPHEME_ALTS.get(g);
      if (alts) out.push(g === "j" && pos === 0 ? ["Y", "J"] : alts);
    }
    pos = (m.index as number) + g.length;
  }
  const w = cps(word);
  if (out.length >= 2 && "yi".includes(w[0] ?? "") && "aou".includes(w[1] ?? "")) out[0] = ["Y"];
  return out;
}

function render(choice: readonly string[]): string {
  let key = "";
  choice.forEach((tok, k) => {
    if (tok === "_") {
      if (k === 0) key += "A";
      return;
    }
    key += tok;
  });
  key = key.replace(/(.)\1+/gu, "$1");
  if (key.length > 1 && key.endsWith("D")) key = `${key.slice(0, -1)}T`;
  return key;
}

const onlyAlpha = (s: string): string => cps(s).filter(isAlpha).join("");

/**
 * Skeleton keys of one name part (several when letters are ambiguous),
 * sorted.  `nameKeys("Mohammed")` → `["MHMT"]`.
 */
export function nameKeys(word: string, language?: string | null, maxKeys = 8): string[] {
  const latin = onlyAlpha(toMatchLatin(word, language));
  if (!latin) return [];
  const graphemes = wordGraphemes(latin);
  const ambiguous = graphemes.map((g, i) => (g.length > 1 ? i : -1)).filter((i) => i >= 0).slice(0, 3);
  const primary = graphemes.map((g) => g[0] as string);
  const keys: string[] = [render(primary)];
  // itertools.product: the last position varies fastest
  const pools = ambiguous.map((i) => graphemes[i] as G);
  const idx = pools.map(() => 0);
  outer: while (true) {
    const choice = [...primary];
    ambiguous.forEach((pos, k) => {
      choice[pos] = (pools[k] as G)[idx[k] as number] as string;
    });
    const key = render(choice);
    if (!keys.includes(key)) keys.push(key);
    if (keys.length >= maxKeys) break;
    let k = pools.length - 1;
    while (k >= 0) {
      idx[k] = (idx[k] as number) + 1;
      if ((idx[k] as number) < (pools[k] as G).length) continue outer;
      idx[k] = 0;
      k--;
    }
    break;
  }
  return [...new Set(keys.filter(Boolean))].sort();
}

/** Split a full name into parts on spaces, commas and hyphens (`al-Rashid` stays one part). */
export function splitName(name: string): string[] {
  const parts: string[] = [];
  for (const chunk of normalize(name).split(/[\s,;/]+/u)) {
    if (!chunk) continue;
    if (/^(al|el|ul|ad|ar|as|ash|at|az|an|ud)-/u.test(chunk.toLowerCase())) {
      parts.push(chunk);
      continue;
    }
    parts.push(...chunk.split("-").filter(Boolean));
  }
  return parts;
}

/** Primary skeleton key of a whole name (parts sorted, particles dropped) — a blocking key. */
export function nameKey(name: string, language?: string | null): string {
  const keys: string[] = [];
  for (const p of splitName(name)) {
    if (PARTICLES.has(p.toLowerCase())) continue;
    const latin = onlyAlpha(toMatchLatin(p, language));
    if (latin) keys.push(render(wordGraphemes(latin).map((g) => g[0] as string)));
  }
  return keys.filter(Boolean).sort().join(" ");
}

/** Jaro–Winkler similarity in [0, 1] (prefix bonus up to 4 characters). */
export function jaroWinkler(a: string, b: string, prefixWeight = 0.1): number {
  if (a === b) return a ? 1.0 : 0.0;
  if (!a || !b) return 0.0;
  const A = cps(a);
  const B = cps(b);
  const la = A.length;
  const lb = B.length;
  const window = Math.max(0, Math.floor(Math.max(la, lb) / 2) - 1);
  const ma = new Array<boolean>(la).fill(false);
  const mb = new Array<boolean>(lb).fill(false);
  let matches = 0;
  for (let i = 0; i < la; i++) {
    const lo = Math.max(0, i - window);
    const hi = Math.min(lb, i + window + 1);
    for (let j = lo; j < hi; j++) {
      if (!mb[j] && B[j] === A[i]) {
        ma[i] = mb[j] = true;
        matches++;
        break;
      }
    }
  }
  if (!matches) return 0.0;
  let t = 0;
  let j = 0;
  for (let i = 0; i < la; i++) {
    if (ma[i]) {
      while (!mb[j]) j++;
      if (A[i] !== B[j]) t++;
      j++;
    }
  }
  const jaro = (matches / la + matches / lb + (matches - t / 2) / matches) / 3;
  let prefix = 0;
  for (let k = 0; k < Math.min(4, la, lb); k++) {
    if (A[k] !== B[k]) break;
    prefix++;
  }
  return jaro + prefix * prefixWeight * (1 - jaro);
}

/** One aligned pair of name parts. */
export interface PartMatch {
  left: string;
  right: string;
  score: number;
  /** exact, same-name, diminutive, equivalent, skeleton, skeleton-coarse, fuzzy, initial, initial-mismatch, different-names */
  reason: string;
}

/** Detailed outcome of `compare()`. */
export interface MatchResult {
  score: number;
  pairs: PartMatch[];
  unmatchedLeft: string[];
  unmatchedRight: string[];
}

interface Part {
  raw: string;
  latin: string;
  keys: ReadonlySet<string>;
  clusters: ReadonlySet<string>;
  shortClusters: ReadonlySet<string>;
  equivClusters: ReadonlySet<string>;
  initial: boolean;
}

const EMPTY: ReadonlySet<string> = new Set();
const intersects = (a: ReadonlySet<string>, b: ReadonlySet<string>): boolean => {
  for (const x of a) if (b.has(x)) return true;
  return false;
};

function clustersOf(part: string, language: string | null): [Set<string>, Set<string>, Set<string>] {
  const lex = getLexicon();
  let found = lex.lookup(part, language);
  if (!found.length && part.includes("-")) found = lex.lookup(part.slice(part.indexOf("-") + 1), language);
  return [
    new Set(found.map((e) => e.id)),
    new Set(lex.lookupShort(part).map((e) => e.id)),
    new Set(lex.lookupEquivalents(part).map((e) => e.id)),
  ];
}

const ARTICLE_PREFIX = /^(al|el|ul|ad|ar|as|ash|at|az|an|ud)-/u;

function prepare(name: string, language0: string | null, useLexicon: boolean): Part[] {
  let language = language0;
  const script = detectScript(name);
  if (language === null && script !== "Latn" && script !== "Zyyy") language = detectLanguage(name).language;
  const parts: Part[] = [];
  for (const raw of splitName(name)) {
    let bare = raw.replace(/\.+$/u, "");
    if (PARTICLES.has(bare.toLowerCase())) continue;
    if (ARTICLE_PREFIX.test(bare.toLowerCase())) bare = bare.slice(bare.indexOf("-") + 1);
    const latin = onlyAlpha(toMatchLatin(bare, language));
    if (!latin || PARTICLES.has(latin)) continue;
    const initial = cps(latin).length === 1 || (raw.endsWith(".") && cps(latin).length <= 3);
    const lookup = useLexicon && !initial;
    const [clusters, shortClusters, equivClusters] = lookup ? clustersOf(bare, language) : [EMPTY, EMPTY, EMPTY];
    parts.push({
      raw,
      latin,
      keys: initial ? EMPTY : new Set(nameKeys(bare, language)),
      clusters,
      shortClusters,
      equivClusters,
      initial,
    });
  }
  return parts;
}

const COARSE: Readonly<Record<string, string>> = { Z: "S", C: "S", X: "S", J: "S", F: "V", P: "B", D: "T" };
const coarse = (key: string): string =>
  cps(key)
    .map((c) => COARSE[c] ?? c)
    .join("")
    .replace(/(.)\1+/gu, "$1");

function partScore(a: Part, b: Part): [number, string] {
  if (a.initial || b.initial) return a.latin.slice(0, 1) === b.latin.slice(0, 1) ? [0.85, "initial"] : [0.0, "initial-mismatch"];
  if (a.latin === b.latin) return [1.0, "exact"];
  if (a.clusters.size && b.clusters.size && intersects(a.clusters, b.clusters)) return [0.98, "same-name"];
  if (intersects(a.shortClusters, b.clusters) || intersects(b.shortClusters, a.clusters)) return [0.86, "diminutive"];
  if (intersects(a.equivClusters, b.clusters) || intersects(b.equivClusters, a.clusters)) return [0.8, "equivalent"];
  const jw = jaroWinkler(a.latin, b.latin);
  let score: number;
  let reason: string;
  if (intersects(a.keys, b.keys)) {
    score = 0.9 + 0.08 * jw;
    reason = "skeleton";
  } else if (intersects(new Set([...a.keys].map(coarse)), new Set([...b.keys].map(coarse)))) {
    score = 0.85 + 0.1 * jw;
    reason = "skeleton-coarse";
  } else {
    let keyJw = 0.0;
    for (const x of a.keys) for (const y of b.keys) keyJw = Math.max(keyJw, jaroWinkler(x, y));
    score = Math.max(jw * 0.95, keyJw * 0.9);
    reason = "fuzzy";
  }
  if (a.clusters.size && b.clusters.size && !intersects(a.clusters, b.clusters)) {
    score = Math.min(score, 0.6); // both known names, but different ones (Hasan ≠ Husayn)
    reason = "different-names";
  }
  return [score, reason];
}

function merged(parts: readonly Part[], language: string | null, useLexicon: boolean): Part[][] {
  const out: Part[][] = [];
  for (let k = 0; k < parts.length - 1; k++) {
    const a = parts[k] as Part;
    const b = parts[k + 1] as Part;
    if (a.initial || b.initial) continue;
    const joined = prepare((a.raw + b.raw).replace(/[-\s]/gu, ""), language, useLexicon);
    if (joined.length !== 1) continue;
    let part = joined[0] as Part;
    if (useLexicon) {
      const [spaced] = clustersOf(`${a.raw} ${b.raw}`, language);
      if (spaced.size) part = { ...part, clusters: new Set([...part.clusters, ...spaced]) };
    }
    out.push([...parts.slice(0, k), part, ...parts.slice(k + 2)]);
  }
  return out;
}

function* permutations(n: number, k: number): Generator<number[]> {
  // itertools.permutations(range(n), k) in lexicographic order
  const used = new Array<boolean>(n).fill(false);
  const cur: number[] = [];
  function* rec(): Generator<number[]> {
    if (cur.length === k) {
      yield [...cur];
      return;
    }
    for (let i = 0; i < n; i++) {
      if (used[i]) continue;
      used[i] = true;
      cur.push(i);
      yield* rec();
      cur.pop();
      used[i] = false;
    }
  }
  yield* rec();
}

function compareParts(pa: Part[], pb: Part[]): [number, MatchResult] {
  const swap = pa.length > pb.length;
  const [small, big] = swap ? [pb, pa] : [pa, pb];
  const matrix = small.map((x) => big.map((y) => partScore(x, y)));
  const cell = (i: number, j: number): [number, string] => (matrix[i] as [number, string][])[j] as [number, string];
  let bestTotal = -1.0;
  let bestPerm: number[] = [];
  if (big.length <= 7) {
    for (const perm of permutations(big.length, small.length)) {
      let total = 0;
      perm.forEach((j, i) => {
        total += cell(i, j)[0];
      });
      if (total > bestTotal) {
        bestTotal = total;
        bestPerm = perm;
      }
    }
  } else {
    const used = new Set<number>();
    for (let i = 0; i < small.length; i++) {
      let bestJ = -1;
      for (let j = 0; j < big.length; j++) {
        if (used.has(j)) continue;
        if (bestJ < 0 || cell(i, j)[0] > cell(i, bestJ)[0]) bestJ = j;
      }
      used.add(bestJ);
      bestPerm.push(bestJ);
    }
  }
  const pairs: PartMatch[] = bestPerm.map((j, i) => {
    const [s, reason] = cell(i, j);
    const [left, right] = swap ? [big[j] as Part, small[i] as Part] : [small[i] as Part, big[j] as Part];
    return { left: left.raw, right: right.raw, score: pyRound(s, 4), reason };
  });
  const extra = big.filter((_, j) => !bestPerm.includes(j));
  const weights = small.map((p) => Math.max(cps(p.latin).length, 3));
  let num = 0;
  bestPerm.forEach((j, i) => {
    num += cell(i, j)[0] * (weights[i] as number);
  });
  let score = num / weights.reduce((a, b) => a + b, 0);
  score *= 1 - Math.min(0.15, 0.04 * extra.length);
  const unmatched = extra.map((p) => p.raw);
  return [
    score,
    {
      score: pyRound(score, 4),
      pairs,
      unmatchedLeft: swap ? unmatched : [],
      unmatchedRight: swap ? [] : unmatched,
    },
  ];
}

export interface CompareOptions {
  languageA?: string | null;
  languageB?: string | null;
  /** Use the name lexicon (default `true`); `false` relies on keys and string similarity only. */
  useLexicon?: boolean;
}

/**
 * Compare two full names; parts are aligned in the best order, missing
 * patronymics/middle names cost little, adjacent parts may be joined
 * (`Abd al-Rahman` ~ `Abdulrahman`).
 */
export function compare(a: string, b: string, options: CompareOptions = {}): MatchResult {
  const useLexicon = options.useLexicon ?? true;
  const pa = prepare(a, options.languageA ?? null, useLexicon);
  const pb = prepare(b, options.languageB ?? null, useLexicon);
  if (!pa.length || !pb.length) return { score: 0.0, pairs: [], unmatchedLeft: [], unmatchedRight: [] };
  let [bestRaw, best] = compareParts(pa, pb);
  if (pa.length !== pb.length && bestRaw < 0.97) {
    const longerIsA = pa.length > pb.length;
    const lang = (longerIsA ? options.languageA : options.languageB) ?? null;
    for (const alt of merged(longerIsA ? pa : pb, lang, useLexicon)) {
      const [raw, res] = longerIsA ? compareParts(alt, pb) : compareParts(pa, alt);
      if (raw > bestRaw) {
        bestRaw = raw;
        best = res;
      }
    }
  }
  return best;
}

/** Similarity of two names in [0, 1], across scripts and spellings. */
export function similarity(a: string, b: string, options: CompareOptions = {}): number {
  return compare(a, b, options).score;
}

/** `true` if `similarity()` is at least `threshold` (default 0.88). */
export function isMatch(a: string, b: string, options: CompareOptions & { threshold?: number } = {}): boolean {
  return similarity(a, b, options) >= (options.threshold ?? 0.88);
}
