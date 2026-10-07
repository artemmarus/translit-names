/**
 * Context-aware, rule-based transliteration engine (port of `_engine.py`).
 *
 * Matching is greedy longest-match over the lower-cased source; among rules
 * of equal length, contextual rules are tried in file order before the plain
 * `map` entry.  Output case is restored from the source, so data files only
 * describe lower-case letters.
 */

import { foldChar } from "./fold.js";
import { pyRegExp, pyReplacement } from "./pyregex.js";
import type { RuleSpec, SchemeSpec } from "./types.js";
import {
  cps,
  isAscii,
  isCased,
  isLetterOrMark,
  isMn,
  isSpace,
  isTitle1,
  isUpper1,
  lower1,
} from "./unicode.js";

/** Characters treated as word-internal when they sit between two letters. */
export const APOSTROPHES: ReadonlySet<string> = new Set([
  "'", "\u2019", "\u02bc", "\u02bb", "\u2018", "`", "\u00b4", "\u02b9", "\u02bd",
]);

const WORD_START = "^";
const WORD_END = "$";

/** `["src", text]` is transliterated by the rules, `["lit", text]` copied verbatim. */
export type Segment = ["src" | "lit", string];
export type WordHook = (scheme: Scheme, text: string) => Segment[];

export class SchemeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "SchemeError";
  }
}

const caseRelevant = (c: string): boolean => isCased(c) && cps(c.toUpperCase()).length === 1;
const isUpperish = (c: string): boolean => isUpper1(c) || isTitle1(c);

/** One substitution: `source` (lower case) becomes `target` in context. */
export interface Rule {
  readonly source: string;
  readonly sourceCps: readonly string[];
  readonly target: string;
  readonly start: boolean;
  readonly end: boolean;
  readonly after: ReadonlySet<string> | null;
  readonly notAfter: ReadonlySet<string> | null;
  readonly before: ReadonlySet<string> | null;
  readonly notBefore: ReadonlySet<string> | null;
  readonly contextual: boolean;
}

function applies(r: Rule, prev: string, nxt: string): boolean {
  if (r.start && prev !== WORD_START) return false;
  if (r.end && nxt !== WORD_END) return false;
  if (r.after && !r.after.has(prev)) return false;
  if (r.notAfter && r.notAfter.has(prev)) return false;
  if (r.before && !r.before.has(nxt)) return false;
  return !(r.notBefore && r.notBefore.has(nxt));
}

function expandSet(spec: unknown, classes: Record<string, string>, where: string): Set<string> | null {
  if (spec === undefined || spec === null) return null;
  let s: unknown = spec;
  if (Array.isArray(s)) s = s.join("");
  if (typeof s !== "string") throw new SchemeError(`${where}: context set must be a string`);
  const expanded = s.replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (_m, name: string) => {
    const cls = classes[name];
    if (cls === undefined) throw new SchemeError(`${where}: unknown class {${name}}`);
    return cls;
  });
  return new Set(cps(expanded.normalize("NFC")).map(lower1));
}

function makeRule(source: string, target: string, ctx: Partial<Omit<Rule, "source" | "sourceCps" | "target" | "contextual">> = {}): Rule {
  const r = {
    source,
    sourceCps: cps(source),
    target,
    start: ctx.start ?? false,
    end: ctx.end ?? false,
    after: ctx.after ?? null,
    notAfter: ctx.notAfter ?? null,
    before: ctx.before ?? null,
    notBefore: ctx.notBefore ?? null,
    contextual: false,
  };
  r.contextual = r.start || r.end || !!r.after || !!r.notAfter || !!r.before || !!r.notBefore;
  return r;
}

const RULE_KEYS = new Set(["from", "to", "start", "end", "after", "not_after", "before", "not_before", "note"]);

/** A compiled transliteration scheme. Obtain instances with `getScheme()`. */
export class Scheme {
  readonly spec: SchemeSpec;
  readonly id: string;
  readonly title: string;
  readonly language: string;
  readonly script: string;
  readonly kind: string;
  readonly status: string;
  readonly year: number | null;
  readonly authority: string;
  readonly description: string;
  readonly sources: readonly string[];
  readonly notes: readonly string[];
  readonly ascii: boolean;
  readonly reversible: boolean;
  readonly samples: readonly (readonly [string, string])[];
  readonly caseMode: "auto" | "preserve" | "upper" | "lower";
  readonly titlecase: boolean;
  readonly lowercaseWords: readonly string[];
  readonly geminate: string | null;
  readonly options: Readonly<Record<string, unknown>>;
  readonly fallback: "keep" | "drop" | "ascii";

