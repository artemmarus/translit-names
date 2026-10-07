/** Unicode clean-up for personal names (port of `normalize.py`). */

import { fold } from "./fold.js";
import { cps, isAlnum, isAlpha, isMn, splitWs } from "./unicode.js";

const SPACES_RE = /[\s\u00a0\u2000-\u200b\u202f\u205f\u3000]+/gu;
const DASHES = new Set(["\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2015", "\u2212", "\ufe58", "\ufe63", "\uff0d"]);
const APOSTROPHE_LIKE = new Set(["'", "\u2019", "\u02bc", "\u02bb", "\u2018", "`", "\u00b4", "\u02b9", "\u02bd", "\u2032"]);

const LAT_TO_CYR: Readonly<Record<string, string>> = {
  a: "а", c: "с", e: "е", o: "о", p: "р", x: "х", y: "у", i: "і", j: "ј",
  A: "А", B: "В", C: "С", E: "Е", H: "Н", K: "К", M: "М", O: "О", P: "Р", T: "Т", X: "Х", Y: "У", I: "І", J: "Ј",
};
const CYR_TO_LAT_SAFE: Readonly<Record<string, string>> = Object.fromEntries(
  Object.entries(LAT_TO_CYR)
    .map(([k, v]) => [v, k] as const)
    .filter(([cyr]) => "аеорсухіјАВЕКМНОРСТХУІЈ".includes(cyr)),
);

const ARABIC_MARKS_RE = /[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06dc\u06df-\u06e8\u06ea-\u06ed]/gu;
const TATWEEL = "ـ";
const DIGITS: Readonly<Record<string, string>> = Object.fromEntries([
  ...Array.from("٠١٢٣٤٥٦٧٨٩", (c, i) => [c, String(i)]),
  ...Array.from("۰۱۲۳۴۵۶۷۸۹", (c, i) => [c, String(i)]),
]);
const ALEF_FORMS: Readonly<Record<string, string>> = { "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ٲ": "ا", "ٳ": "ا" };
const ARABIC_KEY_MAP: Readonly<Record<string, string>> = {
  "ی": "ي", "ى": "ي", "ې": "ي", "ۍ": "ي", "ے": "ي", "ئ": "ي", "ۓ": "ي",
  "ک": "ك", "ڪ": "ك",
  "ہ": "ه", "ھ": "ه", "ۀ": "ه", "ۃ": "ه", "ة": "ه", "ە": "ه",
  "ؤ": "و", "ۆ": "و", "ۇ": "و", "ۈ": "و", "ۋ": "و",
  "ء": "", "\u0654": "",
};

const translate = (text: string, table: Readonly<Record<string, string>>): string =>
  cps(text)
    .map((c) => table[c] ?? c)
    .join("");

const inPresentation = (c: string): boolean =>
  (c >= "ﭐ" && c <= "﷿") || (c >= "ﹰ" && c <= "\ufeff");

function expandPresentationForms(text: string): string {
  const arr = cps(text);
  if (!arr.some(inPresentation)) return text;
  return arr.map((c) => (inPresentation(c) ? c.normalize("NFKC") : c)).join("");
}

/**
 * Basic, lossless clean-up: NFC, all space-like characters → one space,
 * typographic dashes → `-`, Arabic-Indic and Persian digits → ASCII,
 * tatweel removed, Arabic presentation forms expanded.
 */
export function normalize(text: string, form: "NFC" | "NFD" | "NFKC" | "NFKD" = "NFC"): string {
  if (!text) return "";
  let t = expandPresentationForms(text).normalize(form);
  t = t.split(TATWEEL).join("").split("\u200d").join("");
  t = translate(t, DIGITS);
  t = cps(t)
    .map((c) => (DASHES.has(c) ? "-" : c))
    .join("");
  return t.replace(SPACES_RE, " ").trim();
}

/** Replace every apostrophe-like character (’ ʼ ʻ ‘ ` ´ ′) with `to`. */
export function unifyApostrophes(text: string, to = "'"): string {
  return cps(text)
    .map((c) => (APOSTROPHE_LIKE.has(c) ? to : c))
    .join("");
}

