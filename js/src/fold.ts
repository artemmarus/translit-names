/**
 * Folding of Latin letters with diacritics to plain ASCII — ICAO Doc 9303
 * Part 3 §6.A, single-letter options by default (`german` selects Ä→AE,
 * Ö→OE, Ü→UE, Å→AA), plus letters ICAO omits (Ə, Ș/Ț, Ǆ/Ǉ/Ǌ, ı …).
 */

import { capitalize, cps, isAscii, isCombining, isLower1, lower1, pyIsUpper } from "./unicode.js";

/** ICAO Doc 9303 Part 3 §6.A, upper case, first (preferred) option. */
export const ICAO_LATIN: Readonly<Record<string, string>> = {
  À: "A", Á: "A", Â: "A", Ã: "A", Ä: "AE", Å: "AA", Æ: "AE", Ç: "C", È: "E", É: "E", Ê: "E", Ë: "E",
  Ì: "I", Í: "I", Î: "I", Ï: "I", Ð: "D", Ñ: "N", Ò: "O", Ó: "O", Ô: "O", Õ: "O", Ö: "OE", Ø: "OE",
  Ù: "U", Ú: "U", Û: "U", Ü: "UE", Ý: "Y", Þ: "TH", Ā: "A", Ă: "A", Ą: "A", Ć: "C", Ĉ: "C", Ċ: "C",
  Č: "C", Ď: "D", Đ: "D", Ē: "E", Ĕ: "E", Ė: "E", Ę: "E", Ě: "E", Ĝ: "G", Ğ: "G", Ġ: "G", Ģ: "G",
  Ĥ: "H", Ħ: "H", Ĩ: "I", Ī: "I", Ĭ: "I", Į: "I", İ: "I", I: "I", Ĳ: "IJ", Ĵ: "J", Ķ: "K", Ĺ: "L",
  Ļ: "L", Ľ: "L", Ŀ: "L", Ł: "L", Ń: "N", Ņ: "N", Ň: "N", Ŋ: "N", Ō: "O", Ŏ: "O", Ő: "O", Œ: "OE",
  Ŕ: "R", Ŗ: "R", Ř: "R", Ś: "S", Ŝ: "S", Ş: "S", Š: "S", Ţ: "T", Ť: "T", Ŧ: "T", Ũ: "U", Ū: "U",
  Ŭ: "U", Ů: "U", Ű: "U", Ų: "U", Ŵ: "W", Ŷ: "Y", Ÿ: "Y", Ź: "Z", Ż: "Z", Ž: "Z", ẞ: "SS",
};

const SHORT_FORMS: Readonly<Record<string, string>> = { Ä: "A", Å: "A", Ö: "O", Ü: "U" };

const EXTRA: Readonly<Record<string, string>> = {
  Ə: "A", Ș: "S", Ț: "T", Ǆ: "DZ", ǅ: "Dz", ǆ: "dz", Ǉ: "LJ", ǈ: "Lj", ǉ: "lj", Ǌ: "NJ", ǋ: "Nj", ǌ: "nj",
  Ǵ: "G", Ḱ: "K", Ḩ: "H", Ḥ: "H", Ṣ: "S", Ṭ: "T", Ḍ: "D", Ẓ: "Z", Ẕ: "Z", Ḏ: "D", Ṯ: "T", Ḫ: "H",
  Ẏ: "Y", Ḟ: "F", Ṡ: "S", Ṅ: "N", ß: "ss", ı: "i", ĸ: "q", ſ: "s",
};

const MARKS: Readonly<Record<string, string>> = {
  "\u02bb": "'", "\u02bc": "'", "\u2018": "'", "\u2019": "'", "\u02b9": "'", "\u02bd": "'",
  "\u02be": "'", "\u02bf": "'", "\u02ba": '"', "\u201c": '"', "\u201d": '"', "\u00b4": "'",
  "\u2032": "'", "\u2033": '"', "\u00b7": "", "\u0361": "", "\u035c": "",
};

function build(german: boolean): Map<string, string> {
  const table = new Map<string, string>();
  for (const [up, v] of Object.entries(ICAO_LATIN)) {
    const val = !german && up in SHORT_FORMS ? (SHORT_FORMS[up] as string) : v;
    table.set(up, val);
    const low = up.toLowerCase();
    if (cps(low).length === 1 && low !== up && !table.has(low)) table.set(low, val.toLowerCase());
  }
  for (const [k, v] of Object.entries(EXTRA)) {
    table.set(k, v);
    const low = k.toLowerCase();
    if (cps(low).length === 1 && !(low in EXTRA) && !table.has(low)) table.set(low, v.toLowerCase());
  }
  table.set("ı", "i");
  table.set("İ", "I");
  for (const [k, v] of Object.entries(MARKS)) table.set(k, v);
  return table;
}

const TABLE = build(false);
const TABLE_GERMAN = build(true);

/** Fold one character to ASCII (empty string if nothing sensible exists). */
export function foldChar(ch: string, german = false): string {
  if (isAscii(ch)) return ch;
  const table = german ? TABLE_GERMAN : TABLE;
  const hit = table.get(ch);
  if (hit !== undefined) return hit;
  const base = cps(ch.normalize("NFKD"))
    .filter((c) => !isCombining(c))
    .join("");
  if (base && isAscii(base)) return base;
  if (base && base !== ch) return cps(base).map((c) => foldChar(c, german)).join("");
  return "";
}

export interface FoldOptions {
  /** ICAO digraph options: Ä→AE, Ö→OE, Ü→UE, Å→AA. */
  german?: boolean;
  /** Non-ASCII characters to leave untouched. */
  keep?: string;
}

/**
 * Fold text to ASCII using the ICAO §6.A table plus extensions.
 *
 * ```ts
 * fold("Łódź Ærø Məmmədov")   // "Lodz Aeroe Mammadov"
 * ```
 */
export function fold(text: string, options: FoldOptions = {}): string {
  const german = options.german ?? false;
  const keep = options.keep ?? "";
  const arr = cps(text.normalize("NFC"));
  let out = "";
  for (let i = 0; i < arr.length; i++) {
    const ch = arr[i] as string;
    if (keep.includes(ch)) {
      out += ch;
      continue;
    }
    if (isCombining(ch)) continue;
    let res = foldChar(ch, german);
    if (cps(res).length > 1 && pyIsUpper(res)) {
      const nxt = arr[i + 1] ?? "";
      if (nxt && isLower1(nxt)) res = capitalize(res); // Æsir → Aesir, but ÆSIR → AESIR
    }
    out += res;
  }
  return out;
}

export { lower1 };