  private readonly hook: WordHook | null;
  private readonly aliases: Map<string, string>;
  private readonly rulesIndex: Map<string, Rule[]>;
  private readonly post: [RegExp, string][];

  constructor(spec: SchemeSpec, hooks: Readonly<Record<string, WordHook>> = {}) {
    if (!spec.id) throw new SchemeError("scheme without 'id'");
    this.spec = spec;
    this.id = spec.id;
    this.title = spec.title ?? spec.id;
    this.language = spec.language ?? "";
    this.script = spec.script ?? "";
    this.kind = spec.kind ?? "other";
    this.status = spec.status ?? "current";
    this.year = spec.year ?? null;
    this.authority = spec.authority ?? "";
    this.description = spec.description ?? "";
    this.sources = spec.sources ?? [];
    this.notes = spec.notes ?? [];
    this.ascii = !!spec.ascii;
    this.reversible = !!spec.reversible;
    this.samples = (spec.samples ?? []).map((s) => [s[0], s[1]] as const);
    const caseMode = spec.case ?? "auto";
    if (!["auto", "preserve", "upper", "lower"].includes(caseMode)) {
      throw new SchemeError(`${this.id}: unknown case mode ${JSON.stringify(caseMode)}`);
    }
    this.caseMode = caseMode;
    this.titlecase = !!spec.titlecase;
    this.lowercaseWords = spec.lowercase_words ?? [];
    this.geminate = spec.geminate ?? null;
    this.options = spec.options ?? {};
    const fallback = spec.fallback ?? "keep";
    if (!["keep", "drop", "ascii"].includes(fallback)) {
      throw new SchemeError(`${this.id}: unknown fallback ${JSON.stringify(fallback)}`);
    }
    this.fallback = fallback;
    if (spec.hook) {
      const h = hooks[spec.hook];
      if (!h) throw new SchemeError(`${this.id}: unknown hook ${JSON.stringify(spec.hook)}`);
      this.hook = h;
    } else {
      this.hook = null;
    }
    this.aliases = this.compileAliases(spec.aliases ?? {});
    this.rulesIndex = this.compileRules(spec);
    this.post = (spec.post ?? []).map((p) => [pyRegExp(p.pattern, "g"), pyReplacement(p.replace)]);
  }

  private compileAliases(aliases: Record<string, string | null>): Map<string, string> {
    const table = new Map<string, string>();
    for (const [k0, v0] of Object.entries(aliases)) {
      if (v0 === null) continue;
      const k = k0.normalize("NFC");
      const v = v0.normalize("NFC");
      table.set(k, v);
      const up = k.toUpperCase();
      if (up !== k && cps(up).length === cps(k).length && !(up in aliases)) table.set(up, v.toUpperCase());
    }
    return table;
  }

  private compileRules(spec: SchemeSpec): Map<string, Rule[]> {
    const classes: Record<string, string> = {};
    for (const [k, v] of Object.entries(spec.classes ?? {})) classes[k] = v.normalize("NFC");
    const ordered: [number, number, Rule][] = [];
    (spec.rules ?? []).forEach((raw: RuleSpec, n: number) => {
      const where = `${this.id}: rules[${n}]`;
      if (raw.from === undefined || raw.to === undefined) throw new SchemeError(`${where}: needs 'from' and 'to'`);
      const unknown = Object.keys(raw).filter((k) => !RULE_KEYS.has(k));
      if (unknown.length) throw new SchemeError(`${where}: unknown keys ${JSON.stringify(unknown.sort())}`);
      const sources = Array.isArray(raw.from) ? raw.from : [raw.from];
      for (const s of sources) {
        const src = cps(s.normalize("NFC")).map(lower1).join("");
        if (!src) throw new SchemeError(`${where}: empty 'from'`);
        const rule = makeRule(src, raw.to.normalize("NFC"), {
          start: !!raw.start,
          end: !!raw.end,
          after: expandSet(raw.after, classes, where),
          notAfter: expandSet(raw.not_after, classes, where),
          before: expandSet(raw.before, classes, where),
          notBefore: expandSet(raw.not_before, classes, where),
        });
        ordered.push([-cps(src).length, n, rule]);
      }
    });
    const base = ordered.length + 1;
    Object.entries(spec.map ?? {}).forEach(([s, t], n) => {
      if (t === null) return;
      const src = cps(s.normalize("NFC")).map(lower1).join("");
      if (!src) throw new SchemeError(`${this.id}: empty key in map`);
      ordered.push([-cps(src).length, base + n, makeRule(src, t.normalize("NFC"))]);
    });
    ordered.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const index = new Map<string, Rule[]>();
    for (const [, , rule] of ordered) {
      const first = rule.sourceCps[0] as string;
      const list = index.get(first);
      if (list) list.push(rule);
      else index.set(first, [rule]);
    }
    return index;
  }

