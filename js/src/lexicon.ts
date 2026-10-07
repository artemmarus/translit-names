/** Name lexicon: clusters of spellings of the same personal name (port of `lexicon.py`). */

import { detectScript } from "./detect.js";
import { arabicKey, latinKey } from "./normalize.js";
import type { LexiconFile, NameSpec } from "./types.js";

/** One name cluster. */
export interface NameEntry {
  readonly id: string;
  readonly kind: string;
  readonly gender: string;
  readonly origin: string;
  readonly english: string;
  readonly native: Readonly<Record<string, readonly string[]>>;
  readonly latin: Readonly<Record<string, readonly string[]>>;
  readonly variants: readonly string[];
  readonly equivalents: readonly string[];
  readonly short: readonly string[];
  readonly vocalized: string;
  readonly related: readonly string[];
  readonly source: string;
}

const arr = (v: string | string[] | undefined | null): string[] => (v == null ? [] : typeof v === "string" ? [v] : [...v]);
const uniq = (xs: readonly string[]): string[] => [...new Set(xs)];

function toEntry(raw: NameSpec, source: string): NameEntry {
  const mapOf = (m?: Record<string, string | string[]>): Record<string, string[]> =>
    Object.fromEntries(Object.entries(m ?? {}).map(([k, v]) => [k, arr(v)]));
  return {
    id: raw.id,
    kind: raw.kind ?? "given",
    gender: raw.gender ?? "u",
    origin: raw.origin ?? "",
    english: raw.english ?? "",
    native: mapOf(raw.native),
    latin: mapOf(raw.latin),
    variants: arr(raw.variants),
    equivalents: arr(raw.equivalents),
    short: arr(raw.short),
    vocalized: (raw.vocalized ?? "").normalize("NFC"),
    related: arr(raw.related),
    source,
  };
}

function merge(a: NameEntry, b: NameEntry): NameEntry {
  const mergeMap = (x: Readonly<Record<string, readonly string[]>>, y: Readonly<Record<string, readonly string[]>>) => {
    const out: Record<string, string[]> = {};
    for (const [k, v] of Object.entries(x)) out[k] = [...v];
    for (const [k, v] of Object.entries(y)) out[k] = uniq([...(out[k] ?? []), ...v]);
    return out;
  };
  return {
    id: a.id,
    kind: a.kind,
    gender: a.gender !== "u" ? a.gender : b.gender,
    origin: a.origin || b.origin,
    english: a.english || b.english,
    native: mergeMap(a.native, b.native),
    latin: mergeMap(a.latin, b.latin),
    variants: uniq([...a.variants, ...b.variants]),
    equivalents: uniq([...a.equivalents, ...b.equivalents]),
    short: uniq([...a.short, ...b.short]),
    vocalized: a.vocalized || b.vocalized,
    related: uniq([...a.related, ...b.related]),
    source: a.source,
  };
}

/**
 * First conventional Latin spelling for the first matching language key
 * (`"ar_eg"` falls back to `"ar"`, `"en"` means the English form).
 */
export function latinFor(entry: NameEntry, languages: readonly string[]): string | null {
  for (const lang of languages) {
    if (lang === "en" && entry.english) return entry.english;
    for (const key of [lang, lang.split("_")[0] as string]) {
      const forms = entry.latin[key];
      if (forms && forms.length) return forms[0] as string;
    }
  }
  return null;
}

/** Every Latin spelling of a cluster, most canonical first. */
export function allLatin(entry: NameEntry): string[] {
  const seen = new Set<string>();
  if (entry.english) seen.add(entry.english);
  for (const forms of Object.values(entry.latin)) for (const f of forms) seen.add(f);
  for (const f of entry.variants) seen.add(f);
  return [...seen];
}

/** Every native-script spelling of a cluster. */
export function allNative(entry: NameEntry): string[] {
  const seen = new Set<string>();
  for (const forms of Object.values(entry.native)) for (const f of forms) seen.add(f);
  return [...seen];
}

const nativeKey = (text: string): string => text.normalize("NFC").trim().toLowerCase().split("ё").join("е");
const isArabicScript = (text: string): boolean =>
  Array.from(text).some((c) => (c >= "\u0600" && c <= "ۿ") || (c >= "ݐ" && c <= "ݿ"));

function push<T>(map: Map<string, T[]>, key: string, value: T): void {
  const list = map.get(key);
  if (list) list.push(value);
  else map.set(key, [value]);
}

function pushUnique(map: Map<string, NameEntry[]>, key: string, e: NameEntry): void {
  const list = map.get(key);
  if (!list) map.set(key, [e]);
  else if (!list.includes(e)) list.push(e);
}

function rank(hits: readonly [string, NameEntry][], language?: string | null): NameEntry[] {
  const seen = new Map<string, NameEntry>();
  if (language) for (const [lang, e] of hits) if (lang === language && !seen.has(e.id)) seen.set(e.id, e);
  for (const [, e] of hits) if (!seen.has(e.id)) seen.set(e.id, e);
  return [...seen.values()];
}

