/**
 * Arabic-script support: vocalisation of names before romanisation (port of `arabic.py`).
 *
 * 1. text with vowel marks (harakat) is used as is;
 * 2. names found in the lexicon are replaced by their vocalised form (or, for
 *    practical schemes, by their conventional English spelling);
 * 3. optionally, Arabic name templates (فاعل Khalid, فعيل Karim …) are guessed;
 * 4. anything else is romanised letter by letter.
 */

import type { Scheme, Segment } from "./engine.js";
import { getLexicon, latinFor, type NameEntry } from "./lexicon.js";
import { cps } from "./unicode.js";

const FATHA = "\u064e";
const DAMMA = "\u064f";
const KASRA = "\u0650";
const SUKUN = "\u0652";
export const ARTICLE = "ال";
const HARAKAT_RE = /[\u064b-\u0652\u0670]/u;
const WORD_RE = /[ء-غف-ي\u064b-\u065fٮ-ۓەۮۯۺ-ۿݐ-ݿ\u0670\u200c]+/gu;

const ALEFS = new Set(["ا", "آ", "أ", "إ", "ٱ"]);
const YEHS = new Set(["ي", "ی", "ى", "ې"]);
const WAWS = new Set(["و", "ۇ", "ۆ"]);
const TA_MARBUTA = "ة";

export const hasHarakat = (text: string): boolean => HARAKAT_RE.test(text);
const isCons = (c: string | undefined): boolean =>
  c !== undefined && !ALEFS.has(c) && !YEHS.has(c) && !WAWS.has(c) && c !== TA_MARBUTA;

/**
 * Guess short vowels for a bare Arabic name using common templates, or
 * `null` when no template fits.
 */
export function vocalizeWord(word: string): string | null {
  if (!word || hasHarakat(word)) return null;
  const fem = word.endsWith(TA_MARBUTA);
  const L = cps(fem ? cps(word).slice(0, -1).join("") : word);
  const n = L.length;
  const C = (k: number): boolean => isCons(L[k]);
  const Y = (k: number): boolean => YEHS.has(L[k] as string);
  const W = (k: number): boolean => WAWS.has(L[k] as string);
  const A = (k: number): boolean => ALEFS.has(L[k] as string);
  const l = (k: number): string => L[k] as string;
  let out: string[] | null = null;
  if (n === 3) {
    if (C(0) && C(1) && C(2)) out = [l(0), FATHA, l(1), FATHA, l(2)];
    else if (C(0) && Y(1) && C(2)) out = [l(0), FATHA, l(1), SUKUN, l(2)];
    else if (C(0) && W(1) && C(2)) out = [l(0), DAMMA, l(1), l(2)];
    else if (C(0) && C(1) && Y(2)) out = [l(0), FATHA, l(1), KASRA, l(2)];
    else if (C(0) && A(1) && C(2)) out = [l(0), FATHA, l(1), l(2)];
  } else if (n === 4) {
    if (C(0) && A(1) && C(2) && C(3)) out = [l(0), FATHA, l(1), l(2), KASRA, l(3)];
    else if (C(0) && C(1) && Y(2) && C(3)) out = [l(0), FATHA, l(1), KASRA, l(2), l(3)];
    else if (C(0) && C(1) && W(2) && C(3)) out = [l(0), FATHA, l(1), DAMMA, l(2), l(3)];
    else if (C(0) && C(1) && A(2) && C(3)) out = [l(0), FATHA, l(1), FATHA, l(2), l(3)];
    else if (A(0) && C(1) && C(2) && C(3)) {
      const first = l(0) === "إ" ? "إ" : "أ";
      out = [first, first === "إ" ? KASRA : FATHA, l(1), SUKUN, l(2), FATHA, l(3)];
    } else if (C(0) && (Y(1) || W(1)) && C(2) && C(3)) out = [l(0), FATHA, l(1), SUKUN, l(2), FATHA, l(3)];
    else if (C(0) && C(1) && C(2) && C(3)) out = [l(0), FATHA, l(1), SUKUN, l(2), FATHA, l(3)];
    else if (C(0) && C(1) && C(2) && Y(3)) out = [l(0), FATHA, l(1), SUKUN, l(2), KASRA, l(3)];
  } else if (n === 5) {
    if (C(0) && A(1) && C(2) && W(3) && C(4)) out = [l(0), FATHA, l(1), l(2), DAMMA, l(3), l(4)];
    else if (l(0) === "م" && C(1) && C(2) && W(3) && C(4)) out = [l(0), FATHA, l(1), SUKUN, l(2), DAMMA, l(3), l(4)];
    else if (A(0) && C(1) && C(2) && A(3) && C(4)) {
      const first = "إا".includes(l(0)) ? "إ" : l(0);
      out = [first, KASRA, l(1), SUKUN, l(2), FATHA, l(3), l(4)];
    }
  }
  if (!out) return null;
  if (fem) {
    if (![FATHA, DAMMA, KASRA, SUKUN].includes(out[out.length - 1] as string)) out.push(FATHA);
    out.push(TA_MARBUTA);
  }
  return out.join("");
}