/** Rough script of a character: `Latn`, `Cyrl`, `Arab`, `Grek` or `Zyyy`. */
export function scriptOf(ch: string): string {
  if (!isAlpha(ch)) {
    if (ch >= "\u0600" && ch <= "ۿ" && isMn(ch)) return "Arab";
    return "Zyyy";
  }
  const cp = ch.codePointAt(0) as number;
  if (cp < 0x250 || (cp >= 0x1e00 && cp <= 0x1eff) || (cp >= 0x2c60 && cp <= 0x2c7f) || (cp >= 0xa720 && cp <= 0xa7ff)) return "Latn";
  if ((cp >= 0x0400 && cp <= 0x052f) || (cp >= 0x1c80 && cp <= 0x1c8f) || (cp >= 0x2de0 && cp <= 0x2dff) || (cp >= 0xa640 && cp <= 0xa69f)) return "Cyrl";
  if ((cp >= 0x0600 && cp <= 0x06ff) || (cp >= 0x0750 && cp <= 0x077f) || (cp >= 0x08a0 && cp <= 0x08ff) || (cp >= 0xfb50 && cp <= 0xfeff)) return "Arab";
  if (cp >= 0x0370 && cp <= 0x03ff) return "Grek";
  return "Zyyy";
}

const WORD_RE = /[\p{L}\p{No}\p{Nl}]+(?:['\u2019\u02bc][\p{L}\p{No}\p{Nl}]+)*/gu;
const PALOCHKA_RE = /(?<=[гкхпт])[Ii1lІ]|(?<=[ГКХПТ])[Ii1lІ]/gu;

/**
 * Repair words that mix Latin and Cyrillic look-alike letters:
 * `"Аlexey"` (Cyrillic А) → `"Alexey"`, `"Иванoв"` (Latin o) → `"Иванов"`.
 */
export function fixMixedScript(text: string): string {
  return text.replace(WORD_RE, (word) => {
    let latn = 0;
    let cyrl = 0;
    for (const c of word) {
      const s = scriptOf(c);
      if (s === "Latn") latn++;
      else if (s === "Cyrl") cyrl++;
    }
    if (!latn || !cyrl) return word;
    if (cyrl >= latn) {
      const w = cps(word)
        .map((c) => (scriptOf(c) === "Latn" ? (LAT_TO_CYR[c] ?? c) : c))
        .join("");
      return /[Ii1lІ]/u.test(w) ? w.replace(PALOCHKA_RE, "Ӏ") : w;
    }
    return cps(word)
      .map((c) => (scriptOf(c) === "Cyrl" ? (CYR_TO_LAT_SAFE[c] ?? c) : c))
      .join("");
  });
}

/** Remove harakat, shadda, sukun, tanwin, dagger alif and Quranic marks. */
export function stripArabicDiacritics(text: string): string {
  return text.replace(ARABIC_MARKS_RE, "");
}

/** Normalise Arabic-script text, optionally stripping vowel marks or folding alef forms. */
export function normalizeArabic(text: string, options: { stripDiacritics?: boolean; foldAlef?: boolean } = {}): string {
  let t = normalize(text);
  if (options.stripDiacritics) t = stripArabicDiacritics(t);
  if (options.foldAlef) t = translate(t, ALEF_FORMS);
  return t;
}

/**
 * Aggressive Arabic-script key for lookup and matching: no vowel marks, hamza
 * seats and alef forms folded, Persian/Urdu letter shapes unified.
 */
export function arabicKey(text: string): string {
  let t = stripArabicDiacritics(normalize(text));
  t = translate(translate(t, ALEF_FORMS), ARABIC_KEY_MAP);
  t = t.split("\u200c").join("");
  return splitWs(t).join(" ");
}

/** Case-, diacritic- and punctuation-insensitive key: `"Hüseyin"` → `"huseyin"`. */
export function latinKey(text: string): string {
  return cps(fold(normalize(text)).toLowerCase())
    .filter(isAlnum)
    .join("");
}