/** In-memory index over name entries. */
export class Lexicon implements Iterable<NameEntry> {
  readonly entries = new Map<string, NameEntry>();
  private readonly nativeIdx = new Map<string, [string, NameEntry][]>();
  private readonly arabicIdx = new Map<string, [string, NameEntry][]>();
  private readonly latinIdx = new Map<string, NameEntry[]>();
  private readonly shortIdx = new Map<string, NameEntry[]>();
  private readonly equivIdx = new Map<string, NameEntry[]>();

  constructor(entries: Iterable<NameEntry>) {
    for (const e of entries) {
      const prev = this.entries.get(e.id);
      this.entries.set(e.id, prev ? merge(prev, e) : e);
    }
    for (const e of this.entries.values()) this.index(e);
  }

  /** Build a lexicon from the JSON files' contents. */
  static fromFiles(files: readonly LexiconFile[]): Lexicon {
    const entries: NameEntry[] = [];
    for (const f of [...files].sort((a, b) => (a.file < b.file ? -1 : a.file > b.file ? 1 : 0))) {
      for (const raw of f.names) entries.push(toEntry(raw, f.file));
    }
    return new Lexicon(entries);
  }

  private index(e: NameEntry): void {
    for (const [lang, forms] of Object.entries(e.native)) {
      for (const form of forms) {
        push(this.nativeIdx, nativeKey(form), [lang, e]);
        if (isArabicScript(form)) {
          const akey = arabicKey(form);
          push(this.arabicIdx, akey, [lang, e]);
          if (akey.includes(" ")) push(this.arabicIdx, akey.split(" ").join(""), [lang, e]);
        }
      }
    }
    for (const form of allLatin(e)) {
      if (detectScript(form) !== "Latn") continue;
      const key = latinKey(form);
      if (key) pushUnique(this.latinIdx, key, e);
    }
    for (const form of e.equivalents) {
      const key = latinKey(form);
      if (key) pushUnique(this.equivIdx, key, e);
    }
    for (const form of e.short) {
      const keys = new Set([nativeKey(form), detectScript(form) === "Latn" ? latinKey(form) : ""]);
      for (const key of keys) if (key) pushUnique(this.shortIdx, key, e);
    }
  }

  get size(): number {
    return this.entries.size;
  }

  [Symbol.iterator](): Iterator<NameEntry> {
    return this.entries.values();
  }

  get(id: string): NameEntry | undefined {
    return this.entries.get(id);
  }

  /** Entries with `text` among their native-script spellings. */
  lookupNative(text: string, language?: string | null): NameEntry[] {
    let hits = this.nativeIdx.get(nativeKey(text)) ?? [];
    if (!hits.length && isArabicScript(text)) hits = this.arabicIdx.get(arabicKey(text)) ?? [];
    return rank(hits, language);
  }

  /** Arabic-script lookup ignoring vowel marks, hamza seats and Persian/Arabic letter variants. */
  lookupArabic(text: string, language?: string | null): NameEntry[] {
    return rank(this.arabicIdx.get(arabicKey(text)) ?? [], language);
  }

  /** Entries with a Latin spelling equal to `text` (case/diacritics-insensitive). */
  lookupLatin(text: string): NameEntry[] {
    const key = latinKey(text);
    return key ? [...(this.latinIdx.get(key) ?? [])] : [];
  }

  /** Entries for which `text` is a diminutive (Саша, Sasha). */
  lookupShort(text: string): NameEntry[] {
    const found: NameEntry[] = [];
    for (const key of [nativeKey(text), latinKey(text)]) {
      if (!key) continue;
      for (const e of this.shortIdx.get(key) ?? []) if (!found.includes(e)) found.push(e);
    }
    return found;
  }

  /** Entries for which `text` is a translation equivalent (John for Иван). */
  lookupEquivalents(text: string): NameEntry[] {
    const key = latinKey(text);
    return key ? [...(this.equivIdx.get(key) ?? [])] : [];
  }

  /** Look a single name up in any script (native matches first, then Latin spellings). */
  lookup(text: string, language?: string | null, options: { includeShort?: boolean } = {}): NameEntry[] {
    const found = this.lookupNative(text, language);
    if (detectScript(text) === "Latn") {
      for (const e of this.lookupLatin(text)) if (!found.includes(e)) found.push(e);
    }
    if (options.includeShort) {
      for (const e of this.lookupShort(text)) if (!found.includes(e)) found.push(e);
    }
    return found;
  }
}

let registered: readonly LexiconFile[] = [];
let lexicon: Lexicon | null = null;

/** Register lexicon data (done automatically by the main entry point). */
export function registerLexiconData(files: readonly LexiconFile[]): void {
  registered = files;
  lexicon = null;
}

/**
 * The bundled lexicon (built lazily).  With the `translit-names/core` entry
 * point no lexicon data is registered and this returns an empty lexicon.
 */
export function getLexicon(): Lexicon {
  if (!lexicon) lexicon = Lexicon.fromFiles(registered);
  return lexicon;
}