  /** Single source characters this scheme knows how to transliterate. */
  get alphabet(): Set<string> {
    const out = new Set<string>();
    for (const rules of this.rulesIndex.values()) for (const r of rules) if (r.sourceCps.length === 1) out.add(r.source);
    return out;
  }

  /** All compiled rules (contextual rules and map entries). */
  rules(): Rule[] {
    return [...this.rulesIndex.values()].flat();
  }

  toString(): string {
    return `<Scheme ${this.id}: ${this.title}>`;
  }

  preprocess(text: string): string {
    let t = text.normalize("NFC");
    if (this.aliases.size) t = cps(t).map((c) => this.aliases.get(c) ?? c).join("");
    if (this.geminate) t = this.moveGeminationMarks(t);
    return t;
  }

  /** Transliterate `text` with this scheme. */
  transliterate(text: string): string {
    const t = this.preprocess(text);
    const allCaps = textIsAllCaps(t);
    let out: string;
    if (this.hook) {
      out = this.hook(this, t)
        .map(([kind, s]) => (kind === "src" ? this.apply(this.preprocess(s), allCaps) : s))
        .join("");
    } else {
      out = this.apply(t, allCaps);
    }
    for (const [re, repl] of this.post) out = out.replace(re, repl);
    out = out.normalize("NFC");
    if (this.titlecase) out = titlecaseName(out, this.lowercaseWords);
    if (this.caseMode === "upper") out = out.toUpperCase();
    else if (this.caseMode === "lower") out = out.toLowerCase();
    return out;
  }

  private moveGeminationMarks(text: string): string {
    const g = this.geminate as string;
    const chars = cps(text);
    let i = 0;
    while (i < chars.length) {
      if (isMn(chars[i] as string)) {
        let j = i;
        while (j < chars.length && isMn(chars[j] as string)) j++;
        const run = chars.slice(i, j);
        if (run.includes(g)) {
          const gs = run.filter((c) => c === g);
          const rest = run.filter((c) => c !== g);
          chars.splice(i, j - i, ...gs, ...rest);
        }
        i = j;
      } else {
        i++;
      }
    }
    return chars.join("");
  }

  private apply(text: string, textAllCaps: boolean): string {
    if (!text) return "";
    const src = cps(text);
    const low = src.map(lower1);
    const n = src.length;
    const wordCaps = wordCapsMap(src, textAllCaps);
    let out = "";
    let lastLetterTarget = "";
    let i = 0;
    while (i < n) {
      const ch = low[i] as string;
      if (this.geminate && ch === this.geminate) {
        out += lastLetterTarget;
        i++;
        continue;
      }
      const prev = contextPrev(low, i);
      let matched: Rule | null = null;
      for (const rule of this.rulesIndex.get(ch) ?? []) {
        const len = rule.sourceCps.length;
        if (i + len > n) continue;
        let ok = true;
        for (let k = 0; k < len; k++) {
          if (low[i + k] !== rule.sourceCps[k]) {
            ok = false;
            break;
          }
        }
        if (!ok) continue;
        if (rule.contextual && !applies(rule, prev, contextNext(low, i + len))) continue;
        matched = rule;
        break;
      }
      if (!matched) {
        out += this.fallbackChar(src[i] as string);
        i++;
        continue;
      }
      const j = i + matched.sourceCps.length;
      let target = matched.target;
      if (target) {
        if (this.caseMode === "auto") target = recase(src.slice(i, j), target, wordCaps[i] as boolean);
        out += target;
        if (isLetterOrMark(src[i] as string)) lastLetterTarget = matched.target;
      }
      i = j;
    }
    return out;
  }

