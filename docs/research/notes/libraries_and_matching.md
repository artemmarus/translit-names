# Libraries, data and techniques for transliterating and matching personal names (Cyrillic/Slavic and Arabic/Persian/Urdu/Turkic → Latin), state as of October 2026

Method note: package metadata (versions, release dates, licenses, dependencies) was pulled live from the PyPI JSON API, the npm registry and the GitHub API on 2026-10-07. Star counts are approximate as of that date. Rows marked **[empirical]** come from running the libraries locally on real names in this session (macOS, Python 3.9 venv, ICU 78.3 `uconv`). Because the venv used Python 3.9, pip installed iuliia 0.11.5 rather than 0.13.0, which needs Python ≥3.10. The iuliia schema data bug reported below was also confirmed in the upstream master JSON.

---

## 1. Python transliteration libraries (Cyrillic-focused and "any-to-ASCII"): purpose, status, license, and quality on names

### Takeaway
No maintained, permissively licensed Python library handles personal names well across Slavic and Turkic Cyrillic languages:
- **iuliia** has the best Russian name schemas, but its repos are now **archived**. It covers Russian and Uzbek only, and some of its schemas leak Cyrillic `ё` into the output.
- **transliterate** has had no PyPI release since 2018 and uses an idiosyncratic, non-standard scheme.
- **cyrtranslit** uses GOST-7.79 System B digraphs (`shh`, `cz`) and has a casing bug.
- **Unidecode** is GPL and context-free.
- **anyascii** (ISC) is the best permissive universal fallback, but it ignores the language (for example, it gives Ukrainian Г → G).

### Cited Findings

