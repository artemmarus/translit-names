# Romanization of East Slavic (Russian, Ukrainian, Belarusian) personal names: implementation notes for "translit-names" (state as of October 2026)

Conventions used in these notes:
- `∅` = letter is omitted (empty string). `(computed)` = output produced by me by applying the cited table/schema programmatically (Python re-implementation in scratch); it is derived data, not a quote. Every computed column was regression-tested against all official examples printed in the corresponding primary source (KMU 2010: 28 official examples tested, all pass; Belarus 2023 Instruction: 26 official examples tested, all pass; Belarus MVD No. 288: 11 official examples tested, 10 pass, the one failure is an internal inconsistency of the source, see section 3; iuliia: all bundled samples of 14 schemas pass).
- Unicode: ALA-LC ligature tie = U+0361 (t͡s, i͡u, i͡a); ALA-LC/ISO hard sign ʺ = U+02BA, soft sign ʹ = U+02B9; BGN/PCGN apostrophes ’ = U+2019 and ” = U+201D; Latin ë = U+00EB.

## 1. Russian: exact mapping tables (passport current and superseded, GOST 7.79 A/B, BGN/PCGN, ALA-LC, scholarly, iuliia schemes incl. "wikipedia")

### Takeaway
Russian international passports have used the ICAO Doc 9303 table since 2013 (pure letter-by-letter substitution, no context rules: Ё→E, Й→I, Ъ→IE, Ь→∅, Ц→TS, Ю→IU, Я→IA); the 1997–2010 MVD system (Й→Y, Ю→YU, Я→YA, contextual YE) and the 2010–2013 GOST R 52535.1-2006 system (Ц→TC, Ъ→∅) are superseded but still present in older documents and must be generated for matching. The iuliia project (github.com/nalgeon/iuliia) publishes machine-readable JSON for 20 Russian schemas with a simple, reusable rule model (base map + previous-letter map + next-letter map + 2-letter word-ending map) that can be adopted almost directly as package data, with a few data bugs noted below.

### Cited Findings

