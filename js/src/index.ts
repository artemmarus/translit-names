/**
 * translit-names — transliteration, spelling variants and cross-script
 * matching of Slavic and Muslim personal names.
 *
 * ```ts
 * import { transliterate, variants, similarity, mrzName } from "translit-names";
 *
 * transliterate("Щербаков Юрий");              // "Shcherbakov Iurii" (ICAO 9303 passport)
 * transliterate("Щербаков Юрий", "ru_bgn_pcgn"); // "Shcherbakov Yuriy"
 * variants("محمد", { limit: 4 });               // ["Muhammad", "Mohammed", "Mohamed", "Mohammad"]
 * similarity("Мухаммед Али", "Mohammed Ali");  // 0.985
 * mrzName("Щербаков", "Юрий");                 // "SHCHERBAKOV<<IURII<<<…"
 * ```
 *
 * This entry point bundles the name lexicon (≈700 KB of JSON, ≈120 KB
 * gzipped).  Import from `translit-names/core` to leave it out.
 */

import NAMES from "./data/names.js";
import { registerLexiconData } from "./lexicon.js";

registerLexiconData(NAMES);

export * from "./core.js";
