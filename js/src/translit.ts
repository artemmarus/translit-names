/** High-level transliteration entry point (port of `core.py`). */

import { detectLanguage, detectScript } from "./detect.js";
import { Scheme } from "./engine.js";
import { fixMixedScript, normalize } from "./normalize.js";
import { defaultSchemeId, getScheme } from "./registry.js";

export type SchemeLike = string | Scheme;

/**
 * Pick the scheme for `text`.  `purpose` selects the section of
 * defaults.json: `transliterate`, `mrz` or `match`.  Returns `null` when the
 * text needs no transliteration (plain Latin).
 */
export function resolveScheme(
  text: string,
  scheme?: SchemeLike | null,
  options: { language?: string | null; purpose?: string } = {},
): Scheme | null {
  if (scheme instanceof Scheme) return scheme;
  if (scheme) return getScheme(scheme);
  const script = detectScript(text);
  const lang = options.language ?? detectLanguage(text).language;
  const sid = defaultSchemeId(lang, options.purpose ?? "transliterate", script);
  return sid ? getScheme(sid) : null;
}

export interface TransliterateOptions {
  /** Language code to skip auto-detection (`"uk"`, `"bg"`, `"kk"` …). */
  language?: string;
  /** Normalise Unicode and repair Latin/Cyrillic look-alikes first (default `true`). */
  clean?: boolean;
}

/**
 * Transliterate a name into Latin script.
 *
 * ```ts
 * transliterate("Щербаков Юрий")                  // "Shcherbakov Iurii"  (ICAO 9303 passport)
 * transliterate("Щербаков Юрий", "ru_bgn_pcgn")   // "Shcherbakov Yuriy"
 * transliterate("Олександр", undefined, { language: "uk" }) // "Oleksandr"
 * ```
 */
export function transliterate(text: string, scheme?: SchemeLike | null, options: TransliterateOptions = {}): string {
  let t = text;
  if (options.clean ?? true) t = fixMixedScript(normalize(t));
  const sch = resolveScheme(t, scheme, { language: options.language ?? null });
  return sch ? sch.transliterate(t) : t;
}
