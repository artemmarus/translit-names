# translit-names (TypeScript / JavaScript)

[![CI](https://github.com/artemmarus/translit-names/actions/workflows/ci.yml/badge.svg)](https://github.com/artemmarus/translit-names/actions/workflows/ci.yml)
![Types](https://img.shields.io/badge/types-included-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Transliteration, spelling variants and cross-script matching of personal names from Slavic and Muslim-majority countries** — for Node.js and browsers, with full TypeScript types and zero dependencies.

This is the TypeScript port of the [`translit-names`](https://github.com/artemmarus/translit-names) Python package. Both use the **same data** (85 transliteration schemes for 22 languages, a lexicon of 1,100+ name clusters) and CI checks that they produce **identical results** on ~11,700 reference cases.

```ts
import { transliterate, variants, similarity, mrzName } from "translit-names";

transliterate("Щербаков Юрий");                  // "Shcherbakov Iurii"   (Russian passport, ICAO 9303)
transliterate("Щербаков Юрий", "ru_bgn_pcgn");   // "Shcherbakov Yuriy"   (US/UK government standard)
transliterate("Олександр Згурський", null, { language: "uk" }); // "Oleksandr Zghurskyi"
transliterate("محمد بن سلمان");                    // "Muhammad bin Salman"

variants("Юрий", { limit: 4 });      // ["Iurii", "Yuri", "Yury", "Yuriy"]
variants("محمد", { limit: 4 });      // ["Muhammad", "Mohammed", "Mohamed", "Mohammad"]

similarity("Мухаммед Али", "Mohammed Ali");    // 0.985
similarity("Hasan", "Husayn");                 // 0.6 — different names

mrzName("Щербаков", "Юрий");                   // "SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<"
```

## Installation

```bash
npm install translit-names
```

Until the package is published on npm, build it from the repository and install the tarball into your project:

```bash
git clone https://github.com/artemmarus/translit-names.git
cd translit-names/js
npm install && npm run build && npm pack          # → translit-names-0.1.0.tgz
cd /path/to/your-project
npm install /path/to/translit-names/js/translit-names-0.1.0.tgz
```

Works in Node.js ≥ 18 and all modern browsers (ES2020, Unicode property escapes, regex look-behind). Ships ESM and CommonJS builds with type declarations.

## Entry points

| Import | Contents | Size (gzip) |
|---|---|---|
| `translit-names` | everything, including the name lexicon | ≈ 255 KB |
| `translit-names/core` | everything except the lexicon | ≈ 128 KB |

Without the lexicon, transliteration, MRZ and language detection work fully; Arabic-script names are vocalised by templates only (`خالد` → `Khalid` is right, but `محمد` becomes `Mahmad` instead of `Muhammad`), and `variants()` / `compare()` rely on schemes, skeleton keys and string similarity. You can load the lexicon later:

```ts
import { registerLexiconData } from "translit-names/core";
const names = await fetch("/names.json").then((r) => r.json()); // LexiconFile[]
registerLexiconData(names);
```

## API

### `transliterate(text, scheme?, options?)`

```ts
transliterate("Щербаков Юрий");                         // auto-detects ru → ru_icao
transliterate("Щербаков Юрий", "ru_mvd_310");           // "Shcherbakov Yuriy" (passports 1997–2010)
transliterate("Ксения", "ru_mvd_310_fr");               // "Xeniia" (Soviet French-style)
transliterate("Христо Стоичков", null, { language: "bg" }); // "Hristo Stoichkov"
transliterate("عبد الرحمن", "ar_ala_lc");                 // "ʻAbd al-Raḥmān"
```

Without a scheme the language is detected from the letters and its default scheme is used (the current passport system for Cyrillic languages, practical English for Arabic-script names). Names with no language-specific letters (Олександр is valid Russian spelling too) are best given an explicit `language`.

### Schemes

```ts
import { getScheme, listSchemes } from "translit-names";

listSchemes({ language: "uk" }).map((s) => s.id);
// ["uk_ala_lc", "uk_iso_9", "uk_kmu_2010", "uk_national_1996", "uk_passport_2007", "uk_scientific"]

const s = getScheme("uk_kmu_2010");
s.title;        // "Ukrainian — KMU Resolution No. 55 (2010), official/passport"
s.authority;    // legal source
s.sources;      // URLs of primary sources
s.transliterate("Згорани");   // "Zghorany"
```

All 85 schemes are listed in [docs/SCHEMES.md](https://github.com/artemmarus/translit-names/blob/main/docs/SCHEMES.md).

### `variants(name, options?)` / `variantsDetailed(name, options?)`

Ranked plausible Latin spellings for search and record linkage. Options: `language`, `limit` (20), `asciiOnly` (true), `includeShort` (diminutives), `useLexicon` (true).

```ts
variantsDetailed("Хусейн", { limit: 3 });
// [{ text: "Khusein", score: 1, sources: ["lexicon:husayn", "ru_icao", ...] },
//  { text: "Hussein", score: 0.98, sources: ["lexicon:husayn", "lexicon:husayn:ar", ...] }, ...]
```

### `similarity(a, b, options?)` / `compare(a, b, options?)` / `isMatch(a, b, options?)`

```ts
const r = compare("Ivanov Ivan Ivanovich", "IVAN IVANOV");
r.score;          // 0.96 — the missing patronymic costs a little
r.pairs;          // [{ left: "Ivan", right: "IVAN", score: 1, reason: "exact" }, ...]
r.unmatchedLeft;  // ["Ivanovich"]

isMatch("Магомед", "Mehmet");                    // true (threshold 0.88)
nameKey("Мухаммед Али") === nameKey("Mohammed Ali"); // true — use as a blocking key
```

Reasons: `exact`, `same-name` (lexicon), `skeleton`, `skeleton-coarse`, `fuzzy`, `initial`, `diminutive` (Саша ~ Александр, 0.86), `equivalent` (Michael ~ Михаил, 0.80), `different-names` (two different known names, capped at 0.6).

### MRZ

```ts
mrzName("al-Basri", "Huda Muhammad Jawad");   // "AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<<<<<<<"
mrzName(surname, given, { length: 30, strategy: "initials" }); // TD1 ID card
mrzText("D'Artagnan");                        // "DARTAGNAN"
parseMrzName("AL<BASRI<<HUDA<MUHAMMAD");      // ["AL BASRI", "HUDA MUHAMMAD"]
```

### Utilities

`detectLanguage(text)`, `detectScript(text)`, `normalize(text)`, `fixMixedScript(text)`, `fold(text, { german })`, `splitName(name)`, `nameKeys(word)`, `jaroWinkler(a, b)`, `getLexicon()`.

## How results are kept identical to Python

The data lives once, in [`data/`](https://github.com/artemmarus/translit-names/tree/main/data), and is bundled into this package at build time. `scripts/gen_parity_fixtures.py` records the Python outputs for every scheme sample and alphabet, 460 names, 800+ name comparisons, variants, MRZ fields and lexicon lookups; `test/parity.test.ts` requires exactly the same results here. Python-specific regular-expression semantics (Unicode `\w`/`\b`, `\1` replacements) and rounding (`round()` ties to even) are reproduced.

## License

MIT