**Timeline / legal status (Russia)**
- Soviet international passports used a French-based, diacritic-free system — [Wikipedia, Romanization of Russian](https://en.wikipedia.org/wiki/Romanization_of_Russian) (cites MVD Order No. 310).
- 1997: MVD Order No. 310 of 26 May 1997 introduced a diacritic-free English-oriented system (also MVD Order No. 1047 of 31 Dec 2003); abandoned in 2010 — [Wikipedia, Romanization of Russian](https://en.wikipedia.org/wiki/Romanization_of_Russian); iuliia describes MVD 310-1997 as "poorly formalized", "often contradicts itself", with a "French" variant without apostrophes, replaced by ICAO Doc 9303 — [iuliia.ru/mvd-310](https://iuliia.ru/mvd-310/).
- 2010: FMS Order No. 26 of 3 Feb 2010 required GOST R 52535.1-2006 transliteration for passports issued after 2010; citizens could ask to retain the pre-2010 spelling; the standard was abandoned in 2013 — [Wikipedia, Romanization of Russian](https://en.wikipedia.org/wiki/Romanization_of_Russian).
- 2013: FMS Order No. 320 of 15 Oct 2012 (in force 2013) required the ICAO Doc 9303 Part 3 system; it differs from GOST R 52535.1-2006 in ц→ts (instead of tc) and ъ→ie (instead of omission). GOST R 52535.1-2006 was replaced in 2013 by GOST R ISO/IEC 7501-1-2013, which contains no table and refers to ICAO — [Wikipedia, Romanization of Russian](https://en.wikipedia.org/wiki/Romanization_of_Russian).
- Current MVD regulation: MVD Order No. 186 of 31 Mar 2021 (registered by MinJust 19 May 2021, No. 63515), which repealed MVD Order No. 864 of 16 Nov 2017. Para. 139.2: the surname is printed in Russian and, after "/", "by transliteration (simple substitution of Russian letters with Latin ones) in accordance with international requirements and standards for machine-readable travel documents" — [Consultant: MVD Order 186, para 139](https://www.consultant.ru/document/cons_doc_LAW_384459/d3c3b53854fd15c08984f777d0101cede5c99ca8/); [order header](https://www.consultant.ru/document/cons_doc_LAW_384459/2ff7a8c72de3994f30496a0ccbb1ddafdaddf518/). Consultant flags that the application forms were replaced by MVD Order No. 83 of 24 Feb 2026 — [Consultant](https://www.consultant.ru/document/cons_doc_LAW_384459/).
- MFA (consular) side: transliteration rules are an annex to MFA administrative regulations approved by MFA Orders No. 2113 and No. 2114 of 12 Feb 2020; method = "simple substitution of Russian letters by Latin letters"; MFA spokesperson (14 Jun 2024): the same name may be transliterated differently and this "is not an error and not grounds for confiscation" — [Interfax, 14 Jun 2024](https://www.interfax.ru/russia/966690). MFA Order No. 10287 of 27 May 2026 (registered 15 Jul 2026, in force 26 Jul 2026) approved a new passport regulation and repealed Order No. 2113 — [ppt.ru](https://ppt.ru/obzory/vstupaet-v-silu/prikaz-mid-rossii-27-05-2026-10287) (summary did not mention transliteration content).
- iuliia status labels: ICAO DOC 9303 "в силе" (2015 edition), "used by MVD for names in driving licences and by MFA in passports"; MVD 310-1997, MVD 782-2000 (driving-licence instruction), GOST R 52535.1-2006 marked "не действует" (no longer in force) — [iuliia.ru/icao-doc-9303](https://iuliia.ru/icao-doc-9303/), [iuliia.ru/mvd-782](https://iuliia.ru/mvd-782/), [iuliia.ru/gost-52535](https://iuliia.ru/gost-52535/); repo README lists actual vs deprecated schemas — [github.com/nalgeon/iuliia](https://github.com/nalgeon/iuliia).

**ICAO Doc 9303 Part 3, Section 6.B "Transliteration of Cyrillic Characters" (verbatim content, 7th edition 2015, amendment No. 2 of 16/09/16)** — [ICAO Doc 9303 Part 3, 7th ed. (copy hosted by ITF)](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); official landing page [ICAO Doc 9303](https://www2023.icao.int/Security/mrtd/Pages/Document9303.aspx)

| Unicode | Char | Recommended transliteration |
|---|---|---|
| 0401 | Ё | E (except Belorussian = IO) |
| 0402 | Ђ (PDF glyph shows Ћ) | D |
| 0404 | Є | IE (except if Ukrainian first character, then = YE) |
| 0405 | Ѕ | DZ |
| 0406 | І | I |
| 0407 | Ї | I (except if Ukrainian first character, then = YI) |
| 0408 | Ј | J |
| 0409 | Љ | LJ |
| 040A | Њ | NJ |
| 040C | Ќ | K (except Macedonian = KJ) |
| 040E | Ў | U |
| 040F | Џ | DZ (except Macedonian = DJ) |
| 0410–0412 | А Б В | A B V |
| 0413 | Г | G (except Belorussian, Serbian, and Ukrainian = H) |
| 0414 | Д | D |
| 0415 | Е | E |
| 0416 | Ж | ZH (except Serbian = Z) |
| 0417 | З | Z |
| 0418 | И | I (except Ukrainian = Y) |
| 0419 | Й | I (except if Ukrainian first character, then = Y) |
| 041A–0424 | К Л М Н О П Р С Т У Ф | K L M N O P R S T U F |
| 0425 | Х | KH (except Serbian and Macedonian = H) |
| 0426 | Ц | TS (except Serbian and Macedonian = C) |
| 0427 | Ч | CH (except Serbian = C) |
| 0428 | Ш | SH (except Serbian = S) |
| 0429 | Щ | SHCH (except Bulgarian = SHT) |
| 042A | Ъ | IE |
| 042B | Ы | Y |
| 042D | Э | E |
| 042E | Ю | IU (except if Ukrainian first character, then = YU) |
| 042F | Я | IA (except if Ukrainian first character, then = YA) |
| 046A | Ѫ | U |
| 0474 | Ѵ | Y |
| 0490 | Ґ | G |
| 0492 | Ғ | G (except Macedonian = GJ) |
| 04BA | Һ | C |

Note: Ь (U+042C) has no row in the ICAO table (i.e., not rendered). Same source, MRZ rule: the issuing organization "shall transliterate national characters using only the allowed OCR-B characters and/or truncate"; transliteration tables are provided in Section 6 — [ICAO Doc 9303 Part 3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2).

**Master table: all 33 Russian letters (context-free base values).** Values extracted from the iuliia JSON schema files ([github.com/nalgeon/iuliia](https://github.com/nalgeon/iuliia), files `icao_doc_9303.json`, `gost_52535.json`, `mvd_310.json`, `mvd_310_fr.json`, `mvd_782.json`, `gost_779.json`, `gost_779_alt.json`, `bgn_pcgn.json`, `ala_lc.json`, `ala_lc_alt.json`, `scientific.json`, `wikipedia.json`, `bs_2979.json`) and cross-checked against primary/secondary sources: ICAO column against ICAO Doc 9303 (above); BGN/PCGN against the [BGN/PCGN 1947 PDF](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_RUSSIAN.pdf); ALA-LC against the [LoC Russian table, 2012 version](https://www.loc.gov/catdir/cpso/romanization/russian.pdf); all columns against the comparison table in [Wikipedia, Romanization of Russian](https://en.wikipedia.org/wiki/Romanization_of_Russian). Context rules (Е/Ё/endings) are listed after the table and override these base values.

| # | Cyr | ICAO 9303 / RU passport 2013–now | RU passport 2010–13 (GOST R 52535.1-2006) | RU passport 1997–2010 (MVD 310, "en") | MVD 310 "fr" variant | MVD 782-2000 | GOST 7.79-2000 A = ISO 9:1995 | GOST 7.79-2000 B | BGN/PCGN 1947 | ALA-LC (strict) | ALA-LC w/o diacritics | Scholarly | Wikipedia (WP:RUS) | BS 2979:1958 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | А а | a | a | a | a | a | a | a | a | a | a | a | a | a |
| 2 | Б б | b | b | b | b | b | b | b | b | b | b | b | b | b |
| 3 | В в | v | v | v | v | v | v | v | v | v | v | v | v | v |
| 4 | Г г | g | g | g | g | g | g | g | g | g | g | g | g | g |
| 5 | Д д | d | d | d | d | d | d | d | d | d | d | d | d | d |
| 6 | Е е | e | e | e | e | e | e | e | e | e | e | e | e | e |
| 7 | Ё ё | e | e | e | e | yo | ë | yo | ë | ë | e | ë | yo | ë |
| 8 | Ж ж | zh | zh | zh | j | zh | ž | zh | zh | zh | zh | ž | zh | zh |
| 9 | З з | z | z | z | z | z | z | z | z | z | z | z | z | z |
| 10 | И и | i | i | i | i | i | i | i | i | i | i | i | i | i |
| 11 | Й й | i | i | y | i | y | j | j | y | ĭ | i | j | y | ĭ |
| 12 | К к | k | k | k | k | k | k | k | k | k | k | k | k | k |
| 13 | Л л | l | l | l | l | l | l | l | l | l | l | l | l | l |
| 14 | М м | m | m | m | m | m | m | m | m | m | m | m | m | m |
| 15 | Н н | n | n | n | n | n | n | n | n | n | n | n | n | n |
| 16 | О о | o | o | o | o | o | o | o | o | o | o | o | o | o |
| 17 | П п | p | p | p | p | p | p | p | p | p | p | p | p | p |
| 18 | Р р | r | r | r | r | r | r | r | r | r | r | r | r | r |
| 19 | С с | s | s | s | s | s | s | s | s | s | s | s | s | s |
| 20 | Т т | t | t | t | t | t | t | t | t | t | t | t | t | t |
| 21 | У у | u | u | u | ou | u | u | u | u | u | u | u | u | u |
| 22 | Ф ф | f | f | f | f | f | f | f | f | f | f | f | f | f |
| 23 | Х х | kh | kh | kh | kh | kh | h | x | kh | kh | kh | x | kh | kh |
| 24 | Ц ц | ts | tc | ts | ts | ts | c | cz | ts | t͡s | ts | c | ts | ts |
| 25 | Ч ч | ch | ch | ch | tch | ch | č | ch | ch | ch | ch | č | ch | ch |
| 26 | Ш ш | sh | sh | sh | ch | sh | š | sh | sh | sh | sh | š | sh | sh |
| 27 | Щ щ | shch | shch | shch | chtch | shch | ŝ | shh | shch | shch | shch | šč | shch | shch |
| 28 | Ъ ъ | ie | ∅ | " | ∅ | ' | ʺ | `` | ” | ʺ | " | ʺ | ∅ | ʺ |
| 29 | Ы ы | y | y | y | y | y | y | y` | y | y | y | y | y | ȳ |
| 30 | Ь ь | ∅ | ∅ | ' | ∅ | ' | ʹ | ` | ’ | ʹ | ' | ʹ | ∅ | ʹ |
| 31 | Э э | e | e | e | e | e | è | e` | e | ė | e | è | e | é |
| 32 | Ю ю | iu | iu | yu | iou | yu | û | yu | yu | i͡u | iu | ju | yu | yu |
| 33 | Я я | ia | ia | ya | ia | ya | â | ya | ya | i͡a | ia | ja | ya | ya |

Column notes / conflicts:
- Passport 1997 (MVD 310) Ъ/Ь: iuliia gives ъ→" and ь→' ([iuliia.ru/mvd-310](https://iuliia.ru/mvd-310/)); Wikipedia's comparison table gives Ъ→ʺ and Ь→"—" (omitted) for "Passport (1997)" — [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian). Conflict unresolved (primary text of Order 310 not retrievable; pravo.gov.ru link returned 404).
- iuliia data bug: in `bgn_pcgn`, `ala_lc`, `scientific`, `ungegn_1987`, `bs_2979`, `gost_779` the output value for ё is the Cyrillic letter "ё" (U+0451), not Latin "ë" (U+00EB) (verified by inspecting code points in the JSON); BGN/PCGN specifies Ë U+00CB / ë U+00EB — [BGN/PCGN Russian PDF](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_RUSSIAN.pdf). The master table above shows the corrected Latin ë.
- ALA-LC 2012 also maps pre-1918 letters: І→Ī/ī, Ѣ→I͡E/i͡e, Ѳ→Ḟ/ḟ, Ѵ→Ẏ/ẏ; earlier versions 2011, 1997 — [LoC Russian table](https://www.loc.gov/catdir/cpso/romanization/russian.pdf); before the 2012 revision ъ was not romanized at word end — [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian).
- BS 2979:1958: Ы = ȳ (Oxford University Press) or "ui" (British Library; ый = "uy"); iuliia uses ȳ — [iuliia README](https://github.com/nalgeon/iuliia), [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian).
- GOST 7.79-2000 is an adoption of ISO 9:1995 and is the official standard of Russia and the CIS; system A = ISO 9 with diacritics, system B = digraphs — [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian). Road signs use GOST R 52290-2004 (tables Г.4/Г.5), practically identical to GOST 10807-78 — same source.

**Context (positional) rules per system**
- ICAO 9303 / passport 2013–now: no context rules ("Особых правил нет") — [iuliia.ru/icao-doc-9303](https://iuliia.ru/icao-doc-9303/); iuliia `icao_doc_9303.json` has `prev_mapping`, `next_mapping`, `ending_mapping` = null. Samples: Андрей Видный → Andrei Vidnyi; Артём Краевой → Artem Kraevoi; Мадыр Чёткий → Madyr Chetkii; Игорь Ильин → Igor Ilin; Ян Разъездной → Ian Razieezdnoi — [icao_doc_9303.json](https://github.com/nalgeon/iuliia/blob/master/icao_doc_9303.json).
- GOST R 52535.1-2006 (passports 2010–13): no special rules; Юлия Щеглова → Iuliia Shcheglova — [iuliia.ru/gost-52535](https://iuliia.ru/gost-52535/).
- BGN/PCGN 1947 (checked for validity June 2019): Note 1: е → ye initially, after а е ё и о у ы э ю я, and after й ъ ь; otherwise e. Note 2: ё → yë in the same positions, otherwise ë; ё is romanized as ё "whether displayed in the source document with or without dieresis". Note 3 (optional interpunct for non-Russian sequences): й before а у ы э → y·; ы before а у ы э → y·; ы after any vowel → ·y; э after any consonant except й → ·e; тс → t·s; шч → sh·ch. All apostrophes U+2019 — [BGN/PCGN Russian PDF](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_RUSSIAN.pdf). iuliia implements Notes 1–3 in `bgn_pcgn.json` (e.g., Мейеровка → Meyyerovka; Юрьев объезд → Yur’yev ob”yezd) and Notes 1–2 only in `bgn_pcgn_alt.json` — [bgn_pcgn.json](https://github.com/nalgeon/iuliia/blob/master/bgn_pcgn.json).
- Wikipedia (WP:RUS, a modification of BGN/PCGN): е → ye at word start, after vowels, after ь, after ъ, else e; but e after й (Майер = Mayer); ё → yo everywhere (Ёлкино = Yolkino, Озёрск = Ozyorsk); й → y except in -ый/-ий endings; ъ omitted before е ё ю я, → y before а и о у ы э; ь omitted at word end, before consonants and before е ё ю я, → y before а и о у ы э (Ильинский = Ilyinsky); -ый → -y (Красный = Krasny); -ий → -y in personal names and Russian-origin adjectives, -iy in nouns/non-Russian words (Рыркайпий = Ryrkaypiy); -ые → -ye; never use interpunct — [Wikipedia:Romanization of Russian](https://en.wikipedia.org/wiki/Wikipedia:Romanization_of_Russian).
- iuliia `wikipedia.json` encodes: prev_mapping {"е" (word-initial), "ае","ие","ое","уе","эе","юе","яе","ье","ъе"} → ye; next_mapping {ъ,ь}+{а,и,о,у,ы,э} → y; ending_mapping {"ий","ый"} → y; samples Ельцин → Yeltsin, Раздольное → Razdolnoye, Юрьев → Yuryev, Бийск → Biysk, Подъярский → Podyarsky, Усолье → Usolye, Ильинский → Ilyinsky, Великий → Veliky, Набережные Челны → Naberezhnye Chelny — [wikipedia.json](https://github.com/nalgeon/iuliia/blob/master/wikipedia.json); [iuliia.ru/wikipedia](https://iuliia.ru/wikipedia/).
- MVD 782-2000: Е → YE after vowels and after Ъ, Ь, else E; Ё → YE after consonants except Ж Ч Ш Щ, E after Ж Ч Ш Щ, YO in initials and after vowels/Ъ/Ь; И → YI after Ь; ъ ь → ' — [iuliia.ru/mvd-782](https://iuliia.ru/mvd-782/). (The iuliia JSON implements ё after consonants → "ye", e.g., Артём → Artyem.)
- MVD 310-1997 "English" variant: ЬЕ/ЬЁ → YE (Васильева → Vasilyeva); ЕЙ → EY or YEY; ИЙ → IY or Y; ЫЙ → YY or Y. "French" variant: ГЕ→GUE, ГИ→GUI, ГЫ→GUY (Гирев → Guirev); ЬЕ→IE (Vassilieva); КС→X (Оксана → Oxana, Максимов → Maximov); С between two vowels → SS (Гусев → Goussev; not implemented by iuliia); final ИН → INE (Васин → Vassine) — [iuliia.ru/mvd-310](https://iuliia.ru/mvd-310/); [iuliia README](https://github.com/nalgeon/iuliia).
- GOST 7.79-2000 B: ц → c before i, e, y, j, otherwise cz — [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian); iuliia `gost_779_alt.json` next_mapping це/ци/цй/цы → c.
- BS 2979:1958 (iuliia): endings -ий, -ый → -y — [bs_2979.json](https://github.com/nalgeon/iuliia/blob/master/bs_2979.json).
- Mosmetro: ц after т rendered "s" so тц → ts (Битцевский → Bitsevsky); ь/ъ before vowels → y; ьё/ъё → yo (Воробьёвы → Vorobyovy); ё otherwise → e; щ → sch; -ий/-ый → -y — [mosmetro.json](https://github.com/nalgeon/iuliia/blob/master/mosmetro.json).
- Yandex.Maps: е → ye word-initially and after vowels; ъе → ye; ending -ый → -iy; щ → sch; ё → yo — [yandex_maps.json](https://github.com/nalgeon/iuliia/blob/master/yandex_maps.json).
- Yandex.Money (deprecated): й → i, щ → sch, ю → yu, я → ya, no context rules (Иван Брызгальский → Ivan Bryzgalskii) — [yandex_money.json](https://github.com/nalgeon/iuliia/blob/master/yandex_money.json).
- Telegram: ж → j, й → i, х → h, ц → c, щ → sc, ю → iu, я → ia, ъ ь → ∅ — [telegram.json](https://github.com/nalgeon/iuliia/blob/master/telegram.json).
- Full iuliia schema list (files in repo): ala_lc, ala_lc_alt, bgn_pcgn, bgn_pcgn_alt, bs_2979, bs_2979_alt, gost_16876, gost_16876_alt, gost_52290, gost_52535, gost_7034, gost_779, gost_779_alt, icao_doc_9303, iso_9_1954, iso_9_1968, iso_9_1968_alt, mosmetro, mvd_310, mvd_310_fr, mvd_782, scientific, telegram, ungegn_1987, wikipedia, yandex_maps, yandex_money, plus uz (Uzbek); last commits Jan 2025 — [GitHub API listing / repo](https://github.com/nalgeon/iuliia). README: GOST R 7.0.34-2014 defines alternatives for many letters without saying when to use which, iuliia takes the first; iuliia supports only precomposed Ё (not E+combining diaeresis) — [iuliia README](https://github.com/nalgeon/iuliia).

**iuliia rule engine semantics (reference implementation, iuliia-py)** — [schema.py](https://github.com/nalgeon/iuliia-py/blob/master/iuliia/schema.py), [nlp.py](https://github.com/nalgeon/iuliia-py/blob/master/iuliia/nlp.py)
- Text is split on regex `\b` word boundaries; each word is processed letter-by-letter as trigrams (prev, curr, next).
- Lookup order for a letter: `prev_mapping[prev+curr]` → `next_mapping[curr+next]` → `mapping[curr]` → the character unchanged. A one-letter key in `prev_mapping` (e.g., "е") means "word-initial" (prev is the empty string).
- Ending: the last two letters of a word with length > 2 are looked up in `ending_mapping`; if found, stem and ending are translated separately.
- Case: mapping values are capitalized when the source letter is uppercase; for prev-context keys, value is capitalized only when both letters are uppercase; endings are uppercased if the source ending is uppercase.

### Inferences
- For a passport-matching package, the minimum set of Russian "official" generators is: `icao_doc_9303` (2013–now), `gost_52535` (2010–2013), `mvd_310` (1997–2010; apply ий→iy/y and ый→yy/y alternatives as variants), `mvd_310_fr` (Soviet/French-style), plus `bgn_pcgn` (US/UK government) and `wikipedia` (English media style).
- The iuliia model (base + prev + next + 2-letter ending) is sufficient for every Russian scheme listed except BGN/PCGN interpunct rules requiring 2-letter lookahead/lookbehind on non-adjacent context (already encoded as pairs) and the MVD 310-fr "С between vowels → SS" rule (needs a 3-letter context; implement as an extra rule type).
- Capitalization bug to avoid when copying iuliia logic: with mvd_310_fr, "Ксения" → "xeniia" (lowercase x) because the "кс" digraph collapses onto the second (lowercase) letter; a package should re-case the output of a collapsed digraph from the first source letter (computed with my re-implementation of iuliia semantics; the iuliia schema data is the cause, see [mvd_310_fr.json](https://github.com/nalgeon/iuliia/blob/master/mvd_310_fr.json)).
- iuliia's `wikipedia.json` omits е after е, ё, ы, й from prev_mapping, so "Ерофеев" → "Yerofeev", whereas the WP:RUS text ("after vowels") implies "Yerofeyev"; WP:RUS also has the "-iy for non-Russian nouns" exception that cannot be decided letter-by-letter. Treat as a known deviation (computed).
- Store output chars as NFC; normalize input Ё/ё given as Е+U+0308 to precomposed before mapping (iuliia only supports precomposed).

### Gaps
- Could not download ICAO Doc 9303 8th edition (2021) Part 3 PDF (icao.int URLs return 404 after site migration); table above is from the 7th edition (2015) with amendment No. 2 (2016). I found no evidence of a change to Section 6.B, but did not verify against the 8th edition text.
- Primary texts of MVD Order No. 310 (1997), FMS Order No. 26 (2010) and FMS Order No. 320 (2012) could not be retrieved (pravo.gov.ru 404; rg.ru timed out); their tables are taken from iuliia and Wikipedia.
- The MFA "Правила транслитерации кириллических знаков" annex (Orders 2113/2114 of 2020, and the 2026 Order 10287) was not retrieved; its exact table (presumably ICAO-identical) is unverified.

## 2. Ukrainian: KMU Resolution No. 55 of 27 Jan 2010 (exact table and rules), passport application, and the procedure for a different spelling

### Takeaway
Ukraine's single official system for names and places is the table approved by Cabinet of Ministers Resolution No. 55 of 27 Jan 2010 (still in force on 7 Oct 2026); it is letter-by-letter with four context rules (word-initial Є/Ї/Й/Ю/Я → Ye/Yi/Y/Yu/Ya; зг → zgh; ь and apostrophe dropped). Passports use it by default, but a written request can substitute the spelling from earlier Ukrainian documents, legalized foreign civil-status documents, or (since the 24 Dec 2025 amendment) a child's/parent's/spouse's foreign passport.

### Cited Findings
- KMU Resolution No. 55 "Про впорядкування транслітерації українського алфавіту латиницею", amended by KMU Nos. 185 (13.03.2013), 415 (12.06.2013), 682 (26.11.2014), 1121 (23.12.2015); current edition 12.01.2016; status "чинний" as of 07.10.2026 — [zakon.rada.gov.ua 55-2010-п](https://zakon.rada.gov.ua/laws/show/55-2010-%D0%BF).
- Exact table (all 33 letters; Ь has no row, covered by Note 2) — [KMU 55-2010](https://zakon.rada.gov.ua/laws/show/55-2010-%D0%BF):

| # | Ukr | Latin | Position | Official examples |
|---|---|---|---|---|
| 1 | А а | A a | | Алушта Alushta; Андрій Andrii |
| 2 | Б б | B b | | Борщагівка Borshchahivka; Борисенко Borysenko |
| 3 | В в | V v | | Вінниця Vinnytsia; Володимир Volodymyr |
| 4 | Г г | H h | (зг → zgh, Note 1) | Гадяч Hadiach; Богдан Bohdan; Згурський Zghurskyi |
| 5 | Ґ ґ | G g | | Ґалаґан Galagan; Ґорґани Gorgany |
| 6 | Д д | D d | | Донецьк Donetsk; Дмитро Dmytro |
| 7 | Е е | E e | | Рівне Rivne; Олег Oleh; Есмань Esman |
| 8 | Є є | Ye / ie | Ye at start of word; ie elsewhere | Єнакієве Yenakiieve; Гаєвич Haievych; Короп'є Koropie |
| 9 | Ж ж | Zh zh | | Житомир Zhytomyr; Жанна Zhanna; Жежелів Zhezheliv |
| 10 | З з | Z z | | Закарпаття Zakarpattia; Казимирчук Kazymyrchuk |
| 11 | И и | Y y | | Медвин Medvyn; Михайленко Mykhailenko |
| 12 | І і | I i | | Іванків Ivankiv; Іващенко Ivashchenko |
| 13 | Ї ї | Yi / i | Yi at start of word; i elsewhere | Їжакевич Yizhakevych; Кадиївка Kadyivka; Мар'їне Marine |
| 14 | Й й | Y / i | Y at start of word; i elsewhere | Йосипівка Yosypivka; Стрий Stryi; Олексій Oleksii |
| 15 | К к | K k | | Київ Kyiv; Коваленко Kovalenko |
| 16 | Л л | L l | | Лебедин Lebedyn; Леонід Leonid |
| 17 | М м | M m | | Миколаїв Mykolaiv; Маринич Marynych |
| 18 | Н н | N n | | Ніжин Nizhyn; Наталія Nataliia |
| 19 | О о | O o | | Одеса Odesa; Онищенко Onyshchenko |
| 20 | П п | P p | | Полтава Poltava; Петро Petro |
| 21 | Р р | R r | | Решетилівка Reshetylivka; Рибчинський Rybchynskyi |
| 22 | С с | S s | | Суми Sumy; Соломія Solomiia |
| 23 | Т т | T t | | Тернопіль Ternopil; Троць Trots |
| 24 | У у | U u | | Ужгород Uzhhorod; Уляна Uliana |
| 25 | Ф ф | F f | | Фастів Fastiv; Філіпчук Filipchuk |
| 26 | Х х | Kh kh | | Харків Kharkiv; Христина Khrystyna |
| 27 | Ц ц | Ts ts | | Біла Церква Bila Tserkva; Стеценко Stetsenko |
| 28 | Ч ч | Ch ch | | Чернівці Chernivtsi; Шевченко Shevchenko |
| 29 | Ш ш | Sh sh | | Шостка Shostka; Кишеньки Kyshenky |
| 30 | Щ щ | Shch shch | | Щербухи Shcherbukhy; Гоща Hoshcha; Гаращенко Harashchenko |
| 31 | Ь ь | ∅ | Note 2 | (Троць Trots) |
| 32 | Ю ю | Yu / iu | Yu at start of word; iu elsewhere | Юрій Yurii; Корюківка Koriukivka |
| 33 | Я я | Ya / ia | Ya at start of word; ia elsewhere | Яготин Yahotyn; Ярошенко Yaroshenko; Костянтин Kostiantyn; Знам'янка Znamianka; Феодосія Feodosiia |
| – | ' (apostrophe) | ∅ | Note 2 | Знам'янка Znamianka |

- Notes of the resolution (verbatim meaning): (1) the combination "зг" is rendered "zgh" (Згорани – Zghorany, Розгон – Rozghon), as opposed to "zh" for ж; (2) the soft sign and apostrophe are not rendered; (3) transliteration of surnames, given names and geographic names is done by rendering every letter in Latin — [KMU 55-2010](https://zakon.rada.gov.ua/laws/show/55-2010-%D0%BF). Official examples imply "after apostrophe" is NOT word-initial (Короп'є → Koropie, Мар'їне → Marine, Знам'янка → Znamianka).
- BGN/PCGN adopted this national system as the "BGN/PCGN 2019 Agreement", superseding BGN/PCGN 1965; it does not distinguish зг/кг/сг/тс from digraphs and is "not recommended for reverse transliteration"; table lists ’ (code 0146) and ь as "not romanized" — [BGN/PCGN Ukrainian PDF](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_UKRAINIAN.pdf). UNGEGN approved the Ukrainian system at its 27th session (2012) — [Wikipedia, Romanization of Ukrainian](https://en.wikipedia.org/wiki/Romanization_of_Ukrainian).
- ICAO 9303 Ukrainian exceptions (Г→H, И→Y, word-initial Є/Ї/Й/Ю/Я → YE/YI/Y/YU/YA, Ґ→G) coincide with KMU 2010 except that ICAO has no зг→ZGH rule — [ICAO Doc 9303 Part 3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2).
- Passport law: personal names are entered in the Register and documents "in Ukrainian and in Latin letters according to the transliteration rules"; on written request the Latin name may follow its spelling in previously issued Ukrainian identity/citizenship documents or in legalized foreign documents on birth or name change (incl. marriage/divorce) — Art. 10, Law No. 5492-VI on the Unified State Demographic Register (edition 27.06.2026) — [zakon.rada.gov.ua 5492-17](https://zakon.rada.gov.ua/laws/show/5492-17).
- KMU Resolution No. 152 of 7 May 2014 (passport for travel abroad; edition 01.01.2026), para. 108: surname and given name are shown in Ukrainian and, after a slash, in Latin letters "according to the transliteration rules"; on the applicant's written request they may follow the spelling in earlier Ukrainian identity documents, or in foreign documents on birth/name change (incl. marriage/divorce) subject to legalization (unless a treaty provides otherwise), submitted with a notarized Ukrainian translation; the surname may also follow the spelling of the surname of the person's child/parent(s)/spouse in their earlier passports for travel abroad, including foreign passports if those relatives are foreigners (para. 108 para. 2 amended by KMU No. 1709 of 24.12.2025) — [zakon.rada.gov.ua 152-2014-п](https://zakon.rada.gov.ua/laws/show/152-2014-%D0%BF).
- Same resolution: a change of the Latin spelling of surname/name in identity documents is a ground for exchanging the passport (para. 6(1)); documents must be filed within one month (para. 22, edition of KMU No. 1220 of 28.10.2022); if not, the passport is invalidated via the Register (para. 89 and related para.); data page filled per ICAO Doc 9303 (para. 110); field names in Ukrainian and English (para. 109) — [zakon.rada.gov.ua 152-2014-п](https://zakon.rada.gov.ua/laws/show/152-2014-%D0%BF).
- Superseded Ukrainian systems (for matching older documents), per [Wikipedia, Romanization of Ukrainian](https://en.wikipedia.org/wiki/Romanization_of_Ukrainian) (tables "Common systems" and "Ukrainian official systems"):

| Ukr | KMU 2010 (current) | BGN/PCGN 1965 (superseded 2019) | ALA-LC (strict) | ISO 9:1995 | Scholarly | National 1996 | Passport 2004 | Passport 2007 (flagged "failed verification") |
|---|---|---|---|---|---|---|---|---|
| Г | h (зг→zgh) | h | h | g | h | h (зг→zgh) | h, g | g |
| Ґ | g | g | g | g̀ | g | g | g, h | g |
| Е | e | e | e | e | e | e | e | e |
| Є | ye- / ie | ye | i͡e | ê | je | ye- / ie | ye- / ie | ie |
| Ж | zh | zh | z͡h | ž | ž | zh | zh, j | zh |
| И | y | y | y | i | y | y | y | y |
| І | i | i | i | ì | i | i | i | i |
| Ї | yi- / i | yi | ï | ï | ji | yi- / i | yi- / i | i |
| Й | y- / i | y | ĭ | j | j | y- / i | y- / i | i |
| Х | kh | kh | kh | h | x | kh | kh | kh |
| Ц | ts | ts | t͡s | c | c | ts | ts | ts |
| Ч | ch | ch | ch | č | č | ch | ch | ch |
| Ш | sh | sh | sh | š | š | sh | sh | sh |
| Щ | shch | shch | shch | ŝ | šč | sch | shch | shch |
| Ь | ∅ | ʼ | ʹ | ʹ | ʼ | ʼ | ʹ | ∅ |
| Ю | yu- / iu | yu | i͡u | û | ju | yu- / iu | yu- / iu | iu |
| Я | ya- / ia | ya | i͡a | â | ja | ya- / ia | ya- / ia | ia |
| ' | ∅ | ˮ | (not given) | ʼ | – | ˮ | ∅ | ∅ |
(All other letters: А a, Б b, В v (Passport 2004 also w), Д d, З z, К k (Passport 2004 also c), Л l, М m, Н n, О o, П p, Р r, С s, Т t, У u, Ф f in every column.) BGN/PCGN 1965 optional midpoints: зг z·h, кг k·h, сг s·h, тс t·s, цг ts·h. National 1996 simplified form drops doubled ж х ц ч ш (Запоріжжя = Zaporizhia) — same source. ALA-LC Ukrainian ligatures are needed to distinguish ж from зг and ц from тс — [LoC Ukrainian table](https://www.loc.gov/catdir/cpso/romanization/ukrainia.pdf).
- DSTU 9112:2021 (approved 1 Apr 2022) defines an ISO-9-like "A system" (г=ğ, ґ=g, є=je, и=y, і=i, х=x, ь=j, ю=ju, я=ja) and a "B system" (Derzhstandart 1995); not used for passports — [Wikipedia, Romanization of Ukrainian](https://en.wikipedia.org/wiki/Romanization_of_Ukrainian).
- "Modified Library of Congress" practice for names in English texts: initial Є-/Й-/Ю-/Я- → Ye-/Y-/Yu-/Ya-, soft sign ignored, -ий/-ій → -y, familiar names sometimes anglicized (Олександр → Alexander, Михайло → Michael); example Ярослав Рудницький: strict ALA-LC I͡Aroslav Rudnyt͡sʹkyĭ; academic Iaroslav Rudnytskyi; modified LC Yaroslav Rudnytsky; national Yaroslav Rudnytskyi — [Wikipedia, Romanization of Ukrainian](https://en.wikipedia.org/wiki/Romanization_of_Ukrainian).

**Test vectors (computed by applying the KMU 2010 table; the 28 official examples tested from the resolution reproduce exactly):**

| uk (Cyrillic) | KMU 2010 = BGN/PCGN 2019 (computed) | Upper-case (passport style) |
|---|---|---|
| Олександр | Oleksandr | OLEKSANDR |
| Олексій | Oleksii | OLEKSII |
| Андрій | Andrii | ANDRII |
| Сергій | Serhii | SERHII |
| Дмитро | Dmytro | DMYTRO |
| Юрій | Yurii | YURII |
| Євген | Yevhen | YEVHEN |
| Ігор | Ihor | IHOR |
| Олег | Oleh | OLEH |
| Михайло | Mykhailo | MYKHAILO |
| Микола | Mykola | MYKOLA |
| Володимир | Volodymyr | VOLODYMYR |
| В'ячеслав | Viacheslav | VIACHESLAV |
| Віталій | Vitalii | VITALII |
| Григорій | Hryhorii | HRYHORII |
| Ілля | Illia | ILLIA |
| Ярослав | Yaroslav | YAROSLAV |
| Наталія | Nataliia | NATALIIA |
| Тетяна | Tetiana | TETIANA |
| Катерина | Kateryna | KATERYNA |
| Ольга | Olha | OLHA |
| Ірина | Iryna | IRYNA |
| Юлія | Yuliia | YULIIA |
| Оксана | Oksana | OKSANA |
| Анастасія | Anastasiia | ANASTASIIA |
| Марія | Mariia | MARIIA |
| Галина | Halyna | HALYNA |
| Людмила | Liudmyla | LIUDMYLA |
| Світлана | Svitlana | SVITLANA |
| Олена | Olena | OLENA |
| Євгенія | Yevheniia | YEVHENIIA |
| Ганна | Hanna | HANNA |
| Яна | Yana | YANA |
| Шевченко | Shevchenko | SHEVCHENKO |
| Ковальчук | Kovalchuk | KOVALCHUK |
| Зеленський | Zelenskyi | ZELENSKYI |
| Згурський | Zghurskyi | ZGHURSKYI |
| Мельник | Melnyk | MELNYK |
| Бондаренко | Bondarenko | BONDARENKO |
| Кравчук | Kravchuk | KRAVCHUK |
| Їжакевич | Yizhakevych | YIZHAKEVYCH |
| Подоляк | Podoliak | PODOLIAK |
| Гнатюк | Hnatiuk | HNATIUK |
| Лозинська | Lozynska | LOZYNSKA |
| Ящук | Yashchuk | YASHCHUK |

### Inferences
- Implementation: word boundary for "start of word" = beginning of token after whitespace or hyphen (each part of a hyphenated name is a word; "after apostrophe" is NOT word start). Apply зг→zgh before single-letter mapping; uppercase: digraph value fully uppercased when the whole token is uppercase (ZH, SHCH), else title-cased (Zh, Shch).
- Ukrainian KMU output is identical to ICAO-uk for every name without "зг", so one Ukrainian passport generator plus a "no-zgh" variant covers both.
- For search, also generate from the Russian form of a Ukrainian citizen's name (e.g., Олександр/Александр, Сергій/Сергей) because pre-2010 Ukrainian and Soviet documents were often Russian-based (see section 6).

### Gaps
- Could not confirm whether Ukrainian biometric passports show the patronymic in Latin anywhere; KMU 152 para. 108 mentions only surname and given name in Latin.
- The ALA-LC Ukrainian apostrophe mapping could not be extracted from the PDF (ligature/special glyphs dropped in text extraction).

## 3. Belarusian: national system (2007 and 2023), what passports use, BGN/PCGN

### Takeaway
Belarus has three different "official" Latin forms: (a) the geographic-names Instruction of 24 Mar 2023 (no diacritics: Г→G, Х→H, Ц→C, Ў→W, Ч→CH, Ш→SH, Ж→ZH, Й→J, context J-forms), which replaced the 2000/2007 diacritic system (Č Š Ž Ŭ, soft sign as acute: ć ś ź ń ĺ); (b) the MVD Instruction No. 288 of 9 Oct 2008 for names in the population register (Г→G, Й→J, Ў→W, Х→KH, Ц→TS, context JE/IE...), which the MFA still cites for passports; (c) observed passport practice that follows ICAO 9303 with Belarusian exceptions (Г→H, Ё→IO, Й→I, Ў→U, Я→IA: "Maryia Rudz"). These conflict; a matcher must generate all three plus BGN/PCGN 1979 and Russian-based forms.

### Cited Findings
- Geographic names: Resolution of the State Property Committee No. 19 of 24 Mar 2023 (published 04.04.2023, reg. 8/39778) approved the "Instruction on rendering names of geographic objects from Belarusian and Russian into other languages and transliteration in Latin letters"; it repealed the 2000 instruction (Committee on Land Resources No. 15 of 23 Nov 2000) and its amendments of 24 Jul 2006 (No. 12) and 11 Jun 2007 (No. 38); agreed with MVD, MFA, Ministry of Culture and the Academy of Sciences — [pravo.by PDF](https://pravo.by/upload/docs/op/W22339778_1680555600.pdf); [pravo.by card](https://pravo.by/document/?guid=12551&p0=W22339778&p1=1&p5=0).
- 2023 Instruction rules: upper/lower case preserved (p. 8); hyphenated/split/solid spelling preserved (p. 9); for international products, Belarusian objects are transliterated only from the Belarusian form (p. 6) — [pravo.by PDF](https://pravo.by/upload/docs/op/W22339778_1680555600.pdf).
- 2023 Instruction, Appendix 1, Belarusian table (all 32 letters + apostrophe) — [pravo.by PDF](https://pravo.by/upload/docs/op/W22339778_1680555600.pdf):

| Bel | Latin | Rule | Official examples |
|---|---|---|---|
| А а | A a | | Адамаўка Adamawka |
| Б б | B b | | Бабруйск Babrujsk |
| В в | V v | | Воранава Voranava |
| Г г | G g | | Гогалеўка Gogaliewka |
| Д д | D d | | Дзедаў Курган Dziedaw Kurgan |
| Е е | Je je* / ie** | * word-initial, after vowels, apostrophe, separating soft sign and ў; ** after consonants | Ельск Jelsk; Заазер’е Zaazierje; Панізоўе Panizowje; Віцебск Viciebsk |
| Ё ё | Jo jo* / io** | as Е | Ёды Jody; Мікалаёўка Mikalajowka; Вераб’ёвічы Vierabjovichy; Мураўёўка Murawjowka; Вётхава Viothava |
| Ж ж | Zh zh | | Жажэлка Zhazhelka |
| З з | Z z | | Загуззе Zaguzzie |
| І і | I i | after apostrophe → ji (see apostrophe row) | Ізабелін Izabielin |
| Й й | J j | | Лагойск Lagojsk |
| К к | K k | | Каранёўка Karaniowka |
| Л л | L l | | Лепель Liepiel |
| М м | M m | | Мамонава Mamonava |
| Н н | N n | | Нёман Nioman |
| О о | O o | | Обеч Obiech; Полацк Polack |
| П п | P p | | Паперня Papiernia |
| Р р | R r | | Расцяробы Rasciaroby |
| С с | S s | | Свіслач Svislach |
| Т т | T t | | Татаршчына Tatarshchyna |
| У у | U u | | Улукаўе Ulukawje |
| Ў ў | W w | | Тураў Turaw |
| Ф ф | F f | | Фаніпаль Fanipal; Сафіеўка Safijewka |
| Х х | H h | | Хацюхова Haciuhova |
| Ц ц | C c | | Цяцерын Ciacieryn |
| Ч ч | Ch ch | | Чарнаручча Charnaruchcha |
| Ш ш | Sh sh | | Шаркаўшчына Sharkawshchyna |
| Ы ы | y | | Паставы Pastavy |
| Ь ь | ∅ | separating ь not shown, following е ё ю я take j-forms; softening ь not shown | Вільянава Viljanava; Вародзькаў 1 Varodzkaw 1 |
| Э э | E e | | Эйвідавічы Ejvidavichy; Чачэрск Chachersk |
| Ю ю | Ju ju* / iu** | as Е | Юрацішкі Juracishki; Гаюціна Gajucina; Цюрлі Ciurli |
| Я я | Ja ja* / ia** | as Е | Ямнае Jamnaje; Баяры Bajary; Валяр’яны Valiarjany; Гаўя Gawja; Вязынка Viazynka |
| ’ | ∅ | following е ё ю я і → j + vowel | Раз’езд Razjezd; Мар’іна Горка Marjina Gorka |

- 2023 Instruction, Appendix 2 (Russian-language names in Belarus): А a, Б b, В v, Г g, Д d, Е e (always: Еленка → Elenka), Ё jo (Ёни → Joni, Берёзки → Berjozki), Ж zh, З z, И i, Й j, К k, Л l, М m, Н n, О o, П p, Р r, С s, Т t, У u, Ф f, Х h, Ц c, Ч ch, Ш sh, Щ shch, Ъ → j with following vowel (Подъелье → Podjelje), Ы y, Ь separating → j with following vowel (Курганье → Kurganje), softening ь → ∅ (Мальковка Malkovka, Глинь Glin), Э e, Ю ju (Любань → Ljuban), Я ja (Якимово Лядо → Jakimovo Ljado) — [pravo.by PDF](https://pravo.by/upload/docs/op/W22339778_1680555600.pdf).
- Superseded national geographic systems (per [Wikipedia, Romanization of Belarusian](https://en.wikipedia.org/wiki/Romanization_of_Belarusian)): National 2000: Г h, Е je/ie, Ё jo/io, Ж ž, Й j, Ў ú, Х ch, Ц c, Ч č, Ш š, Ь ʼ, Ю ju/iu, Я ja/ia, ' –. National 2007: same but Ў ŭ and Ь = combining acute on preceding consonant (Беларусь → Bielaruś, Магілёў → Mahilioŭ). National 2023: Беларусь → Bielarus, Лукашэнка → Lukashenka, Магілёў → Magiliow, сям’я → siamja.
- Personal names (register / passports): MVD Resolution No. 288 of 9 Oct 2008 "Instruction on transliteration of surnames and given names of citizens of the Republic of Belarus when including their personal data in the population register" (reg. 8/19678 of 23.10.2008, published 3 Nov 2008), agreed with the Kolas & Kupala Institute of Language and Literature — [pravo.by card](https://pravo.by/document/?guid=3961&p0=W20819678); text — [levonevsky mirror](http://pravo.levonevsky.org/bazaby11/republic13/text623.htm). Key points: transliteration from the correct Belarusian OR Russian spelling attested by identity documents (p. 2); letter-by-letter (p. 3); softness marked by an acute diacritic over the consonant: дзь dź, зь ź, ль ĺ, нь ń, сь ś, ць ć (p. 5); compound names keep solid/space/hyphen spelling (p. 7).
- MVD No. 288 table (35 rows; Belarusian and Russian combined) — [levonevsky mirror](http://pravo.levonevsky.org/bazaby11/republic13/text623.htm); identical table on the [Belarus Embassy in France site](https://france.mfa.gov.by/be/consular_issues/passport/trans/):

| # | Letter | Latin | Rule / example (verbatim content) |
|---|---|---|---|
| 1 | А | A | |
| 2 | Б | B | |
| 3 | В | V | |
| 4 | Г | G | (no Belarusian exception in the table) |
| 5 | Д | D | |
| 6 | Е | E | except Belarusian: IE after consonant; JE word-initially, after vowel and after ў; "consonant + ь/’ + Е" → consonant + JE (Ева → Jeva, Васільева → Vasiljeva) |
| 7 | Ё | E | except Belarusian: IO after consonant; JO word-initially, after vowel and ў; consonant + ь/’ + Ё → consonant + JO (Васілёнак → Vasilionak, Ёрш → Jorsh, Вераб’ёў → Vierabjow, Салаўёва → Salawjova) |
| 8 | Ж | ZH | |
| 9 | З | Z | |
| 10 | И | I | |
| 11 | І | I | |
| 12 | Й | J | |
| 13–23 | К Л М Н О П Р С Т У Ф | K L M N O P R S T U F | |
| 24 | Х | KH | |
| 25 | Ц | TS | |
| 26 | Ч | CH | |
| 27 | Ш | SH | |
| 28 | Щ | SHCH | |
| 29 | Ы | Y | |
| 30 | Ъ | J with the following vowel (Адъютантов → Adjutantov) | |
| 31 | Э | E | |
| 32 | Ю | IU | except Belarusian: IU after consonant; JU word-initially, after vowel and ў; consonant + ь/’ + Ю → JU (Любоў → Liubow, В’юноў → Vjunow) |
| 33 | Я | IA | except Belarusian: IA after consonant; JA word-initially, after vowel and ў; consonant + ь/’ + Я → JA (Чарняк → Charniak, Лябецкая → Liabetskaja) |
| 34 | Ў | W | |
| 35 | ’ | J with the following vowel (Дар’я → Darja) | |

- Embassy guidance (current site): transliteration follows MVD No. 288; "if the applicant has not indicated a Latin transcription, automatic transliteration from Belarusian into English is performed"; changing the transliteration at the citizen's wish "more than once is not allowed"; superscript marks and punctuation are not allowed in surname/name except the apostrophe — [Belarus Embassy in France](https://france.mfa.gov.by/be/consular_issues/passport/trans/).
- Practice reports: a 2019 article states default transliteration follows "ICAO recommendations", that Belarusian Г is recorded as Latin H, gives the passport spelling "Maryia Rudz" for Марыя Рудзь, notes MVD Instruction No. 200 of 28 Jun 2010 (passport issuance) prohibits diacritics (contradicting p. 5 of No. 288), allows only one change, and requires name and surname to follow the same language — [ex-press.live, 23 Aug 2019](https://ex-press.live/rubrics/obshhestvo/2019/08/23/prosto-maria-legko-li-belorusam-izmenit-transliteraciyu-imeni-i-familii); a 2019 petition article confirms automatic transliteration from the Belarusian form and that citizens could not independently choose Russian-based transliteration at the time — [belnovosti.by, 18 Sep 2019](https://www.belnovosti.by/obshchestvo/belorusy-prosyat-mvd-pomenyat-pravila-transliteracii-imen-i-familiy). A commercial translation site gives an ICAO-style table for Belarusian passports (Г H, Ё IO, Й I, Ў U, Х KH, Ц TS, Ю IU, Я IA, Ь and apostrophe not written) — [24glo.com](https://24glo.com/ru/by/translit.html) (low-reliability source; it also contains an obvious error, Юрый → "Iurii").
- ICAO 9303 explicitly provides Belarusian exceptions Г → H and Ё → IO, and Ў → U — [ICAO Doc 9303 Part 3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2).
- BGN/PCGN 1979 Belarusian (checked Oct 2017): а a, б b, в v, г h, д d, е ye, ё yo, ж zh, з z, і i, й y, к k, л l, м m, н n, о o, п p, р r, с s, т t, у u, ў w, ф f, х kh, ц ts, ч ch, ш sh, ы y, ь ’, э e, ю yu, я ya, ’ (U+02BC) → ”; optional midpoints зг z·h, кг k·h, сг s·h, тс t·s, цг ts·h; apostrophes U+2019; "The Belarusian alphabet contains three characters not present in the Russian alphabet: і, ў, and ’" — [BGN/PCGN Belarusian PDF](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_BELARUSIAN.pdf). Note е/ё/ю/я are ye/yo/yu/ya in all positions (no positional rule).
- ALA-LC Belarusian (per Wikipedia comparison): Г h, Е e, Ё i͡o, Ж z͡h, Й ĭ, Ў ŭ, Х kh, Ц ts, Ч ch, Ш sh, Ы y, Ь ʹ, Э ė, Ю i͡u, Я i͡a, ' not romanized; Scholarly: Г h, Ё ë, Ж ž, Й j, Ў ŭ (w), Х x (ch), Ц c, Ч č, Ш š, Ь ʹ, Э è, Ю ju, Я ja; ISO 9: Г g, Ё ë, І ì, Ў ǔ, Х h, Э è, Ю û, Я â, ' ʼ — [Wikipedia, Romanization of Belarusian](https://en.wikipedia.org/wiki/Romanization_of_Belarusian).

**Test vectors (computed; each column applies the cited table; "ICAO-style" = ICAO 9303 base + Belarusian exceptions, matching the reported passport example "Maryia Rudz"):**

| be | ICAO 9303 w/ Belarusian exceptions (observed passport practice) | MVD No.288 table, strict | BGN/PCGN 1979 | National 2023 (geographic) |
|---|---|---|---|---|
| Аляксандр | Aliaksandr | Aliaksandr | Alyaksandr | Aliaksandr |
| Аляксей | Aliaksei | Aliaksiej | Alyaksyey | Aliaksiej |
| Сяргей | Siarhei | Siargiej | Syarhyey | Siargiej |
| Уладзімір | Uladzimir | Uladzimir | Uladzimir | Uladzimir |
| Яўген | Iauhen | Jawgien | Yawhyen | Jawgien |
| Андрэй | Andrei | Andrej | Andrey | Andrej |
| Дзмітрый | Dzmitryi | Dzmitryj | Dzmitryy | Dzmitryj |
| Юрый | Iuryi | Juryj | Yuryy | Juryj |
| Віктар | Viktar | Viktar | Viktar | Viktar |
| Ігар | Ihar | Igar | Ihar | Igar |
| Алег | Aleh | Alieg | Alyeh | Alieg |
| Павел | Pavel | Paviel | Pavyel | Paviel |
| Міхаіл | Mikhail | Mikhail | Mikhail | Mihail |
| Мікалай | Mikalai | Mikalaj | Mikalay | Mikalaj |
| Арцём | Artsiom | Artsiom | Artsyom | Arciom |
| Кірыл | Kiryl | Kiryl | Kiryl | Kiryl |
| Ганна | Hanna | Ganna | Hanna | Ganna |
| Кацярына | Katsiaryna | Katsiaryna | Katsyaryna | Kaciaryna |
| Вольга | Volha | Volga | Vol’ha | Volga |
| Марыя | Maryia | Maryja | Maryya | Maryja |
| Алена | Alena | Aliena | Alyena | Aliena |
| Таццяна | Tatstsiana | Tatstsiana | Tatstsyana | Tacciana |
| Святлана | Sviatlana | Sviatlana | Svyatlana | Sviatlana |
| Ірына | Iryna | Iryna | Iryna | Iryna |
| Наталля | Natallia | Natallia | Natallya | Natallia |
| Юлія | Iuliia | Julija | Yuliya | Julija |
| Ксенія | Kseniia | Ksienija | Ksyeniya | Ksienija |
| Дар'я | Daria | Darja | Dar”ya | Darja |
| Вікторыя | Viktoryia | Viktoryja | Viktoryya | Viktoryja |
| Лукашэнка | Lukashenka | Lukashenka | Lukashenka | Lukashenka |
| Ціханоўская | Tsikhanouskaia | Tsikhanowskaja | Tsikhanowskaya | Cihanowskaja |
| Ціханоўскі | Tsikhanouski | Tsikhanowski | Tsikhanowski | Cihanowski |
| Магілёў | Mahiliou | Magiliow | Mahilyow | Magiliow |
| Беларусь | Belarus | Bielarus | Byelarus’ | Bielarus |
| Віцебск | Vitsebsk | Vitsiebsk | Vitsyebsk | Viciebsk |
| Гомель | Homel | Gomiel | Homyel’ | Gomiel |
| Рудзь | Rudz | Rudz | Rudz’ | Rudz |
| Шушкевіч | Shushkevich | Shushkievich | Shushkyevich | Shushkievich |
| Малашонак | Malashonak | Malashonak | Malashonak | Malashonak |
| Багдановіч | Bahdanovich | Bagdanovich | Bahdanovich | Bagdanovich |
| Мар'іна | Marina | Marjina | Mar”ina | Marjina |

### Inferences
- Internal inconsistency in MVD No. 288: its own example "Лябецкая → Liabetskaja" violates its own rule (е after consonant б should give IE → "Liabietskaja"); treat the official example as an attested variant.
- Observed practice (H for Г, IA/IU without J, U for Ў, "Maryia") is not reproducible from the MVD No. 288 table; best current model of passport output is ICAO-9303-Belarusian. Because citizens may also have Russian-based spellings (No. 288 allows Belarusian or Russian source), a Belarus generator should emit: ICAO-be from the Belarusian form, ICAO-ru from the Russian form (e.g., Сяргей → SIARHEI vs Сергей → SERGEI), MVD-288 strict, BGN/PCGN, and National 2023.
- Belarusian sources mix Latin "i" (U+0069) into Cyrillic words (verified in the MVD No. 288 text: "Васiльева", "Васiлёнак" contain U+0069); normalize Latin i/I between Cyrillic letters to Cyrillic і/І (U+0456/U+0406) before detection and transliteration.

### Gaps
- No primary MVD document found that sets the ICAO-style rules actually seen in Belarusian passports (MVD Instruction No. 200 of 28.06.2010 text not retrieved; no post-2021 biometric-passport regulation located); I could not verify MRZ samples.
- ALA-LC Belarusian PDF from LoC was not retrievable (returned HTML).

## 4. Passport practice for specific letters, endings, double names, patronymics, MRZ formatting

### Takeaway
In current Russian passports the letters are mapped context-free per ICAO (Ё→E, Й→I, Ъ→IE, Ь→∅, Щ→SHCH, Ы→Y, Э→E, Х→KH, Ц→TS, Ж→ZH); hence -ий → -II (DMITRII), -ый → -YI, Дарья → DARIA, кс stays KS; data are printed in upper case, hyphenated/compound surnames become "<" in the MRZ, apostrophes are removed, and the patronymic appears in Cyrillic only. Ukraine applies KMU 2010 (word-initial Y-forms), Belarus effectively ICAO-be.

### Cited Findings
- Russia, MVD Order 186: data printed in upper case (139.1); surname line 1 in Russian, line 2 transliterated (139.2); "Имя" field: name(s) and patronymic (if any) in Russian on line 1, and line 2 "duplicated by transliteration (only the name(s))" (139.3) — patronymic is not transliterated — [Consultant, para 139](https://www.consultant.ru/document/cons_doc_LAW_384459/d3c3b53854fd15c08984f777d0101cede5c99ca8/).
- Russia, MRZ (Appendix 12 to Order 186): positions 6–44 of line 1 = surname and name(s); "Double or compound surnames are separated by the symbol '<', apostrophes are excluded"; surname and name separated by "<<"; unused positions filled with "<"; if too long, preferred names printed, initials or abbreviations may be used; OCR-B font; check digits mod 10 with weights 7-3-1 — [Consultant, App. 12](https://www.consultant.ru/document/cons_doc_LAW_384459/62023e40ffe7c02553bb9c9549df200b0945e989/).
- ICAO/passport Russian outputs (iuliia samples): Андрей Видный → Andrei Vidnyi; Мадыр Чёткий → Madyr Chetkii; Артём Краевой → Artem Kraevoi; Оксана Клеёнкина → Oksana Kleenkina; Игорь Ильин → Igor Ilin; Гайа Васильева → Gaia Vasileva; Ян Разъездной → Ian Razieezdnoi — [icao_doc_9303.json](https://github.com/nalgeon/iuliia/blob/master/icao_doc_9303.json).
- Ё problem: MFA (2024) acknowledged complaints about names with "ё" (e.g., "Semyon", "Fyodor") and said differing transliterations are not an error — [Interfax](https://www.interfax.ru/russia/966690).
- Pre-2010 passport endings: ИЙ → IY or Y, ЫЙ → YY or Y, ЕЙ → EY or YEY (MVD 310 "English") — [iuliia.ru/mvd-310](https://iuliia.ru/mvd-310/); passport 1997 column footnote: ий either iy or y, ый either y or yy — [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian).
- КС → X only in the MVD 310 "French" variant (Oxana, Maximov) — [iuliia.ru/mvd-310](https://iuliia.ru/mvd-310/); German Duden recommends кс → x "in all cases", German Wikipedia applies it only to Greek/Latin-origin words (Алексей → Alexei) — [de.wikipedia, Kyrillisches Alphabet](https://de.wikipedia.org/wiki/Kyrillisches_Alphabet#Russisch).
- Ukraine: passport shows surname and name in Ukrainian and Latin; data page per ICAO Doc 9303; field captions Ukrainian+English — [KMU 152-2014, paras 108–110](https://zakon.rada.gov.ua/laws/show/152-2014-%D0%BF). KMU 2010 Note 3: every letter of a name is rendered; ь and apostrophe dropped — [KMU 55-2010](https://zakon.rada.gov.ua/laws/show/55-2010-%D0%BF).
- Belarus: compound names keep solid/space/hyphen spelling (MVD 288 p. 7); no superscripts or punctuation except apostrophe — [levonevsky mirror](http://pravo.levonevsky.org/bazaby11/republic13/text623.htm), [Belarus Embassy France](https://france.mfa.gov.by/be/consular_issues/passport/trans/).
- Double surnames exist by law/custom (e.g., Ivanov-Petrovsky / Ivanova-Petrovskaya for spouses) — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).

**Russian passport (ICAO) outputs for problem letters (computed with the ICAO table):** Дмитрий → DMITRII; Юрий → IURII; Евгений → EVGENII; Алексей → ALEKSEI; Сергей → SERGEI; Красный → KRASNYI; Пётр → PETR; Фёдор → FEDOR; Семён → SEMEN; Артём → ARTEM; Хрущёв → KHRUSHCHEV; Щербаков → SHCHERBAKOV; Дарья → DARIA; Наталья → NATALIA; Татьяна → TATIANA; Ольга → OLGA; Игорь → IGOR; Ксения → KSENIIA; Максим → MAKSIM; Подъячев → PODIEIACHEV; Анна-Мария → ANNA-MARIIA (VIZ) / ANNA<MARIIA (MRZ name part); Петров-Водкин → PETROV-VODKIN / PETROV<VODKIN.

### Inferences
- Package should expose an `mrz=True` option: upper-case, map space/hyphen → "<", drop apostrophes and any non A–Z characters, "<<" between primary and secondary identifiers, pad/truncate to field length (39 chars for TD3 line 1 names per App. 12).
- Hyphenated given names (Анна-Мария) and surnames should be split on "-" and each part treated as a separate word for word-initial rules (relevant for KMU 2010, BGN/PCGN, WP, Belarus 2023), then rejoined.
- Since Russian passports omit patronymics in Latin, a matcher should allow the patronymic to be absent on the Latin side and present (Cyrillic) on the other.

### Gaps
- No primary source found specifying how Russian MRZ handles given names with hyphen beyond the surname rule (assumed same "<" convention per ICAO); not verified on samples.

## 5. Can a citizen request a custom spelling? Rules

### Takeaway
Yes in all three countries, but only with documentary evidence: Russia (application form + one of: previous passport, foreign civil-status documents, spouse's/parent's passport, foreign residence permit), Ukraine (written request + earlier Ukrainian documents, legalized foreign birth/name-change documents with notarized translation, or relatives' passports), Belarus (applicant may state a Latin transcription; change at own wish allowed once).

### Cited Findings
- Russia (MVD Order 186, para 32): applicant wishing to change the spelling submits an "application for changing the spelling of surname and/or name in Latin letters" (form in Appendix No. 4) stating the reason, with one of: a previously issued passport (incl. biometric); foreign-issued civil-status documents (birth, name change, marriage/divorce showing the surname); passport of the spouse whose surname was taken at marriage; passport of the parent/legal representative whose surname a minor bears; residence permit or other document of permanent residence abroad — [Consultant, para 32](https://www.consultant.ru/document/cons_doc_LAW_384459/7865c83f2bf1ed36676f3f3d90cc0747f49bd85a/). Para 140: the name is then written "as indicated in the confirming document" upon the authorized manager's resolution — [Consultant, para 140](https://www.consultant.ru/document/cons_doc_LAW_384459/d3c3b53854fd15c08984f777d0101cede5c99ca8/). Form text: "Прошу произвести написание фамилии и (или) имени ... следующим образом ___ в соответствии с представленным мной документом" — [Consultant, App. 4](https://www.consultant.ru/document/cons_doc_LAW_384459/8d4bc6d806ae0d2c6cb614bf3ed7870ba1fe60e1/). New forms: MVD Order No. 83 of 24.02.2026 — [Consultant](https://www.consultant.ru/document/cons_doc_LAW_384459/).
- Russia (MFA): citizens may request modified transliteration based on documents listed in the regulations, including foreign birth, marriage, and name-change certificates — [Interfax 2024](https://www.interfax.ru/russia/966690). In 2010, citizens wishing to keep pre-2010 spellings could apply to the migration office — [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Russian).
- Ukraine: Art. 10 Law 5492-VI and KMU 152 para. 108 (details in section 2) — [Law 5492-VI](https://zakon.rada.gov.ua/laws/show/5492-17), [KMU 152](https://zakon.rada.gov.ua/laws/show/152-2014-%D0%BF).
- Belarus: Latin transcription may be indicated by the applicant; otherwise automatic from Belarusian; change at own wish no more than once — [Belarus Embassy France](https://france.mfa.gov.by/be/consular_issues/passport/trans/); both name and surname must follow the same language rules — [ex-press.live 2019](https://ex-press.live/rubrics/obshhestvo/2019/08/23/prosto-maria-legko-li-belorusam-izmenit-transliteraciyu-imeni-i-familii).

### Inferences
- Because custom spellings are legal, any Latin spelling of a person's name may be "official"; a matching package cannot treat non-standard spellings as errors and should score fuzzy/phonetic matches across all generators.

### Gaps
- Did not find statistics on how often custom spellings are requested.

## 6. Popular / English-conventional spellings vs strict; variant sets and variation patterns

### Takeaway
Real-world spellings form a lattice: passport-ICAO (Iurii, Dmitrii, Evgenii), pre-2010 passport (Yuriy, Dmitriy, Evgeniy), BGN/media (Yuri/Yury, Dmitry, Yevgeny), French (Iouri, Dmitri, Evgueni, Serguei, Tchaikovski), German (Juri, Jewgeni, Tschaikowski), Polish (Jurij, Czajkowski), plus Ukrainian/Belarusian national forms of cognate names (Oleksandr, Aliaksandr). Most variation is concentrated in ~12 letters/contexts: й/-ий/-ый, е-iotation, ё, ь/ъ, х, ж, ч, ш, щ, ц, ю/я, кс, and -ов/-ев endings (-ov/-off/-ow).

### Cited Findings
**Variant sets documented by Wikipedia name articles (spellings as listed):**
- Юрий: Jury, Jurij, Iurii, Iouri, Yury, Yuri, Youri, Yurii, Yuriy, Yurij (Belarusian Юры Jury; Ukrainian Юрій Yurii) — [Wikipedia, Yury](https://en.wikipedia.org/wiki/Yury).
- Евгений: Yevgeni, Yevgeny, Yevgenii, Yevgeniy, Evgeni, Evgeny, Evgenii, Evgeniy, Evgenyi, Evgenij; Женя: Zhenya, Jenya, Shenya — [Wikipedia, Yevgeny](https://en.wikipedia.org/wiki/Yevgeny).
- Ксения: Xenia, Ksenia, Kseniia, Ksenija, Kseniya; related Oksana — [Wikipedia, Xenia (name)](https://en.wikipedia.org/wiki/Xenia_(name)).
- Татьяна: Tatiana, Tatianna, Tatyana, Tatjana, Tatijana — [Wikipedia, Tatiana](https://en.wikipedia.org/wiki/Tatiana).
- Юлия: Yulia, Yulya, Julia, Julja, Julija, Yuliia, Yuliya, Juliya, İulia, Ioulia, Iuliia — [Wikipedia, Yulia](https://en.wikipedia.org/wiki/Yulia).
- Екатерина: Ekaterina is an alternative transliteration of Yekaterina — [Wikipedia, Ekaterina](https://en.wikipedia.org/wiki/Ekaterina).
- Александр: variants Aleksandar, Aleksander, Oleksandr, Oleksander, Aleksandr, Alekzandr (and Alexander) — [Wikipedia, Alexander](https://en.wikipedia.org/wiki/Alexander).
- Алексей: Alexey, Aleksey; Ukrainian Oleksii, Belarusian Aliaksiej; church form Alexiy/Aleksiy — [Wikipedia, Alexey](https://en.wikipedia.org/wiki/Alexey).
- Дмитрий: Dmitry; church forms Dimitry/Dimitri; D'mitriy — [Wikipedia, Dmitry](https://en.wikipedia.org/wiki/Dmitry).
- Вячеслав: Vyacheslav, Viacheslav, Viatcheslav; Belarusian Viachaslau — [Wikipedia, Vyacheslav](https://en.wikipedia.org/wiki/Vyacheslav).
- Виталий: Vitali, Vitalii, Vitaly, Vitaliy — [Wikipedia, Vitali](https://en.wikipedia.org/wiki/Vitali).
- Анатолий: Anatoly, Anatoliy (ru), Anatolii (uk) — [Wikipedia, Anatoly](https://en.wikipedia.org/wiki/Anatoly).
- Григорий: Grigory, Grigori, Grigoriy — [Wikipedia, Grigory](https://en.wikipedia.org/wiki/Grigory).
- Василий: Vasili, Vasily, Vasilii, Vasiliy — [Wikipedia, Vasily](https://en.wikipedia.org/wiki/Vasily).
- Геннадий: Gennady, Gennadi, Gennadiy, Hennadiy, Hienadzij, Hennady, Henadzi — [Wikipedia, Gennady](https://en.wikipedia.org/wiki/Gennady).
- Валерий: Valery, Valeriy, Valeri — [Wikipedia, Valery](https://en.wikipedia.org/wiki/Valery).
- Фёдор: Fyodor, Fedor, Feodor — [Wikipedia, Fyodor](https://en.wikipedia.org/wiki/Fyodor).
- Илья: Ilya, Iliya, Ilia, Ilja, Ilija, Illia (uk Ілля Illia) — [Wikipedia, Ilya](https://en.wikipedia.org/wiki/Ilya).
- Артём: Artyom; Artem when ё is not written; Belarusian Artsyom; Moldovan Artiom — [Wikipedia, Artyom](https://en.wikipedia.org/wiki/Artyom).
- Максим: Maxim, Maksim, Maksym, Maxym — [Wikipedia, Maxim (given name)](https://en.wikipedia.org/wiki/Maxim_(given_name)).
- Матвей: Matvei, Matvey — [Wikipedia, Matvei](https://en.wikipedia.org/wiki/Matvei).
- Егор: Yegor, Egor, Egori, Jegor; Belarusian Yahor; Ukrainian Yehor — [Wikipedia, Yegor](https://en.wikipedia.org/wiki/Yegor).
- Николай: Nikolai, Nikolay — [Wikipedia, Nikolai](https://en.wikipedia.org/wiki/Nikolai).
- Ольга: Olga; Ukrainian Olha; Belarusian Vol'ha — [Wikipedia, Olga (name)](https://en.wikipedia.org/wiki/Olga_(name)).
- Ирина: Irina, Iryna — [Wikipedia, Irina](https://en.wikipedia.org/wiki/Irina).
- Оксана: Oksana, Oxana, Aksana (be) — [Wikipedia, Oksana](https://en.wikipedia.org/wiki/Oksana).
- Людмила: Ludmila, Ludmilla, Liudmila, Liudmyla, Lyudmila, Lyudmyla — [Wikipedia, Ludmila](https://en.wikipedia.org/wiki/Ludmila).
- Галина: Galina; Halyna (uk), Halina (be) — [Wikipedia, Galina](https://en.wikipedia.org/wiki/Galina).
- Любовь: Lyubov, Liubov, Lubov — [Wikipedia, Lyubov](https://en.wikipedia.org/wiki/Lyubov).
- Наталья: Natalya, Russian form of Natalia; Natasha — [Wikipedia, Natalya](https://en.wikipedia.org/wiki/Natalya).

**Strict-system outputs for common Russian names and surnames (computed by applying each iuliia schema; column names = iuliia schema IDs):**

| ru | icao_doc_9303 | gost_52535 | mvd_310 | mvd_310_fr | mvd_782 | bgn_pcgn_alt | wikipedia | ala_lc_alt | gost_779_alt | scientific | telegram | yandex_money |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Александр | Aleksandr | Aleksandr | Aleksandr | Alexandr | Aleksandr | Aleksandr | Aleksandr | Aleksandr | Aleksandr | Aleksandr | Aleksandr | Aleksandr |
| Алексей | Aleksei | Aleksei | Aleksey | Alexei | Aleksey | Aleksey | Aleksey | Aleksei | Aleksej | Aleksej | Aleksei | Aleksei |
| Анатолий | Anatolii | Anatolii | Anatoliy | Anatolii | Anatoliy | Anatoliy | Anatoly | Anatolii | Anatolij | Anatolij | Anatolii | Anatolii |
| Андрей | Andrei | Andrei | Andrey | Andrei | Andrey | Andrey | Andrey | Andrei | Andrej | Andrej | Andrei | Andrei |
| Артём | Artem | Artem | Artem | Artem | Artyem | Artëm | Artyom | Artem | Artyom | Artëm | Artem | Artem |
| Валерий | Valerii | Valerii | Valeriy | Valerii | Valeriy | Valeriy | Valery | Valerii | Valerij | Valerij | Valerii | Valerii |
| Василий | Vasilii | Vasilii | Vasiliy | Vasilii | Vasiliy | Vasiliy | Vasily | Vasilii | Vasilij | Vasilij | Vasilii | Vasilii |
| Виталий | Vitalii | Vitalii | Vitaliy | Vitalii | Vitaliy | Vitaliy | Vitaly | Vitalii | Vitalij | Vitalij | Vitalii | Vitalii |
| Вячеслав | Viacheslav | Viacheslav | Vyacheslav | Viatcheslav | Vyacheslav | Vyacheslav | Vyacheslav | Viacheslav | Vyacheslav | Vjačeslav | Viacheslav | Vyacheslav |
| Геннадий | Gennadii | Gennadii | Gennadiy | Guennadii | Gennadiy | Gennadiy | Gennady | Gennadii | Gennadij | Gennadij | Gennadii | Gennadii |
| Георгий | Georgii | Georgii | Georgiy | Gueorguii | Georgiy | Georgiy | Georgy | Georgii | Georgij | Georgij | Georgii | Georgii |
| Григорий | Grigorii | Grigorii | Grigoriy | Grigorii | Grigoriy | Grigoriy | Grigory | Grigorii | Grigorij | Grigorij | Grigorii | Grigorii |
| Дмитрий | Dmitrii | Dmitrii | Dmitriy | Dmitrii | Dmitriy | Dmitriy | Dmitry | Dmitrii | Dmitrij | Dmitrij | Dmitrii | Dmitrii |
| Евгений | Evgenii | Evgenii | Evgeniy | Evguenii | Evgeniy | Yevgeniy | Yevgeny | Evgenii | Evgenij | Evgenij | Evgenii | Evgenii |
| Егор | Egor | Egor | Egor | Egor | Egor | Yegor | Yegor | Egor | Egor | Egor | Egor | Egor |
| Игорь | Igor | Igor | Igor' | Igor | Igor' | Igor’ | Igor | Igor' | Igor` | Igorʹ | Igor | Igor |
| Илья | Ilia | Ilia | Il'ya | Ilia | Il'ya | Il’ya | Ilya | Il'ia | Il`ya | Ilʹja | Ilia | Ilya |
| Константин | Konstantin | Konstantin | Konstantin | Konstantine | Konstantin | Konstantin | Konstantin | Konstantin | Konstantin | Konstantin | Konstantin | Konstantin |
| Максим | Maksim | Maksim | Maksim | Maxim | Maksim | Maksim | Maksim | Maksim | Maksim | Maksim | Maksim | Maksim |
| Матвей | Matvei | Matvei | Matvey | Matvei | Matvey | Matvey | Matvey | Matvei | Matvej | Matvej | Matvei | Matvei |
| Михаил | Mikhail | Mikhail | Mikhail | Mikhail | Mikhail | Mikhail | Mikhail | Mikhail | Mixail | Mixail | Mihail | Mikhail |
| Николай | Nikolai | Nikolai | Nikolay | Nikolai | Nikolay | Nikolay | Nikolay | Nikolai | Nikolaj | Nikolaj | Nikolai | Nikolai |
| Пётр | Petr | Petr | Petr | Petr | Pyetr | Pëtr | Pyotr | Petr | Pyotr | Pëtr | Petr | Petr |
| Сергей | Sergei | Sergei | Sergey | Serguei | Sergey | Sergey | Sergey | Sergei | Sergej | Sergej | Sergei | Sergei |
| Семён | Semen | Semen | Semen | Semen | Semyen | Semën | Semyon | Semen | Semyon | Semën | Semen | Semen |
| Фёдор | Fedor | Fedor | Fedor | Fedor | Fyedor | Fëdor | Fyodor | Fedor | Fyodor | Fëdor | Fedor | Fedor |
| Юрий | Iurii | Iurii | Yuriy | Iourii | Yuriy | Yuriy | Yury | Iurii | Yurij | Jurij | Iurii | Yurii |
| Ярослав | Iaroslav | Iaroslav | Yaroslav | Iaroslav | Yaroslav | Yaroslav | Yaroslav | Iaroslav | Yaroslav | Jaroslav | Iaroslav | Yaroslav |
| Анастасия | Anastasiia | Anastasiia | Anastasiya | Anastasiia | Anastasiya | Anastasiya | Anastasiya | Anastasiia | Anastasiya | Anastasija | Anastasiia | Anastasiya |
| Дарья | Daria | Daria | Dar'ya | Daria | Dar'ya | Dar’ya | Darya | Dar'ia | Dar`ya | Darʹja | Daria | Darya |
| Евгения | Evgeniia | Evgeniia | Evgeniya | Evgueniia | Evgeniya | Yevgeniya | Yevgeniya | Evgeniia | Evgeniya | Evgenija | Evgeniia | Evgeniya |
| Екатерина | Ekaterina | Ekaterina | Ekaterina | Ekaterina | Ekaterina | Yekaterina | Yekaterina | Ekaterina | Ekaterina | Ekaterina | Ekaterina | Ekaterina |
| Елена | Elena | Elena | Elena | Elena | Elena | Yelena | Yelena | Elena | Elena | Elena | Elena | Elena |
| Ксения | Kseniia | Kseniia | Kseniya | Xeniia (a) | Kseniya | Kseniya | Kseniya | Kseniia | Kseniya | Ksenija | Kseniia | Kseniya |
| Любовь | Liubov | Liubov | Lyubov' | Lioubov | Lyubov' | Lyubov’ | Lyubov | Liubov' | Lyubov` | Ljubovʹ | Liubov | Lyubov |
| Людмила | Liudmila | Liudmila | Lyudmila | Lioudmila | Lyudmila | Lyudmila | Lyudmila | Liudmila | Lyudmila | Ljudmila | Liudmila | Lyudmila |
| Мария | Mariia | Mariia | Mariya | Mariia | Mariya | Mariya | Mariya | Mariia | Mariya | Marija | Mariia | Mariya |
| Надежда | Nadezhda | Nadezhda | Nadezhda | Nadejda | Nadezhda | Nadezhda | Nadezhda | Nadezhda | Nadezhda | Nadežda | Nadejda | Nadezhda |
| Наталья | Natalia | Natalia | Natal'ya | Natalia | Natal'ya | Natal’ya | Natalya | Natal'ia | Natal`ya | Natalʹja | Natalia | Natalya |
| Наталия | Nataliia | Nataliia | Nataliya | Nataliia | Nataliya | Nataliya | Nataliya | Nataliia | Nataliya | Natalija | Nataliia | Nataliya |
| Ольга | Olga | Olga | Ol'ga | Olga | Ol'ga | Ol’ga | Olga | Ol'ga | Ol`ga | Olʹga | Olga | Olga |
| Софья | Sofia | Sofia | Sof'ya | Sofia | Sof'ya | Sof’ya | Sofya | Sof'ia | Sof`ya | Sofʹja | Sofia | Sofya |
| Татьяна | Tatiana | Tatiana | Tat'yana | Tatiana | Tat'yana | Tat’yana | Tatyana | Tat'iana | Tat`yana | Tatʹjana | Tatiana | Tatyana |
| Юлия | Iuliia | Iuliia | Yuliya | Iouliia | Yuliya | Yuliya | Yuliya | Iuliia | Yuliya | Julija | Iuliia | Yuliya |
| Яна | Iana | Iana | Yana | Iana | Yana | Yana | Yana | Iana | Yana | Jana | Iana | Yana |
| Щербаков | Shcherbakov | Shcherbakov | Shcherbakov | Chtcherbakov | Shcherbakov | Shcherbakov | Shcherbakov | Shcherbakov | Shherbakov | Ščerbakov | Scerbakov | Scherbakov |
| Хрущёв | Khrushchev | Khrushchev | Khrushchev | Khrouchtchev | Khrushchev | Khrushchëv | Khrushchyov | Khrushchev | Xrushhyov | Xruščëv | Hruscev | Khruschev |
| Чайковский | Chaikovskii | Chaikovskii | Chaykovskiy | Tchaikovskii | Chaykovskiy | Chaykovskiy | Chaykovsky | Chaikovskii | Chajkovskij | Čajkovskij | Chaikovskii | Chaikovskii |
| Горбачёв | Gorbachev | Gorbachev | Gorbachev | Gorbatchev | Gorbachev | Gorbachëv | Gorbachyov | Gorbachev | Gorbachyov | Gorbačëv | Gorbachev | Gorbachev |
| Ельцин | Eltsin | Eltcin | El'tsin | Eltsine | El'tsin | Yel’tsin | Yeltsin | El'tsin | El`cin | Elʹcin | Elcin | Eltsin |
| Достоевский | Dostoevskii | Dostoevskii | Dostoevskiy | Dostoevskii | Dostoyevskiy | Dostoyevskiy | Dostoyevsky | Dostoevskii | Dostoevskij | Dostoevskij | Dostoevskii | Dostoevskii |
| Соловьёв | Solovev | Solovev | Solov'ev | Solovev | Solovyov | Solov’yëv | Solovyov | Solov'ev | Solov`yov | Solovʹëv | Solovev | Solovev |
| Воробьёва | Vorobeva | Vorobeva | Vorob'eva | Vorobeva | Vorobyova | Vorob’yëva | Vorobyova | Vorob'eva | Vorob`yova | Vorobʹëva | Vorobeva | Vorobeva |
| Васильева | Vasileva | Vasileva | Vasilyeva | Vasilieva | Vasilyeva | Vasil’yeva | Vasilyeva | Vasil'eva | Vasil`eva | Vasilʹeva | Vasileva | Vasileva |
| Ильин | Ilin | Ilin | Il'in | Iline | Ilyin | Il’in | Ilyin | Il'in | Il`in | Ilʹin | Ilin | Ilin |
| Кузнецов | Kuznetsov | Kuznetcov | Kuznetsov | Kouznetsov | Kuznetsov | Kuznetsov | Kuznetsov | Kuznetsov | Kuzneczov | Kuznecov | Kuznecov | Kuznetsov |
| Жуков | Zhukov | Zhukov | Zhukov | Joukov | Zhukov | Zhukov | Zhukov | Zhukov | Zhukov | Žukov | Jukov | Zhukov |
| Подъячев | Podieiachev | Podiachev | Pod"yachev | Podiatchev | Pod'yachev | Pod”yachev | Podyachev | Pod"iachev | Pod``yachev | Podʺjačev | Podiachev | Podyachev |
| Аксёнов | Aksenov | Aksenov | Aksenov | Axenov | Aksyenov | Aksënov | Aksyonov | Aksenov | Aksyonov | Aksënov | Aksenov | Aksenov |
| Ерофеев | Erofeev | Erofeev | Erofeev | Erofeev | Erofeyev | Yerofeyev | Yerofeev (b) | Erofeev | Erofeev | Erofeev | Erofeev | Erofeev |
| Ковальчук | Kovalchuk | Kovalchuk | Koval'chuk | Kovaltchouk | Koval'chuk | Koval’chuk | Kovalchuk | Koval'chuk | Koval`chuk | Kovalʹčuk | Kovalchuk | Kovalchuk |
| Петров-Водкин | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkine | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin | Petrov-Vodkin |

(a) iuliia's own engine yields lowercase "xeniia" here (case-propagation bug); corrected. (b) WP:RUS text implies "Yerofeyev"; iuliia omits е-after-е.

**Foreign-language conventions (Wikipedia interlanguage article titles):**

| Russian | en | de | fr | pl | cs | es | it | nl | sv | tr |
|---|---|---|---|---|---|---|---|---|---|---|
| Горбачёв | Gorbachev | Gorbatschow | Gorbatchev | Gorbaczow | Gorbačov | Gorbachov | Gorbačëv | Gorbatsjov | Gorbatjov | Gorbaçov |
| Чайковский | Tchaikovsky | Tschaikowski | Tchaïkovski | Czajkowski | Čajkovskij | Chaikovski | Čajkovskij | Tsjaikovski | Tjajkovskij | Çaykovski |
| Хрущёв | Khrushchev | Chruschtschow | Khrouchtchev | Chruszczow | Chruščov | Jrushchov | Chruščëv | Chroesjtsjov | Chrusjtjov | Kruşçev |
| Ельцин | Yeltsin | Jelzin | Eltsine | Jelcyn | Jelcin | Yeltsin | El'cin | Jeltsin | Jeltsin | Yeltsin |
| Рахманинов | Rachmaninoff | Rachmaninow | Rachmaninov | Rachmaninow | Rachmaninov | Rajmáninov | Rachmaninov | Rachmaninov | Rachmaninov | Rahmaninov |
| Евтушенко (Евгений) | Yevgeny Yevtushenko | Jewgeni Jewtuschenko | Ievgueni Ievtouchenko | Jewgienij Jewtuszenko | Jevgenij Jevtušenko | Yevgueni Yevtushenko | Evgenij Evtušenko | Jevgeni Jevtoesjenko | Jevgenij Jevtusjenko | Yevgeni Yevtuşenko |
| Жириновский | Zhirinovsky | Schirinowski | Jirinovski | Żyrinowski | Žirinovskij | Zhirinovski | Žirinovskij | Zjirinovski | Zjirinovskij | Jirinovski |
| Достоевский (Фёдор) | Fyodor Dostoevsky | Fjodor Dostojewski | Fiodor Dostoïevski | Fiodor Dostojewski | Fjodor Dostojevskij | Fiódor Dostoyevski | Fëdor Dostoevskij | Fjodor Dostojevski | Fjodor Dostojevskij | Fyodor Dostoyevski |
| Шостакович | Shostakovich | Schostakowitsch | Chostakovitch | Szostakowicz | Šostakovič | Shostakóvich | Šostakovič | Sjostakovitsj | Sjostakovitj | Şostakoviç |
| Калашников | Kalashnikov | Kalaschnikow | Kalachnikov | Kałasznikow | Kalašnikov | Kaláshnikov | Kalašnikov | Kalasjnikov | Kalasjnikov | Kalaşnikov |
| Солженицын | Solzhenitsyn | Solschenizyn | Soljenitsyne | Sołżenicyn | Solženicyn | Solzhenitsyn | Solženicyn | Solzjenitsyn | Solzjenitsyn | Soljenitsin |
| Михаил | Mikhail | Michail | Mikhaïl | Michaił | Michail | Mijaíl | Michail | Michail | Michail | Mihail |
Sources: interlanguage links of [Mikhail Gorbachev](https://en.wikipedia.org/wiki/Mikhail_Gorbachev), [Pyotr Ilyich Tchaikovsky](https://en.wikipedia.org/wiki/Pyotr_Ilyich_Tchaikovsky), [Nikita Khrushchev](https://en.wikipedia.org/wiki/Nikita_Khrushchev), [Boris Yeltsin](https://en.wikipedia.org/wiki/Boris_Yeltsin), [Sergei Rachmaninoff](https://en.wikipedia.org/wiki/Sergei_Rachmaninoff), [Yevgeny Yevtushenko](https://en.wikipedia.org/wiki/Yevgeny_Yevtushenko), [Vladimir Zhirinovsky](https://en.wikipedia.org/wiki/Vladimir_Zhirinovsky), [Fyodor Dostoevsky](https://en.wikipedia.org/wiki/Fyodor_Dostoevsky), [Dmitri Shostakovich](https://en.wikipedia.org/wiki/Dmitri_Shostakovich), [Mikhail Kalashnikov](https://en.wikipedia.org/wiki/Mikhail_Kalashnikov), [Aleksandr Solzhenitsyn](https://en.wikipedia.org/wiki/Aleksandr_Solzhenitsyn) (titles retrieved via MediaWiki API langlinks, Oct 2026; patronymics omitted).

**Rule-level conventions**
- French (fr.wikipedia "Transcription du russe en français"): г → gu before е, и, ы (Сергей → Sergueï, Георгий → Gueorgui); е → e after consonant/и/й, ïe after other vowels (Дудаев → Doudaïev), ie word-initially and after ь/ъ (Васильев → Vassiliev), conventional e (Ельцин → Eltsine); ё → io, conventional e (Горбачёв → Gorbatchev); ж → j; и → ï after a vowel other than и (Михаил → Mikhaïl); й → not written in -ий/-ый (Достоевский → Dostoïevski, Грозный → Grozny), else ï (Андрей → Andreï); н → ne word-finally after и/ы (Гагарин → Gagarine, Солженицын → Soljenitsyne); с → ss between vowels (Новосибирск → Novossibirsk); у → ou; х → kh; ц → ts; ч → tch; ш → ch; щ → chtch; ъ, ь not written (sometimes '); ы → y; ю → ou after и/й, ïou after other vowels, iou elsewhere, you by convention; я → a after и/й (Мария → Maria), ïa after other vowels (Маяковский → Maïakovski), ia elsewhere, ya by convention (Ялта → Yalta); variants: в → w/ff — [fr.wikipedia](https://fr.wikipedia.org/wiki/Transcription_du_russe_en_fran%C3%A7ais).
- German (Duden-based, de.wikipedia): в w; г g (w in genitive -ого/-его); е e, je word-initially/after vowels/ь/ъ (Ельцин → Jelzin); ё jo, but o after ж ч ш щ (Горбачёв → Gorbatschow); ж sch (DDR/Steinitz: sh); з s; й i at word end and between vowel and consonant (Андрей → Andrei, Чуйков → Tschuikow), not written after и/ы (Горький → Gorki), j before vowels; кс → x (Duden "in all cases"); с → ss between vowels; х ch; ц z; ч tsch; ш sch; щ schtsch (DDR stsch); ь not written, but ьи/ье/ьо → ji/je/jo; ы y; э e; ю ju; я ja — [de.wikipedia, Kyrillisches Alphabet (Russisch)](https://de.wikipedia.org/wiki/Kyrillisches_Alphabet#Russisch).
- "-off" was common for -ов in French and German in the 19th/early 20th c. (Smirnoff, Davidoff) — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Simplified BGN/PCGN in English publications: ë → yo, -iy/-yy → -y, apostrophes for ъ/ь omitted — [Wikipedia, Romanization of Russian](https://en.wikipedia.org/wiki/Romanization_of_Russian). "Modified LC": initial Ye-/Y-/Yu-/Ya-, -ий → -y, familiar names anglicized — [Wikipedia, Romanization of Ukrainian](https://en.wikipedia.org/wiki/Romanization_of_Ukrainian).

### Inferences
Variant-generation operators (derived from the tables above; recommended as weighted rewrite rules applied to a canonical BGN-like form):
- -ий: iy | y | ii | i | ij | iĭ | yi (Ukrainian -ий) — sources: MVD 310 (iy/y), WP/BS (y), ICAO (ii), French/German (i), GOST B/scholarly (ij), ALA-LC (iĭ), KMU (yi). -ый: y | yy | yi | yj (fr Грозный → Grozny).
- е (initial / after vowel / after ь,ъ): ye | e | ie | je | ïe (fr). ё: e | yo | io | jo | ë | ye (MVD 782 after consonant) | o (after ж ч ш щ in WP-de convention: Gorbatschow).
- й (non-final): y | i | j | ï (fr) | ĭ.
- ь: ∅ | ' | ’ | y (WP before non-iotated vowel) | i (fr ie) | j (de before и/е/о).
- ъ: ∅ | ie (ICAO) | " | ” | y (WP).
- х: kh | h | ch (de, pl, cs) | x | j (es).
- ж: zh | j (fr, es-fr) | sch (de) | sh | ž | ż (pl) | zj (nl, sv).
- ч: ch | tch (fr) | tsch (de) | č | cz (pl) | tsj (nl) | tj (sv) | ç (tr).
- ш: sh | ch (fr) | sch (de) | š | sz (pl) | sj (nl, sv) | ş (tr).
- щ: shch | sch | shh | sc | chtch (fr) | schtsch/stsch (de) | szcz (pl) | šč | sjtsj (nl) | sjtj (sv) | şç (tr).
- ц: ts | tc | c | cz | z (de) | tz.
- ю: yu | iu | ju | iou (fr) | ou (fr after и) | u. я: ya | ia | ja | a (fr after и: Maria) | ïa.
- кс: ks | x. в: v | w (de, pl) | ff (old final -ов → -off). final -ов/-ев: ov | off | ow (de, pl) | ev.
- Ukrainian-specific: г h ↔ g (Russian-based); и y ↔ i; і i; ї yi/i/ji/ï; є ye/ie/je.
- For names like Наталья/Наталия (two Cyrillic spellings), generate from both Cyrillic forms.

### Gaps
- No corpus-based frequency data (e.g., from passport databases or sanctions lists) was found to weight variants by real-world prevalence; weights must be set heuristically or learned.
- Wikipedia name pages for Сергей, Михаил, Пётр, Семён, Кирилл, Дарья, Анастасия did not list variant spellings in their lead sections.

## 7. Grammar specifics: gender forms of surnames, patronymics, Ukrainian and Belarusian surname types

### Takeaway
Adjectival surnames inflect for gender (-ов/-ова, -ев/-ева, -ин/-ина, -ский/-ская, -цкий/-цкая, -ой/-ая); nominal surnames (-енко, -ук/-юк/-чук, -ич, -онак) are gender-invariant. Patronymics: -ович/-евич/-ич (m) and -овна/-евна/-ична/-инична (f). Name matching must normalize gender forms and, in Latin, the -sky/-skiy/-skii/-skyi vs -skaya/-skaia/-ska pairs.

### Cited Findings
- Adjectival surnames: male -ov, -ev, -in, -iy/-oy/-yy ↔ female -ova, -eva, -ina, -aya (Ельцин/Ельцина; Толстой/Толстая); all other (non-adjectival) surnames are the same for both genders, including -енко and -ич; the correct English transliteration of feminine forms is debated and sometimes the masculine form is used — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Plural/family forms: -овы/-евы/-ёвы, -ины, -ие/-ые — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Declension: Иванов → Иванова (gen.), Иванову (dat.), Ивановым (instr.), Иванове (prep.); feminine Иванова → Ивановой/Иванову; masculine-noun surnames of women are not declined (Анне Жук) — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Patronymics: suffix -ович/-овна; after й or a soft consonant -евич/-евна (Дмитрий → Дмитриевич/Дмитриевна); for some vowel-final names -ич with female -ична or -инична (Фока → Фокич/Фокична; Кузьма → Кузьмич/Кузьминична); examples: Ilya → Ilyich/Ilyinichna; Nikolay → Nikolayevich/Nikolayevna; Yakov → Yakovlevich/Yakovlevna; surnames in -ich are gender-invariant but patronymics are gendered (Ivan Petrovich Mirovich; Anna Petrovna Mirovich) — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Suffix table: -ов/-ев (-ova/-eva), -ин (-ina); -ский/-ская, -цкий/-цкая, -ський/-ська (uk), -ски/-ска; -ко/-енко (Ukrainian origin, also Belarus); -ак/-ик/-ук/-юк, -чак/-чик/-чук (Ukraine, Belarus, Russia, Poland...); -ович/-евич/-ич — [Wikipedia, Slavic name suffixes](https://en.wikipedia.org/wiki/Slavic_name_suffixes).
- Ukrainian/Belarusian-origin surnames use -ко, -ук, -ич (Писаренко, Ковальчук) — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Belarusian surnames: -vič/-ič (Mickievič), -cki/-ski with feminine -ckaja/-skaja (Kalinoŭski, Sadoŭski), -čuk and -iuk/-juk (Ramančuk, Maliuk), -ka (cf. Ukrainian -ko: Łukašenka, Jakavienka), -onak/-jonak (-ionak)/-enak (Malašonak, Manionak), -jenia/-ienia (Astapienia) — [Wikipedia, Belarusian name](https://en.wikipedia.org/wiki/Belarusian_name).
- Foreign citizens naturalized in Russia may have no patronymic; Turkic patronymics like -uly/-qyzy, oglu occur — [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).

### Inferences
- Gender-normalization table for matching (Cyrillic): -ов↔-ова, -ев↔-ева, -ёв↔-ёва, -ин↔-ина, -ын↔-ына, -ский↔-ская, -цкий↔-цкая, -ской↔-ская, -ой↔-ая (Толстой/Толстая), -ый↔-ая, -ий↔-ая (e.g., Горький/Горькая); Ukrainian -ський↔-ська, -цький↔-цька, -ий↔-а (Зелений/Зелена); Belarusian -скі↔-ская, -цкі↔-цкая, -оў↔-ова, -еў↔-ева, -ін↔-іна. Latin equivalents differ by system: -skaya (BGN/WP/MVD310), -skaia (ICAO), -skaja (scholarly/Belarus 288/2023), -ska (KMU uk: Лозинська → Lozynska).
- Ukrainian patronymic forms (-ович/-йович, -івна/-ївна, e.g., Іванович/Іванівна, Сергійович/Сергіївна) and Belarusian (-авіч/-евіч, -аўна/-еўна) are standard but I did not obtain a citable source in this session; KMU 2010 gives Ivanovych/Ivanivna, Serhiiovych/Serhiivna (computed).

### Gaps
- No citable source collected for Ukrainian and Belarusian patronymic suffix rules (see Inferences).

## 8. Automatic language detection of Cyrillic names (Russian vs Ukrainian vs Belarusian)

### Takeaway
Letter inventories give hard signals: ґ є ї → Ukrainian; ў → Belarusian; ъ → Russian; і → Ukrainian or Belarusian; и щ → Russian or Ukrainian (not Belarusian); ы э ё → Russian or Belarusian (not Ukrainian). Names written only with the 27 letters shared by all three (а б в г д е ж з й к л м н о п р с т у ф х ц ч ш ь ю я) are ambiguous and need suffix/lexicon heuristics.

### Cited Findings
- Ukrainian alphabet (33 letters, incl. Ґ Є И І Ї Й Щ Ь, no Ё Ъ Ы Э) plus apostrophe — [KMU 55-2010 table](https://zakon.rada.gov.ua/laws/show/55-2010-%D0%BF); BGN/PCGN Ukrainian lists 33 letters + ’ (code 0146 = U+2019) — [BGN/PCGN Ukrainian](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_UKRAINIAN.pdf).
- Belarusian alphabet: 32 letters (incl. І Ў Ы Э Ё, no И Щ Ъ) plus apostrophe ’ (U+02BC); "contains three characters not present in the Russian alphabet: і, ў, and ’" — [BGN/PCGN Belarusian](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_BELARUSIAN.pdf); [2023 Instruction App. 1](https://pravo.by/upload/docs/op/W22339778_1680555600.pdf).
- Russian alphabet: 33 letters incl. Ё (7th letter, dieresis "generally not shown in writing") — [BGN/PCGN Russian](https://geonames.nga.mil/geonames/GNSSearch/GNSDocs/romanization/ROMANIZATION_OF_RUSSIAN.pdf).
- Set arithmetic over these three inventories (computed): only-ru {ъ}; only-uk {ґ, є, ї}; only-be {ў}; ru∩uk∖be {и, щ}; ru∩be∖uk {ё, ы, э}; uk∩be∖ru {і}; common to all {а б в г д е ж з й к л м н о п р с т у ф х ц ч ш ь ю я}.
- Morphological cues documented: Ukrainian -енко (also Belarus), -ук/-юк/-чук (uk/be), Belarusian -онак/-ёнак, -ка, -скі; Russian -ов/-ев/-ин, -ский — [Wikipedia, Slavic name suffixes](https://en.wikipedia.org/wiki/Slavic_name_suffixes), [Wikipedia, Belarusian name](https://en.wikipedia.org/wiki/Belarusian_name), [Wikipedia, East Slavic name](https://en.wikipedia.org/wiki/East_Slavic_name).
- Cognate given names differ by language: Александр / Олександр / Аляксандр; Алексей / Олексій / Аляксей; Ольга / Ольга / Вольга; Егор / Єгор / Ягор; Оксана / Оксана / Аксана; Галина (uk Halyna, be Halina) — [Wikipedia, Alexander](https://en.wikipedia.org/wiki/Alexander), [Alexey](https://en.wikipedia.org/wiki/Alexey), [Olga (name)](https://en.wikipedia.org/wiki/Olga_(name)), [Yegor](https://en.wikipedia.org/wiki/Yegor), [Oksana](https://en.wikipedia.org/wiki/Oksana), [Galina](https://en.wikipedia.org/wiki/Galina).

### Inferences
- Decision procedure: (1) normalize (NFC; Latin i/I inside Cyrillic words → і/І; apostrophe variants U+0027, U+2019, U+02BC, U+02BB, ` → one internal apostrophe); (2) hard rules: {ґ,є,ї} → uk; {ў} → be; {ъ} → ru; {і} + {и or щ} → uk; {і} + {ы, э or ё} → be; {і} alone → uk|be (look at -енко/-ук vs -онак/-ка, -ў/-аў/-оў endings, akanye "а" for unstressed "о": Аляксандр); {ы,э,ё} + {и or щ} → ru; {ы,э,ё} alone → ru|be; {и or щ} alone → ru|uk (Ukrainian -ій/-ський vs Russian -ий/-ский: "ій" impossible in Russian, "ський" vs "ский"); apostrophe inside word → uk|be; (3) otherwise ambiguous → return ranked list and transliterate with all candidate languages.
- Ambiguity examples (shared-letter names): Роман, Олег, Богдан, Марта, Оксана, Анна, Павлов? (Russian -ов strongly suggests ru but Ukrainians carry Russian-form surnames), Шевчук (uk/be/ru).
- A mixed-language full name (e.g., Ukrainian surname + Russian given name) is common in Soviet-era documents; detect per token, not per string.

### Gaps
- No published accuracy figures for letter-based detection of short name strings were found.
