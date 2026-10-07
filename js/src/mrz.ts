/**
 * Names in the machine-readable zone (MRZ) of passports and ID cards —
 * ICAO Doc 9303 (8th edition) Part 3 §4.6 and Parts 4/5 (port of `mrz.py`).
 */

import { detectLanguage, detectScript } from "./detect.js";
import { fold } from "./fold.js";
import { normalize } from "./normalize.js";
import { defaultSchemeId, getScheme } from "./registry.js";
import { resolveScheme, type SchemeLike } from "./translit.js";
import { cps, rstrip, strip } from "./unicode.js";

/** Passport (TD3) name field length. */
export const TD3 = 39;
/** TD2 cards and MRV-B visas. */
export const TD2 = 31;
/** ID cards (TD1). */
export const TD1 = 30;

const APOSTROPHES = "'\u2019\u02bc\u02bb\u2018`\u00b4\u02b9";
const SEP_RE = /[\s\-\u2010-\u2015,]+/gu;

export interface MrzTextOptions {
  scheme?: SchemeLike | null;
  language?: string | null;
  /** ICAO digraph options (Ä→AE, Ö→OE, Ü→UE). */
  german?: boolean;
}

/** Convert one identifier (surname or given names) to MRZ characters: `"Smith-Jones"` → `"SMITH<JONES"`. */
export function mrzText(text: string, options: MrzTextOptions = {}): string {
  let t = normalize(text);
  if (!t) return "";
  const german = options.german ?? false;
  if (options.scheme || detectScript(t) !== "Latn") {
    const sch = resolveScheme(t, options.scheme ?? null, { language: options.language ?? null, purpose: "mrz" });
    if (sch) t = sch.transliterate(t);
  } else if (!german) {
    // Latin-script languages with national letters (Azerbaijani Ə, Uzbek Oʻ/X …)
    const lang = options.language ?? detectLanguage(t).language;
    const sid = defaultSchemeId(lang, "mrz", "Latn");
    if (sid) t = getScheme(sid).transliterate(t);
  }
  t = cps(t)
    .filter((c) => !APOSTROPHES.includes(c))
    .join("");
  t = fold(t, { german }).toUpperCase();
  t = t.replace(SEP_RE, "<");
  t = cps(t)
    .filter((c) => (c >= "A" && c <= "Z") || c === "<")
    .join("");
  return strip(t.replace(/<+/g, "<"), "<");
}

function longest(parts: readonly string[]): number {
  let best = 0;
  for (let i = 1; i < parts.length; i++) if ((parts[i] as string).length > (parts[best] as string).length) best = i;
  return best;
}

function fit(primary: readonly string[], secondary: readonly string[], length: number, strategy: "cut" | "initials"): string {
  const build = (p: readonly string[], s: readonly string[]): string => {
    const head = p.filter(Boolean).join("<");
    const tail = s.filter(Boolean).join("<");
    return head + (tail ? `<<${tail}` : "");
  };
  const full = build(primary, secondary);
  if (full.length <= length) return full;
  const sec = [...secondary];
  if (strategy === "initials") {
    for (let k = sec.length - 1; k > 0; k--) {
      sec[k] = (sec[k] as string).slice(0, 1);
      if (build(primary, sec).length <= length) return build(primary, sec);
    }
  } else if (strategy !== "cut") {
    throw new RangeError(`unknown truncation strategy ${JSON.stringify(strategy)}`);
  }
  const prim = [...primary];
  let need = prim.reduce((n, x) => n + x.length, 0) + Math.max(0, prim.length - 1) + (sec.length && sec[0] ? 3 : 0);
  while (need > length) {
    const k = longest(prim);
    if ((prim[k] as string).length <= 1) break;
    prim[k] = (prim[k] as string).slice(0, -1);
    need -= 1;
  }
  let out = build(prim, sec).slice(0, length);
  while (out.endsWith("<")) {
    const k = longest(prim);
    if ((prim[k] as string).length <= 1) {
      out = rstrip(out, "<");
      break;
    }
    prim[k] = (prim[k] as string).slice(0, -1);
    out = build(prim, sec).slice(0, length);
  }
  return out;
}

export interface MrzNameOptions {
  /** 39 for passports (TD3, default), 31 for TD2, 30 for ID cards (TD1). */
  length?: number;
  scheme?: SchemeLike | null;
  language?: string | null;
  /** How over-long names are shortened: `"cut"` (default) or `"initials"`. */
  strategy?: "cut" | "initials";
  /** Pad with `<` to the field length (default `true`). */
  pad?: boolean;
}

/**
 * Build the MRZ name field.
 *
 * ```ts
 * mrzName("Щербаков", "Юрий")  // "SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<"
 * ```
 */
export function mrzName(surname: string, givenNames = "", options: MrzNameOptions = {}): string {
  const length = options.length ?? TD3;
  const textOpts = { scheme: options.scheme ?? null, language: options.language ?? null };
  const p = mrzText(surname, textOpts);
  const s = givenNames ? mrzText(givenNames, textOpts) : "";
  const primary = p.split("<").filter(Boolean);
  const secondary = s.split("<").filter(Boolean);
  let field = fit(primary, secondary, length, options.strategy ?? "cut");
  const pad = options.pad ?? true;
  if (!secondary.length && pad && field.length + 2 <= length) field += "<<";
  return pad ? field.padEnd(length, "<") : field;
}

/** Split an MRZ name field into `[surname, givenNames]`. */
export function parseMrzName(field: string): [string, string] {
  const f = rstrip(field.trim(), "<");
  const idx = f.indexOf("<<");
  const primary = idx >= 0 ? f.slice(0, idx) : f;
  const secondary = idx >= 0 ? f.slice(idx + 2) : "";
  return [primary.split("<").join(" ").trim(), secondary.split("<").join(" ").trim()];
}
