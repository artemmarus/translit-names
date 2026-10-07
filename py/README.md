# translit-names (Python)

[![CI](https://github.com/artemmarus/translit-names/actions/workflows/ci.yml/badge.svg)](https://github.com/artemmarus/translit-names/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%20%E2%80%93%203.14-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/artemmarus/translit-names/blob/main/LICENSE)

**Transliteration, spelling variants and cross-script matching of personal names from Slavic and Muslim-majority countries.** Pure Python 3.9+, zero dependencies, fully typed.

Part of the [`translit-names`](https://github.com/artemmarus/translit-names) project; the [TypeScript package](https://github.com/artemmarus/translit-names/tree/main/js) uses the same data and gives identical results.

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

## Installation

```bash
pip install "git+https://github.com/artemmarus/translit-names.git#subdirectory=py"
```

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

Without a scheme, the language is detected from the letters and its default scheme is used: the current passport system for Cyrillic languages, practical English for Arabic-script names. Names that contain no language-specific letter (Олександр is valid Russian spelling too) are best transliterated with an explicit `language=`. All 85 schemes are listed in [docs/SCHEMES.md](https://github.com/artemmarus/translit-names/blob/main/docs/SCHEMES.md).

### Spelling variants

```python
from translit_names import variants, variants_detailed

variants("Юрий", limit=6)      # ['Iurii', 'Yuri', 'Yury', 'Yuriy', 'Iury', 'Iuri']
variants("Хусейн", limit=6)    # ['Khusein', 'Hussein', 'Gusein', 'Husein', 'Khuseyn', 'Khusain']
variants("Евгений Щербаков")   # 'Evgenii Shcherbakov', 'Yevgeny Shcherbakov', 'Evgeny Shcherbakov' …

for v in variants_detailed("محمد", limit=3):
    print(v.score, v.text, v.sources)
```

Variants come from every applicable scheme (weighted: current passport > practical > superseded passport > geographic > library), from the lexicon and from rewrite rules for systematic alternations. Pass `include_short=True` for diminutives (Sasha), `ascii_only=False` to keep diacritics (Hüseyin), `use_lexicon=False` to rely on schemes and rules only.

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
mrz_name(surname, given, length=30, strategy="initials")   # TD1 ID card
mrz_text("D'Artagnan")                       # 'DARTAGNAN'
parse_mrz_name("AL<BASRI<<HUDA<MUHAMMAD")    # ('AL BASRI', 'HUDA MUHAMMAD')
```

### Language detection and clean-up

```python
from translit_names import detect_language, normalize, fix_mixed_script

detect_language("Олександр Їжакевич")          # Detection(language='uk', script='Cyrl', confidence=…)
detect_language("محمود احمدی‌نژاد").language   # 'fa'
fix_mixed_script("Иванoв")                     # 'Иванов'  (the 'o' was Latin)
normalize("Е\u0308лкин")                       # 'Ёлкин'   (NFC, spaces, dashes, digits)
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

## Data

Schemes, the name lexicon and the variant rules are JSON files in the repository's [`data/`](https://github.com/artemmarus/translit-names/tree/main/data) directory (format: [docs/data-format.md](https://github.com/artemmarus/translit-names/blob/main/docs/data-format.md)); the build bundles them into the package as `translit_names/data`.

## License

MIT
