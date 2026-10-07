# translit-names

[![CI](https://github.com/artemmarus/translit-names/actions/workflows/ci.yml/badge.svg)](https://github.com/artemmarus/translit-names/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%20%E2%80%93%203.14-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Transliteration, spelling variants and cross-script matching of personal names from Slavic and Muslim-majority countries.** Available for **Python** and **TypeScript/JavaScript** — same data, identical results.

[Русская версия →](README.ru.md) · [TypeScript package →](js/README.md)

One name has many legitimate Latin spellings. **Юрий** is `Iurii` in a Russian passport issued today, was `Yuriy` in one issued in 2005, is `Yuri` in the press, `Yury` on Wikipedia, `Jurij` in German records and `Iouri` in French ones. **محمد** is `Muhammad`, `Mohammed`, `Mohamed`, `Mohammad`, `Mehmet` or `Magomed` depending on the country. `translit-names` knows the official standards behind these spellings and the practice around them:

```python
>>> from translit_names import transliterate, variants, similarity, mrz_name
>>> transliterate("Щербаков Юрий")                 # Russian passport (ICAO Doc 9303)
'Shcherbakov Iurii'
>>> transliterate("Щербаков Юрий", "ru_bgn_pcgn")  # US/UK government standard
'Shcherbakov Yuriy'
>>> variants("محمد", limit=6)
['Muhammad', 'Mohammed', 'Mohamed', 'Mohammad', 'Muhamad', 'Muhammed']
>>> similarity("Мухаммед Али", "Mohammed Ali")
0.985
>>> mrz_name("Щербаков", "Юрий")
'SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<'
```

## Features

- **85 transliteration schemes for 22 languages**, each with its legal source, adoption year, status (current / superseded / informal) and the official examples from the source document as unit tests:
  - **East Slavic**: Russian (ICAO 2013 passports, GOST R 52535.1 2010–13, MVD 310 1997–2010, Soviet French-style, BGN/PCGN, GOST 7.79 A/B = ISO 9, ALA-LC, scholarly, Wikipedia, Telegram, Yandex, Moscow Metro), Ukrainian (KMU No. 55 of 2010 with all 76 official examples, 1996, 2007 passports, ISO 9, ALA-LC), Belarusian (passport practice, 2023 Instruction with all 51 official examples, 2007, MVD 288, BGN/PCGN, ALA-LC, ISO 9);
  - **South Slavic**: Bulgarian (Transliteration Act 2009 incl. the final ‑ия → ‑ia rule, ISO 9, legacy systems), Serbian (Gaj Latin, ICAO MRZ, practical `Dj`), Macedonian (2008 official, BGN/PCGN, ISO 9), Serbo-Croatian Latin → ASCII;
  - **Turkic and Caucasus**: Kazakh (passport, 2021 Latin alphabet, BGN/PCGN), Uzbek (official Latin 1995, passport), Kyrgyz, Tajik, Turkmen, Turkish, Azerbaijani (incl. Cabinet Resolution No. 498 of 2020), Tatar, Bashkir, Chechen/Ingush;
  - **Arabic script**: Arabic (ALA-LC, DIN 31635, UNGEGN 2017, BGN/PCGN, IJMES, Buckwalter, ICAO MRZ, practical English, Egyptian and Maghreb French-style), Persian (UN 2012, BGN/PCGN, ALA-LC, practical), Urdu, Pashto;
  - **ICAO Doc 9303 §6.A** folding of every Latin letter with diacritics (Polish, Czech, Slovak, Croatian, Slovene, Turkish, German, Nordic …).
- **Arabic-script vocalisation.** Names are written without short vowels (محمد = m-ḥ-m-d). A lexicon of vowelled names plus Arabic name templates (فاعل *Khalid*, فعيل *Karim*, مفعول *Mahmud*, أفعل *Ahmad* …) supplies them before romanisation.
- **Name lexicon** of 1,100+ name clusters (Slavic and Muslim given names, common surnames, Arabic name elements such as *Abd*, *bin*, *-uddin*, *-ullah*): native spellings in every script, conventional Latin spellings per country, attested variants, diminutives and translation equivalents.
- **`variants()`** — ranked plausible Latin spellings of a name for search and record linkage.
- **`similarity()` / `compare()`** — cross-script name matching that understands transliteration: lexicon clusters, transliteration-aware skeleton keys (`kh/h/x`, `sh/ch/sch/sz`, `zh/j/dj`, `ks/x`, `-iy/-y/-ii`, `al-/el-/ul-`, `-uddin/-eddine` …), Jaro–Winkler, order-independent alignment of name parts, initials and missing patronymics.
- **`mrz_name()`** — the ICAO Doc 9303 machine-readable-zone name field (TD1/TD2/TD3, truncation), verified against the official ICAO examples.
- **`detect_language()`** — the language of a name from its letters (ґ є ї → Ukrainian, ұ → Kazakh, ٹ ڈ ڑ → Urdu, ə → Azerbaijani …).
- **Clean-up**: Unicode normalisation, mixed Latin/Cyrillic look-alikes (`Иванoв` with a Latin *o*), apostrophe variants, Arabic/Persian letter forms, tatweel, presentation forms.
- **Zero dependencies**, pure Python 3.9+, fully typed (`py.typed`, mypy strict), command-line tool included.

## Installation

**Python** (3.9+):

```bash
pip install git+https://github.com/artemmarus/translit-names.git
```

**TypeScript / JavaScript** (Node.js 18+, browsers) — see [js/README.md](js/README.md):

```ts
import { transliterate, variants, similarity, mrzName } from "translit-names";

transliterate("Щербаков Юрий");               // "Shcherbakov Iurii"
variants("محمد", { limit: 4 });               // ["Muhammad", "Mohammed", "Mohamed", "Mohammad"]
similarity("Мухаммед Али", "Mohammed Ali");   // 0.985
```

The TypeScript package is a port of the Python one built from the same JSON data; CI checks that both give identical results on ~11,700 reference cases (`scripts/gen_parity_fixtures.py` → `js/test/parity.test.ts`).

## Usage

### Transliterate

```python
from translit_names import transliterate, list_schemes

transliterate("Щербаков Юрий")                    # 'Shcherbakov Iurii'   (language detected: ru)
transliterate("Щербаков Юрий", "ru_mvd_310")      # 'Shcherbakov Yuriy'   (passports 1997–2010)
transliterate("Ксения", "ru_mvd_310_fr")          # 'Xeniia'              (Soviet French-style)
transliterate("Олександр Згурський")              # 'Oleksandr Zghurskyi' (Ukrainian, KMU 2010)
transliterate("Нұрсұлтан Назарбаев")              # 'Nursultan Nazarbayev'
transliterate("محمد بن سلمان")                     # 'Muhammad bin Salman'
transliterate("عبد الرحمن", "ar_ala_lc")           # 'ʻAbd al-Raḥmān'
transliterate("حسین")                             # 'Hossein'             (Persian)
transliterate("Христо Стоичков", language="bg")  # 'Hristo Stoichkov'

[s.id for s in list_schemes("uk")]
# ['uk_ala_lc', 'uk_iso_9', 'uk_kmu_2010', 'uk_national_1996', 'uk_passport_2007', 'uk_scientific']
```

Without a scheme, the language is detected from the letters and its default scheme is used: the current passport system for Cyrillic languages, practical English for Arabic-script names. Names that contain no language-specific letter (Олександр is valid Russian spelling too) are best transliterated with an explicit `language=`. All schemes are listed in [docs/SCHEMES.md](docs/SCHEMES.md).

### Spelling variants

```python
from translit_names import variants, variants_detailed

variants("Юрий", limit=6)      # ['Iurii', 'Yuri', 'Yury', 'Yuriy', 'Iury', 'Iuri']
variants("Хусейн", limit=6)    # ['Khusein', 'Hussein', 'Gusein', 'Husein', 'Khuseyn', 'Khusain']
variants("Евгений Щербаков")   # 'Evgenii Shcherbakov', 'Yevgeny Shcherbakov', 'Evgeny Shcherbakov' …

for v in variants_detailed("محمد", limit=3):
    print(v.score, v.text, v.sources)
```

Variants come from every applicable scheme (weighted: current passport > practical > superseded passport > geographic > library), from the lexicon and from rewrite rules for systematic alternations. Pass `include_short=True` for diminutives (Sasha), `ascii_only=False` to keep diacritics (Hüseyin).

### Matching names

```python
from translit_names import similarity, compare, is_match, name_key

similarity("Щербаков Юрий", "Yuri Scherbakov")   # 0.977
similarity("Hasan", "Husayn")                    # 0.6  — two different names
is_match("Магомед", "Mehmet")                    # True — the same name (Muhammad)

r = compare("Ivanov Ivan Ivanovich", "IVAN IVANOV")
r.score            # 0.96 — the missing patronymic costs a little
r.pairs            # (PartMatch('Ivan', 'IVAN', 1.0, 'exact'), PartMatch('Ivanov', 'IVANOV', 1.0, 'exact'))
r.unmatched_left   # ('Ivanovich',)

name_key("Мухаммед Али") == name_key("Mohammed Ali")   # True — use as a blocking key
```

Each matched pair carries a reason: `exact`, `same-name` (lexicon), `skeleton`, `skeleton-coarse`, `fuzzy`, `initial`, `diminutive` (Саша ~ Александр, 0.86), `equivalent` (Michael ~ Михаил, 0.80 — a translation, not a transliteration) or `different-names` (both known, but different: capped at 0.6). The default threshold of `is_match` is 0.88.

### Passport MRZ

```python
from translit_names import mrz_name, mrz_text, parse_mrz_name

mrz_name("Щербаков", "Юрий")                 # 'SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<'
mrz_name("al-Basri", "Huda Muhammad Jawad")  # 'AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<<<<<<<'
mrz_name("Əliyev", "İlham")                  # 'ALIYEV<<ILHAM<<<<<<<<<<<<<<<<<<<<<<<<<<'
mrz_name("…", "…", length=30, strategy="initials")   # TD1 ID card, shorten given names to initials
mrz_text("D'Artagnan")                       # 'DARTAGNAN'
parse_mrz_name("AL<BASRI<<HUDA<MUHAMMAD")    # ('AL BASRI', 'HUDA MUHAMMAD')
```

### Language detection and clean-up

```python
from translit_names import detect_language, normalize, fix_mixed_script

detect_language("Олександр Їжакевич")   # Detection(language='uk', script='Cyrl', confidence=…)
detect_language("محمود احمدی‌نژاد").language   # 'fa'
fix_mixed_script("Иванoв")               # 'Иванов'  (the 'o' was Latin)
normalize("Ёлкин")                 # 'Ёлкин'
```

### Command line

```bash
translit-names "Щербаков Юрий"                     # Shcherbakov Iurii
translit-names translit --all "Юрий"               # every Russian scheme side by side
translit-names variants --scores "Хусейн"
translit-names match "Мухаммед Али" "Mohammed Ali" # exit code 0 if they match
translit-names mrz Щербаков Юрий
translit-names detect "Нұрсұлтан"
translit-names schemes -l kk
cat names.txt | translit-names -s uk_kmu_2010      # one name per line
```

## How it works

1. **Schemes are data.** Every standard is a JSON file in [`src/translit_names/data/schemes/`](src/translit_names/data/schemes) — a letter map plus context rules (word start/end, previous/next letter, letter classes), as defined in [docs/data-format.md](docs/data-format.md). The engine does longest-match substitution and restores capitalisation from the source (`Щ` → `Shch`, `ЩЕРБАКОВ` → `SHCHERBAKOV`). Every `sample` in a scheme file is a test.
2. **Arabic script is vocalised first**: vowel marks in the input are respected; known names are replaced by their vowelled form (or, for practical schemes, by their conventional spelling); unknown names are vocalised by template; the rest is romanised letter by letter.
3. **Variants** combine all schemes of the language, the lexicon and rewrite rules ([`variant_rules.json`](src/translit_names/data/variant_rules.json)) with plausibility scores.
4. **Matching** converts both names to Latin, splits them into parts and aligns the parts in the best order; parts are compared by lexicon cluster, then skeleton keys, then Jaro–Winkler.

### Benchmark

`python scripts/benchmark.py` measures the lexicon-free machinery on pairs drawn from the lexicon (threshold 0.88):

| Metric | Value |
|---|---|
| Same-name recall, Latin vs Latin, **without lexicon** | 0.80 |
| Same-name recall, native script vs Latin, without lexicon | 0.93 |
| False-positive rate on random different names | 0.000 |
| Conventional Russian spellings proposed by `variants()` without lexicon (top 30) | 0.78 |
| Speed (pure Python) | ~5,000 comparisons/s |

With the lexicon enabled (the default), all spellings of known names match.

## Accuracy and limitations

- **There is no single correct spelling.** Countries change their passport tables (Russia: 1997, 2010, 2013) and several countries (Russia, Ukraine, Bulgaria, Belarus, Kyrgyzstan since 2026) let citizens choose their spelling. Use `variants()` and `similarity()` for search, not string equality.
- **Passport practice for some countries is not published.** The schemes for Kazakh, Kyrgyz, Tajik, Turkmen, Uzbek and Azerbaijani passports and for Belarusian passports follow observed practice; they are marked `status: informal` and their notes describe the evidence.
- **Unvowelled Arabic-script names outside the lexicon are guessed.** Template vocalisation is right for common Arabic name patterns but can be wrong; give vowel marks in the input when accuracy matters.
- **ICAO Doc 9303 has known errors** in its Cyrillic table (Serbian Г→H, Һ→C, Macedonian GJ on the wrong letter); they are not reproduced.
- **ISO 233 and parts of DIN 31635** are behind a paywall; those schemes rely on published descriptions (see each file's `notes`).

## Research

The design is based on a research report (in Russian) on how names from Muslim-majority and Slavic countries are romanised: official standards, passport practice, name structure, existing libraries and matching techniques — [docs/research/README.md](docs/research/README.md), with detailed source notes in [docs/research/notes/](docs/research/notes).

## Contributing

Corrections with a link to the primary source are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Most contributions are JSON data, not code.

## License

[MIT](LICENSE). Transliteration tables are facts taken from public laws and standards; sources are cited in every scheme file.