**Metadata (PyPI and GitHub, 2026-10-07)**
- **transliterate** (barseghyanartur): "Bi-directional transliterator for Python… according to the rules specified in the language packs".
  - Last PyPI release is 1.10.2 from **2018-09-17**, although the repo was still being pushed to in 2026-03.
  - About 314★. PyPI license is "GPL 2.0/LGPL 2.1"; GitHub shows no SPDX license.
  - Language packs: `hy, mn, el, ru, uk, sr, mk, bg, ka, l1`. No Kazakh, Uzbek, Kyrgyz or Tajik, and no Arabic script.
  - Sources: [PyPI](https://pypi.org/project/transliterate/), [GitHub](https://github.com/barseghyanartur/transliterate)
- **cyrtranslit**: MIT, v1.2.0 released **2025-11-20**, about 124★, zero dependencies. The API is `to_latin(text, lang)` / `to_cyrillic`. — [PyPI](https://pypi.org/project/cyrtranslit/), [GitHub](https://github.com/opendatakosovo/cyrillic-transliteration)
- **iuliia** (nalgeon): MIT, latest 0.13.0 released 2025-01-05, requires Python ≥3.10, zero dependencies.
  - The GitHub repos `nalgeon/iuliia` (schemas, about 73★) and `nalgeon/iuliia-py` (about 127★) are **archived** (read-only). The JS port `iuliia-js` is archived too.
  - Pitch from the README: "20 Russian transliteration schemas… Official Uzbek transliteration schema… zero third-party dependencies".
  - API: `iuliia.WIKIPEDIA.translate("Юлия Щеглова")` → `'Yuliya Shcheglova'`.
  - Sources: [PyPI](https://pypi.org/project/iuliia/), [iuliia-py](https://github.com/nalgeon/iuliia-py), [iuliia schemas](https://github.com/nalgeon/iuliia)
- **iuliia schema list [empirical]**: `ala_lc, ala_lc_alt, bgn_pcgn, bgn_pcgn_alt, bs_2979, bs_2979_alt, gost_16876, gost_16876_alt, gost_52290, gost_52535, gost_7034, gost_779, gost_779_alt, icao_doc_9303, iso_9_1954, iso_9_1968, iso_9_1968_alt, mosmetro, mvd_310, mvd_310_fr, mvd_782, scientific, telegram, ungegn_1987, wikipedia, yandex_maps, yandex_money` (uz is in 0.13). — [iuliia-py](https://github.com/nalgeon/iuliia-py)
- **iuliia data format**: each schema is JSON with `mapping`, `prev_mapping`, `next_mapping` and `ending_mapping`, which give contextual rules. For example, BGN/PCGN `е` → `ye` after vowels or ъ/ь, and `тс` → `t·`. This is a good model for a names package. — [bgn_pcgn.json](https://raw.githubusercontent.com/nalgeon/iuliia/master/bgn_pcgn.json)
- **iuliia's stated limitations**: "Supports only the Russian and Uzbek Cyrillic subsets" and it does not support decomposed Unicode such as Е+◌̈. MVD-310's "С between two vowels → SS" rule is ignored. — [iuliia README](https://github.com/nalgeon/iuliia/blob/master/README.md#issues-and-limitations)
- **iuliia data bug [empirical, plus confirmed in upstream JSON]**: in `ala_lc.json` the key `ё` (U+0451) maps to `ё` (U+0451), meaning Cyrillic is emitted instead of Latin `ë`.
  - `iuliia.translate("Пётр Ёлкин", ala_lc)` → `Pёtr Ёlkin`, with Cyrillic U+0451 and U+0401 left in the output.
  - The same leak appears for `bgn_pcgn` (`Yёlkin Pёtr`), `scientific` and `gost_779`.
  - Because the repo is archived, this will not be fixed upstream.
  - Source: [ala_lc.json](https://raw.githubusercontent.com/nalgeon/iuliia/master/ala_lc.json)
- **Unidecode**: v1.4.0 released **2025-04-24**, license **GPLv2+**, about 611★ on the GitHub mirror. — [PyPI](https://pypi.org/project/Unidecode/), [GitHub](https://github.com/avian2/unidecode)
- **text-unidecode**: v1.3 from 2019-08-30, dual-licensed **Artistic or GPL** ("choose whatever you want"). It is the default dependency of python-slugify. — [PyPI](https://pypi.org/project/text-unidecode/), [GitHub](https://github.com/kmike/text-unidecode)
- **anyascii**: **ISC** license, v0.3.3 released 2025-06-29, about 423★. Ports exist for C, Elixir, Go, Java, JS, Julia, PHP, Python, Ruby, Rust, Shell and .NET. — [PyPI](https://pypi.org/project/anyascii/), [GitHub](https://github.com/anyascii/anyascii)
- **translitcodec**: MIT, last release 0.7.0 on 2021-05-08 (repo active 2026-07). It is a "Unicode to 8-bit charset transliteration codec", which makes it a diacritic stripper rather than a name transliterator. — [PyPI](https://pypi.org/project/translitcodec/), [GitHub](https://github.com/claudep/translitcodec)
- **trans**: BSD, last release 2.1.0 on **2016-08-19**, abandoned. — [PyPI](https://pypi.org/project/trans/), [GitHub](https://github.com/zzzsochi/trans)
- **Other small packages**: `translit` (LGPLv3+, 0.2, 2026-06) and `unihandecode` (GPLv3/Perl, 2020). Neither is names-oriented. — [PyPI translit](https://pypi.org/project/translit/), [PyPI unihandecode](https://pypi.org/project/unihandecode/)
- **python-slugify**: MIT, v9.1.3 released 2026-10-07. Its default backend is `text-unidecode`, with optional extras `unidecode` and `anyascii`. It is useful only as a fallback model of "pluggable backends". — [PyPI](https://pypi.org/project/python-slugify/), [GitHub](https://github.com/un33k/python-slugify)

**Quality on real names [empirical, 2026-10-07]**

| Input | iuliia ICAO_DOC_9303 | iuliia BGN_PCGN | iuliia WIKIPEDIA | transliterate (ru) | cyrtranslit (ru) | Unidecode | anyascii |
|---|---|---|---|---|---|---|---|
| Щербаков Юрий | Shcherbakov Iurii | Shcherbakov Yuriy | Shcherbakov Yury | Scherbakov Jurij | **SHHerbakov** Yurij | Shcherbakov Iurii | Shcherbakov Yuriy |
| Ёлкин Пётр | Elkin Petr | **Yёlkin Pёtr** (Cyrillic leak) | Yolkin Pyotr | Elkin Petr | YOlkin Pyotr | **Iolkin Piotr** | Elkin Petr |
| Наталья Ильинична | Natalia Ilinichna | Natal’ya Il’inichna | Natalya Ilyinichna | Natal'ja Il'inichna | Natal'ya Il'inichna | Natal'ia Il'inichna | Natal'ya Il'inichna |
| Евгений Объедков | Evgenii **Obieedkov** | Yevgeniy Ob”yedkov | Yevgeny Obyedkov | Evgenij Ob'edkov | Evgenij Ob''edkov | Evgenii Ob'edkov | Evgeniy Ob'edkov |
| Ксения Цой | Kseniia Tsoi | Kseniya Tsoy | Kseniya Tsoy | Ksenija Tsoj | Kseniya **CZoj** | Kseniia Tsoi | Kseniya Tsoy |
| Мухаммед Алиев | Mukhammed Aliev | Mukhammed Aliyev | Mukhammed Aliyev | Muhammed Aliev | Muhammed Aliev | Mukhammed Aliev | Mukhammed Aliev |

Sources: [iuliia](https://pypi.org/project/iuliia/), [transliterate](https://pypi.org/project/transliterate/), [cyrtranslit](https://pypi.org/project/cyrtranslit/), [Unidecode](https://pypi.org/project/Unidecode/), [anyascii](https://pypi.org/project/anyascii/).

What the table shows:
- **cyrtranslit**: title-cased input with Щ gives `SHHerbakov`, and Ц gives `CZ`. Its Russian output follows a GOST 7.79 System-B style (`shh`, `cz`), which is unsuitable for names.
- **transliterate**: uses `j` for й/ю/я (`Jurij`, `Ksenija`). That matches none of the passport, BGN or common-English conventions.
- **Unidecode**: renders ё as `io` (`Iolkin Piotr`).
- **iuliia ICAO**: turns ъ into `ie` (`Obieedkov`). This is faithful to ICAO Doc 9303 but surprising to users.

Non-Russian Cyrillic **[empirical]**:
- **Ukrainian** "Олександр Григорій / Юлія Тимошенко":
  - transliterate `uk`: `Oleksandr Hryhorij`, `Julija Tymoshenko`
  - cyrtranslit `ua`: `Hryhorij`, `Tymošenko` (diacritics)
  - Unidecode: `Grigorii`, `Iuliia Timoshenko`
  - anyascii: `Grigoriy`, `Yuliya Timoshenko`
  - Unidecode and anyascii ignore the language: Г becomes G instead of H, and и becomes i instead of y.
  - None of them produces the official Ukrainian KMU-2010 forms (`Hryhorii`, `Yuliia Tymoshenko`).
- **Kazakh** "Жұмабек Нұрғали / Әлихан Бөкейхан":
  - Unidecode: `Zhu'mabek Nu'rg'ali`, `@likhan` (Ә → `@`)
  - anyascii: `Zhumabek Nurghali`, `Alikhan Bokeykhan`, which is reasonable.

Arabic script **[empirical]**: "محمد عبد الله"
- Unidecode: `mHmd `bd llh`
- anyascii: `mhmd `bd llh`
- "حسین رضایی" → Unidecode `Hsyn rDyy`
- "عائشة" → Unidecode `` `y'sh@ ``, anyascii `` `i'shh ``
- All of them produce consonant skeletons with no vowels.

Sources: [Unidecode](https://pypi.org/project/Unidecode/), [anyascii](https://pypi.org/project/anyascii/).

### Inferences
- iuliia's JSON schemas (MIT) are the most reusable asset for Russian. They can be vendored with attribution, but they need a patch for the `ё` leak and an extension to other Cyrillic alphabets. Since the project is archived, a new package can position itself as its successor.
- anyascii is the best permissive "last resort" fallback for unknown scripts. Unidecode, text-unidecode and pyphonetics should not be dependencies of an MIT or Apache package because of GPL contamination. text-unidecode's Artistic option is legally usable, but it is stale.
- For names, "one ASCII form" is the wrong output model. The table shows at least four legitimate spellings of Юрий (Iurii, Yuriy, Yury, Yuri). Each is "correct" under a different authority, which argues for scheme-explicit output plus variant generation.

### Gaps
- Not verified: whether iuliia 0.13.0 (Python ≥3.10) fixed the `ё` leak in code. The master JSON still contains the bug, which suggests not.
- The full cyrtranslit language list was not re-checked in this session. It is known to include ru, ua, sr, me, mk, bg, mn and tj.

---

## 2. ICU/PyICU and Arabic-script and "universal" tools (camel-tools, pyarabic, uroman, Nisaba, Aksharamukha, epitran, lingua, Polyglot)

### Takeaway
ICU transforms are the most complete rule-based engine, with BGN/PCGN rules for Russian, Ukrainian, Belarusian, Kazakh, Kyrgyz, Uzbek, Azerbaijani, Turkmen, Persian, Pashto and Arabic. But:
- PyICU is still **sdist-only**, so it needs the ICU C library and a compiler.
- The Arabic-script transforms produce unvowelled scholarly skeletons, and some leave letters untransliterated.
- There is no Urdu-Latin transform.

The Arabic NLP toolkits (camel-tools, pyarabic) provide scholarly, reversible schemes (Buckwalter, HSB) and normalization, but not English-style name romanization.

### Cited Findings

**PyICU and its alternatives**
- **PyICU** v2.16.2 was released 2026-03-20 and ships **only `pyicu-2.16.2.tar.gz`** on PyPI, with no wheels. The project moved to gitlab.pyicu.org, and the old GitHub repo is archived. — [PyPI](https://pypi.org/project/PyICU/), [GitHub (archived)](https://github.com/ovalhub/pyicu)
- Third-party wheel projects exist: `pyicu-wheels` 2.15.2 (2026-03-11) and the stale `PyICU-binary` 2.7.4 (2021). — [PyPI pyicu-wheels](https://pypi.org/project/pyicu-wheels/), [PyPI PyICU-binary](https://pypi.org/project/PyICU-binary/)
- **icu4py** (Adam Johnson, new in 2026, v1.1.0 on 2026-04-02, MIT) ships wheels. Its modules are `breakers`, `locale` and `messageformat`, so there is **no Transliterator yet**. — [PyPI](https://pypi.org/project/icu4py/), [GitHub](https://github.com/adamchainz/icu4py)
- **ICU 78.3 transform IDs available [empirical, `uconv -L`]**:
  - Russian, Ukrainian and Belarusian: `Russian-Latin/BGN`, `Ukrainian-Latin/BGN`, `Belarusian-Latin/BGN`
  - Central Asian and Caucasus: `Kazakh-Latin/BGN`, `Kirghiz-Latin/BGN`, `Uzbek-Latin/BGN`, `Azerbaijani-Latin/BGN`, `Turkmen-Latin/BGN`, `Mongolian-Latin/BGN`
  - Arabic script: `Persian-Latin/BGN`, `Pashto-Latin/BGN`, `Arabic-Latin/BGN`, `Arabic-Latin`, `Maldivian-Latin/BGN`
  - Generic: `Cyrillic-Latin`, `Any-Latin`, `Latin-ASCII`, `Latin-Russian/BGN`, `de-ASCII`
  - **Urdu-Latin is not in the list**: `uconv -x "Urdu-Latin"` returns `U_INVALID_ID`.
  - Sources: [ICU transforms user guide](https://unicode-org.github.io/icu/userguide/transforms/general/), [CLDR transforms directory](https://github.com/unicode-org/cldr/tree/main/common/transforms)
- **ICU on Cyrillic names [empirical]**, input `Щербаков Юрий Ёлкин Пётр Наталья Объедков Ксения Цой | Олександр Григорій | Жұмабек Әлихан`:
  - `Russian-Latin/BGN` → `Shcherbakov Yuriy Yëlkin Pëtr Natalʹya Obʺyedkov Kseniya Tsoy`. It needs ASCII folding for the modifier letters ʹ ʺ and for ë. Applied to Ukrainian and Kazakh text it leaves Cyrillic `і`, `ұ`, `Ә` untouched (`Grigorіy`, `Zhұmabek`, `Әlikhan`).
  - `Any-Latin; Latin-ASCII` → `Serbakov Urij Elkin Petr … Ksenia Coj`. This is ISO 9 folded to ASCII, so Щ becomes `S` and Ю becomes `U`, which is **destructive for names**. Schwa survives (`Əlihan`), so the result is not even pure ASCII.
  - `Ukrainian-Latin/BGN` on Russian text leaves `Ё` and `ъ`, and gives `Hryhoriy` for Ukrainian.
  - `Uzbek-Latin/BGN` leaves `Щ`.
  - Source: [ICU user guide](https://unicode-org.github.io/icu/userguide/transforms/general/)
- **ICU on Arabic-script names [empirical]**, input `محمد عبد الله | عبد الرحمن بن علي | حسین رضایی | پرویز | عائشة`:
  - `Arabic-Latin` → `mḥmd ʿbd ạllh | ʿbd ạlrḥmn bn ʿly | ḥsy̰n rḍạy̰y̰ | prwy̰z | ʿạỷsẖẗ`
  - `Arabic-Latin/BGN` leaves Persian `ی`/`پ` and Arabic `ي` untransliterated.
  - `Persian-Latin/BGN` → `ḥsyn rẕاyy`, leaving alef `ا` in the output, and `‘ئshh` for عائشة.
  - `Any-Latin; Latin-ASCII` → `mhmd ʿbd allh` (ʿ remains).
  - Source: [CLDR Arabic-Latin.xml](https://github.com/unicode-org/cldr/blob/main/common/transforms/Arabic-Latin.xml)

**normality and rigour (OpenSanctions)**
- **normality** v3.x (MIT, v3.1.0 on 2026-03-08) now **hard-requires `pyicu>=2.10.0`**.
  - Its `ascii_text` uses the chain `"Any-Latin; NFKD; [:Nonspacing Mark:] Remove; Accents-Any; [:Symbol:] Remove; [:Nonspacing Mark:] Remove; Latin-ASCII"`. The code comment calls this chain "becoming a bit silly".
  - The module docstring still claims it avoids GPL and C dependencies, but the code imports `icu` unconditionally.
  - Sources: [normality transliteration.py](https://github.com/pudo/normality/blob/main/normality/transliteration.py), [PyPI](https://pypi.org/project/normality/)
- **rigour 2.x** (OpenSanctions) is built with **maturin/Rust** (ICU4X) and ships wheels for all major platforms.
  - Its transliteration "Covers only six admitted scripts (Latin, Cyrillic, Greek, Armenian, Georgian, Hangul)… For broader-script, lossy transliteration (Han, Arabic, Devanagari, etc.) use `normality.ascii_text`… rigour deliberately does not try to duplicate that surface."
  - Sources: [rigour translit.py](https://github.com/opensanctions/rigour/blob/main/rigour/text/translit.py), [rigour pyproject](https://github.com/opensanctions/rigour/blob/main/pyproject.toml)

**Arabic NLP toolkits**
- **camel-tools** (NYU Abu Dhabi CAMeL Lab): MIT, v1.6.0 on 2026-06-08, about 583★, requires **Python ≥3.11**.
  - Dependencies are heavy: `camel-kenlm`, `dill`, `editdistance`, `emoji`, `muddler`, `cachetools` and others.
  - Charmaps: `ar2bw, ar2safebw, ar2xmlbw, ar2hsb, bw2ar, bw2hsb, bw2safebw, bw2xmlbw, hsb2ar, hsb2bw, hsb2safebw, hsb2xmlbw, safebw2*`, plus `arclean`.
  - These are reversible scholarly schemes, not English-style romanization.
  - Sources: [PyPI](https://pypi.org/project/camel-tools/), [charmaps dir](https://github.com/CAMeL-Lab/camel_tools/tree/master/camel_tools/utils/charmaps), [transliterate docs](https://camel-tools.readthedocs.io/en/latest/api/utils/transliterate.html)
- camel-tools normalization functions: `normalize_unicode` (NFC/NFKC), `normalize_alef_*` ("various Alef variations to plain Alef"), `normalize_alef_maksura_*` (ى→ي) and `normalize_teh_marbuta_*` (ة→ه), each for ar/bw/safebw/xmlbw/hsb. — [camel normalize docs](https://camel-tools.readthedocs.io/en/latest/api/utils/normalize.html)
- **pyarabic**: **GPL**, last PyPI release 0.6.15 on 2022-06-18, about 492★. — [PyPI](https://pypi.org/project/PyArabic/), [GitHub](https://github.com/linuxscout/pyarabic)
- The rest of the Arabic ecosystem by the same author is also GPL: Qalsadi (2025), Tashaphyne (2022) and Mishkal (diacritizer, 2021). — [PyPI qalsadi](https://pypi.org/project/qalsadi/), [PyPI mishkal](https://pypi.org/project/mishkal/)
- Small Arabic transliteration packages on PyPI are Buckwalter-only:
  - `arabic-buckwalter-transliteration` (MIT, 1.0.5, 2023)
  - `lang-trans` (Apache-2.0, 0.6.0, 2018)
  - No maintained PyPI package does Arabic → English-style name romanization. Names tried without success: `arabic-romanizer`, `persian-transliterate`, `ar-translit`.
  - Sources: [PyPI arabic-buckwalter-transliteration](https://pypi.org/project/arabic-buckwalter-transliteration/), [PyPI lang-trans](https://pypi.org/project/lang-trans/)

**Universal romanizers and G2P**
- **uroman** (USC/ISI, Ulf Hermjakob): Python 1.3.1.1 released 2024-06-28 (Perl 1.2.8 from 2021), requires Python ≥3.10, depends on `regex`. It is "not fully reversible" and "does not vowelize text that lacks explicit vowelization such as normal text in Arabic and Hebrew".
  - License metadata conflicts: the PyPI classifier says Apache, while LICENSE.txt contains MIT-style permission text, "Copyright (C) 2015-2024 Ulf Hermjakob".
  - Sources: [GitHub](https://github.com/isi-nlp/uroman), [PyPI](https://pypi.org/project/uroman/), [LICENSE](https://github.com/isi-nlp/uroman/blob/master/LICENSE.txt)
- **Google Nisaba**: Apache-2.0, about 54★, active (pushed 2026-09-02), "Finite-state script normalization and processing utilities".
  - It is not on PyPI under that name. PyPI's `nisaba` is an **unrelated AGPL** "multi-modal annotation" tool, which is a name-collision trap.
  - Sources: [GitHub](https://github.com/google-research/nisaba), [PyPI nisaba (unrelated)](https://pypi.org/project/nisaba/)
- **Aksharamukha**: **AGPL-3.0**, v2.3 on 2024-10-14. Dependencies are heavy (requests, pykakasi, pyyaml, langcodes, fonttools, lxml, regex), and it focuses on Indic/Asian scripts. — [PyPI](https://pypi.org/project/aksharamukha/), [GitHub](https://github.com/virtualvinodh/aksharamukha)
- **epitran** (orthography → IPA G2P): MIT, v1.35.2 on 2026-06-18, about 841★. Dependencies include panphon, marisa-trie, requests and jamo.
  - Relevant maps: `rus-Cyrl, ukr-Cyrl, kaz-Cyrl, kaz-Latn, kir-Cyrl, kir-Arab, uzb-Cyrl, uzb-Latn, tgk-Cyrl, tuk-Cyrl/Latn, aze-Cyrl/Latn, tur-Latn, ara-Arab, fas-Arab, urd-Arab, uig-Arab, ckb-Arab`.
  - Sources: [PyPI](https://pypi.org/project/epitran/), [GitHub map dir](https://github.com/dmort27/epitran/tree/master/epitran/data/map)

**Language detection**
- **lingua** (`lingua-language-detector`): Apache-2.0, v2.2.0 on 2026-03-09, Rust-backed, **requires Python ≥3.12**, about 1.8k★. The README claims accuracy "even on single words and phrases" and benchmarks on single words of length ≥5. — [PyPI](https://pypi.org/project/lingua-language-detector/), [GitHub](https://github.com/pemistahl/lingua-py)
- **Polyglot**: GPLv3, last PyPI release 16.7.4 on **2016-07-03**, unmaintained. — [PyPI](https://pypi.org/project/polyglot/), [GitHub](https://github.com/aboSamoor/polyglot)

**Unicode data**
- **unicodedata2**: Apache-2.0, 18.0.0rc1 on 2026-09-18, a backport of the newest UCD. It is useful if a package must pin Unicode behaviour independently of the running Python. — [PyPI](https://pypi.org/project/unicodedata2/)

### Inferences
- ICU's BGN rule files (CLDR XML) are a good *source of rules to port* into pure-Python tables. CLDR data is under the permissive Unicode license ([Unicode license](https://www.unicode.org/license.txt)). Depending on PyICU at runtime is a poor fit for a lightweight library, because it is sdist-only and needs a C build.
- For Arabic, Persian and Urdu, rule-based romanization from unvowelled script cannot produce "Muhammad" from محمد. A names package needs a **lexicon of vocalized name forms**, covering common Muslim given names and theophoric compounds, plus rules only as a fallback that outputs a consonant skeleton.
- lingua requires Python ≥3.12 and carries a large model, so it is too heavy as a core dependency. Script detection (Unicode Script property), plus language-specific letters (і/ї/є/ґ for Ukrainian, ә/ғ/қ/ң/ө/ұ/ү/һ for Kazakh, ў/ҳ/қ/ғ for Uzbek, پ/چ/ژ/گ for Persian, ٹ/ڈ/ڑ/ں/ے for Urdu), is cheap and decisive for names.

### Gaps
- I did not verify whether Nisaba exposes Python wheels (it is built on Pynini/OpenFst) or exactly which Perso-Arabic normalizations it covers. Only the repo description was checked.
- Polyglot's transliteration coverage and data provenance were not checked in this session.
- The internal quality of `Kazakh-Latin/BGN` looks odd: `Yurīī̆` for Юрий applied to Russian text. Kazakh input itself was not tested in depth.

---

## 3. Phonetic and string-similarity libraries (rapidfuzz, jellyfish, abydos, BMPM, Daitch–Mokotoff, pyphonetics, Double Metaphone)

### Takeaway
RapidFuzz (MIT, very active) and jellyfish (MIT, Rust core) are the safe permissive choices for edit-distance metrics. All English-centric phonetic codes (Soundex, Metaphone, NYSIIS, Match Rating) break on transliteration-induced variation such as `kh`/`h` and `tch`/`ch`. The only name-oriented, multi-language phonetic system (Beider–Morse, which has Russian, Polish, Arabic, Cyrillic and Turkish rules) is available in Python only through **GPL** abydos, which has been unmaintained since 2020.

### Cited Findings

**Metadata**
- **RapidFuzz**: MIT, v3.14.6 on 2026-08-30, about 4.15k★, requires Python ≥3.11, C++ core. It provides Levenshtein, Jaro-Winkler and token-sort/set ratios. — [PyPI](https://pypi.org/project/RapidFuzz/), [GitHub](https://github.com/rapidfuzz/RapidFuzz), [docs](https://rapidfuzz.github.io/RapidFuzz/)
- **jellyfish**: MIT, v1.2.1 on 2025-10-11, about 2.2k★ (canonical repo now on Codeberg). It provides `soundex, metaphone, nysiis, match_rating_codex`, plus Levenshtein, Damerau, Jaro and Jaro-Winkler. — [PyPI](https://pypi.org/project/jellyfish/), [GitHub](https://github.com/jamesturk/jellyfish), [docs](https://jellyfish.jpt.sh/)
- **abydos**: **GPLv3+**, last release 0.5.0 on **2020-01-11**, requires numpy.
  - The BMPM data defines name modes `gen`, `ash`, `sep` and languages `L_ARABIC, L_CYRILLIC, L_CZECH, L_DUTCH, L_ENGLISH, L_FRENCH, L_GERMAN, L_GREEK, L_GREEKLATIN, L_HEBREW, L_HUNGARIAN, L_ITALIAN, L_LATVIAN, L_POLISH, L_PORTUGUESE, L_ROMANIAN, L_RUSSIAN, L_SPANISH, L_TURKISH`.
  - Sources: [PyPI](https://pypi.org/project/abydos/), [_beider_morse_data.py](https://github.com/chrislit/abydos/blob/master/abydos/phonetic/_beider_morse_data.py), [docs](https://abydos.readthedocs.io/en/stable/_modules/abydos/phonetic/_beider_morse.html)
- **Beider–Morse Phonetic Matching**: designed by Alexander Beider (linguistics) and Stephen P. Morse. Its "sounds-alike" test is based "not only on spelling, but on linguistic properties of various languages". The name modes strip particles such as van, von and ben. — [stevemorse.org BMPM](https://stevemorse.org/phonetics/bmpm.htm), [Avotaynu article](https://avotaynuonline.com/2008/07/beider-morse-phonetic-matching-an-alternative-to-soundex-with-fewer-false-hits-by-alexander-beider-and-stephen-p-morse/)
- There are permissive (Apache-2.0) BMPM and Daitch–Mokotoff implementations in Java: Apache Commons Codec and the Solr `BeiderMorseFilter`. — [Solr phonetic matching](https://solr.apache.org/guide/phonetic-matching.html), [commons-codec](https://github.com/apache/commons-codec)
- **Daitch–Mokotoff Soundex**: invented in 1985 by Gary Mokotoff and Randy Daitch "to improve matching of Slavic and Yiddish surnames".
  - It produces 6-digit codes, encodes the first letter, encodes multi-letter n-grams, and can give **multiple codes per name**.
  - BMPM was developed later to address the "large number of false positive results generated by the D–M Soundex".
  - Source: [Wikipedia](https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex)
- **pyphonetics**: MIT, but **depends on `unidecode` (GPL)**, last release 2020. **Metaphone** (oubiwann): BSD, 2016. **DoubleMetaphone**: Artistic, 1.2 in 2025. **Fuzzy**: Artistic, 2017, C ext. — [PyPI pyphonetics](https://pypi.org/project/pyphonetics/), [PyPI Metaphone](https://pypi.org/project/Metaphone/), [PyPI DoubleMetaphone](https://pypi.org/project/DoubleMetaphone/), [PyPI Fuzzy](https://pypi.org/project/Fuzzy/)
- **nomquamgender** (MIT) depends on `unidecode` (GPL), pandas and numpy. **gender-guesser** is GPLv3 (2016). — [PyPI nomquamgender](https://pypi.org/project/nomquamgender/), [PyPI gender-guesser](https://pypi.org/project/gender-guesser/)

**Phonetic codes on transliteration variants [empirical, jellyfish 1.2.1]**

| Name | Soundex | Metaphone | NYSIIS | MRA codex |
|---|---|---|---|---|
| Muhammad | M530 | MHMT | MAHANAD | MHMD |
| Mohammed | M530 | MHMT | MAHANAD | MHMD |
| Mohamad | M530 | MHMT | MAHANAD | MHMD |
| **Mukhammed** (Russian route) | **M253** | **MKHMT** | **MACKANAD** | **MKHMD** |
| Shcherbakov | S612 | XXRBKF | SCARBACAV | SHCBKV |
| Scherbakov | S612 | SXRBKF | SARBACAV | SCHBKV |
| Tchernov | T265 | XRNF | TCARNAV | TCHRNV |
| Chernov | C651 | XRNF | CARNAV | CHRNV |

- Jaro-Winkler(Mohammed, Muhammad) = 0.85, and Levenshtein = 2.
- Source: [jellyfish](https://pypi.org/project/jellyfish/)

### Inferences
- The Russian-route spelling `Mukhammed` (kh for Arabic ح via Cyrillic Х) defeats every English phonetic key. Soundex also keeps the first letter, so `Tchernov` and `Chernov` never match.
- A cross-script names package needs its own **transliteration-aware skeleton**. It should canonicalize digraph families (kh/h/x/ḥ → H; sh/ch/tch/sch/shch/ş/š; ts/tz/c; zh/j/ž; y/j/i in ya/ja/ia, yu/ju/iu, ye/je/ie, yo/jo/io/ë) before collapsing vowels.
- Porting BMPM rules from Apache Commons Codec (Apache-2.0) is a clean-room-compatible path. Porting from abydos (GPL) would contaminate the license.

### Gaps
- Apache Commons Codec's BMPM rule-file license headers were not checked in this session. They are presumed Apache-2.0 because they ship in the Apache project.
- No benchmark numbers for BMPM against Double Metaphone on Russian or Arabic names were found.

---

## 4. JS/npm ecosystem (for comparison)

### Takeaway
npm has more maintained and far more popular generic transliterators, but they are equally names-agnostic. The only Russian standards-based one (iuliia-js) is archived.

### Cited Findings
- **transliteration** (yf-hk): MIT, 2.6.1 on 2026-01-20, about 642★, **about 1.0M downloads per week** (week of 2026-09-28). Covers "UTF-8 to ASCII transliteration / slugify". — [npm](https://www.npmjs.com/package/transliteration), [GitHub](https://github.com/yf-hk/transliteration)
- **any-ascii**: ISC, 0.3.3 on 2025-06-29, about 100k per week. — [npm](https://www.npmjs.com/package/any-ascii)
- **cyrillic-to-translit-js**: MIT, 3.2.1 on **2022-05-05**, about 19k per week. — [npm](https://www.npmjs.com/package/cyrillic-to-translit-js)
- **iuliia** (JS): MIT, 0.8.2 on 2022-01-26, about 1.2k per week, repo **archived**. — [npm](https://www.npmjs.com/package/iuliia), [GitHub](https://github.com/nalgeon/iuliia-js)
- **@sindresorhus/transliterate**: MIT, 2.3.1 on 2026-01-08, about 321★. — [npm](https://www.npmjs.com/package/@sindresorhus/transliterate), [GitHub](https://github.com/sindresorhus/transliterate)

### Inferences
- Demand for generic transliteration is high (about 1M per week on npm), but nothing on either ecosystem targets names with multiple standards, variants and matching.
- Shipping language-neutral JSON rule data would let a JS port reuse the same tables later, as iuliia and anyascii both do.

### Gaps
- No names-specific Arabic → Latin npm package was found. The search was not exhaustive.

---

## 5. Name-matching products and open-source stacks (OpenSanctions, Rosette/Babel Street, IBM GNR/GNM, Senzing)

### Takeaway
OpenSanctions' open stack (rigour, nomenklatura, yente, all MIT) is the most relevant prior art. It analyzes names into tagged parts and Wikidata-QID "symbols", aligns parts across names, and scores with weighted Levenshtein. However, it explicitly excludes Arabic-script transliteration from its Rust core, so it depends on ICU's lossy output. The commercial leaders (Babel Street/Rosette, IBM GNM, Senzing) describe two-pass candidate retrieval with culture-aware pairwise scoring, but publish few algorithmic details.

### Cited Findings

**OpenSanctions open stack**
- Package status:
  - **rigour** v2.5.0 on 2026-09-10 (MIT, about 68★): "Data cleaning and validation functions for names, languages, identifiers".
  - **fingerprints** repo: "Now included in rigour".
  - **nomenklatura** v4.17.1 on 2026-10-07 (MIT, about 268★).
  - **yente** v5.5.0 on 2026-06-23 (MIT, about 178★), an API for entity search and bulk matching that supports the Reconciliation API.
  - Sources: [rigour](https://github.com/opensanctions/rigour), [fingerprints](https://github.com/opensanctions/fingerprints), [nomenklatura](https://github.com/opensanctions/nomenklatura), [yente](https://github.com/opensanctions/yente)
- **rigour's name pipeline** runs end-to-end in Rust via PyO3.
  - A `Name` holds the original, a normalized `form`, a type tag (PER/ORG/ENT/OBJ/UNK), `parts` (NamePart with `form, tag, latinize, ascii, comparable, metaphone`) and `spans` carrying a `Symbol`.
  - Examples of symbols: "`NAME:Q4925477` for a recognised person name, `ORG_CLASS:LLC` for a legal form, `INITIAL:j` for a single-letter stand-in".
  - Source: [arch-name-pipeline.md](https://github.com/opensanctions/rigour/blob/main/plans/arch-name-pipeline.md)
- **rigour's normalization**:
  - Flags: STRIP, NFKD/NFKC/NFC, and **CASEFOLD**, described as "Unicode full casefold (e.g. ß → ss). Not the same as str.lower()".
  - Transliteration pipeline: per-script ICU4X transliterator (`und-Latn-t-und-{script}`) → NFKD + nonspacing-mark strip → CLDR Latin-ASCII → custom `ASCII_FALLBACK` overrides.
  - Source: [arch-text-normalisation.md](https://github.com/opensanctions/rigour/blob/main/plans/arch-text-normalisation.md)
- **nomenklatura logic-v2** (`match_name_symbolic`):
  - Pairs symbols between query and result via `rigour.names.symbol.pair_symbols`. Symbol categories get per-category scores and weights.
  - Unmatched parts get fuzzy scores and "extra" weights. Stopwords get `weight *= 0.7`, and a `family_name_weight` applies.
  - The final score is a weighted average. Object names use `strict_levenshtein(..., max_rate=5)`.
  - Sources: [match.py](https://github.com/opensanctions/nomenklatura/blob/main/nomenklatura/matching/logic_v2/names/match.py), [distance.py](https://github.com/opensanctions/nomenklatura/blob/main/nomenklatura/matching/logic_v2/names/distance.py)
- **OpenSanctions matcher docs**:
  - logic-v2 "uses cultural reference data for precise and explainable cross-language and cross-script matching".
  - The deprecated logic-v1 used Jaro-Winkler (weight 0.80) and Damerau-Levenshtein on fingerprinted names.
  - "name-based" combines Jaro-Winkler (0.5) with Soundex-style phonetics (0.5).
  - Source: [OpenSanctions matcher](https://www.opensanctions.org/matcher/)
- **OpenSanctions blog (2025-06)** stresses explainability and auditability for regulators. It also mentions published resources on org-type suffixes and "symbolic representations… multilingual equivalencies… for common name components", and integrations with Senzing, Quantifind, TiloRes and Quantexa. — [OpenSanctions blog](https://www.opensanctions.org/articles/2025-06-24-name-matching.md)

**Commercial products**
- **Babel Street Match / Rosette Name Indexer**: a "patented two-pass process". The first pass quickly generates candidates, and the second pass does pairwise scoring. It claims support for more than 24 languages and scripts, including Arabic, Russian and Urdu, using ML. — [Babel Street RNI](https://www.babelstreet.com/landing/understanding-rosette-name-indexer), [Babel Street Match docs](https://docs.babelstreet.com/Identity/en/babel-street-match.html)
- **IBM InfoSphere Global Name Recognition / Management**:
  - The NameHunter API manages "variants, TAQs (titles, affixes, and qualifiers), regularization rules, transliteration rules".
  - Global Name Scoring identifies "the most likely ethnic/cultural context for a name".
  - It handles transliteration from Arabic, Cyrillic, Greek, Hangul and Kana.
  - Sources: [IBM NameHunter class](https://ibm.com/docs/SSEV5M_5.0.0/com.ibm.iis.gnm.api.doc/topics/gnr_nh_api_namehunter_class.html), [IBM GNM overview](https://www.ibm.com/support/knowledgecenter/en/SSEV5M_6.0.0/com.ibm.iis.gnm.overview.doc/topics/gnr_gnm_con_gnmoverview.html), [globalname-scoring PDF](https://public.dhe.ibm.com/software/data/mdm/pdf/globalname-scoring.pdf)
- **Senzing**: its globalization guide describes cross-script comparison and culture groups, such as Southwest Asian (Afghan, Arabic, Farsi, Pakistani). Per the search summary, it leverages IBM GNM for culturally-aware name comparison. — [Senzing Globalization Guide](https://senzing.com/docs/globalization/)

### Inferences
- The "symbol" idea (name variants → shared QID) is the key insight. Cross-script matching works best when Мухаммед, Muhammad, Mohammed and محمد all map to one concept ID. String distance should be the fallback, not the primary mechanism.
- A lightweight package can expose the same idea as a `name_key()` canonical ID plus a phonetic skeleton, without Rust or Elasticsearch.
- Babel Street and IBM both stress culture classification, which means detecting Arabic vs Russian vs Persian naming conventions before matching. Script detection plus simple morphology (‑ov/‑ova, ‑uly/‑kyzy, bin/ibn, ‑zade/‑oğlu) can give a cheap approximation.

### Gaps
- Rosette's public material gives no concrete algorithm details beyond "two-pass" and "ML". The white paper excerpt was mostly marketing.
- The Senzing–IBM GNM relationship is reported in a search summary, but the Senzing page was not fetched directly.
- Senzing's license and free-tier terms were not verified.
- "namematcher" as a distinct product was not found.

---

## 6. Public datasets of name variants and transliterations

### Takeaway
The best openly licensed sources are:
- **Wikidata** (CC0), via the name items' labels, aliases, P1705 native label and P2440 transliteration with P459 scheme. OpenSanctions already mines these.
- **ParaNames** (CC BY 4.0, 118M names).
- **ANETAC** for Arabic–English (about 80k pairs).

JRC-Names is excellent for variants (up to 413 spellings of Gaddafi), but it sits behind an EULA. names-dataset comes from the 533M-user Facebook breach and should not be bundled.

### Cited Findings
- **OpenSanctions namesdb `name_forms.csv`** (snapshot 2026-09-22): 150,587 rows over 94,234 Wikidata items, 76 MB.
  - Columns: `group` (QID), `classes` (family name, given name, patronymic and so on), `native_langs`, `form`, `script`, `langs`, `source` (L label / A alias / N P1705 / T P2440), and `scheme` (the P459 qualifier, i.e. the "transliteration standard").
  - It is "intended as raw material for training transliteration models".
  - Caveats: "80% of rows are family names and 17% female given names; male given names are rare (129 rows)".
  - Source: [NAME_FORMS.md](https://github.com/opensanctions/rigour/blob/main/contrib/namesdb/NAME_FORMS.md)
- **ParaNames**: "118 million names spanning across 400 languages" for 13.6M entities (PER/LOC/ORG), built from Wikidata, data under **CC BY 4.0**. The code repo is MIT, about 42★, last pushed 2024-05. — [arXiv 2202.14035](https://arxiv.org/abs/2202.14035), [GitHub](https://github.com/bltlab/paranames)
- **JRC-Names** (European Commission JRC):
  - "307,000 distinct entities plus 333,000 variants" as of 2016, across 27 writing systems including Cyrillic and Arabic (incl. Farsi). Muammar Gaddafi has 413 spellings.
  - It is a by-product of Europe Media Monitor (about 220k news reports per day).
  - Users must accept the `LICENCE-EULA_JRC-Names_2011.pdf` terms. Linked-data version since 2016.
  - Sources: [JRC-Names page](https://joint-research-centre.ec.europa.eu/language-technology-resources/jrc-names_en), [Semantic Web Journal paper](https://semantic-web-journal.net/content/jrc-names-multilingual-entity-name-variants-and-titles-linked-data-1)
- **ANETAC**: 79,924 English–Arabic named-entity triplets (English, Arabic, class ∈ Person/Location/Organization), built from parallel corpora, released on GitHub in July 2019 by Hadj Ameur, Meziane and Guessoum. — [arXiv 1907.03110](https://arxiv.org/abs/1907.03110), [Papers with Code](https://cs.paperswithcode.com/dataset/anetac)
- **NEWS 2018 shared task** (ACL 2018): covered English to and from Thai, **Persian**, Chinese, Vietnamese, Hindi, Tamil, Kannada, Bangla, Hebrew, Japanese and Korean. The datasets are hand-crafted, with "at most 30k names per language pair". — [NEWS 2018 report](https://preview.aclanthology.org/menus/W18-2409/), [ParaNames paper (comparison)](https://arxiv.org/pdf/2202.14035)
- **Design Challenges in Named Entity Transliteration** (2018) built Wikidata-derived transliteration pairs. — [arXiv 1808.02563](https://arxiv.org/pdf/1808.02563)
- **Dakshina** (Google): CC BY-SA 4.0, a romanization lexicon with attested romanizations for 12 South Asian languages. The repo is archived. — [GitHub](https://github.com/google-research-datasets/dakshina)
- **Proper Noun Diacritization for Arabic Wikipedia** (Bondok, Nassar, Khalifa, Micallef and Habash, 2025): a dataset of manually diacritized Arabic proper nouns with English glosses. GPT-4o reached **73%** accuracy recovering full diacritization. — [arXiv 2505.02656](https://arxiv.org/abs/2505.02656)
- **names-dataset** (philipperemy):
  - About 1k★, v3.3.1 on 2025-04-08. The source is "a massive Facebook dump (533M users)": 730K first names and 983K last names across 105–106 countries, with gender and country fields.
  - Needs about 3.2 GB RAM. The license is Apache-2.0 on GitHub but **MIT on PyPI** (a conflict). The README says only that name lists are "generally" not copyrightable.
  - Sources: [GitHub](https://github.com/philipperemy/name-dataset), [PyPI](https://pypi.org/project/names-dataset/)

### Inferences
- For a bundled lexicon, use Wikidata (CC0), optionally cross-checked against ParaNames (CC BY 4.0, which requires attribution). Keep ANETAC and JRC-Names for *evaluation* only, unless their licenses are confirmed.
- Avoid names-dataset entirely. Its breach provenance creates legal and ethical risk, and it is large.
- The rarity of male given names in OpenSanctions' snapshot (129 rows) shows that a curated given-name lexicon (Muhammad, Abdullah, Yusuf, Hussein, Aleksandr, Yevgeny…) is still missing from open tooling.

### Gaps
- The exact license terms of the JRC-Names EULA (commercial use, redistribution) and of the ANETAC GitHub repository were not retrieved. The ANETAC repo URL guessed via the GitHub API returned 404.
- The exact NEWS dataset licensing (historically distributed by organizers under agreements) was not verified.
- Whether Dakshina includes Urdu and Sindhi (Perso-Arabic script) lexicons was not re-confirmed in this session.

---

## 7. Techniques for transliteration, variant generation and cross-script name matching

### Takeaway
State-of-the-practice for a lightweight library is:
1. Deterministic **context-sensitive rule tables** with longest-match, word-initial/post-vowel/final contexts and scheme-specific outputs.
2. An **exceptions lexicon** of established spellings.
3. **Bounded variant generation** from one-to-many mappings.
4. A **cross-script phonetic skeleton** for blocking.
5. **Name-part alignment** with weighted string similarity.

ML and LLM approaches help with Arabic vowel restoration, but are too heavy and nondeterministic for a core library. GPT-4o got only 73% on Arabic proper-noun diacritization.

### Cited Findings

**Contextual rules**
- iuliia schemas show the canonical rule model: a base mapping plus `prev_mapping` (letter depends on the previous letter), `next_mapping` and `ending_mapping`. Example: BGN/PCGN `е` → `ye` word-initially and after vowels or ъ/ь. — [bgn_pcgn.json](https://raw.githubusercontent.com/nalgeon/iuliia/master/bgn_pcgn.json)
- ICU transform rule syntax supports context (`before { x } after → y`), filters, `::NFD;`-style compound IDs and custom rule sets via `createFromRules`. — [ICU transforms user guide](https://unicode-org.github.io/icu/userguide/transforms/general/)
- **Ukrainian national transliteration** (Cabinet of Ministers Resolution No. 55, 27 Jan 2010, used for passports) is position-dependent. Є, Ї, Й, Ю, Я become `Ye, Yi, Y, Yu, Ya` at word start and `ie, i, i, iu, ia` elsewhere. `зг` → `zgh`, `Г` → `h`, and the soft sign and apostrophe are omitted. — [Wikipedia: Romanization of Ukrainian](https://en.wikipedia.org/wiki/Romanization_of_Ukrainian)

**Reversible vs lossy**
- Scholarly and reversible schemes (ISO 9 = GOST 7.79 System A, one Cyrillic letter to one Latin letter with diacritics) contrast with lossy name-practice schemes. GOST 7.79-2000 "is ISO 9:1995" in verbatim translation, apart from one letter. — [Wikipedia GOST 7.79-2000](https://en.wikipedia.org/wiki/GOST_7.79-2000)
- uroman is explicitly not fully reversible. — [uroman](https://github.com/isi-nlp/uroman)

**ICAO MRZ**
- MRZ is limited to "A" to "Z" and "<". The ICAO Arabic table uses "X" as an escape: ح → `XH`, ص → `XSS`, ش → `XSH`. — [Keesing: Transliteration of Arabic in MRTDs](https://platform.keesingtechnologies.com/transliteration-of-arabic-in-mrtds/), [ICAO Doc 9303 Part 3](https://icao.int/publications/Documents/9303_p3_cons_en.pdf)
- The ICAO Cyrillic table yields `Iurii`, `Kseniia Tsoi`, and ъ → `IE` (`Obieedkov`) **[empirical via iuliia icao_doc_9303]**. — [iuliia](https://github.com/nalgeon/iuliia-py)

**Variant explosion**
- JRC-Names records up to 413 real-world spellings for one person (Gaddafi). Variant generation must therefore be ranked and capped rather than exhaustive. — [JRC-Names](https://joint-research-centre.ec.europa.eu/language-technology-resources/jrc-names_en)
- Daitch–Mokotoff already emits multiple codes per name, which is the "branching" approach. BMPM reduces false positives by applying language-specific rules first. — [Wikipedia D–M](https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex), [BMPM](https://stevemorse.org/phonetics/bmpm.htm)

**Skeleton keys**
- English phonetic keys split `Mukhammed`/`Mohammed` and `Tchernov`/`Chernov` (see the table in section 3). — [jellyfish](https://pypi.org/project/jellyfish/)
- Match Rating codex gives `MHMD` for Mohammed, Muhammad and Mohamad, effectively a consonant skeleton. It still fails for `MKHMD`. — [jellyfish](https://pypi.org/project/jellyfish/)

**Similarity and structure**
- OpenSanctions moved from Jaro-Winkler plus phonetics (logic-v1 and name-based) to symbol pairing with weighted Levenshtein (logic-v2), down-weighting stopwords (×0.7) and weighting family names. — [OpenSanctions matcher](https://www.opensanctions.org/matcher/), [nomenklatura match.py](https://github.com/opensanctions/nomenklatura/blob/main/nomenklatura/matching/logic_v2/names/match.py)
- rigour tags `INITIAL:` symbols for single-letter stand-ins and has a `names/prefix.py` and `names/ordering.py`, i.e. explicit handling of prefixes and particles and of name order. — [rigour tree](https://github.com/opensanctions/rigour/tree/main/rigour/names)
- BMPM's name modes discard particles such as van, von and ben. — [abydos BMPM](https://abydos.readthedocs.io/en/stable/_modules/abydos/phonetic/_beider_morse.html)
- IBM GNM manages TAQs ("titles, affixes, and qualifiers") as first-class data. — [IBM NameHunter](https://ibm.com/docs/SSEV5M_5.0.0/com.ibm.iis.gnm.api.doc/topics/gnr_nh_api_namehunter_class.html)
- Name parsers are Western-centric: **nameparser** (LGPL, 2.3.0 on 2026-09-12) and **probablepeople** (MIT, 0.5.6, 2024; "Parse romanized names… using advanced NLP"). — [PyPI nameparser](https://pypi.org/project/nameparser/), [PyPI probablepeople](https://pypi.org/project/probablepeople/)

**ML and LLM**
- A Transformer-based multilingual personal-name transliteration study used a dataset in 445 Wikidata languages (37 scripts). It found that multilingual models beat bilingual ones for low-resource languages. This comes from a search-result summary and the paper was not opened. — [search result reference: arXiv cs/0609051 and related](https://arxiv.org/pdf/cs/0609051)
- ParaNames trained a multilingual canonical name-translation model. — [ParaNames](https://arxiv.org/abs/2202.14035)
- GPT-4o reached 73% on full diacritization of Arabic proper nouns. — [arXiv 2505.02656](https://arxiv.org/abs/2505.02656)
- **hmni** (ML fuzzy name matching, MIT) has had no release since 2020. — [PyPI hmni](https://pypi.org/project/hmni/)

### Inferences
- Recommended matching cascade:
  1. Normalize.
  2. Exact match on a canonical key (lexicon QID-like ID).
  3. Match on the skeleton key (blocking).
  4. Align name parts (Hungarian/greedy assignment over parts, order-insensitive, with initials compatible with full names).
  5. Score parts with Jaro-Winkler/Levenshtein on the *best pair of variants*.
  6. Apply penalties for unmatched parts, weighted by part type: particles, patronymics and stopwords weigh less.
- Variant generation should be a weighted automaton or beam (top-k by prior probability per mapping) with a hard cap, for example `max_variants=32`. An exhaustive Cartesian product would explode for long Arabic compound names.
- Keep ML optional (an extra, or a pluggable "vowelizer" callback). The core should be deterministic and explainable, which is the stated priority of OpenSanctions and of regulated users.

### Gaps
- I found no published head-to-head benchmark of rule-based vs seq2seq vs LLM transliteration specifically on Russian, Kazakh or Arabic *personal* names with 2024–2026 models.
- The source and venue of the "445 Wikidata languages" paper could not be pinned down. The cited arXiv link from the search results may be a different, older paper.

---

## 8. Unicode and normalization best practices for names

### Takeaway
Normalize with **NFC for storage and display** and **NFKC + casefold for comparison keys**, but special-case:
- Turkish and Azerbaijani İ/ı. Python's `casefold()` and `lower()` are locale-independent and turn `İ` into `i̇` (two code points).
- Apostrophe-like letters (ʻ ʼ ’ ‘ ' `), which are *letters* in Uzbek and Ukrainian.
- Arabic and Persian letter variants (ي/ی, ك/ک, ة/ه, alef forms).
- Latin/Cyrillic homoglyphs, using UTS #39 mixed-script detection and confusables.

### Cited Findings
- **UTS #39** v18.0.0 (2026-08-27) defines `confusables.txt` and `skeleton()`, using the rule that "X and Y are confusable if and only if skeleton(X) = skeleton(Y)". It also defines mixed-script detection via resolved script sets, whole-script vs mixed-script confusables, and six restriction levels from ASCII-Only to Unrestricted. — [UTS #39](https://www.unicode.org/reports/tr39/)
- **Homoglyphs [empirical]**: `"Аlexey"` with Cyrillic А (U+0410) followed by Latin letters goes through anyascii silently as `Alexey`. That is good for matching but hides an anomaly that should be flagged. — [anyascii](https://pypi.org/project/anyascii/)
- **Turkish İ [empirical, Python 3.9]**: `"İ".lower()` → `"i̇"` (length 2, i + U+0307), and `"İ".casefold()` gives the same. The Turkish and Azerbaijani-specific mappings (İ→i, I→ı) are conditional, language-sensitive entries in SpecialCasing, which Python does not apply. — [Unicode SpecialCasing.txt](https://www.unicode.org/Public/UCD/latest/ucd/SpecialCasing.txt), [Python str.casefold docs](https://docs.python.org/3/library/stdtypes.html#str.casefold)
- **rigour** uses full casefold for comparison keys, "Not the same as str.lower()", and runs NFKD + nonspacing-mark removal before CLDR Latin-ASCII so that rules act on base letters. — [rigour arch-text-normalisation](https://github.com/opensanctions/rigour/blob/main/plans/arch-text-normalisation.md)
- **Uzbek apostrophes**:
  - The official 1995 Latin alphabet uses U+02BB (ʻ) in `oʻ` and `gʻ`, and U+02BC (ʼ) for tutuq belgisi.
  - In practice sites, "including some operated by the Uzbek government", use U+2018 ‘ or U+0027 ' for the former and U+2019 ’ or U+0027 for the latter.
  - Wikipedia also reports a July 2026 parliamentary reform replacing oʻ/gʻ/sh/ch with Ö/Ğ/Ş/Ç. This is single-source and needs verification.
  - Source: [Wikipedia: Uzbek alphabet](https://en.wikipedia.org/wiki/Uzbek_alphabet)
- **Arabic normalization** (camel-tools): alef variants → bare alef, alef maksura ى → ي, teh marbuta ة → ه, and NFC/NFKC. — [camel normalize](https://camel-tools.readthedocs.io/en/latest/api/utils/normalize.html)
- ICU `Persian-Latin/BGN` fails on Arabic-codepoint input (it leaves ا and ي), and `Arabic-Latin/BGN` leaves Persian ی/پ **[empirical]**. Persian and Urdu text often mixes Arabic ي (U+064A) / ك (U+0643) with Persian ی (U+06CC) / ک (U+06A9), so codepoint unification must run *before* language-specific rules. — [CLDR transforms](https://github.com/unicode-org/cldr/tree/main/common/transforms)
- iuliia does not handle decomposed sequences (Е + U+0308), so NFC must be applied first. — [iuliia README](https://github.com/nalgeon/iuliia/blob/master/README.md#issues-and-limitations)
- **ICAO MRZ**: output alphabet A–Z plus `<`, with name fields separated by `<<`. Arabic uses X-escapes. — [Keesing](https://platform.keesingtechnologies.com/transliteration-of-arabic-in-mrtds/), [ICAO 9303 Part 3](https://icao.int/publications/Documents/9303_p3_cons_en.pdf)

### Inferences
- Pipeline order:
  1. NFC.
  2. Strip invisible format characters (ZWJ/ZWNJ, tatweel U+0640, bidi marks).
  3. Map apostrophe-like characters to canonical letters per language (Uzbek ʻ/ʼ; Ukrainian ʼ U+02BC as the recommended apostrophe).
  4. Unify Arabic and Persian codepoints.
  5. Repair or flag homoglyphs in mixed-script tokens.
  6. Transliterate.
  7. Produce the comparison key with NFKC + casefold, Turkish-aware via a `lang="tr"|"az"` option, and diacritic stripping.
- Never casefold before transliteration for Turkish or Azerbaijani input.
- Expose a `detect_mixed_script()` diagnostic. In KYC contexts a Cyrillic А inside a Latin name is a data-quality or fraud signal, not just noise.

### Gaps
- The full ICAO Doc 9303 Part 3 tables (Cyrillic and Arabic) were not extracted from the PDF in this session. Exact letter mappings should be taken from the PDF directly.
- The Ukrainian recommendation for the apostrophe codepoint (U+02BC) is from general knowledge and was not re-verified here.

---

## 9. Python packaging best practices (2026) and license compatibility of data sources

### Takeaway
The current baseline:
- `pyproject.toml` with **PEP 639 SPDX `license = "MIT"`** (or Apache-2.0) plus `license-files`. This is supported by hatchling ≥1.27, setuptools ≥77.0.3 and uv-build ≥0.7.19.
- A src layout and `py.typed`.
- Data as JSON or TOML inside the package.
- ruff, mypy and pytest across a CI matrix.
- **Trusted Publishing** via GitHub OIDC, using `pypa/gh-action-pypi-publish@release/v1`, which produces PEP 740 attestations by default since v1.11.0.

On licensing: avoid GPL and AGPL dependencies and data (Unidecode, abydos, pyarabic, Aksharamukha, Polyglot). CLDR, iuliia (MIT), anyascii (ISC) and Wikidata (CC0) are safe sources.

### Cited Findings
- **PEP 639**: `license = "MIT"` (SPDX expression) and `license-files = ["LICEN[CS]E*", ...]`. Backend support: hatchling 1.27.0+, setuptools 77.0.3+, flit-core 3.12+, pdm-backend 2.4.0+, poetry-core 2.2.0+, uv-build 0.7.19+. The guide advises against upper bounds on `requires-python`. CLIs go in `[project.scripts]`, and `dynamic = ["version"]` is supported. — [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- **Trusted publishing**:
  - `id-token: write` is "mandatory for trusted publishing", and the action is `pypa/gh-action-pypi-publish@release/v1`.
  - "Building distributions in a publishing job is unsupported", so build and publish must be separate jobs. Artifacts move via `actions/upload-artifact@v5` and `actions/download-artifact@v6`.
  - Use GitHub environments `pypi` (with manual approval) and `testpypi`, and register pending publishers.
  - "Starting with version v1.11.0, pypa/gh-action-pypi-publish generates and uploads PEP 740-compatible attestations… by default."
  - Sources: [PyPA guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/), [PyPI trusted publishers docs](https://docs.pypi.org/trusted-publishers/)
- Trusted publishing mints short-lived API tokens (15 minutes) from the OIDC identity, so there are no long-lived secrets. — [PyPI docs](https://docs.pypi.org/trusted-publishers/)
- **Peer practice (rigour)**: `requires-python >= 3.10`, classifiers through 3.14, ships `py.typed` and `_core.pyi` stubs, ruff pinned to a minor range "because ruff's default rule selection moves between minor releases", and mypy in strict mode (`no_implicit_reexport`). — [rigour pyproject.toml](https://github.com/opensanctions/rigour/blob/main/pyproject.toml)
- **Minimum Python versions in the ecosystem**: RapidFuzz ≥3.11, camel-tools ≥3.11, lingua ≥3.12, iuliia/uroman/epitran/rigour ≥3.10. — [PyPI RapidFuzz](https://pypi.org/project/RapidFuzz/), [PyPI lingua](https://pypi.org/project/lingua-language-detector/)

**License landscape (from PyPI and GitHub metadata)**

| License | Packages |
|---|---|
| GPL / AGPL (avoid as dependencies) | Unidecode (GPLv2+), abydos (GPLv3+), pyarabic (GPL), gender-guesser (GPLv3), Polyglot (GPLv3), Aksharamukha (AGPL-3.0), unihandecode (GPLv3) |
| Weak copyleft | transliterate (GPL-2.0/LGPL-2.1), nameparser (LGPL), translit (LGPLv3+) |
| Indirect GPL | pyphonetics and nomquamgender both depend on Unidecode |
| Permissive | anyascii (ISC), iuliia, cyrtranslit, RapidFuzz, jellyfish, camel-tools, rigour (MIT), epitran (MIT-Modern-Variant), lingua and unicodedata2 (Apache-2.0) |

Sources: [PyPI Unidecode](https://pypi.org/project/Unidecode/), [PyPI abydos](https://pypi.org/project/abydos/), [PyPI aksharamukha](https://pypi.org/project/aksharamukha/), [PyPI anyascii](https://pypi.org/project/anyascii/)

**Standards data**
- ISO 9:1995 is reproduced verbatim as GOST 7.79-2000 (in effect 2002-07-01, official in Russia and the CIS). — [Wikipedia GOST 7.79-2000](https://en.wikipedia.org/wiki/GOST_7.79-2000)
- The ALA-LC romanization tables are jointly maintained by the ALA and the Library of Congress and published on the LoC website. — [interscript ALA-LC](https://interscript.org/featured-authorities/alalc)

### Inferences
- Use `hatchling` (or `uv_build`) with `src/translit_names/`, and data under `src/translit_names/data/*.json`, loaded with `importlib.resources.files()`.
- Use zero runtime dependencies, with extras:
  - `[fuzzy]` → rapidfuzz
  - `[icu]` → PyICU, for users who want ICU fallback for exotic scripts
  - `[detect]` → lingua
- CLI via stdlib `argparse` to stay dependency-free, with typer as an optional extra if wanted.
- CI matrix: CPython 3.10–3.14 on ubuntu, macos and windows. Run ruff, mypy `--strict` and pytest with golden-file tests per scheme.
- Publish with trusted publishing, with a `pypi` environment that requires approval.
- License the code under **MIT or Apache-2.0**. Apache-2.0 adds a patent grant, which is useful if corporate KYC users adopt the package.
- Mappings from government and intergovernmental standards (ICAO, BGN/PCGN, KMU-2010, GOST 52535) are functional facts. Cite the standard in each data file's header.
- For ISO 9 and ALA-LC, encode the mapping independently from public descriptions such as Wikipedia, CLDR or LoC, rather than copying ISO's published document text.

### Gaps
- No authoritative statement was found on whether the ALA-LC tables are US public domain (LoC works are generally public domain, but ALA is co-author) or on ISO's position on reproducing transliteration *tables* (as opposed to document text). This needs a legal read. It is generally believed that mapping tables are facts, but this was not verified.
- License texts for the BGN/PCGN publications (UK PCGN pages are under the Open Government Licence) were not checked in this session.

---

## 10. Design recommendations and gap analysis for "translit-names"

### Takeaway
The gap is clear and defensible. Nobody ships a permissively licensed, zero-dependency, maintained Python library that does all of the following:
1. Names-aware transliteration for Russian **and** the other Slavic and Turkic Cyrillic languages (uk, be, kk, ky, uz, tg, tt, ba, az-Cyrl) under explicit standards (ICAO, BGN/PCGN, national passport schemes, common-English "Wikipedia" style).
2. **Readable** romanization of Arabic, Persian and Urdu personal names, via a vocalized-name lexicon plus fallback rules. Every existing tool emits consonant skeletons such as `mhmd `bd llh`.
3. **Ranked variant generation** for search.
4. **Cross-script matching keys** and a name-aware similarity score that handles particles, patronymics, initials and order.

### Cited Findings (evidence for each gap)
- **Russian-only or archived**:
  - iuliia (best schemas) is archived and limited to Russian and Uzbek. — [iuliia](https://github.com/nalgeon/iuliia)
  - iuliia data leaks Cyrillic ё in ALA-LC, BGN/PCGN, scientific and GOST 779 **[empirical]**. — [ala_lc.json](https://raw.githubusercontent.com/nalgeon/iuliia/master/ala_lc.json)
  - transliterate has had no release since 2018. — [PyPI](https://pypi.org/project/transliterate/)
- **Non-name schemes**: cyrtranslit gives `SHHerbakov` and `CZoj`, and transliterate gives `Jurij` **[empirical]**. — [cyrtranslit](https://pypi.org/project/cyrtranslit/), [transliterate](https://pypi.org/project/transliterate/)
- **Language-agnostic universal tools** mis-render Ukrainian (`Grigorii`/`Grigoriy` instead of `Hryhorii`) and Kazakh (Unidecode `@likhan`) **[empirical]**. — [Unidecode](https://pypi.org/project/Unidecode/), [anyascii](https://pypi.org/project/anyascii/)
- **Arabic script**:
  - ICU, Unidecode, anyascii and uroman output unvowelled skeletons. ICU leaves untransliterated letters in its BGN Persian and Arabic transforms and has no Urdu transform **[empirical]**. — [CLDR transforms](https://github.com/unicode-org/cldr/tree/main/common/transforms), [uroman](https://github.com/isi-nlp/uroman)
  - camel-tools offers only scholarly schemes. — [camel charmaps](https://github.com/CAMeL-Lab/camel_tools/tree/master/camel_tools/utils/charmaps)
  - rigour explicitly excludes Arabic. — [rigour translit.py](https://github.com/opensanctions/rigour/blob/main/rigour/text/translit.py)
- **Heavy or awkward dependencies**: PyICU is sdist-only. — [PyPI PyICU](https://pypi.org/project/PyICU/)
  - normality 3 hard-requires PyICU, and rigour depends on normality, so the OpenSanctions stack drags in an ICU C build. — [PyPI normality](https://pypi.org/project/normality/), [rigour pyproject](https://github.com/opensanctions/rigour/blob/main/pyproject.toml)
  - camel-tools pulls in kenlm and other heavy packages. — [PyPI camel-tools](https://pypi.org/project/camel-tools/)
- **Phonetics**: English codes fail on `Mukhammed` and `Tchernov` **[empirical]**. Multi-language BMPM is only available as GPL abydos, unmaintained since 2020. — [jellyfish](https://pypi.org/project/jellyfish/), [abydos](https://pypi.org/project/abydos/)
- **Lexicon data exists but is unpackaged**: OpenSanctions' Wikidata name-forms export (CC0 source, 94k items, 2026-09) is "raw material", with few male given names. — [NAME_FORMS.md](https://github.com/opensanctions/rigour/blob/main/contrib/namesdb/NAME_FORMS.md)
- ParaNames (CC BY 4.0) is available for evaluation and lexicon mining. — [ParaNames](https://arxiv.org/abs/2202.14035)

### Inferences (concrete recommendations)

**1. API surface (typed and small)**
- `transliterate(name, *, lang=None, scheme="icao"|"bgn_pcgn"|"common"|"kmu2010"|"ala_lc"|"iso9"|"mrz", ascii=True) -> str`
- `variants(name, *, lang=None, max_variants=32, schemes=...) -> list[Variant(text, score, scheme, trace)]`
- `name_key(name) -> str` (canonical skeleton for blocking)
- `similarity(a, b, *, lang_a=None, lang_b=None) -> MatchResult(score, alignment, explanation)`
- `detect(name) -> (script, likely_lang, mixed_script_flags)`
- Every function should be pure and deterministic, and return a **trace** of applied rules, for explainability as emphasized by [OpenSanctions](https://www.opensanctions.org/articles/2025-06-24-name-matching.md).

**2. Data model**
- One JSON or TOML file per language and scheme, in an iuliia-compatible structure (`mapping`, `prev`, `next`, `ending`), extended with:
  - `word_initial` contexts (needed for Ukrainian KMU-2010)
  - multi-output weighted alternatives for variant generation (for example `х: [("kh",0.7),("h",0.2),("x",0.05)]`, `й` at word end: `[("y",.5),("i",.3),("j",.1)]`)
  - `source`/`standard` metadata with a URL
- Validate the data with a JSON Schema in tests.
- Seed the Russian tables from iuliia (MIT, with attribution) after fixing the ё bug. Port the BGN tables for kk, ky, uz, az, tk, be, uk, fa and ps from CLDR XML (Unicode license).

**3. Coverage priorities**
- **Cyrillic**: ru, uk, be, bg, sr, mk, kk, ky, uz-Cyrl→uz-Latn official, tg, tt, ba, mn.
- **Latin Turkic normalization**: tr, az, uz-Latn, tk, kk-Latn 2021, including apostrophe canonicalization.
- **Arabic script**: ar, fa, ur, ps, ug, ku-Arab, each with a **name lexicon** (top N given names and name elements: Muhammad, Ahmad, Ali, Hasan, Husayn, Abd + 99 divine names → Abdul-/Abd al-/Abdu-, -ullah/-allah, -uddin/-al-din, Nur, Fatima, Zaynab…). Each entry carries multiple ranked English spellings (Muhammad/Mohammed/Mohamed/Mohammad/Mukhammed/Magomed), and the lexicon can be harvested from Wikidata P2440/P1705.

**4. Name structure handling**
- Tokenize and tag parts: given, patronymic (‑ovich/‑evich/‑ovna/‑evna/‑ich; Turkic ‑uly/‑ulı/‑kyzy/‑qızı/‑oğlu; Arabic bin/ibn/bint/ben), family name, particles (al‑/el‑/ul‑, abu/umm, von/van/de), and initials.
- Treat Slavic gendered surname pairs (‑ov/‑ova, ‑sky/‑skaya, ‑in/‑ina) as related in matching.
- Handle Arabic sun-letter assimilation (al‑R → ar‑R), compound units (عبد الله as one token), and ezafe (Persian ‑e/‑i).
- Allow order-insensitive alignment (Russian "Surname Given Patronymic" vs Western "Given Surname").

**5. Matching**
- Blocking key = skeleton: transliterate, map digraph families to canonical consonant classes, drop vowels except the initial one, collapse doubles.
- Score = weighted part alignment with Jaro-Winkler/Levenshtein. Use stdlib or a pure-Python implementation by default, and accelerate with rapidfuzz if it is installed.
- Down-weight particles and patronymics (OpenSanctions uses ×0.7 for stopwords), and treat initials as compatible.

**6. Unicode hygiene**
- NFC on input, removal of invisible and format characters, apostrophe and Arabic codepoint unification, and mixed-script detection with homoglyph repair from a TR39 confusables subset (Latin↔Cyrillic↔Greek only, kept small).
- Turkish-aware casing option, with casefold applied only for keys.

**7. Optional add-ons (extras)**
- `[icu]` fallback for unsupported scripts.
- `[fuzzy]` rapidfuzz.
- A pluggable `vowelizer` callback for ML or LLM diacritization of Arabic, since GPT-4o reaches only 73% on proper nouns ([arXiv 2505.02656](https://arxiv.org/abs/2505.02656)). Do not make this part of the core.

**8. Evaluation**
- Ship a benchmark harness: precision and recall of `variants()` against Wikidata/ParaNames gold spellings, and ROC curves for `similarity()` on ANETAC (Arabic–English) and Wikidata cross-script pairs.
- Publish the numbers in the README. No competitor publishes names-specific accuracy.

**9. What not to do**
- Do not depend on Unidecode, abydos, pyarabic, Aksharamukha or names-dataset (license and provenance).
- Do not use `Any-Latin; Latin-ASCII` as the default for Cyrillic, because it destroys щ/ю.
- Do not output a single "canonical English" spelling without a scheme label.

### Gaps
- Per-language lexicon size targets and an expected accuracy baseline are not established. No public benchmark for names-specific Cyrillic/Arabic → Latin romanization quality was found.
- Exact current national passport schemes for kk (2021 Latin), ky, tg, tk and az were not verified in this research slice. They need a separate standards survey, which another researcher is likely covering.
