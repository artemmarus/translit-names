/**
 * translit-names/core — everything except the bundled name lexicon.
 *
 * Use this entry point in browsers when bundle size matters: transliteration,
 * MRZ and language detection work fully; Arabic-script names are vocalised by
 * templates only, and `variants()` / `compare()` rely on schemes, skeleton
 * keys and string similarity (no lexicon clusters).  Register a lexicon later
 * with `registerLexiconData()` if needed.
 */

export { ARTICLE, arabicHook, hasHarakat, vocalizeWord } from "./arabic.js";
export { detectLanguage, detectScript, type Detection } from "./detect.js";
export { APOSTROPHES, Scheme, SchemeError, capitalizeFirst, titlecaseName, type Rule, type Segment, type WordHook } from "./engine.js";
export { fold, foldChar, ICAO_LATIN, type FoldOptions } from "./fold.js";
export { Lexicon, allLatin, allNative, getLexicon, latinFor, registerLexiconData, type NameEntry } from "./lexicon.js";
export {
  PARTICLES,
  compare,
  isMatch,
  jaroWinkler,
  nameKey,
  nameKeys,
  similarity,
  splitName,
  toMatchLatin,
  type CompareOptions,
  type MatchResult,
  type PartMatch,
} from "./matching.js";
export { TD1, TD2, TD3, mrzName, mrzText, parseMrzName, type MrzNameOptions, type MrzTextOptions } from "./mrz.js";
export {
  arabicKey,
  fixMixedScript,
  latinKey,
  normalize,
  normalizeArabic,
  scriptOf,
  stripArabicDiacritics,
  unifyApostrophes,
} from "./normalize.js";
export { defaultSchemeId, defaultsConfig, getScheme, listSchemes, schemeSpecs, type ListSchemesOptions } from "./registry.js";
export { resolveScheme, transliterate, type SchemeLike, type TransliterateOptions } from "./translit.js";
export type { DefaultsConfig, LexiconFile, NameSpec, RuleSpec, SchemeSpec } from "./types.js";
export { schemeWeight, variants, variantsDetailed, type Variant, type VariantsOptions } from "./variants.js";

export const VERSION = "0.1.0";
