# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-10-07

First public release.

### Added
- Context-aware rule engine (word start/end, previous/next letter, classes,
  longest match, automatic case restoration, Arabic shadda gemination).
- Transliteration schemes as JSON data with sources, status and official
  examples as tests: Russian, Ukrainian, Belarusian, Bulgarian, Serbian,
  Macedonian, Serbo-Croatian Latin, Kazakh, Kyrgyz, Uzbek, Tajik, Turkmen,
  Turkish, Azerbaijani, Tatar, Bashkir, Chechen, Arabic, Persian, Urdu,
  Pashto, and ICAO folding of Latin diacritics.
- Arabic-script vocalisation: name lexicon with vowelled forms plus
  template-based guessing (فاعل, فعيل, مفعول, أفعل …).
- Name lexicon of Slavic and Muslim given names: native spellings, per-country
  Latin spellings, attested variants, diminutives.
- `variants()` — ranked plausible Latin spellings of a name.
- `similarity()` / `compare()` / `is_match()` — cross-script name matching
  with lexicon clusters, transliteration-aware skeleton keys and
  Jaro–Winkler; order-independent part alignment.
- `mrz_name()` — ICAO Doc 9303 MRZ name field (TD1/TD2/TD3, truncation).
- `detect_language()` — language of a name from its letters.
- `normalize()`, `fix_mixed_script()` — Unicode, homoglyph and Arabic
  letter-form clean-up.
- `translit-names` command-line tool.
- Research report (Russian) on romanisation standards in `docs/research/`.