type Token = [boolean, string];

function tokenize(text: string): Token[] {
  const tokens: Token[] = [];
  let pos = 0;
  for (const m of text.matchAll(WORD_RE)) {
    const start = m.index as number;
    if (start > pos) tokens.push([false, text.slice(pos, start)]);
    tokens.push([true, m[0]]);
    pos = start + m[0].length;
  }
  if (pos < text.length) tokens.push([false, text.slice(pos)]);
  return tokens;
}

function phrase(tokens: readonly Token[], i: number, words: number): [string, number] | null {
  const parts: string[] = [];
  let j = i;
  for (let k = 0; k < words; k++) {
    const t = tokens[j];
    if (!t || !t[0]) return null;
    parts.push(t[1]);
    j++;
    if (k < words - 1) {
      const sep = tokens[j];
      if (!sep || sep[0] || !["", "-"].includes(sep[1].trim())) return null;
      j++;
    }
  }
  return [parts.join(" "), j];
}

function lookup(scheme: Scheme, text: string): NameEntry | null {
  const lex = getLexicon();
  let hits = lex.lookupArabic(text, scheme.language);
  if (!hits.length) {
    const joined = text.split(" ").join("");
    if (joined !== text) hits = lex.lookupArabic(joined, scheme.language);
  }
  return hits[0] ?? null;
}

function render(scheme: Scheme, entry: NameEntry, article: boolean): Segment | null {
  const practical = scheme.options["practical"] as string[] | undefined;
  if (practical && practical.length) {
    const latin = latinFor(entry, [...practical, "en"]);
    if (latin) {
      const prefix = article ? ((scheme.options["article"] as string | undefined) ?? "al-") : "";
      return ["lit", prefix + latin];
    }
  }
  if (entry.vocalized) return ["src", (article ? ARTICLE : "") + entry.vocalized];
  return null;
}

/** Word hook used by Arabic-script schemes (`"hook": "arabic"`). */
export function arabicHook(scheme: Scheme, text: string): Segment[] {
  const useLexicon = (scheme.options["lexicon"] as boolean | undefined) ?? true;
  const guess = (scheme.options["vocalize"] as boolean | undefined) ?? false;
  const tokens = tokenize(text);
  const segments: Segment[] = [];
  let i = 0;
  while (i < tokens.length) {
    const [isWord, tok] = tokens[i] as Token;
    if (!isWord || hasHarakat(tok)) {
      segments.push(["src", tok]);
      i++;
      continue;
    }
    if (useLexicon) {
      let done = false;
      for (const span of [3, 2]) {
        const ph = phrase(tokens, i, span);
        if (!ph) continue;
        const entry = lookup(scheme, ph[0]);
        if (entry) {
          const seg = render(scheme, entry, false);
          if (seg) {
            segments.push(seg);
            i = ph[1];
            done = true;
            break;
          }
        }
      }
      if (done) continue;
      let seg: Segment | null = null;
      const entry = lookup(scheme, tok);
      if (entry) seg = render(scheme, entry, false);
      else if (tok.startsWith(ARTICLE) && cps(tok).length > 3) {
        const stem = lookup(scheme, cps(tok).slice(2).join(""));
        if (stem) seg = render(scheme, stem, true);
      }
      if (seg) {
        segments.push(seg);
        i++;
        continue;
      }
    }
    if (guess) {
      const article = tok.startsWith(ARTICLE) && cps(tok).length > 4;
      const stem = article ? cps(tok).slice(2).join("") : tok;
      const voc = vocalizeWord(stem);
      if (voc !== null) {
        segments.push(["src", (article ? ARTICLE : "") + voc]);
        i++;
        continue;
      }
    }
    segments.push(["src", tok]);
    i++;
  }
  return segments;
}