  private fallbackChar(ch: string): string {
    if (this.fallback === "keep" || isSpace(ch) || isAscii(ch)) return ch;
    if (this.fallback === "drop") return "";
    return foldChar(ch);
  }
}

function contextPrev(low: readonly string[], i: number): string {
  if (i === 0) return WORD_START;
  const p = low[i - 1] as string;
  if (isLetterOrMark(p)) return p;
  if (APOSTROPHES.has(p) && i >= 2 && isLetterOrMark(low[i - 2] as string)) return p;
  return WORD_START;
}

function contextNext(low: readonly string[], j: number): string {
  if (j >= low.length) return WORD_END;
  const c = low[j] as string;
  if (isLetterOrMark(c)) return c;
  if (APOSTROPHES.has(c) && j + 1 < low.length && isLetterOrMark(low[j + 1] as string)) return c;
  return WORD_END;
}

function textIsAllCaps(text: string): boolean {
  const cased = cps(text).filter((c) => isCased(c) && caseRelevant(c));
  return cased.length >= 2 && cased.every(isUpper1);
}

function wordCapsMap(src: readonly string[], textAllCaps: boolean): boolean[] {
  const n = src.length;
  const result: boolean[] = new Array(n).fill(false);
  const inWord = (c: string): boolean => isLetterOrMark(c) || APOSTROPHES.has(c);
  let i = 0;
  while (i < n) {
    if (!inWord(src[i] as string)) {
      i++;
      continue;
    }
    let j = i;
    while (j < n && inWord(src[j] as string)) j++;
    const cased = src.slice(i, j).filter((c) => isCased(c) && caseRelevant(c));
    const caps = cased.every(isUpper1) && (cased.length >= 2 || (cased.length === 1 && textAllCaps));
    for (let k = i; k < j; k++) result[k] = caps;
    i = j;
  }
  return result;
}

function recase(source: readonly string[], target: string, wordIsCaps: boolean): string {
  const first = source.find(isCased);
  if (first === undefined) return target;
  if (wordIsCaps && !caseRelevant(first)) return target.toUpperCase(); // ß inside GROß
  if (!isUpperish(first)) return target;
  const cased = source.filter(caseRelevant);
  if (wordIsCaps || (cased.length >= 2 && cased.every(isUpper1))) return target.toUpperCase();
  return capitalizeFirst(target);
}

/** Upper-case the first cased character. */
export function capitalizeFirst(s: string): string {
  const arr = cps(s);
  for (let k = 0; k < arr.length; k++) {
    const c = arr[k] as string;
    if (isCased(c)) return arr.slice(0, k).join("") + c.toUpperCase() + arr.slice(k + 1).join("");
  }
  return s;
}

/**
 * Capitalise each name part of a romanisation made from an uncased script.
 * Entries of `lowercaseWords` ending in `-` are prefixes (`"al-"`).
 */
export function titlecaseName(text: string, lowercaseWords: readonly string[] = []): string {
  const prefixes = lowercaseWords.filter((w) => w.endsWith("-")).sort((a, b) => cps(b).length - cps(a).length);
  const words = new Set(lowercaseWords.filter((w) => !w.endsWith("-")));
  let first = true;
  const fixPart = (part: string, isFirst: boolean): string => {
    const low = part.toLowerCase();
    for (const p of prefixes) {
      if (low.startsWith(p) && cps(part).length > cps(p).length) {
        const arr = cps(part);
        const plen = cps(p).length;
        let head = arr.slice(0, plen).join("");
        head = isFirst ? capitalizeFirst(head) : head;
        return head + capitalizeFirst(arr.slice(plen).join(""));
      }
    }
    if (!isFirst && words.has(low)) return part;
    return capitalizeFirst(part);
  };
  return text.replace(/[^\s]+/gu, (token) => {
    const pieces = token.split("-");
    let fixed: string;
    if (pieces.length > 1 && prefixes.some((p) => token.toLowerCase().startsWith(p))) {
      fixed = fixPart(token, first);
    } else {
      fixed = pieces.map((p, k) => (p ? fixPart(p, first && k === 0) : p)).join("-");
    }
    first = false;
    return fixed;
  });
}
