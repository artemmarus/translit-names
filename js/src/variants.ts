/**
 * Generation of plausible Latin spellings of a name (port of `variants.py`).
 *
 * Sources: every applicable scheme (current passport system first), the name
 * lexicon (English, per-country spellings, attested variants) and rewrite
 * rules for systematic alternations (`-iy/-y/-ii`, `ks/x`, `ou/u` …).
 */

import RULES_FILE from "./data/variantRules.js";
import { detectLanguage, detectScript } from "./detect.js";
import type { Scheme } from "./engine.js";
import { fold } from "./fold.js";
import { getLexicon, type NameEntry } from "./lexicon.js";
import { fixMixedScript, normalize } from "./normalize.js";
import { pyRegExp, pyReplacement } from "./pyregex.js";
import { listSchemes } from "./registry.js";
import type { VariantRuleSpec } from "./types.js";
import { cmpStr, cps, isAlnum, isAlpha, isUpper1, pyIsLower, pyIsUpper, pyRound, strip } from "./unicode.js";

/** A candidate spelling with a heuristic plausibility score in (0, 1]. */
export interface Variant {
  text: string;
  score: number;
  /** Schemes and lexicon entries that produced this spelling. */
  sources: string[];
}

const ARABIC_SCRIPT_LANGS = new Set(["ar", "fa", "ur", "ps"]);
const STRIP_MARKS = /[\u2019\u201d\u02b9\u02ba\u02bb\u02bc\u02bf\u02be"`\u00b4]/gu;

const KIND_WEIGHT: Readonly<Record<string, number>> = {
  passport: 1.0, practical: 0.93, official: 0.85, geographic: 0.82, ascii: 0.85, legacy: 0.7, library: 0.6, scholarly: 0.45,
};

/** How likely a scheme's output is to appear in real-world records. */
export function schemeWeight(scheme: Scheme): number {
  let base = KIND_WEIGHT[scheme.kind] ?? 0.5;
  if (scheme.status === "superseded") base *= 0.9;
  else if (scheme.status === "draft") base *= 0.75;
  else if (scheme.status === "informal") base *= 0.97;
  return base;
}

type CompiledRule = [RegExp, string[], number];
let rulesCache: Map<string, CompiledRule[]> | null = null;

function rules(): Map<string, CompiledRule[]> {
  if (!rulesCache) {
    rulesCache = new Map();
    for (const [family, list] of Object.entries(RULES_FILE)) {
      if (!Array.isArray(list)) continue;
      rulesCache.set(
        family,
        (list as VariantRuleSpec[]).map((r) => [pyRegExp(r.pattern, "i"), r.alts.map(pyReplacement), r.weight]),
      );
    }
  }
  return rulesCache;
}

function fixWordCase(text: string): string {
  const fix = (word: string): string => {
    const w = cps(word);
    const letters = w.filter(isAlpha);
    if (letters.length > 1 && letters.every(isUpper1)) return (w[0] ?? "") + w.slice(1).join("").toLowerCase();
    if (w.length > 2 && isUpper1(w[0] as string) && isUpper1(w[1] as string) && pyIsLower(w.slice(2).join(""))) {
      return (w[0] as string) + w.slice(1).join("").toLowerCase();
    }
    return word;
  };
  return text
    .split(" ")
    .map((w) => w.split("-").map(fix).join("-"))
    .join(" ");
}

function clean(text: string, asciiOnly: boolean): string {
  let t = text.replace(STRIP_MARKS, "").split("\u0361").join("").split("\u00b7").join("");
  if (asciiOnly) {
    t = cps(fold(t))
      .filter((c) => isAlnum(c) || " -'".includes(c))
      .join("");
  }
  t = strip(t.replace(/\s+/gu, " "), " -");
  return fixWordCase(t);
}

function matchCase(template: string, text: string): string {
  if (pyIsUpper(template) && cps(template).length > 1) return text.toUpperCase();
  const first = cps(template)[0];
  if (first && pyIsUpper(first)) {
    const t = cps(text);
    return (t[0] ?? "").toUpperCase() + t.slice(1).join("");
  }
  return text;
}

const family = (language: string | null, script: string): string =>
  script === "Arab" || (language !== null && ARABIC_SCRIPT_LANGS.has(language)) ? "arabic" : "cyrillic";

interface Cand {
  text: string;
  score: number;
  sources: string[];
}

class Pool {
  private readonly items = new Map<string, { text: string; score: number; sources: Set<string> }>();
  private readonly base = new Map<string, number>();

  add(text: string, score: number, source: string): void {
    if (!text) return;
    const key = text.toLowerCase();
    const item = this.items.get(key);
    if (item) {
      item.sources.add(source);
      const base = Math.max(this.base.get(key) as number, score);
      this.base.set(key, base);
      const bonus = 0.01 * Math.min(item.sources.size - 1, 3);
      item.score = base >= 1.0 ? base : Math.min(base + bonus, 0.995);
    } else {
      this.base.set(key, score);
      this.items.set(key, { text, score, sources: new Set([source]) });
    }
  }

  ranked(): Cand[] {
    return [...this.items.values()]
      .map((v) => ({ text: v.text, score: v.score, sources: [...v.sources].sort(cmpStr) }))
      .sort((a, b) => b.score - a.score || cmpStr(a.text, b.text));
  }
}

function lexiconEntries(part: string, language: string | null): NameEntry[] {
  const lex = getLexicon();
  let found = lex.lookup(part, language);
  const low = part.toLowerCase();
  if (!found.length && (low.startsWith("al-") || low.startsWith("el-"))) found = lex.lookup(cps(part).slice(3).join(""), language);
  return found;
}

interface PartOptions {
  asciiOnly: boolean;
  includeShort: boolean;
  useLexicon: boolean;
  schemes: readonly Scheme[];
}

function partVariants(part: string, language: string | null, script: string, o: PartOptions): Cand[] {
  const pool = new Pool();
  if (script !== "Latn") {
    for (const sch of o.schemes) {
      if (sch.caseMode === "preserve") continue;
      pool.add(clean(sch.transliterate(part), o.asciiOnly), schemeWeight(sch), sch.id);
    }
  } else {
    pool.add(o.asciiOnly ? clean(part, o.asciiOnly) : part, 1.0, "input");
  }
  const langKey = language ?? "en";
  const entries = o.useLexicon ? lexiconEntries(part, language) : [];
  entries.forEach((entry, n) => {
    const damp = n === 0 ? 1.0 : 0.85;
    (entry.latin[langKey] ?? []).forEach((form, k) => {
      pool.add(clean(form, o.asciiOnly), 0.97 * damp * 0.97 ** k, `lexicon:${entry.id}`);
    });
    if (entry.english) pool.add(clean(entry.english, o.asciiOnly), 0.95 * damp, `lexicon:${entry.id}`);
    for (const [lang, forms] of Object.entries(entry.latin)) {
      if (lang === langKey) continue;
      forms.forEach((form, k) => {
        pool.add(clean(form, o.asciiOnly), 0.78 * damp * 0.97 ** k, `lexicon:${entry.id}:${lang}`);
      });
    }
    entry.variants.forEach((form, k) => {
      pool.add(clean(form, o.asciiOnly), 0.72 * damp * 0.995 ** k, `lexicon:${entry.id}`);
    });
    if (o.includeShort) {
      for (const form of entry.short) {
        if (detectScript(form) === "Latn") pool.add(clean(form, o.asciiOnly), 0.4 * damp, `lexicon:${entry.id}:short`);
      }
    }
  });

  // Rewrite rules on the strongest candidates (one or two steps).
  const all = rules();
  const ruleList = [...(all.get("all") ?? []), ...(all.get(family(language, script)) ?? [])];
  let frontier: [string, number][] = pool
    .ranked()
    .slice(0, 8)
    .map((v) => [v.text, v.score]);
  for (let depth = 0; depth < 2; depth++) {
    const next: [string, number][] = [];
    for (const [text, score] of frontier) {
      for (const [re, alts, weight] of ruleList) {
        const low = text.toLowerCase();
        if (!re.test(low)) continue;
        for (const alt of alts) {
          const replaced = clean(matchCase(text, low.replace(re, alt)), o.asciiOnly);
          if (replaced && replaced.toLowerCase() !== low) {
            const s = score * weight;
            if (s >= 0.35) {
              pool.add(replaced, s, "rule");
              next.push([replaced, s]);
            }
          }
        }
      }
    }
    frontier = next.sort((a, b) => b[1] - a[1]).slice(0, 12);
  }
  return pool.ranked();
}

const SEP_RE = /(\s+|-)/u;
const isSep = (t: string): boolean => /^(?:\s+|-)$/u.test(t);

function groupArabicPhrases(tokens: string[]): string[] {
  const lex = getLexicon();
  const out: string[] = [];
  let i = 0;
  while (i < tokens.length) {
    let joined: string | null = null;
    let used = 1;
    for (const span of [5, 3]) {
      const chunk = tokens.slice(i, i + span);
      const words = chunk.filter((_, k) => k % 2 === 0);
      const seps = chunk.filter((_, k) => k % 2 === 1);
      if (chunk.length === span && !words.some(isSep)) {
        if (seps.every((t) => /^\s+$/u.test(t)) && lex.lookupArabic(words.join(" ")).length) {
          joined = chunk.join("");
          used = span;
          break;
        }
      }
    }
    if (joined !== null) {
      out.push(joined);
      i += used;
    } else {
      out.push(tokens[i] as string);
      i++;
    }
  }
  return out;
}

export interface VariantsOptions {
  /** Language code, overrides detection (`"uk"` for a Ukrainian name without Ukrainian-only letters). */
  language?: string | null;
  /** Maximum number of spellings (default 20). */
  limit?: number;
  /** Fold to ASCII (default `true`); `false` keeps diacritics (Hüseyin). */
  asciiOnly?: boolean;
  /** Include diminutives (Sasha for Aleksandr). */
  includeShort?: boolean;
  /** Use the name lexicon (default `true`). */
  useLexicon?: boolean;
}

/** Like `variants()` but with scores and the sources of every spelling. */
export function variantsDetailed(name: string, options: VariantsOptions = {}): Variant[] {
  const limit = options.limit ?? 20;
  const asciiOnly = options.asciiOnly ?? true;
  const includeShort = options.includeShort ?? false;
  const useLexicon = options.useLexicon ?? true;
  const n = fixMixedScript(normalize(name));
  if (!n) return [];
  const script = detectScript(n);
  let language = options.language ?? null;
  if (language === null && script !== "Latn") language = detectLanguage(n).language;
  let schemes: Scheme[] = [];
  if (script !== "Latn" && language) {
    schemes = listSchemes({ language }).filter(
      (s) =>
        s.script === script &&
        s.kind !== "scholarly" &&
        (s.options["variants"] ?? true) &&
        !(s.reversible && !s.ascii), // reversible diacritic systems (ISO 9 …) fold into unrealistic spellings
    );
  }
  let tokens = n.split(SEP_RE);
  if (script === "Arab" && useLexicon) tokens = groupArabicPhrases(tokens);
  const perPart: Cand[][] = [];
  for (const tok of tokens) {
    if (!tok || isSep(tok)) {
      perPart.push([{ text: /^\s+$/u.test(tok) ? " " : tok, score: 1.0, sources: [] }]);
      continue;
    }
    const vs = partVariants(tok, language, script, { asciiOnly, includeShort, useLexicon, schemes });
    const top = vs.slice(0, Math.max(limit, 8));
    perPart.push(top.length ? top : [{ text: tok, score: 0.5, sources: [] }]);
  }

  // Best-first combination of the parts.
  let combos: [number, string, Set<string>][] = [[1.0, "", new Set()]];
  for (const options2 of perPart) {
    const next: [number, string, Set<string>][] = [];
    for (const [score, text, srcs] of combos) {
      for (const v of options2) next.push([score * v.score, text + v.text, new Set([...srcs, ...v.sources])]);
    }
    next.sort((a, b) => b[0] - a[0]);
    combos = next.slice(0, limit * 3);
  }
  const seen = new Map<string, Variant>();
  for (const [score, text0, srcs] of combos) {
    const text = text0.replace(/\s+/gu, " ").trim();
    const key = text.toLowerCase();
    if (key && !seen.has(key)) seen.set(key, { text, score: pyRound(score, 4), sources: [...srcs].sort(cmpStr) });
    if (seen.size >= limit) break;
  }
  return [...seen.values()];
}

/**
 * Plausible Latin spellings of a name, most likely first.
 *
 * ```ts
 * variants("Юрий", { limit: 4 })   // ["Iurii", "Yuri", "Yury", "Yuriy"]
 * ```
 */
export function variants(name: string, options: VariantsOptions = {}): string[] {
  return variantsDetailed(name, options).map((v) => v.text);
}
