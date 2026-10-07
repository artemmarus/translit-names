# Romanization of personal names from Turkic and Muslim-majority post-Soviet / Caucasus languages (Turkish, Azerbaijani, Uzbek, Karakalpak, Kazakh, Kyrgyz, Turkmen, Tajik, Tatar, Bashkir, Chechen/Ingush/Dagestani, Uyghur): state as of October 2026, for the `translit-names` package

Scope note: these are research notes for a Python package. Every row in a "Cited Findings" table comes from the cited source. Rows marked *derived* apply a cited table mechanically; they are not observed passport output. Unsourced linguistic knowledge (variant clusters, heuristics) is kept under "Inferences". Primary sources used most: ICAO Doc 9303 Part 3 (8th ed., 2021), the PCGN/BGN tables on gov.uk (checked 2019–2024), Russian MVD Order No. 996 (2019), and news on the 2026 Uzbek and Kyrgyz changes.

---

## 1. ICAO Doc 9303 baseline and the Russian passport table (the fallback for every Cyrillic name, and the governing rule for Tatar, Bashkir, Chechen, Ingush and Dagestani names)

### Takeaway
ICAO Doc 9303 Part 3 (8th ed., 2021) gives one MRZ table for Latin letters with diacritics (Ç→C, Ğ→G, İ/ı→I, Ş→S; Ö→"OE or O", Ü→"UE or UXX or U", Ä→"AE or A", Ñ→"N or NXX"). It has no entry for Azerbaijani **Ə**. Its Cyrillic table covers Russian plus some Slavic letters, and among the Turkic letters only **Ғ** (→G) and **Һ** (listed as →"C", apparently an error). It has nothing for Ә Қ Ң Ө Ұ Ү Ҳ Ҷ Ӣ Ӯ Җ Ҙ Ҫ Ҡ Ӏ, so each issuing state fills those gaps itself. Russian passports use the ICAO-derived MVD table (Й→I, Х→KH, Ц→TS, Ъ→IE, Ю→IU, Я→IA, Ё→E; Ь dropped). Russia's MFA has said that differing transliterations of the same name are not errors.

### Cited Findings
- Doc 9303 Part 3 is the 8th edition (2021). Section 4.6: names in the MRZ "shall be printed using upper-case OCR-B characters … without diacritical marks". The issuing state "shall transliterate national characters using only the allowed OCR-B characters and/or truncate". The primary identifier is followed by `<<`. Multiple name components are separated by a single `<`. The field is padded with `<`. — [ICAO Doc 9303 Part 3 (2021)](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Section 3.1 (VIZ): "Diacritics are permitted. Latin-based national characters listed in Section 6.A … may also be used in the VIZ without transliteration. When mandatory data elements are in a language that does not use the Latin alphabet, a transcription or transliteration shall also be provided." So the VIZ may show `ŞÜKRÜ` while the MRZ shows `SUKRU`. — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Appendix B.4.1: "a group of nine characters that are treated specially, for example, the character 'Ñ' can be transliterated into the MRZ as 'NXX'". Example: `CAÑON` → `CANXXON<<TERESA`. — [ICAO Doc 9303 Part 3, App. B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

**ICAO 6.A, multinational Latin characters (extract of the letters relevant here; verbatim mappings)** — [ICAO Doc 9303 Part 3 §6.A](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

| Char | Unicode | ICAO MRZ | Char | Unicode | ICAO MRZ |
|---|---|---|---|---|---|
| À Á Â Ã | 00C0–00C3 | A | Ň | 0147 | N |
| Ä | 00C4 | AE or A | Ŋ | 014A | N |
| Å | 00C5 | AA or A | Ò Ó Ô Õ | 00D2–00D5 | O |
| Ā Ă Ą | 0100/0102/0104 | A | Ö | 00D6 | OE or O |
| Ç | 00C7 | C | Ō Ŏ Ő | 014C/014E/0150 | O |
| Č Ć | 010C/0106 | C | Ş | 015E | S |
| È É Ê Ë Ē Ė | … | E | Š Ś | 0160/015A | S |
| Ğ | 011E | G | Ù Ú Û | 00D9–00DB | U |
| Ġ Ģ Ĝ | … | G | Ü | 00DC | UE or UXX or U |
| Ì Í Î Ï Ī | … | I | Ū Ŭ Ů Ű Ų | … | U |
| İ | 0130 | I | Ý | 00DD | Y |
| ı ("I without dot (Turkey)") | 0131 | I | Ÿ Ŷ | … | Y |
| Ñ | 00D1 | N or NXX | Ž Ź Ż | 017D/0179/017B | Z |
| Ń Ņ | 0143/0145 | N | ẞ | 1E9E | SS |
| **Ə / ə** | 018F/0259 | **not listed** | Ǵ, Ḡ (Uzbek/Kazakh proposals) | 01F4, 1E20 | **not listed** |

**ICAO 6.B, Cyrillic (complete list as printed)** — [ICAO Doc 9303 Part 3 §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

| Cyr | U+ | ICAO | Cyr | U+ | ICAO |
|---|---|---|---|---|---|
| А | 0410 | A | Т | 0422 | T |
| Б | 0411 | B | У | 0423 | U |
| В | 0412 | V | Ф | 0424 | F |
| Г | 0413 | G (Belarusian/Serbian/Ukrainian = H) | Х | 0425 | KH (Serbian/Macedonian = H) |
| Д | 0414 | D | Ц | 0426 | TS (Serbian/Macedonian = C) |
| Е | 0415 | E | Ч | 0427 | CH (Serbian = C) |
| Ё | 0401 | E (Belarusian = IO) | Ш | 0428 | SH (Serbian = S) |
| Ж | 0416 | ZH (Serbian = Z) | Щ | 0429 | SHCH (Bulgarian = SHT) |
| З | 0417 | Z | Ъ | 042A | IE |
| И | 0418 | I (Ukrainian = Y) | Ы | 042B | Y |
| Й | 0419 | I (Ukrainian initial = Y) | Ь | 042C | **not listed (dropped)** |
| К | 041A | K | Э | 042D | E |
| Л | 041B | L | Ю | 042E | IU (Ukrainian initial = YU) |
| М | 041C | M | Я | 042F | IA (Ukrainian initial = YA) |
| Н | 041D | N | Ђ (printed "Ћ") | 0402 | D |
| О | 041E | O | Є | 0404 | IE (Ukr. initial YE) |
| П | 041F | P | Ѕ | 0405 | DZ |
| Р | 0420 | R | І | 0406 | I |
| С | 0421 | S | Ї | 0407 | I (Ukr. initial YI) |
| Ј | 0408 | J | Љ / Њ | 0409/040A | LJ / NJ |
| Ќ | 040C | K (Macedonian KJ) | **Ў** | 040E | **U** |
| Џ | 040F | DZ (Macedonian DJ) | Ѫ | 046A | U |
| Ѵ | 0474 | Y | Ґ | 0490 | G |
| **Ғ** | 0492 | **G** (note says "Macedonian = GJ", but Macedonian uses Ѓ U+0403, so the note looks like a table error) | **Һ** | 04BA | **"C"** as printed (phonetically /h/; looks like a table error) |

Not in ICAO 6.B (no international MRZ rule; each state decides): **Ә Қ Ң Ө Ұ Ү Ҳ Ҷ Ӣ Ӯ Җ Ҙ Ҫ Ҡ Ҝ Ҹ Ӏ/ӏ**.

**Russian Federation passport table** (appendix "Транслитерация кириллических знаков" to MVD Order No. 996 of 31.12.2019) — [ConsultantPlus, Приказ МВД России от 31.12.2019 N 996](https://www.consultant.ru/document/cons_doc_LAW_346719/413ce7cde653ee8a7c578654112520bdd971d99d/)

| А A | Б B | В V | Г G | Д D | Е E | Ё E | Ж ZH | З Z | И I | Й I |
|---|---|---|---|---|---|---|---|---|---|---|
| К K | Л L | М M | Н N | О O | П P | Р R | С S | Т T | У U | Ф F |
| Х KH | Ц TS | Ч CH | Ш SH | Щ SHCH | Ъ IE | Ы Y | Ь (not listed → dropped) | Э E | Ю IU | Я IA |

- On 14 June 2024 Russia's MFA (Zakharova) said that different transliterations of the same name are "not an error and not grounds for passport confiscation". The rules are in MFA orders No. 2113 and No. 2114 (2020). A citizen may ask for a different spelling, backed by documents such as foreign birth or marriage certificates. — [Interfax, 14.06.2024](https://www.interfax.ru/russia/966690)

### Inferences
- In practice the MRZ alphabet is `A–Z` and `<`. Hyphens, apostrophes (Uzbek ʻ ʼ, Chechen Ӏ) and spaces become `<` or are dropped. The package needs (a) a **strict ICAO profile** and (b) **per-language override tables** for the Cyrillic and Latin letters that ICAO omits (Ə, Ә, Қ, Ң, Ө, Ұ, Ү, Ҳ, Ҷ, Ӣ, Ӯ, Җ, Ҙ, Ҫ, Ҡ, Ӏ).
- Do not apply ICAO's `Һ → C` literally. Every national and PCGN table maps Һ to `H` (see §5, §9). Treat it as an ICAO table error and default to `H`, with a strict flag that reproduces ICAO.
- ICAO 6.B maps **Ў→U** (the Belarusian letter). The same code point U+040E is Uzbek **Ў = oʻ**. A naive ICAO pass turns `Ўринов` into `URINOV`, while the Uzbek Latin form gives `ORINOV`. Both must be produced as variants (§4).
- Pre-2014 Russian passports and Soviet-era documents used other conventions (Й→Y, Ю→YU, Я→YA, sometimes Х→H, КС→X). The variant generator should emit these older forms as well; see the Slavic research notes for the details.
- Because the ICAO table makes Ъ→IE, a Russian-form spelling of a Uzbek or Tajik name containing Ъ (e.g., `Маъруф`) comes out as `MAIERUF` under strict ICAO/MVD rules. The national Latin form is `Maʼruf` → `MARUF`. *Derived.*

### Gaps
- I could not extract the Doc 9303 Part 4 (TD3 passport) truncation rules for over-long names; only Part 3 was read.
- I did not find the full list of the "nine specially treated characters" in Appendix B; only Ñ→NXX is given as an example.
- I found no ICAO statement on Ə or on Kazakh, Uzbek or Tajik Cyrillic letters. None seems to exist in 9303 Part 3.

---

## 2. Turkish (Ç Ğ I/ı İ/i Ö Ş Ü; â î û); MRZ rendering, English variants, Python casing pitfalls

### Takeaway
In the Turkish MRZ, ICAO's simple mapping applies: Ç→C, Ğ→G, İ/ı→I, Ö→O, Ş→S, Ü→U. ICAO also allows OE/UE (and UXX). Secondary sources say Turkish passports use the plain-letter forms, but I found no official Turkish rule text. The main software risk is Unicode casing. Python's `"İ".lower()` returns `"i̇"` (two code points), `"ı".upper()` returns `"I"`, and `"I".lower()` returns `"i"`, never `"ı"`. NFKD followed by stripping combining marks folds Ş/Ç/Ğ/Ö/Ü/İ correctly but leaves `ı` (U+0131) unchanged, so it needs an explicit mapping.

### Cited Findings
- The Turkish alphabet uses the letters above. The circumflexes â, î, û are optional. They mark a long vowel or palatalization of a preceding k/g/l in Arabic/Persian loans (e.g., *kâr* "profit" vs *kar* "snow"). Q, W, X are not native letters (native replacements: K, V, KS). — [Wikipedia: Turkish alphabet](https://en.wikipedia.org/wiki/Turkish_alphabet)
- ICAO 6.A: Ç→C, Ğ→G, İ (U+0130)→I, ı (U+0131, "I without dot (Turkey)")→I, Ö→"OE or O", Ş (U+015E)→S, Ü→"UE or UXX or U", Â→A, Î→I, Û→U. — [ICAO Doc 9303 Part 3 §6.A](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Turkish-language Q&A sources say it is normal for the Turkish passport MRZ to show "Ç" as "C" and "Ş" as "S", and that converting Turkish characters to C, S, G, I is standard. *Weak, non-official sources.* — [Yandex YaCevap](https://yandex.com.tr/yacevap/c/seyahat/q/pasaportta-turkce-karakter-kullanilir-mi-3034095488); [kimlikokuyucu.com FAQ](https://kimlikokuyucu.com/s.-sorulan-sorular.html)
- Unicode does not encode a separate capital dotless I or small dotted i. Most software uppercases `ı` to `I` but lowercases `I` to `i` unless it is set up for Turkish, so upper-then-lower does not round-trip. Windows has `NORM_LINGUISTIC_CASING` for the Turkish/Azerbaijani I→ı mapping. Oracle, PHP, Java and Unixware have had Turkish-locale bugs. People in Turkey and Azerbaijan often type `1` for `ı`. — [Wikipedia: Dotted and dotless I in computing](https://en.wikipedia.org/wiki/Dotted_and_dotless_I_in_computing)
- Local check (Python 3.9.6, `unicodedata` 13.0.0), run for these notes. The behaviour matches Unicode SpecialCasing (the `tr`/`az` mappings are conditional and Python does not apply them):

| Expression | Result |
|---|---|
| `"İ".lower()` | `'i̇'` = U+0069 U+0307 (length 2) |
| `"İstanbul".lower()` | `'i̇stanbul'` |
| `"I".lower()` | `'i'` (Turkish would expect `ı`) |
| `"ı".upper()` | `'I'` |
| `"IŞIK".lower()` | `'işik'` (Turkish: `ışık`) |
| `"ışık".upper()` | `'IŞIK'` |
| `"İ".casefold()` | `'i̇'` (casefold is not Turkish-aware) |
| `unicodedata.normalize('NFD','İ')` | U+0049 U+0307 |
| NFKD + drop combining on `"Şükrü Çağlar Gökhan İnönü Işık"` | `"Sukru Caglar Gokhan Inonu Isık"`: **`ı` is not folded** |
| NFKD of `ə` (U+0259), `ı` (U+0131) | unchanged (no decomposition) |

### Inferences
- **Required Turkish/Azerbaijani case layer:** before any case operation, apply a locale-aware mapping: `upper: i→İ, ı→I`; `lower: I→ı, İ→i`. Then strip U+0307 after the ASCII fold. For matching (not display), fold `İ, I, ı, i` to `I`. Never call `.lower()` on Turkish input before transliterating, or `İ` becomes `i` + U+0307, and a later "drop combining marks" step gives `i` (correct by luck). Lowercasing `I` (meant as `ı`) gives `i`, which is fine for ASCII output but loses information for round-trip and phonetic profiles.
- **Turkish output profiles** (proposal):
  - `icao`: Ç C, Ğ G, I/ı I, İ/i I, Ö O, Ş S, Ü U, Â A, Î I, Û U.
  - `icao_de` (German-style, ICAO-permitted): Ö OE, Ü UE. Germany's own MRZ practice for its residence documents is believed to use AE/OE/UE, so Turkish-origin names in German documents can appear as `GOEKHAN`, `SUEKRUE`. *Unverified; generate as a low-weight variant.*
  - `english_phonetic`: Ç CH, Ş SH, C J, Ğ ∅/G (Ğ lengthens the preceding vowel: Doğan → Doan/Dogan; Tuğba → Tuba/Tugba), Ö O/U, Ü U/YU, J ZH.
  - `russian_form` (Turkish names as they appear in Russian or Central Asian documents): Ç Ч, Ş Ш, C ДЖ, Ö Ё/Е, Ü Ю/У, Ğ Г, then ICAO → e.g., Hüseyin → Гусейн/Хусейн → GUSEIN/KHUSEIN.
- **Name variant examples (heuristic, unsourced):**
  - Şükrü → SUKRU | Shukru | Sukru | Shukri (Arabic-form) | Шукру.
  - Mehmet (Turkish standard) ↔ Mehmed (Ottoman/Bosnian) ↔ Muhammed/Muhammet (separate given names in Turkey) ↔ Muhammad. Link them in the cross-name cluster with a lower weight than spelling variants.
  - Hüseyin → HUSEYIN | Huseyin | Hussein | Husayn | Hüseyn (Az) | Guseyn/Gusein (Russian-form).
  - Gökhan → GOKHAN | Goekhan | Gokhan.
  - Çağlar → CAGLAR | Chaglar | Caglar | Tschaglar (German phonetic).
  - Cem → CEM | Jem | Djem.
  - Ayşe → AYSE | Ayshe | Aishe | Aysha.
  - Ömer → OMER | Oemer | Umar (Arabic cluster).

### Gaps
- I found no Turkish government text (Nüfus ve Vatandaşlık İşleri / passport regulation) stating the MRZ mapping. Use of `O/U` rather than `OE/UE` is supported only by weak sources and by consistency with ICAO.
- I did not verify whether Turkish passports print circumflexes (â î û) in the VIZ.

---

## 3. Azerbaijani (Latin since 1991/1992: Ə Ç Ğ I/ı İ/i Ö Ş Ü X Q C J); passport rendering, Cyrillic legacy, surname and patronymic forms

### Takeaway
Azerbaijani passports are printed in Azerbaijani and English. ICAO has no Ə, so Azerbaijan decides. The only MRZ-level evidence I found (a PRADO specimen snippet: `HUSEYNLI ORKHAN`) shows **Ü→U** and **X→KH** (Orxan → ORKHAN). English-language practice for persons is dominated by **Ə→A** (Məmmədov → Mammadov, Əliyev → Aliyev), but a documented rule-based scheme writes Ə as **E** next to l, m, n, r, y (Azər → Azer). The package must emit A and E variants for Ə, KH/X/H for X, G/Q/K for Q, J/C for C, and the Russified forms (Mamedov, Guliyev, Gasanov).

### Cited Findings
**Azerbaijani Cyrillic (1958–1991) → Latin (since 1991): BGN/PCGN 1993 Agreement, checked Sept 2022** — [PCGN Azerbaijani table of correspondences (PDF)](https://assets.publishing.service.gov.uk/media/6329af69d3bf7f75cce70557/TABLE_OF_CORRESPONDENCES_FOR_AZERBAIJANI_-_with_examples.pdf)

| # | Cyrillic | U+ | Latin | Example |
|---|---|---|---|---|
| 1 | А а | 0410 | a | Астара Astara |
| 2 | Б б | 0411 | b | Балакән Balakən |
| 3 | В в | 0412 | v | Товуз Tovuz |
| 4 | **Г г** | 0413 | **q** | Гах Qax |
| 5 | Ғ ғ | 0492 | ğ | Ағдаш Ağdaş |
| 6 | Д д | 0414 | d | Дашкәсән Daşkəsən |
| 7 | Е е | 0415 | e | Лерик Lerik |
| 8 | Ә ә | 04D8 | ə | Бәрдә Bərdə |
| 9 | Ж ж | 0416 | j | Жиј Jiy |
| 10 | З з | 0417 | z | Зәнҝилан Zəngilan |
| 11 | И и | 0418 | i (İ) | Имишли İmişli |
| 12 | Ы ы | 042B | ı | Бакы Bakı |
| 13 | **Ј ј** | 0408 | **y** | Јевлах Yevlax |
| 14 | К к | 041A | k | Кәлбәҹәр Kəlbəcər |
| 15 | **Ҝ ҝ** | 049C | **g** | Ҝәнҹә Gəncə |
| 16 | Л л | 041B | l | |
| 17 | М м | 041C | m | Минҝәчевир Mingəçevir |
| 18 | Н н | 041D | n | Нахчыван Naxçıvan |
| 19 | О о | 041E | o | Оғуз Oğuz |
| 20 | Ө ө | 04E8 | ö | Ҝөјчај Göyçay |
| 21 | П п | 041F | p | |
| 22 | Р р | 0420 | r | Гусар Qusar |
| 23 | С с | 0421 | s | Самух Samux |
| 24 | Т т | 0422 | t | |
| 25 | У у | 0423 | u | Шуша Şuşa |
| 26 | Ү ү | 04AE | ü | Күрдәмир Kürdəmir |
| 27 | Ф ф | 0424 | f | Füzuli |
| 28 | Х х | 0425 | x | Хырдалан Xırdalan |
| 29 | Һ һ | 04BA | h | Шаһбуз Şahbuz |
| 30 | Ч ч | 0427 | ç | Хачмаз Xaçmaz |
| 31 | **Ҹ ҹ** | 04B8 | **c** | Уҹар Ucar |
| 32 | Ш ш | 0428 | ş | Шәки Şəki |
| 33 | ’ | 2019 | ’ | |

- PCGN notes: use Ə **U+018F/U+0259** in Latin and **U+04D8/U+04D9** in Cyrillic. "When it cannot be reproduced … the letter **Ä ä** may be substituted". Obsolete Cyrillic й, э, ю, я → ẏ, ė, yu, ya. — [PCGN Azerbaijani](https://assets.publishing.service.gov.uk/media/6329af69d3bf7f75cce70557/TABLE_OF_CORRESPONDENCES_FOR_AZERBAIJANI_-_with_examples.pdf)
- "Passport content is printed both in Azerbaijani and in English." The MRZ starts `P<AZE`. The article does not describe how names are transliterated. — [Wikipedia: Azerbaijani passport](https://en.wikipedia.org/wiki/Azerbaijani_passport)
- A PRADO specimen of the Azerbaijani ordinary passport (AZE-AO-02002) shows the holder as "HUSEYNLI ORKHAN" (Hüseynli Orxan). *From a search snippet; the PRADO page returned HTTP 403 to direct fetch.* — [PRADO AZE-AO-02002](https://www.consilium.europa.eu/prado/en/AZE-AO-02002/index.html)
- Cabinet of Ministers Resolution No. 498 (16 Dec 2020) approved the "Rules of Transliteration of Names of Geographical Features" from Azerbaijani into Russian and English (Schedules 1 and 2). Traditional spellings can override the letter rules (Bakı → Baku). This covers place names, not personal names. — [Mondaq summary](https://www.mondaq.com/knowledge-management/1048876/)
- Rule-based Azerbaijani→English transliteration (expert-system paper, ICT Institute, Baku, 2023): **ə → "e"** when it precedes or follows l, m, n, r, y (Azər → Azer; Adıgözəl → Adigozel). **Otherwise ə → "a"** (Əfqan → Afgan; Əflatun → Aflatun). — [Mammadova & Mammadzada (2023), PDF](https://library.ict.az/elektron/2023/Principles_of_formation_of_transliteration_rules_for_the_azerbaijani_language_using_expert_systems.pdf)
- Surnames and patronymics (Slavic Cataloging Manual): native surname suffixes -ly/-li/-liu, -zade, -oglu, also -gil, -soy (e.g., Vahabzadə, Osmanly). Russified -ov/-ev, -ova/-eva (Hasanov, Namazova). Patronymic particles **oğlu** "son of" and **qızı** "daughter of" form one unit with the father's name ("Khalil oglu", "Namaz gizi") and must never start an access point. ALA-LC transliteration of the Cyrillic forms: "ogly ġyzy". Script history: Latin 1922–1939, Cyrillic 1939–1991, revised Latin 1991–present. — [Slavic Cataloging Manual: Azerbaijani personal names](https://sites.google.com/site/seesscm/azerbaijani-personal-names)
- Both Latin-derived and Russified surname forms appear as separate English Wikipedia entries ("Mammadov", "Mamedov"). — [Wikipedia: Mammadov](https://en.wikipedia.org/wiki/Mammadov); [Wikipedia: Mamedov](https://en.wikipedia.org/wiki/Mamedov)

### Inferences
- **Azerbaijani letter table for the package** (MRZ column is *derived/proposed* unless marked):

| Az Latin | Az Cyrillic (legacy) | Typical Russian-form Cyrillic | MRZ (proposed) | English / search variants |
|---|---|---|---|---|
| Ə ə | Ә ә | А / Е / Я (Мамедов, Алиев, Гасанов) | **A** (dominant in personal names), alt E | A, E, Ä |
| C c | Ҹ ҹ | ДЖ (Джейхун) | C (ASCII-legal), alt J | J, DJ, DZH, C (Ceyhun → Jeyhun, Dzheikhun) |
| Ç ç | Ч ч | Ч | C, alt CH | CH, C |
| Ğ ğ | Ғ ғ | Г | G, alt GH | GH, G |
| H h | Һ һ | Г or Х (Həsən → Гасан; Hüseyn → Гусейн) | H | H, G, KH |
| X x | Х х | Х | **KH** (specimen: ORKHAN), alt X | KH, X, H |
| I ı | Ы ы | Ы | I | I, Y |
| İ i | И и | И | I | I |
| J j | Ж ж | Ж | J, alt ZH | ZH, J |
| Q q | Г г | Г or К (Гасымов, Касумов, Кулиев) | Q or G (unverified) | **G** (Quliyev → Guliyev), Q, K, GH |
| G g | Ҝ ҝ | Г / ГЯ / КЯ (Gəncə → Гянджа) | G | G |
| Ö ö | Ө ө | Ё / О / Е | O, alt OE | O, YO |
| Ş ş | Ш ш | Ш | S, alt SH | SH, S |
| Ü ü | Ү ү | Ю / У (Hüseynov → Гусейнов / Гюсейнов) | **U** (specimen: HUSEYNLI), alt UE | U, YU |
| Y y | Ј ј | Й | Y | Y, I (via Russian ICAO Й→I) |

- **Surname mapping clusters to generate:**
  - Məmmədov ↔ Mammadov | Mamedov | Memmedov | Mamadov | Мамедов → MAMEDOV.
  - Əliyev ↔ Aliyev | Aliev | Alijev (German) | Алиев → ALIEV.
  - Həsənov ↔ Hasanov | Gasanov | Hasenov | Гасанов.
  - Hüseynov ↔ Huseynov | Guseynov | Guseinov | Gusejnov | Гусейнов → GUSEINOV.
  - Quliyev ↔ Guliyev | Guliev | Kuliev | Qulijev | Кулиев/Гулиев.
  - Qasımov ↔ Gasimov | Gasymov | Kasimov | Kasumov | Qasimov | Гасымов/Касумов.
  - Xəlilov ↔ Khalilov | Xalilov | Halilov | Халилов → KHALILOV.
  - Cəfərov ↔ Jafarov | Jafarli | Djafarov | Dzhafarov | Джафаров → DZHAFAROV.
  - Suffix alternation -ov ↔ -lı/-li/-lu/-lü ↔ -zadə/-zade ↔ -bəyli (e.g., Hüseynli above). Treat as a soft equivalence only when the stem matches.
- Patronymics: Latin `oğlu`/`qızı` (MRZ OGLU/QIZI); Russian-document forms `оглы`/`кызы` (→ OGLY/KYZY under ICAO). Variants: oglu, ogly, ogli, oghlu; qizi, gizi, kyzy, kizi. Detect them and strip them from the given-name and surname match keys (keep as a separate field).
- Ə→A versus Ə→E: use the 2023 rule (E next to l, m, n, r, y) as the primary *phonetic* rendering. Use A as the primary *passport-likelihood* rendering for surnames. Always output both.

### Gaps
- I found no official Azerbaijani transliteration table for passports or ID cards (State Migration Service / Ministry of Internal Affairs). The PRADO evidence is a single search snippet. **Ə, Q, C, Ç, Ş in the MRZ are unverified** (e.g., whether Q→Q or G, Ç→C or CH).
- The text of Resolution No. 498, Schedule 2 (English), was not retrieved.
- I found no source on any official Azerbaijani reform replacing -ov/-ev with -lı/-li or other suffixes. If such a reform exists, I could not confirm it.

---

## 4. Uzbek (Latin 1993/1995; 2026 reform; Cyrillic legacy; apostrophe code points; passports) and Karakalpak

### Takeaway
The valid standard in October 2026 is still the **1995 Uzbek Latin alphabet**: 26 letters plus Sh, Ch, Ng; Oʻ and Gʻ written with U+02BB; the tutuq belgisi ʼ is U+02BC. A **reform law** replacing **Oʻ→Ö, Gʻ→Ğ, Sh→Ş, Ch→Ç** (28 letters + apostrophe; Ng dropped as a unit) passed the Legislative Chamber (July 2026) and the **Senate (10 Sept 2026)**. It went to the President, and I found no confirmation of signing. Documents issued in the old alphabet stay valid. Schools start in 2027 and all textbooks are due by 2031. The earlier 2021 proposals (Ŏ/Ō/Ḡ and others) never took effect. Passports are in Uzbek (Latin) and English. Commentators report that the English/passport form renders X as **KH** (Xoʻjayev → Khojayev), which yields many variants.

### Cited Findings
- History: Latin reintroduced in 1992/1993. The 1993 alphabet had Ç, Ğ, Ɉ, Ñ, Ö, Ş. It was **revised in 1995** into the current standard of 26 letters and three combinations (Sh, Ch, Ng), with Oʻ and Gʻ written with an apostrophe-like sign. February 2021: plan to finish moving official documentation to Latin by 1 Jan 2023. Proposals in 2018, May 2019, March 2021 (Ç Ş Ğ Ŏ), Nov 2021 and Sept 2023 "none of these proposals entered into force". July 2026: the Legislative Chamber approved replacing Oʻ→Ö, Gʻ→Ğ, Sh→Ş, Ch→Ç, with Ng removed as a separate unit. The Senate approved on **10 September 2026**. — [Wikipedia: Uzbek alphabet](https://en.wikipedia.org/wiki/Uzbek_alphabet) (citing [kun.uz 7 Jul 2026](https://kun.uz/en/news/2026/07/07/parliaments-lower-house-passes-bill-to-revise-uzbek-alphabet-848eb2), [yuz.uz 10 Sep 2026](https://yuz.uz/en/news/lotin-ezuviga-asoslangan-zbek-alifbosini-takomillastirisga))
- The Senate approved the law and "sent it to the president for signing". It moves to "28 letters and 1 apostrophe instead of the current 26 letters (including 2 letters with an apostrophe — Oʻ and Gʻ)". NG stays usable as a letter combination covered by spelling rules. Older documents, currency and securities remain in circulation during the transition. — [Gazeta.uz, 10 Sep 2026](https://www.gazeta.uz/en/2026/09/10/uzb-alphabet/)
- "Documents issued under the existing alphabet will remain valid." First-grade textbooks in the new alphabet from 2027, all textbooks by 2031. The law had been "sent to the president for consideration". One stated driver: Oʻ/Gʻ have "more than ten variants in practice", which breaks search. — [Times of Central Asia](https://timesca.com/uzbekistan-latin-alphabet-changes-senate/); also [Gazeta.uz 9 Jul 2026 (lower house)](https://www.gazeta.uz/en/2026/07/09/alphabet/)
- Code points: Oʻ/Gʻ are "properly rendered" with **U+02BB MODIFIER LETTER TURNED COMMA**, but most sites, including government ones, use **U+2018** or **U+0027**. The tutuq belgisi is **U+02BC MODIFIER LETTER APOSTROPHE** (marks a glottal stop in loans, *sanʼat*, or vowel length, *maʼno*). Many sites use U+2019 or U+0027 instead. ʼ is also used to split s+h (*Isʼhoq*, Исҳоқ). Tutuq is not written after oʻ (*moʻjiza*, Cyrillic мўъжиза). — [Wikipedia: Uzbek alphabet](https://en.wikipedia.org/wiki/Uzbek_alphabet) (Orthographic Rules: Cabinet Resolution No. 339, 24 Aug 1995; [lex.uz](https://lex.uz/docs/-1625271))
- Cyrillic rules: **Е** → *ye* at word start and after a vowel, otherwise *e*. **Ц** → *ts* after a vowel, otherwise *s*. **Ь** omitted (but ье, ьи, ьо → ye, yi, yo). Ё, Ю, Я → yo, yu, ya. Uzbek Cyrillic has no Щ or Ы: Russian Щедрин → Шчедрин, Быков → Биков. — [Wikipedia: Uzbek alphabet](https://en.wikipedia.org/wiki/Uzbek_alphabet)

**Uzbek Cyrillic → Latin: BGN/PCGN 2000 Agreement (checked Nov 2022). Supersedes BGN/PCGN 1979.** "ongoing discussions on altering the official alphabet. In the meantime, the presentation below should continue to be used." — [PCGN Uzbek table (PDF)](https://assets.publishing.service.gov.uk/media/636cda6dd3bf7f16466f478f/TABLE_OF_CORRESPONDENCES_FOR_UZBEK_2022_final.pdf)

| Cyr | U+ | 1995 Latin (PCGN) | 2026 law (pending) | Russian/ICAO of same Cyrillic *(derived)* | Example |
|---|---|---|---|---|---|
| А | 0410 | a | a | A | |
| Б | 0411 | b | b | B | |
| В | 0412 | v | v | V | Водник Vodnik |
| Г | 0413 | g | g | G | |
| Д | 0414 | d | d | D | |
| Е | 0415 | e / **ye** (initial; after а е ё и о у э ю я ў; after й ъ ь) | same | E | Етимоғ Yetimogʻ |
| Ё | 0401 | yo | yo | E | Ёшлик Yoshlik |
| Ж | 0416 | **j** | j | ZH | Жўш Joʻsh |
| З | 0417 | z | z | Z | |
| И | 0418 | i | i | I | |
| Й | 0419 | y | y | I | Испой Ispoy |
| К | 041A | k | k | K | |
| Л М Н О П Р С Т У Ф | | l m n o p r s t u f | same | same | |
| Х | 0425 | **x** | x | **KH** | Хамза Xamza |
| Ц | 0426 | ts (PCGN) / s or ts (orthography) | same | TS | |
| Ч | 0427 | ch | **ç** | CH | Чадоқ Chadoq |
| Ш | 0428 | sh | **ş** | SH | Шўрсув Shoʻrsuv |
| Ъ | 042A | ʼ (PCGN ’) | ʼ | IE | Съезд S’yezd |
| Ь | 042C | ’ (PCGN) / omitted (orthography) | — | (dropped) | Судочье Sudoch’ye |
| Э | 042D | e | e | E | Эшқудуқ Eshquduq |
| Ю | 042E | yu | yu | IU | |
| Я | 042F | ya | ya | IA | Янгиарик Yangiarik |
| **Ў** | 040E | **oʻ** | **ö** | **U** (ICAO "Belarusian ў") | Жўш Joʻsh |
| **Қ** | 049A | **q** | q | not in ICAO → K in Russian-form | Қорақишлоқ Qoraqishloq |
| **Ғ** | 0492 | **gʻ** | **ğ** | G | Ғозғон Gʻozgʻon |
| **Ҳ** | 04B2 | **h** | h | not in ICAO → KH in Russian-form (Х) | Ҳива Hiva |

- PCGN renders ʻ with U+2018 and ’ with U+2019 in its own tables. — [PCGN Uzbek](https://assets.publishing.service.gov.uk/media/636cda6dd3bf7f16466f478f/TABLE_OF_CORRESPONDENCES_FOR_UZBEK_2022_final.pdf)
- Superseded or proposed forms of oʻ/gʻ that may turn up in data: Ö, Ŏ, Ó, Ō, Õ for oʻ; Ğ, Ǵ, Ḡ for gʻ (proposal columns 1993–2026). — [Wikipedia: Uzbek alphabet (reform-projects table)](https://en.wikipedia.org/wiki/Uzbek_alphabet)
- The Uzbek passport is "in the Uzbek and English languages", with fields Surname, Given Names and Father's Name. — [Wikipedia: Uzbekistan passport](https://en.wikipedia.org/wiki/Uzbekistan_passport)
- Cabinet of Ministers Resolution No. 61 of 10 Feb 2021 provides for issuing identity documents, ID cards and residence certificates "in the Uzbek alphabet based on improved Latin graphics". — [Norma.uz](https://www.norma.uz/novoe_v_zakonodatelstve/perehodim_na_latinicu)
- Kun.uz (2022, opinion piece on wrong name spellings) gives this Soviet-legacy chain: Uzbek → Russian Cyrillic → English. **X**: Xoʻjayev → Ходжаев/Xodjayev → **Khojayev**. **Q**: Qosimov → Kasimov → Qasimov. **Oʻ**: Oʻrinov → Urinov (U/O). **J**: Joʻramurodova → Djuramuradova → Juramuradova. **Gʻ**: Gʻafforova → Gaffarova → **Ghaffarova**. **H**: Hotamov → Xatamov → Hatamov. Example: "Jumamurod" in Uzbek appears as "Djumamurat" in a birth certificate. Corrections must cascade through birth certificate → passport → diplomas. — [Kun.uz, 1 Apr 2022](https://kun.uz/uz/news/2022/04/01/xato-ism-familiyalar-buni-bartaraf-etishni-istaganlarga-soddalashtirilgan-tizim-va-jarayon-kerak)
- The same discussion, per the search summary, says that in passports' English rendering Cyrillic Х becomes "Kh", so surnames that could be HASANJONOV appear as **KHASANDJANOV**. *From a search-engine summary of Uzbek-language sources; not verified on the page.* — [Kun.uz](https://kun.uz/uz/news/2022/04/01/xato-ism-familiyalar-buni-bartaraf-etishni-istaganlarga-soddalashtirilgan-tizim-va-jarayon-kerak)
- Name-matching examples: Хўжаев → Ходжаев (Soviet Cyrillic), Hodjaev, Xoʻjayev, Khodjaev. Якубов/Ёқубов → Yakubov / Yoqubov. Patronymics: traditional *oʻgʻli* (son) / *qizi* (daughter) versus Soviet *-ovich/-ovna* ("Shohjahon Qodirov Olimjon oʻgʻli" = Шоҳжаҳон Қодиров Олимжон ўғли; "Akramov Sherzod Salimovich"). One person may legitimately have very different spellings across documents. — [Babel Street: Challenges of name matching in Uzbek](https://www.babelstreet.com/blog/challenges-of-name-matching-in-uzbek)
- **Karakalpak** (Karakalpakstan, Uzbekistan): written in Latin after independence, though Latin adoption in Karakalpakstan is gradual. Letter pairs (Latin / Cyrillic): **á/ә, ǵ/ғ, ń/ң, ó/ө, ú/ү, ı/ы** (plus q/қ, x/х, h/ҳ, w/ў). Examples: үш → úsh, төрт → tórt, алты → altı, тоғыз → toǵız, мың → mıń. — [Wikipedia: Karakalpak language](https://en.wikipedia.org/wiki/Karakalpak_language)

### Inferences
- **Input normalization for Uzbek oʻ/gʻ:** treat the following as the same modifier after `o`/`O`/`g`/`G`: U+02BB ʻ, U+2018 ‘, U+0027 ', U+2019 ’, U+02BC ʼ, U+0060 `, U+00B4 ´, U+02B9 ʹ, U+02BD ʽ, U+055A, U+FF07. Also accept precomposed or proposed forms Ö, Ŏ, Ō, Ó, Õ (=oʻ) and Ğ, Ǵ, Ḡ (=gʻ). Canonicalize to `oʻ`/`gʻ` (U+02BB) for the 1995 profile, or to `ö`/`ğ` for the 2026 profile. After any other letter, the same apostrophe characters mean the tutuq ʼ (U+02BC). For MRZ/ASCII output, drop all of them: `Oʻ → O`, `Gʻ → G`, `Maʼruf → MARUF`.
- **Disambiguating `sh`/`ch` in the 1995 Latin alphabet:** `sʼh`/`sʼh` (tutuq-split) means s+h. In the 2026 profile, `sh` written without tutuq would mean s+h, because ş is the digraph.
- **Uzbek variant axes** (generate the cartesian product with weights):
  - X/Х: X | KH | H.
  - Q/Қ: Q | K.
  - Gʻ/Ғ: G | GH | Ğ→G.
  - Oʻ/Ў: O | U | OO (rare).
  - J/Ж: J | DJ | DZH | ZH (DZH appears when the Russian form is spelled Дж: Джурабек → DZHURABEK).
  - H/Ҳ: H | KH | X (Russian-form Ҳ→Х→KH).
  - E initial: YE | E.
  - Ё: YO | E (ICAO) | IO.
  - Ю/Я: YU/YA | IU/IA.
  - Й: Y | I.
  - -yev ↔ -ev ↔ -yeyev: Mirziyoyev | Mirziyoev | Mirzieev (from ICAO Мирзиёев: Ё→E).
  - -jon ↔ -dzhon ↔ -djon ↔ -zhon (Hasanjonov | Khasandjanov | Khasanzhonov).
  - Also the o/a Soviet vowel shift in Russian-form spellings (Uzbek o ↔ Russian а: Qodirov ↔ Кадыров/Kadyrov; Murod ↔ Мурат/Murat). This is a heavier transformation and should get a lower weight.
- Expected MRZ for Uzbek passports (*proposed, unverified*): Latin VIZ in Uzbek orthography with the MRZ stripped of ʻ/ʼ (OʻTKIR → OTKIR), **or** an English-style rendering (X→KH, Gʻ→GH) per the kun.uz reports. Generate both.
- Karakalpak: add a small table: á→a, ǵ→g/gh, ı→i/y, ń→n/ng, ó→o, ú→u/yu, w→w/v/u, plus Cyrillic ә ғ қ ң ө ү ў ҳ. Karakalpak names usually reach passports through Uzbek documents, so the Uzbek rules apply after normalization.

### Gaps
- **As of 7 Oct 2026, I could not confirm whether the President signed the Senate-approved alphabet law, or when it takes effect.** Check before release.
- I found no official Uzbek table for passport Latin/English transliteration (the Ministry of Internal Affairs rules for the biometric passport, e.g., under Decree PF-4262 of 5 Jan 2011, lex.uz). Kun.uz is an opinion piece. I did not find whether the MRZ keeps `X` or uses `KH`, or how Q is handled.
- I did not research how the 2026 alphabet will apply to passport VIZ names (Ş/Ç/Ö/Ğ in the VIZ, S/C/O/G in the MRZ?).

---

## 5. Kazakh (Cyrillic ә ғ қ ң ө ұ ү һ і; Latin alphabets of 2017, 2018 and 2021; passport practice)

### Takeaway
Kazakh is still effectively Cyrillic in 2026. The official target alphabet is the **April 2021 Latin version** (31 letters: A Ä B D E F G Ğ H I/ı İ/i J K L M N Ñ O Ö P Q R S Ş T U Ū Ü V Y Z). Use was "officially" from 2023, with completion moved from 2025 to **2031**. The 2017 apostrophe version (Decree 569) and the 2018 acute-accent version (Decree 637) are superseded but persist in data. Passports are printed in Kazakh and English. I found no official MVD transliteration table. Observed English/passport conventions use Ye-, Zh-, Kh- and often a doubled "ss" (Kassym, Assel).

### Cited Findings
- Presidential Decree No. 569 (26 Oct 2017) ordered the move to Latin by 2025. Decree No. 637 (19 Feb 2018) amended it, replacing apostrophes with diacritics and digraphs. In January 2021 a revision added ä, ö, ü, ğ, ū, ŋ, ş, and the target year was moved to **2031**. A revision of 22 April 2021 replaced ŋ with **ñ**. The 2021 revision is "officially used starting 2023". The Kazakh Cyrillic alphabet (since 1940) has 42 letters: the 33 Russian letters plus ә ғ қ ң ө ұ ү һ і. — [Wikipedia: Kazakh alphabets](https://en.wikipedia.org/wiki/Kazakh_alphabets); [Decree 569 on adilet.zan.kz](https://adilet.zan.kz/rus/docs/U1700000569)
- President Tokayev said in 2022 that Latinization should not be rushed, and in 2023 that it "should not be a mere mechanical switch". *From a search summary of Wikipedia and press.* — [Wikipedia: Kazakh alphabets](https://en.wikipedia.org/wiki/Kazakh_alphabets); [The Diplomat 2024](https://thediplomat.com/2024/09/the-latinization-of-kazakhstan-language-modernization-and-geopolitics/)

**Kazakh Latin alphabet, April 2021 (letter, with Cyrillic source)** — [Wikipedia: Kazakh alphabets](https://en.wikipedia.org/wiki/Kazakh_alphabets), citing [Astana Times, Feb 2021](https://astanatimes.com/2021/02/kazakhstan-presents-new-latin-alphabet-plans-gradual-transition-through-2031/)

A (А) · Ä (Ә) · B (Б) · D (Д) · E (Е) · F (Ф) · G (Г) · Ğ (Ғ) · **H (Х and Һ)** · **I ı (І)** · **İ i (И and Й)** · J (Ж) · K (К) · L (Л) · M (М) · N (Н) · Ñ (Ң) · O (О) · Ö (Ө) · P (П) · Q (Қ) · R (Р) · S (С) · Ş (Ш) · T (Т) · U (У) · Ū (Ұ) · Ü (Ү) · V (В) · Y (Ы) · Z (З).
Letters with no 2021 letter: Ё, Ц, Ч, Щ, Ъ, Ь, Э, Ю, Я. Wikipedia's comparison lists Ч→"tş", and for 2018: Ц→ts, Щ→ştş, Ю→iu, Я→ia, Ё→io. *Treat the Ч/Ю/Я handling under 2021 as uncertain.*

**2018 version (Decree 637), superseded:** Ә Á, Ғ Ǵ, И/Й I ı, Ң Ń, Ө Ó, У Ý, Ұ U, Ү Ú, Х/Һ H, Ы Y, І I i, Ж J, Ш sh, Ч ch. — [resmihat.kz translit page](https://resmihat.kz/translit); [Wikipedia: Kazakh alphabets](https://en.wikipedia.org/wiki/Kazakh_alphabets)
**2017 version (Decree 569, "apostrophe alphabet"), superseded:** sample text in Wikipedia shows a', g', i', n', o', u', y' (e.g., "ja'ne", "ten'", "Adamdarg'a", "du'ni'ege", "ty'mysynan"). — [Wikipedia: Kazakh alphabets](https://en.wikipedia.org/wiki/Kazakh_alphabets)

**BGN/PCGN 1979 Kazakh (checked Feb 2022)** — [PCGN Kazakh romanization (PDF)](https://assets.publishing.service.gov.uk/media/621caa32e90e0710b73fd4ff/ROMANIZATION_KAZAKH_Feb_22_19_.pdf)

| Cyr | U+ | PCGN | Example | Cyr | U+ | PCGN | Example |
|---|---|---|---|---|---|---|---|
| А | 0410 | a | Павлодар Pavlodar | П | 041F | p | Петропавл Petropavl |
| Ә | 04D8 | ä | Сәтбаев Sätbaev | Р С Т | | r s t | Түркістан Türkistan |
| Б | 0411 | b | | **У** | 0423 | **ū** | Шу Shū |
| В | 0412 | v | Лисаковск Līsakovsk | **Ұ** | 04B0 | **u** | Нұр-Сұлтан Nur-Sultan |
| Г | 0413 | g | Аягөз Ayagöz | Ү | 04AE | ü | Үшарал Üsharal |
| Ғ | 0492 | gh | Жезқазған Zhezqazghan | Ф | 0424 | f | |
| Д | 0414 | d | | Х | 0425 | kh | Шахан Shakhan |
| Е | 0415 | e | Ембі Embi | Һ | 04BA | h | |
| Ё | 0401 | yo | Фёдоров Fyodorov | Ц | 0426 | ts | Клинцы Klīntsy |
| Ж | 0416 | **zh** | Жаркент Zharkent | Ч | 0427 | ch | Мичурино Mīchūrīno |
| З | 0417 | z | | Ш | 0428 | sh | Көкшетау Kökshetaū |
| **И** | 0418 | **ī** | Риддер Rīdder | Щ | 0429 | shch | |
| Й | 0419 | y | Алтай Altay | Ъ | 042A | ” | |
| К | 041A | k | | Ы | 042B | y | Алматы Almaty |
| Қ | 049A | q | Қызылорда Qyzylorda | І | 0406 | i | Ембі Embi |
| Л М Н | | l m n | Семей Semey | Ь | 042C | ’ | |
| Ң | 04A2 | ng | Байқоңыр Bayqongyr | Э | 042D | ė | Эрзерум Ėrzerūm |
| О | 041E | o | Орал Oral | Ю | 042E | yu | Юсупов Yusūpov |
| Ө | 04E8 | ö | Өскемен Öskemen | Я | 042F | ya | Аягөз Ayagöz |

- PCGN notes: гһ, зһ, кһ, нг, сһ, цһ may be written g·h, z·h, k·h, n·g, s·h, ts·h to separate them from digraphs. ы may be written i̵. — [PCGN Kazakh](https://assets.publishing.service.gov.uk/media/621caa32e90e0710b73fd4ff/ROMANIZATION_KAZAKH_Feb_22_19_.pdf)
- The passport data page is "printed in Kazakh and English only". The article says nothing on transliteration. — [Wikipedia: Kazakhstani passport](https://en.wikipedia.org/wiki/Kazakhstani_passport)
- 2018 plans: the MVD was to issue passports and ID cards on the Latin basis from 2021, with ID documents in Latin "from 2023". *Plans; I did not verify implementation.* — [Informburo.kz](https://informburo.kz/novosti/v-rk-planiruyut-nachat-vydachu-udostovereniy-lichnosti-i-pasportov-na-latinice-s-2021-goda.html); [Kursiv, 12 Nov 2018](https://kz.kursiv.media/2018-11-12/dokumenty-na-latinskiy-lad-pasporta-i-udostovereniya-lichnosti-v/); [Kazpravda](https://kazpravda.kz/n/v-2023-godu-kazahstantsy-nachnut-poluchat-lichnye-dokumenty-na-latinitse/)
- Kazakh ID documents are filled in the state language or Russian at the holder's choice, and the passport also in English. The applicant may ask for a specific English spelling based on documents such as a foreign passport, marriage certificate or published works, via a free-form written statement. *From a search summary of Kazakh legal Q&A and regulations; I did not read the text.* — [dogovor24.kz](https://dogovor24.kz/questions/sushchestvuyut-li-ustanovlennye-trebovaniyapravila-napisaniya-kazahskih-familii-imen-i-otchestv-sotrudnikov-naprimer-v-prikazah-2997.html); [adilet.zan.kz: Rules on documenting the population](https://adilet.zan.kz/rus/docs/P000001063_)
- "Common passport style uses Ye-, Zh- and Kh- (as in Yerlan, Zhanar and Bakhyt)", but "there is no single standard". Kassym is an alternative transcription of Қасым, and Assel a variant of Asel. *Weak source.* — [Behind the Name: Kazakh](https://www.behindthename.com/submit/names/usage/kazakh)
- Examples of doubled-s spellings in English names: [Kalmukhanbet Kassymov](https://en.wikipedia.org/wiki/Kalmukhanbet_Kassymov), [Makhmud Kassymbekov](https://en.wikipedia.org/wiki/Makhmud_Kassymbekov).

### Inferences
- **Kazakh letter table for the package** (passport column is *proposed*):

| Cyr | PCGN | 2021 Latin | MRZ (proposed) | Variants |
|---|---|---|---|---|
| Ә | ä | ä | A | A, AE, E (Әлия → Aliya; Әсел → Asel/Assel) |
| Ғ | gh | ğ | G | G, GH |
| Қ | q | q | K | K, Q |
| Ң | ng | ñ | N | N, NG |
| Ө | ö | ö | O | O, OE, U |
| Ұ | u | ū | U | U |
| Ү | ü | ü | U | U, UE, YU |
| Һ | h | h | H | H, KH |
| І | i | ı (sic) | I | I |
| И | ī | i | I | I, Y (word-final -ий → -IY/-II) |
| Й | y | i | I (ICAO) | Y, I |
| Ж | zh | j | ZH | ZH, J (Kassym-Jomart), DZH |
| Х | kh | h | KH | KH, H |
| Е (initial) | e | e | E (ICAO) | YE, E (Yerlan/Erlan, Yerzhan/Erzhan) |
| Ы | y | y | Y | Y, I |
| Ю | yu | — | IU | YU, IU |
| Я | ya | — | IA | YA, IA |
| С between vowels | s | s | S | S, **SS** (Kassym, Assel, Yeleussinov) |

- Patronymic and new-style surnames: **-ұлы / -қызы** (Kazakh "son/daughter of") → uly / qyzy, kyzy, kizi. They appear as surname replacements (e.g., Alimkhanuly) and as patronymics. Russian-style -ович/-овна and -ов/-ова/-ев/-ева coexist. Equivalence clusters: Nurlanuly ↔ Nurlanovich (patronymic), Kassymov ↔ Kasymov ↔ Qasymov.
- Example derivations: Нұрсұлтан → NURSULTAN (all systems). Әлия → ALIYA (common) | ALIIA (strict ICAO via the Russian form Алия) | Äliya (PCGN). Қасым-Жомарт Тоқаев → KASSYM-JOMART TOKAYEV (official English) | KASYM-ZHOMART TOKAEV (ICAO from Cyrillic) | Qasym-Jomart Toqaev (2021 Latin).
- Kazakh "ı" (dotless) in the 2021 alphabet means **І** (front vowel), while Turkish/Azerbaijani "ı" is the back vowel (=Kazakh Ы, which is Y in 2021). The ASCII mapping is I in both cases, but a reverse or phonetic mapping must be language-specific.

### Gaps
- **I could not find the Kazakhstan MVD transliteration table for passports and ID cards**, or any confirmation that passports are now issued in the 2021 Latin alphabet. The ICAO-style IU/IA vs YU/YA usage and the "ss" convention for intervocalic С have no official source here.
- I could not confirm an implementation status report for 2025–2026 (e.g., a government plan revision). Only "on track for 2031" summaries were found.
- The 2021 handling of Ч, Ц, Ю, Я, Ё is unclear in the sources I read.

---

## 6. Kyrgyz (Cyrillic ң ө ү; passport practice; uulu/kyzy)

### Takeaway
Kyrgyz is Cyrillic only, with no commonly accepted romanization. BGN/PCGN 1979 is used for geographic names (notably **Ж→j**, Ң→ng, Ө→ö, Ү→ü). Passport spellings have been inconsistent (Жумагулов → Dzhumagulov). Applicants could request a spelling. A new Government resolution, **No. 651 of 29 Sept 2026**, formally lets applicants state their preferred Latin spelling of surname, name and patronymic, provided meaning and phonetics are kept.

### Cited Findings
**BGN/PCGN 1979 Kyrgyz (checked Feb 2022)** — [PCGN Kyrgyz romanization (PDF)](https://assets.publishing.service.gov.uk/media/621caa11e90e0710c30a4706/ROMANIZATION_KYRGYZ_Feb22_9_.pdf)

| Cyr | PCGN | Example | Cyr | PCGN | Example |
|---|---|---|---|---|---|
| А | a | Арпа Arpa | П | p | Пүлгөн Pülgön |
| Б | b | Бишкек Bishkek | Р | r | Рават Ravat |
| В | v | | С | s | Сүлүктү Sülüktü |
| Г | g | Гүлчө Gülchö | Т | t | Талас Talas |
| Д | d | Дөң-Арык Döng-Aryk | У | u | Учкун Uchkun |
| Е | e | Бишкек Bishkek | **Ү** (04AE) | **ü** | Чүй Chüy |
| Ё | yo | | Ф | f | Фергана Fergana |
| **Ж** | **j** | Жалал-Абад Jalal-Abad | Х | kh | Халмион Khalmion |
| З | z | Кызыл-Суу Kyzyl-Suu | Ц | ts | (loans only) |
| И | i | Исфана Isfana | Ч | ch | Чүй Chüy |
| Й | y | Чүй Chüy | Ш | sh | Шопоков Shopokov |
| К | k | Кара-Балта Kara-Balta | Щ | shch | (loans only) |
| Л М Н | l m n | Нарын Naryn | Ъ | ” | |
| **Ң** (04A2) | **ng** | Дөң-Арык Döng-Aryk | Ы | y | Ысык-Көл Ysyk-Köl |
| О | o | Ош Osh | Ь | ’ | |
| **Ө** (04E8) | **ö** | Өзгөн Özgön | Э | e | Эркеч-Там Erkech-Tam |
| | | | Ю / Я | yu / ya | Ак-Моюн Ak-Moyun, Каныш-Кыя Kanysh-Kyya |

- PCGN notes: нг may be written n·g. ы may be i̵. Apostrophes are U+2019. — [PCGN Kyrgyz](https://assets.publishing.service.gov.uk/media/621caa11e90e0710c30a4706/ROMANIZATION_KYRGYZ_Feb22_9_.pdf)
- "There is no commonly accepted system of romanization for Kyrgyz". For geographic names the government adopted BGN/PCGN. Latin proposals have made little progress. — [Wikipedia: Romanization of Kyrgyz](https://en.wikipedia.org/wiki/Romanization_of_Kyrgyz)
- Government Resolution **No. 651**, signed 29 Sept 2026 by Chair of the Cabinet Adylbek Kasymaliev, in force 10 days after publication. "When submitting an application, a citizen will be able to indicate the desired spelling of surname, name and patronymic in Latin letters", but "the chosen spelling must not change the meaning and phonetics". The article gives no table. — [Economist.kg, 2 Oct 2026](https://economist.kg/pravo-znat/2026/10/02/pravila-oformleniya-pasportov/)
- Earlier reporting (2015) says passport Latin spellings were inconsistent: "Жумагулов может стать Dzhumagulov, а Хамид — Khamid вместо Hamid". The letters ж, к, ң, ы, ө, ү "набираются в 3-4 произвольных вариантах". The State Registration Service lets a citizen, on a reasoned application, choose a Latin spelling by which the name remains identifiable, and officers must explain the transliteration rules. *From a search summary; the GRS page had an expired certificate.* — [Kloop.kg, 2015](https://kloop.kg/blog/2015/08/11/bektur-iskender-kak-izbezhat-idiotskogo-napisaniya-imeni-v-zagranpasporte/); [24.kg](https://24.kg/obschestvo/5051_grs_kyirgyizstantsyi_mogut_sami_proverit_napisanie_familii_i_imeni_v_zagranpasporte/); [GRS FAQ](https://grs.gov.kg/ru/questions/21-Pravovaia-ghramotnost-napisaniie-familii-v-pasport/)
- A proposed Kyrgyz Latin script (unofficial) uses six extra letters: Ç (ч), Ğ (ғ), Ñ (ң), Ö (ө), Ş (ш), Ü (ү). *Search summary.* — [qyrgyz.com](https://www.qyrgyz.com/kyrgyzskaya-latinitsa)

### Inferences
- Kyrgyz variant axes: Ж → ZH | J | DZH (Жапаров → Japarov/Zhaparov/Dzhaparov). Ң → N | NG. Ө → O | OE | U. Ү → U | UE | YU. Ы → Y | I. Х → KH | H. Е (initial) → E | YE. Ю/Я → YU/YA | IU/IA. Й → Y | I.
- Patronymic markers **уулу** (son) → uulu | uuly | ulu, and **кызы** (daughter) → kyzy | kizi | qizi. They are also used as surname replacements (e.g., "Asanbek uulu"). Russian-style -ович/-овна, -ов/-ова/-ев/-ева coexist. *Unsourced here; widely documented.*
- Resolution 651 increases spelling diversity, since holders may choose their own forms. Matching must rely on variant generation and fuzzy keys rather than a single canonical form.

### Gaps
- I did not retrieve the text of Resolution 651 or any official Kyrgyz transliteration annex, so it is unknown whether a default table (ICAO/Russian-style or BGN-style) exists.

---

## 7. Turkmen (Latin 1993/1999: Ä Ç Ž Ň Ö Ş Ü Ý, W, J for /dʒ/; Cyrillic legacy; passport rendering)

### Takeaway
Turkmen has used Latin officially since 1993. Currency-sign letters ($, ¢, £, ¥) were replaced in 1999 by Ş/Ç/Ž/Ý, and Ñ by Ň. The PCGN 2000 table gives the legacy Cyrillic mapping. Key differences from other Turkic standards: Cyrillic **В→w**, **Ж→ž**, **Җ→j**, **Й→ý**, **Х→h**, **Ә→ä**; surnames end in **-ow/-owa** in Latin (Nyýazow) but -ov/-ova in Russian-form documents. I found no source on how Turkmen passports render ý/ž/ň/ä in the MRZ.

### Cited Findings
**Turkmen Cyrillic → Latin: BGN/PCGN 2000 Agreement (checked Sept 2022)** — [PCGN Turkmen table (PDF)](https://assets.publishing.service.gov.uk/media/6329b1638fa8f53cb45763b4/TABLE_OF_CORRESPONDENCES_FOR_TURKMEN_with_examples.pdf)

| # | Cyr | Latin | Example | # | Cyr | Latin | Example |
|---|---|---|---|---|---|---|---|
| 1 | А | a | Ашгабат Aşgabat | 20 | П | p | Мургап Murgap |
| 2 | Б | b | Лебап Lebap | 21 | Р | r | Мары Mary |
| 3 | **В** | **w** | Ныязов Nyýazow | 22 | С | s | Сарахс Sarahs |
| 4 | Г | g | Тагта Tagta | 23 | Т | t | |
| 5 | Д | d | Дашховуз Daşhowuz | 24 | У | u | |
| 6 | Е | e / **ýe** (initial; after vowels; after й) | Небитдаг Nebitdag | 25 | Ү | ü | Түркменбашы Türkmenbaşy |
| 7 | Ё | ýo | Ёлөтен Ýolöten | 26 | Ф | f | Фарап Farap |
| 8 | **Ж** | **ž** | | 27 | **Х** | **h** | Дашховуз Daşhowuz |
| 9 | **Җ** (0496) | **j** | Теҗен Tejen | 28 | Ц | s | |
| 10 | З | z | Газанҗык Gazanjyk | 29 | Ч | ç | Челекен Çeleken |
| 11 | И | i | Керки Kerki | 30 | Ш | ş | |
| 12 | **Й** | **ý** | Бүзмейин Büzmeýin | 31 | Щ | şç | |
| 13 | К | k | Кака Kaka | 32 | Ъ | (not romanized) | |
| 14 | Л | l | | 33 | Ы | y | Мары Mary |
| 15 | М | m | | 34 | Ь | (not romanized) | |
| 16 | Н | n | | 35 | Э | e | Эсенгулы Esenguly |
| 17 | **Ң** | **ň** | Чаршаңңы Çarşaňňy | 36 | **Ә** (04D8) | **ä** | Әнев Änew |
| 18 | О | o | | 37 | Ю | ýu | |
| 19 | Ө | ö | Ёлөтен Ýolöten | 38 | Я | ýa | Ныязов Nyýazow |

- PCGN notes for 1993-era data: Ұ (U+04BE, sic) / ÿ → **Ý/ý**; £ / ſ → **Ž/ž**; ñ → **ň**. Letter inventory: Ý Ž Ü Ç Ş Ň Ö Ä. — [PCGN Turkmen](https://assets.publishing.service.gov.uk/media/6329b1638fa8f53cb45763b4/TABLE_OF_CORRESPONDENCES_FOR_TURKMEN_with_examples.pdf)
- Wikipedia's Turkmen alphabet table has columns "Cyrillic, 1940–1993", "1993–1999" and "Current, since 1999". The 1993 forms include £ for Ž and $ / ¢ for another letter (Ş per common accounts). The article is tagged "more citations needed" on the currency-sign claim. — [Wikipedia: Turkmen alphabet](https://en.wikipedia.org/wiki/Turkmen_alphabet)
- Since 1991 the -ov(a) surname ending has become -ow(a) in Turkmen Latin. *Search summary of secondary sources.* — [Wikipedia: Turkmen alphabet](https://en.wikipedia.org/wiki/Turkmen_alphabet); [A primer on Turkmen names (blog)](https://carrieannebrownian.wordpress.com/2017/05/05/a-primer-on-turkmeni-names/)

### Inferences
- Proposed Turkmen MRZ fold (ICAO 6.A): Ä→A (or AE), Ç→C, Ň→N, Ö→O (or OE), Ş→S, Ü→U (or UE), Ý→Y, Ž→Z. English-phonetic profile: Ç→CH, Ş→SH, Ž→ZH, Ň→NG, Ý→Y, J→J/DZH, W→W/V.
- Variant examples: Nyýazow (Latin) → NYYAZOW (MRZ fold) | Niyazov (English) | NIIAZOV (ICAO via Russian Ниязов) | Nijazow (German). Berdimuhamedow ↔ Berdimuhamedov ↔ Berdymukhamedov (Russian Бердымухамедов → BERDYMUKHAMEDOV).
- Turkmen patronymic markers: ogly (son) / gyzy (daughter). *Unsourced here.*
- Russian-form Cyrillic of Turkmen names uses В for /w/, Ж for /dʒ/ (Җ absent from Russian), Х for /h/. So Latin w ↔ v, j ↔ dzh/zh, h ↔ kh must be equivalence axes.

### Gaps
- **No source found** on Turkmen passport MRZ practice (e.g., whether `-OW` or `-OV`, Ý→Y), or on any Turkmen government transliteration rule for documents.

---

## 8. Tajik (Cyrillic ғ ӣ қ ӯ ҳ ҷ; 1998 orthography; surname reforms 2007/2016; 2026 name register)

### Takeaway
Tajik is written in Cyrillic: 35 letters after the 1998 reform abolished ц, щ, ь, ы, plus six extra letters ғ ӣ қ ӯ ҳ ҷ. BGN/PCGN 1994 gives Ғ→gh, Ӣ→í, Қ→q, Ӯ→ŭ, Ҳ→h, Ҷ→j, Х→kh, Ж→zh. A 2016 law bans Russian-style -ov/-ev/-ovich/-ovna for newborn registrations in favour of -zod, -zoda, -ī, -yon, -far, -pur (President Rahmonov became Rahmon in 2007). A revised register of approved given names (Feb 2026) removed many Arabic names. I found no primary source for passport transliteration.

### Cited Findings
**BGN/PCGN 1994 Tajik (checked Sept 2022)** — [PCGN Tajik romanization (PDF)](https://assets.publishing.service.gov.uk/media/634e72918fa8f534627a6e60/ROMANIZATION_OF_TAJIK-2022.pdf)

| Cyr | U+ | PCGN | Example | Cyr | U+ | PCGN | Example |
|---|---|---|---|---|---|---|---|
| А | 0410 | a | Омударё Omudaryo | Н | 041D | n | Гулистон Guliston |
| Б | 0411 | b | Бохтар Bokhtar | О | 041E | o | |
| В | 0412 | v | Ворух Vorukh | П | 041F | p | Помир Pomir |
| Г | 0413 | g | Зигар Zigar | Р С Т | | r s t | |
| **Ғ** | 0492 | **gh** | Суғд Sughd | У | 0423 | u | Хуҷанд Khujand |
| Д | 0414 | d | Дарбанд Darband | **Ӯ** | 04EE | **ŭ** | Қарокӯл Qarokŭl |
| Е | 0415 | e | Душанбе Dushanbe | Ф | 0424 | f | Фарғона Farghona |
| Ё | 0401 | yo | Сирдарё Sirdaryo | Х | 0425 | **kh** | Хоруғ Khorugh |
| Ж | 0416 | zh | (loans only) | **Ҳ** | 04B2 | **h** | Кӯҳҳои Помир Kŭhhoi Pomir |
| З | 0417 | z | Зафаробод Zafarobod | Ч | 0427 | ch | Сомончӣ Somonchí |
| И | 0418 | i | Ҷумҳурии Тоҷикистон Jumhurii Tojikiston | **Ҷ** | 04B6 | **j** | Панҷ Panj |
| **Ӣ** | 04E2 | **í** | Сомонӣ Somoní | Ш | 0428 | sh | Шаҳристон Shahriston |
| Й | 0419 | y | Шайдон Shaydon | Ъ | 042A | ’ | Роштқалъа Roshtqal’a |
| К | 041A | k | Кӯлоб Kŭlob | Э | 042D | ė | Энгелс Ėngels |
| **Қ** | 049A | **q** | Қайроққум Qayroqqum | Ю | 042E | yu | Юқори Yuqori |
| Л М | | l m | Хатлон Khatlon | Я | 042F | ya | Янгиобод Yangiobod |

- 1998 reform (government decree of 3 Sept 1998) abolished ц, щ, ь, ы. Legacy romanization: ц → s (before a vowel and/or after a consonant) or ts (between vowels); щ → sh; ь → not romanized; ы → i. гҳ, зҳ, кҳ, сҳ may be written g·h, z·h, k·h, s·h. — [PCGN Tajik](https://assets.publishing.service.gov.uk/media/634e72918fa8f534627a6e60/ROMANIZATION_OF_TAJIK-2022.pdf)
- Before 1998 the alphabet had 39 letters: the 33 Russian letters plus ғ ӣ қ ӯ ҳ ҷ. — [Wikipedia: Tajik alphabets](https://en.wikipedia.org/wiki/Tajik_alphabets)
- The 2016 law banned surnames and patronymics with "-ov", "-ev", "-ovich", "-ovna". Names are to be formed with Tajik endings "-zod", "-zoda", "-y", "-yon", "-far", "-pur". President Rahmon proposed the change in 2007 and changed his own name from Emomali Sharifovich Rakhmonov to Emomali Rakhmon. — [The Moscow Times, 29 Apr 2016](https://www.themoscowtimes.com/2016/04/29/russian-surnames-officially-banned-in-tajikistan-a52732); [RFE/RL 2016](https://www.rferl.org/a/tajikistan-bans-giving-babies-russian-style-last-names/27708093.html)
- RFE/RL (21 June 2026): in 2016 parliament also banned "foreign"/"Arabic-sounding" names and Islamic titles added to names (mullah, khalifa, shaikh, amir, sufi). A revised official name list approved in **Feb 2026** removed 1,745 of 4,056 names and added 965 "Aryan"/Persian names (~4,000 total). Arabic names linked to Islamic figures (e.g., Muhammad, Abubakr, Sumayah, Khadija) are being removed. — [RFE/RL, 2026](https://www.rferl.org/a/tajikistan-baby-names-approved-list/33784703.html)
- Academic overview of the naming laws and privacy. — [Academia.edu: "From Rahmonov to Rahmon"](https://www.academia.edu/41662082/From_Rahmonov_to_Rahmon_Naming_Laws_and_the_Right_to_Privacy_in_Tajikistan)

### Inferences
- **Tajik variant axes:**
  - Ҷ → J | DZH | DJ | ZH (Russian form writes Дж: Ҷамшед → Джамшед → DZHAMSHED/Jamshed).
  - Ғ → GH | G.
  - Қ → Q | K.
  - Ҳ → H | KH (Russian form Х).
  - Х → KH | H | X.
  - Ӣ → I | EE | IY | Y (final -ӣ is the adjectival/ezafe -ī in surnames like Rahmonī).
  - Ӯ → U | O | OO (Кӯлоб → Kulob).
  - О → O | A (Russian form often writes а: Раҳмон → Рахмон/Рахмонов; Мирзо → Мирза).
  - Е (initial) → E | YE.
  - Ё/Ю/Я → YO/YU/YA | E/IU/IA (ICAO).
- **Surname clusters:**
  - -ov/-ova/-ev/-eva ↔ ∅ ↔ -zoda/-zoda ↔ -zod ↔ -ī/-i ↔ -iyon/-yon ↔ -far ↔ -pur.
  - Example: Rahmonov ↔ Rahmon ↔ Rakhmonov ↔ Rakhmon ↔ Rahmonzoda.
  - Example: Sharipov ↔ Sharifzoda ↔ Sharifī ↔ Sharifi.
  - Russian patronymic -ovich ↔ Tajik "-zod/-far" or none.
  - Persian-style given-name compounds to segment: -jon/-dzhon (Sharifjon), -boy/-bai (Saidboy), -bek, -khon/-xon/-hon, -niso/-nisso, -gul/-gul', -mo/-moh, Mahmad-/Muhammad- prefixes (Mahmadali = Muhammad + Ali). *Unsourced heuristics.*
- Since the 2026 register removes Arabic names, newer Tajik records may hold Persian replacements. Matching across generations within a family cannot rely on name continuity.

### Gaps
- **I found no primary source on Tajik passport Latin transliteration** (biometric passports since 2010). Whether Ҷ is J or DZH and Ғ is GH or G in the MRZ is unverified.
- I did not find whether the 2016 suffix ban covers Latin spellings in passports of adults who re-register.

---

## 9. Tatar and Bashkir (extra Cyrillic letters; Russian passports)

### Takeaway
Tatars and Bashkirs in Russia hold Russian documents. Names in passports are written in **Russian Cyrillic** and romanized with the MVD/ICAO table (§1), so the extra letters (Tatar ә ө ү җ ң һ; Bashkir ә ө ү ғ ҡ ң ҙ ҫ һ) usually do not appear and have no MVD mapping. The PCGN 2007 tables are the reference for romanizing native-script forms. Tatar Latin (Zamanälif) was made illegal as an official script by a 2002 federal amendment, upheld by the Constitutional Court in 2004. Since 2012 it is Tatarstan's official *romanization*, while Cyrillic remains the only official script.

### Cited Findings
**Tatar Cyrillic → Roman: BGN/PCGN 2007 Agreement (checked Aug 2019)** — [PCGN Tatar table (PDF)](https://assets.publishing.service.gov.uk/media/5d6f828ce5274a097c07b95c/TABLE_OF_CORRESPONDENCES_FOR_TATAR.pdf)

| Cyr | Roman | Cyr | Roman |
|---|---|---|---|
| А | a | Р С Т | r s t |
| **Ә** | **ə** (zamanalif: ä) | У | u / w (w after a vowel) |
| Б | b | **Ү** | **ü / w** |
| В | w / v (v in loans) | Ф | f |
| Г | ğ (back-vowel words) / g (front) | Х | x |
| Д | d | **Һ** | **h** |
| Е | e, yı/ye (after a vowel except и, ю; after ъ, ь; word-initially) | Ц | ts |
| Ж | j | Ч | ç |
| **Җ** | **c** | Ш | ş |
| З | z | Щ | şç |
| И | i | Ъ | not romanized |
| Й | y | Ы | ı, ıy (loans), i (after ğ, q: Гыйльмиев → Ğilmiev) |
| К | q (back) / k (front) | Ь | ’ |
| Л М Н | l m n | Э | e, ’ (after a vowel in Arabic-origin words) |
| **Ң** | **ꞑ** (zamanalif: ñ) | Ю | yu / yü; ü after и |
| О | o | Я | ya / yä; a/ä after и |
| **Ө** | **ɵ** (zamanalif: ö) | П | p |

- PCGN calls the alphabet "yaꞑalif-2". The simpler "zamanalif" set uses ä, ñ, ö for ə, ꞑ, ɵ, "all three alternatives must be used as a set". Code points: Ə U+018F/U+0259, Ꞑ U+A790/U+A791, Ɵ U+019F/U+0275. — [PCGN Tatar](https://assets.publishing.service.gov.uk/media/5d6f828ce5274a097c07b95c/TABLE_OF_CORRESPONDENCES_FOR_TATAR.pdf)

**Bashkir Cyrillic → Roman: BGN/PCGN 2007 Agreement (checked Aug 2019)** — [PCGN Bashkir table (PDF)](https://assets.publishing.service.gov.uk/media/5d6f825aed915d08f9a72a4d/TABLE_OF_CORRESPONDENCES__FOR_BASHKIR.pdf)

| Cyr | Roman | Cyr | Roman |
|---|---|---|---|
| А Б | a b | Ө | ö |
| В | v, w (word-initial and before a vowel) | П Р С | p r s |
| Г | g | **Ҫ** (04AA) | **ś** |
| **Ғ** (0492) | **ğ** | Т | t |
| Д | d | У | u / w (between or after vowels) |
| **Ҙ** (0498) | **ź** | Ү | ü / w |
| Е | e, ye (word-initial and before a vowel) | Ф | f |
| Ё | ë | Х | x |
| Ж З И Й | j z i y | **Һ** (04BA) | **h** |
| К | k | Ц Ч Ш Щ | ts ç ş şç |
| **Ҡ** (04A0) | **q** | Ъ / Ь | not romanized |
| Л М Н | l m n | Ы | i |
| **Ң** (04A2) | **ñ** | Э | e |
| О | o | **Ә** (04D8) | **ə** |
| | | Ю / Я | yu / ya |

- Tatar Latin history: a 1999 decree planned Latin as sole official script by 1 Sept 2011. On 15 Nov 2002 the State Duma amended federal law (Cyrillic required for state languages of republics). On 16 Nov 2004 the Constitutional Court declined Tatarstan's appeal. The decree was rescinded on 22 Jan 2005. A Tatarstan law of 24 Dec 2012 made the 2000 Latin alphabet (Zamanälif) the official *romanization* and Yaña imlâ the Arabic transliteration. "As of 2020, Cyrillic remains the only official script in Tatarstan." — [Wikipedia: Tatar alphabets](https://en.wikipedia.org/wiki/Tatar_alphabets)
- The Russian passport table covers only the 33 Russian letters (and drops Ь). — [MVD Order 996 appendix](https://www.consultant.ru/document/cons_doc_LAW_346719/413ce7cde653ee8a7c578654112520bdd971d99d/)

### Inferences
- In the package, **Tatar/Bashkir input in native Cyrillic** should be (1) romanized with PCGN, and (2) mapped to a *Russian-form Cyrillic* guess and then the MVD table, because that is what passports carry. Proposed Russian-form fallbacks:
  - Ә → А/Я/Э (Сәлимә → Салима).
  - Ө → О/Ё.
  - Ү → У/Ю.
  - Җ → Дж/Ж (Җәлил → Джалиль/Жалиль).
  - Ң → Н/НГ.
  - Һ → Х/Г.
  - Ғ → Г.
  - Ҡ → К.
  - Ҙ → З.
  - Ҫ → С.
- Example: Tatar Гыйльмиев → PCGN Ğilmiev; Russian passport form Гильмиев → GILMIEV.
- Patronymics in Russian documents use -ович/-овна (e.g., Рустамович). Native forms are Tatar улы/кызы and Bashkir улы/ҡыҙы. Strip both kinds when building match keys.
- ICAO's literal Һ→"C" must not be used. Ғ→G is acceptable.

### Gaps
- I did not verify whether Russian internal passports for Tatarstan/Bashkortostan residents can show the native-script name (e.g., on an insert page) and how it would be romanized. Most likely it never reaches the MRZ.

---

## 10. Chechen, Ingush and Dagestani languages (Avar etc.): palochka, digraphs, Russian passports

### Takeaway
Chechen, Ingush, Avar, Dargwa, Lak, Lezgian and Tabassaran use the **palochka Ӏ** (U+04C0; lowercase U+04CF since Unicode 5.0, 2006). It marks ejective or pharyngeal consonants and, in digraphs, sounds like хӀ = /h/. In practice it is often typed as Latin I, l, digit 1, Roman numeral Ⅰ or Cyrillic І. Bearers hold Russian passports, so names are in Russian Cyrillic (Рамзан, Ахмат, Хамзат, Магомед, Шамиль), romanized by the MVD/ICAO table (RAMZAN, AKHMAT, KHAMZAT, MAGOMED, SHAMIL). The PCGN 2008 Chechen table gives the native-script romanization, with digraphs кх→q, къ→q̇, кӀ→kh, тӀ→th, хь→ẋ, хӀ→h, гӀ→ġ.

### Cited Findings
- Palochka: "introduced to the Cyrillic script in the late 1930s as the Hindu-Arabic digit ⟨1⟩. On some Cyrillic keyboards, it is usually typeset as the Roman numeral ⟨I⟩". Unicode encodes the caseless/capital palochka at **U+04C0** and a rarer lowercase at **U+04CF** (added in Unicode 5.0, July 2006). Its uppercase resembles Latin **I** and its lowercase Latin **l**. It is used in Abaza, Avar, Chechen, Dargwa, Ingush, Lak, Lezgian, Tabassaran and Tsakhur as a modifier for ejective or pharyngeal sounds. In Chechen, after a voiceless stop or affricate it marks an ejective, after a voiced one pharyngealization. Alone it is /ʔˤ/. In хӀ it gives /h/. Ingush is similar. Avar example: кӀалъазе. — [Wikipedia: Palochka](https://en.wikipedia.org/wiki/Palochka)
- Local Unicode check (Python `unicodedata` 13.0): U+04C0 is "CYRILLIC LETTER PALOCHKA" (`.lower()` → U+04CF) and U+04CF is "CYRILLIC SMALL LETTER PALOCHKA" (`.upper()` → U+04C0). Common look-alikes: U+0049 I, U+006C l, U+0031 1, U+007C |, U+0406 І, U+0456 і, U+2160 Ⅰ, U+01C0 ǀ, U+0399 Ι (Greek). *Local verification.*

**Chechen Cyrillic → Roman: BGN/PCGN 2008 Agreement (checked Jan 2024)** — [PCGN Chechen table (PDF)](https://assets.publishing.service.gov.uk/media/65b78e360c75e30012d8019c/TABLE_OF_CORRESPONDENCES_FOR_CHECHEN.pdf)

| Cyr | Roman | Cyr | Roman | Cyr | Roman |
|---|---|---|---|---|---|
| А | a, ə (ə = short a) | Кх | q | Ф | f |
| Аь | ä | Къ | q̇ | Х | x |
| Б В Г | b v g | КӀ | kh | Хь | ẋ |
| ГӀ | ġ | Л М | l m | ХӀ | h |
| Д | d | Н | n, ŋ (nasalization) | Ц | c |
| Е | e, ye (word- and syllable-initial) | О | o (also ꭣ / oa in sources) | ЦӀ | ċ |
| Ё | yo (loans) | Оь | ö | Ч | ç |
| Ж | z̵ | П | p | ЧӀ | ç̇ |
| З И Й | z i y | ПӀ | ph | Ш / Щ | ş / şç (loans) |
| К | k | Р С Т | r s t | Ъ | ’ (loans) |
| | | ТӀ | th | Ы | i (loans) |
| | | У | u | Ь | not romanized |
| | | Уь | ü | Э | e |
| | | | | Ю / Юь | yu / yü |
| | | | | Я / Яь | ya / yä |
| | | | | **Ӏ** (alone) | **j** (except in гӏ кӏ пӏ тӏ хӏ цӏ чӏ) |

- PCGN notes: ккх → qq, ккъ → q̇q̇. Several outputs use combining dot (U+0307) or combining short stroke (U+0335): Ġ, Q̇, Ẋ, Ċ, Ç̇, Z̵. — [PCGN Chechen](https://assets.publishing.service.gov.uk/media/65b78e360c75e30012d8019c/TABLE_OF_CORRESPONDENCES_FOR_CHECHEN.pdf)
- The Russian passport table has no palochka or Caucasian digraph rules. Only the 33 Russian letters are mapped. — [MVD Order 996 appendix](https://www.consultant.ru/document/cons_doc_LAW_346719/413ce7cde653ee8a7c578654112520bdd971d99d/)

### Inferences
- **Palochka normalizer** (Cyrillic context only): if a token is mostly Cyrillic and contains `I l 1 | Ⅰ ǀ І і ӏ` **immediately after** г, к, п, т, х, ц, ч (Chechen/Ingush/Avar digraphs) or between Cyrillic letters, map it to U+04C0. Never do this in Latin-script tokens.
- For passport/ICAO output, **drop the palochka** (Russian-form names normally lack it). For PCGN output, use the table above.
- **Russian-form name examples** (derived via MVD 996):
  - Рамзан → RAMZAN.
  - Ахмат → AKHMAT.
  - Хамзат → KHAMZAT.
  - Магомед → MAGOMED.
  - Мухаммад → MUKHAMMAD.
  - Абдулла → ABDULLA.
  - Шамиль → SHAMIL (Ь dropped).
  - Ильяс → ILIAS (ICAO: Ь dropped, Я→IA). The common older/English form is ILYAS.
  - Зелимхан → ZELIMKHAN.
  - Айшат → AISHAT.
  - Хадижат → KHADIZHAT.
  - Рамазан → RAMAZAN.
- Caucasus-specific forms of Arabic names (Магомед, Магомедов, Магомедрасул, Гаджи-, Исмаил, Сулейман, Хаджимурад, Патимат for Fatima, Хадижат, Айшат, Зайнаб/Зейнаб) must sit in the same clusters as their Arabic and Turkic counterparts (§12).
- Dagestani compounds: Магомед-/Гаджи-/Абдул- prefixes and -ов/-ова surnames are often hyphenated or fused (Магомедрасулов vs Магомед-Расулов). Normalize hyphen and space and generate both fused and split forms.

### Gaps
- I found no BGN/PCGN tables for Ingush or Avar in the gov.uk list. Their digraphs are similar to Chechen but were not verified.
- I could not verify whether any Russian civil-registry rule forbids or allows the palochka in names in internal passports.

---

## 11. Uyghur (brief): ULY / New Uyghur Latin, and names in Chinese passports

### Takeaway
Uyghur is officially written in Perso-Arabic in Xinjiang. The Latin auxiliary ULY (Uyghur Latin Yëziqi, finalized at Xinjiang University, 2000–2001) and its 2008 New Uyghur Latin (NUL) form are widely used. BGN/PCGN adopted it in 2023. Chinese passports and ID cards, however, show the **Pinyin of a Chinese-character transcription**, e.g., Ilham Tohti → 伊力哈木·土赫提 → **Yilihamu Tuheti**. A Uyghur therefore has three or more written forms. Central-Asian Uyghurs use Cyrillic and fall under Kazakh, Kyrgyz or Uzbek document rules.

### Cited Findings
- BGN/PCGN 2023 Uyghur agreement (checked Feb 2024) reflects the **New Uyghur Latin Romanization System (NUL)**, published by the Xinjiang Language and Writing Systems Committee on 11 Jan 2008 and based on the Latin Script for Uyghur (LSU, Xinjiang University, 2000–2001). NUL "has not been officially utilized in Xinjiang" but "has been widely adopted by Uyghurs both inside and outside China". About half a million Uyghurs in Central Asia use Cyrillic. Example consonants: چ → ch (Cherchen), خ → x (Xoten), ج → j. — [PCGN Uyghur romanization (PDF)](https://assets.publishing.service.gov.uk/media/65f317e99d99de001d03df0c/Uyghur_romanization.pdf)
- ULY letters (Latin, IPA): A a, E e, B b, P p, T t, J j /dʒ/, **CH ch**, **X x** /χ/, D d, R r, Z z, **ZH zh**, S s, **SH sh**, **GH gh** /ʁ/, F f, Q q, K k, G g, **NG ng**, L l, M m, N n, H h, O o, U u, Ö ö, Ü ü, W w, Ë ë (é), I i, Y y. "In 2023, the alphabet was agreed as the BGN/PCGN romanization system". — [Wikipedia: Uyghur Latin alphabet](https://en.wikipedia.org/wiki/Uyghur_Latin_alphabet)
- "Most Uyghurs' official documents, including passports and government-issued ID cards, use a Pinyin transliteration of the Chinese transliteration of their given names". Pinyin versions "often render the names very differently from their Uyghur originals". Uyghurs often have three or more name versions (Uyghur script, Chinese characters, Latin from Uyghur and/or from Chinese). — [UHRP: Decolonizing the discussion of Uyghurs](https://uhrp.org/report/decolonizing-the-discussion-of-uyghurs-recommendations-for-journalists-and-researchers/)
- Ilham Tohti: Uyghur ئىلھام توختى; Chinese 伊力哈木·土赫提; pinyin Yīlìhāmù Tǔhètí. — [Wikipedia: Ilham Tohti](https://en.wikipedia.org/wiki/Ilham_Tohti)

### Inferences
- In the package, Uyghur support should cover (a) ULY/NUL → ASCII (x→KH/X/H, gh→GH/G, ë/é→E, ö→O, ü→U, q→Q/K) and (b) an optional **known-pairs dictionary** linking Uyghur names to Chinese-pinyin forms, which cannot be derived letter by letter. Commonly seen pinyin patterns (heuristic, unsourced): Muhammad/Memet → Maimaiti (买买提); Ahmat → Aihemaiti; Abdu- → Abudu-/Abuduli-; -jan → -jiang (江); Ilham → Yilihamu; Tohti → Tuheti. Mark these as "transcription via Chinese", not transliteration.
- Chinese ID formatting puts the given name first and joins Uyghur name parts with "·" (middle dot) in Chinese. In pinyin passport fields the order and segmentation may differ. Matching should be order-insensitive.

### Gaps
- I did not retrieve an official Chinese standard for transcribing minority names into characters or pinyin for passports (e.g., GB/T standards or the 少数民族人名汉字音译 rules).

---

## 12. Cross-language variant patterns: the Muhammad cluster, Russified forms, sh/ch/kh/zh, q/k, ğ/g/gh, ü/u/yu, ö/o/yo, ə/a/e, patronymic and surname affixes

### Takeaway
Across these languages the same phoneme is written very differently by national Latin, PCGN and Russian/ICAO conventions. The variation is systematic, so a small set of **equivalence axes** plus a **Russian-form round-trip** covers most real-world variants. The cited sources show these axes directly: Soviet-legacy Uzbek chains, Kyrgyz passport inconsistencies, and the different PCGN choices for Ж.

### Cited Findings
- Uzbek Soviet-legacy chains: X → Kh; Q → K/Q; Oʻ → U/O; J → Dj/J; Gʻ → G/Gh; H → X/H (via Russian Х). — [Kun.uz 2022](https://kun.uz/uz/news/2022/04/01/xato-ism-familiyalar-buni-bartaraf-etishni-istaganlarga-soddalashtirilgan-tizim-va-jarayon-kerak)
- Uzbek surname variants Хўжаев → Ходжаев / Hodjaev / Xoʻjayev / Khodjaev. Patronymics oʻgʻli/qizi vs -ovich/-ovna. — [Babel Street](https://www.babelstreet.com/blog/challenges-of-name-matching-in-uzbek)
- Kyrgyz: Жумагулов → Dzhumagulov; Хамид → Khamid vs Hamid. ж, к, ң, ы, ө, ү appear in 3–4 arbitrary variants. — [Kloop.kg 2015](https://kloop.kg/blog/2015/08/11/bektur-iskender-kak-izbezhat-idiotskogo-napisaniya-imeni-v-zagranpasporte/)
- PCGN differs on **Ж**: j (Azerbaijani, Uzbek, Kyrgyz), zh (Kazakh, Tajik), ž (Turkmen), z̵ (Chechen), j (Tatar, Bashkir). ICAO/Russian gives ZH. — PCGN tables: [Aze](https://assets.publishing.service.gov.uk/media/6329af69d3bf7f75cce70557/TABLE_OF_CORRESPONDENCES_FOR_AZERBAIJANI_-_with_examples.pdf), [Uzb](https://assets.publishing.service.gov.uk/media/636cda6dd3bf7f16466f478f/TABLE_OF_CORRESPONDENCES_FOR_UZBEK_2022_final.pdf), [Kir](https://assets.publishing.service.gov.uk/media/621caa11e90e0710c30a4706/ROMANIZATION_KYRGYZ_Feb22_9_.pdf), [Kaz](https://assets.publishing.service.gov.uk/media/621caa32e90e0710b73fd4ff/ROMANIZATION_KAZAKH_Feb_22_19_.pdf), [Tgk](https://assets.publishing.service.gov.uk/media/634e72918fa8f534627a6e60/ROMANIZATION_OF_TAJIK-2022.pdf), [Tuk](https://assets.publishing.service.gov.uk/media/6329b1638fa8f53cb45763b4/TABLE_OF_CORRESPONDENCES_FOR_TURKMEN_with_examples.pdf), [Che](https://assets.publishing.service.gov.uk/media/65b78e360c75e30012d8019c/TABLE_OF_CORRESPONDENCES_FOR_CHECHEN.pdf); [ICAO](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Russia accepts multiple transliterations of the same name as valid. — [Interfax 2024](https://www.interfax.ru/russia/966690)

**Phoneme × writing-system grid** (compiled from the PCGN tables, the national alphabets above and ICAO; each cell is cited in §§1–11):

| Sound | Tr | Az (Lat / Cyr) | Uz 1995 / 2026 / Cyr | Kk Cyr / 2021 | Ky Cyr | Tk Lat / Cyr | Tg Cyr | Tt / Ba Cyr | ULY | Russian-form → ICAO |
|---|---|---|---|---|---|---|---|---|---|---|
| /ʃ/ | ş | ş / ш | sh / ş / ш | ш / ş | ш | ş / ш | ш | ш | sh | Ш → SH |
| /tʃ/ | ç | ç / ч | ch / ç / ч | ч / (tş?) | ч | ç / ч | ч | ч | ch | Ч → CH |
| /dʒ/ | c | c / ҹ | j / j / ж | (ж) | ж (j PCGN) | j / җ | ҷ | җ (Tt) | j | ДЖ → DZH |
| /ʒ/ | j | j / ж | (j) | ж / j | — | ž / ж | ж | ж | zh | Ж → ZH |
| /χ, x/ | h | x / х | x / x / х | х / h | х | h / х | х | х | x | Х → KH |
| /h/ | h | h / һ | h / h / ҳ | һ / h | — | h / х | ҳ | һ | h | Х/Г → KH/G |
| /q/ | k | q / г | q / q / қ | қ / q | к | g,k / г,к | қ | к (Tt q) / ҡ (Ba) | q | К → K |
| /ʁ, ɣ/ | ğ | ğ / ғ | gʻ / ğ / ғ | ғ / ğ | г | g / г | ғ | г (Tt ğ) / ғ (Ba) | gh | Г → G |
| /ŋ/ | n(g) | n(g) | ng / ng / нг | ң / ñ | ң | ň / ң | нг | ң | ng | Н(Г) → N(G) |
| /æ/ | e | ə / ә | a | ә / ä | — | ä / ә | — | ә | e | А/Е/Я → A/E/IA |
| /ø/ | ö | ö / ө | (oʻ) | ө / ö | ө | ö / ө | — | ө | ö | О/Ё → O/E |
| /y/ | ü | ü / ү | (u) | ү / ü | ү | ü / ү | ӯ (/ɵ/) | ү | ü | У/Ю → U/IU |
| /ɯ, ə/ | ı | ı / ы | i | ы / y | ы | y / ы | и | ы | i | Ы → Y |
| /j/ | y | y / ј | y / y / й | й / i | й | ý / й | й | й | y | Й → I |
| /ʊ/ (Kk) | — | — | — | ұ / ū | — | — | — | — | — | У → U |

### Inferences
- **Equivalence axes for variant generation** (bidirectional, weighted; heuristic):
  - `sh ~ ş ~ s(MRZ) ~ sch(de) ~ ch(fr)`
  - `ch ~ ç ~ c(MRZ) ~ tsch(de) ~ tch(fr)`
  - `j ~ dzh ~ dj ~ zh ~ c(tr/az) ~ g(before e/i in Arabic forms)`
  - `zh ~ j ~ ž ~ z`
  - `kh ~ x ~ h ~ ch(de)`
  - `q ~ k ~ g(az) ~ gh`
  - `gh ~ g ~ ğ ~ ∅(tr)`
  - `ng ~ n ~ ñ ~ ň`
  - `yu ~ iu ~ u ~ ü ~ ue`
  - `yo ~ io ~ e ~ o ~ ö ~ oe`
  - `ya ~ ia ~ a ~ ä ~ ə`
  - `ye ~ e ~ ie`
  - `y ~ i ~ ı ~ j(de)`
  - `ə ~ a ~ e ~ ä`
  - `w ~ v ~ u`
  - doubled consonants ~ single (`ss ~ s`, `mm ~ m`, `ll ~ l`)
  - `-iy ~ -ii ~ -i ~ -y`
  - `-yev ~ -ev ~ -yeyev ~ -iev`
  - `-ov ~ -ow ~ -off(fr/de legacy)`
- **Muhammad cluster** (one canonical ID, many surface forms; heuristic, unsourced):
  - Muhammad, Muhammed, Mohammed, Mohammad, Mukhammad, Mukhammed, Muhamed.
  - Magomed, Magomet, Mahomed, Makhammad (Caucasus / Russian-form).
  - Mehmet, Mehmed (Turkish); Məhəmməd, Mahammad (Azerbaijani); Muhammet (Turkish/Turkmen); Mukhamed, Mukhamet (Tatar/Bashkir); Mamed (Az/Ru short form → Mamedov).
  - Muhammadjon, Mamadjon, Mahmadjon, Makhmadzhon (Tajik/Uzbek -jon).
  - Mahmad- (Tajik prefix: Mahmadali).
  - Maimaiti (Uyghur via Chinese).
  - Mahmud/Makhmud (Mahmud) is a **different name**. Link it at low weight only.
- **Other high-frequency clusters to ship (examples):**
  - Abdulla ~ Abdullah ~ Abdullo (Tg) ~ Abdulloh ~ Avdulla ~ Abdyla.
  - Ahmad ~ Ahmed ~ Akhmad ~ Akhmed ~ Ahmet (Tr) ~ Əhməd ~ Akhmat (Chechen) ~ Ahmat ~ Akhmet (Kk) ~ Aihemaiti (Uyghur-pinyin).
  - Hasan ~ Khasan ~ Gasan (Az-Ru) ~ Hassan ~ Həsən ~ Asan (Ky).
  - Husayn ~ Huseyin ~ Hüseyn ~ Guseyn ~ Gusein ~ Khusein ~ Hussein ~ Usein.
  - Ali ~ Əli ~ Aly.
  - Umar ~ Omar ~ Ömer ~ Umar ~ Gumar (Tatar Гумар).
  - Usman ~ Osman ~ Usmon (Tg/Uz) ~ Gusman (Tatar).
  - Yusuf ~ Yusup ~ Iusuf ~ Jusup ~ Yusif (Az) ~ Yusuf.
  - Ibrahim ~ Ibragim ~ Ibrohim ~ İbrahim ~ Ybraýym (Tk) ~ Ibraim.
  - Ismail ~ Ismoil ~ İsmayıl ~ Smail.
  - Ramzan ~ Ramazan ~ Ramadan ~ Ramzon.
  - Hamza ~ Khamza ~ Hamzat ~ Khamzat ~ Gamzat (Dagestan).
  - Shamil ~ Şamil ~ Shamil' ~ Schamil.
  - Fatima ~ Fotima (Uz/Tg) ~ Patimat (Dagestan) ~ Fatma (Tr) ~ Fatimə.
  - Khadija ~ Xadicha (Uz) ~ Xədicə (Az) ~ Khadizhat (Caucasus) ~ Hatice (Tr) ~ Khadicha.
  - Aisha ~ Oysha (Uz) ~ Ayşe (Tr) ~ Aishat (Caucasus) ~ Ayşə.
  - Zaynab ~ Zeynep (Tr) ~ Zeynəb (Az) ~ Zainab ~ Zaynab ~ Zeynab.
  - Gulnara ~ Gulnora (Uz) ~ Gülnarə (Az) ~ Gulnar.
  - Khurshid ~ Xurshid ~ Hurshid ~ Khurşid ~ Hurşit (Tr).
- **Patronymic/kinship markers** (detect, then strip or keep as a separate field). Uzbek and Azerbaijani forms are cited above; the others are unsourced here:
  - Uzbek: oʻgʻli / qizi (Cyr ўғли/қизи; Russian-form угли/кизи; English ugli, ogli, o'g'li, qizi, kizi).
  - Azerbaijani: oğlu / qızı (Russian оглы / кызы; English oglu, ogly, gizi, kyzy).
  - Kazakh: ұлы / қызы (uly / qyzy, kyzy).
  - Kyrgyz: уулу / кызы (uulu / kyzy).
  - Turkmen: ogly / gyzy.
  - Tatar: улы / кызы.
  - Bashkir: улы / ҡыҙы.
  - Russian: -ович/-евич/-ич, -овна/-евна/-ична.
- **Surname affix classes** for suffix-insensitive matching:
  - Russian: -ov/-ev/-ova/-eva/-in/-ina.
  - Turkmen: -ow/-owa.
  - Tajik: -zoda/-zod/-zade, -ī/-i/-iy, -iyon/-yon/-on, -far, -pur.
  - Azerbaijani: -zadə/-zade, -li/-lı/-lu/-lü/-ly, -bəyli/-beyli, -oğlu as a surname.
  - Kazakh/Kyrgyz: -uly/-uulu/-qyzy/-kyzy as surnames.
  - Russified Arabic stems: Magomed-ov, Gadzhi-ev.

### Gaps
- I found no corpus-based frequencies to weight these variants. Real weights should come from data (e.g., sanctions lists, sports rosters, Wikidata labels).

---

## 13. Implementation synthesis for `translit-names` (Unicode/Python pitfalls, profiles, language detection, test vectors)

### Takeaway
Use explicit per-language mapping tables, not generic Unicode folding. NFKD+strip misses `ı`, `ə`, `ʻ`/`ʼ` and all the Cyrillic extensions, and Python casing breaks Turkish İ/ı. Offer several output **profiles**:
- `icao_strict`
- `passport_<country>` (best guess, documented confidence)
- `ru_mvd` (Russian-form names)
- `bgn_pcgn_<lang>`
- `national_latin_<lang>[_year]`
- `english_phonetic`

Generate variants by combining profiles with the equivalence axes in §12.

### Cited Findings
- Python's default casing is not Turkish-aware (`"İ".lower()` → `i̇`; `"I".lower()` → `i`), and NFKD does not decompose `ı` or `ə`. *Local verification, Python 3.9.6, unicodedata 13.0.0 (§2).*
- Uzbek apostrophe code points: U+02BB (proper oʻ/gʻ), U+02BC (tutuq). In practice U+2018, U+2019 and U+0027 are used instead. — [Wikipedia: Uzbek alphabet](https://en.wikipedia.org/wiki/Uzbek_alphabet)
- Azerbaijani schwa must be U+018F/U+0259 in Latin. Cyrillic U+04D8/U+04D9 look identical but are different characters. Ä is an acceptable substitute. — [PCGN Azerbaijani](https://assets.publishing.service.gov.uk/media/6329af69d3bf7f75cce70557/TABLE_OF_CORRESPONDENCES_FOR_AZERBAIJANI_-_with_examples.pdf)
- Azerbaijani Cyrillic uses **Ј ј (U+0408)** for /j/ (→ y). ICAO maps U+0408 to **J** (the Serbian/Macedonian value). — [PCGN Azerbaijani](https://assets.publishing.service.gov.uk/media/6329af69d3bf7f75cce70557/TABLE_OF_CORRESPONDENCES_FOR_AZERBAIJANI_-_with_examples.pdf); [ICAO §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- PCGN Turkmen notes legacy look-alike characters (¥/ÿ → ý, £/ſ → ž, ñ → ň) that appear in 1993–1999 data. — [PCGN Turkmen](https://assets.publishing.service.gov.uk/media/6329b1638fa8f53cb45763b4/TABLE_OF_CORRESPONDENCES_FOR_TURKMEN_with_examples.pdf)
- People in Turkey and Azerbaijan often type the digit `1` for `ı`. — [Wikipedia: Dotted and dotless I in computing](https://en.wikipedia.org/wiki/Dotted_and_dotless_I_in_computing)

### Inferences
**A. Pre-normalization pipeline (proposed)**
1. NFC normalize. Map compatibility look-alikes:
   - Latin Ә-look-alikes Ə/ə (U+018F/U+0259) vs Cyrillic Ә/ә (U+04D8/U+04D9): choose by the script of the surrounding letters.
   - Ꞑ → ñ.
   - Ɵ/ɵ (U+019F/U+0275) → ö.
   - Turkmen legacy ¥ ÿ £ ſ $ ¢.
   - Uzbek apostrophe zoo → U+02BB/U+02BC (§4).
   - Palochka look-alikes in Cyrillic context → U+04C0 (§10).
   - In a word that is otherwise Cyrillic, convert Latin homoglyphs (a, c, e, o, p, x, y, A, B, C, E, H, K, M, O, P, T, X, Y) to Cyrillic, and the reverse. Mixed-script tokens are common in scanned or OCR data.
2. Script and language detection (token-level, with an optional user-supplied language hint):
   - **Latin**:
     - `ə/Ə` → az.
     - `oʻ/gʻ` or `o'/g'` → uz.
     - `ý ž ň ä` → tk.
     - `ū` or `ñ` with `ä/ğ/ş` → kk-2021.
     - `á ǵ ń ó ú` (acute set) → kk-2018 or kaa.
     - `ı İ ş ç ğ ö ü` without `ə`/`x`/`q` → tr.
     - with `x` or `q` → az.
     - `ë` with gh/zh/ng digraphs → ug (ULY).
   - **Cyrillic**:
     - `Ӏ` → ce/inh/av (Caucasus).
     - `ў` with `қ ғ ҳ` → uz.
     - `ӣ ӯ ҷ` → tg.
     - `ә ғ қ ң ө ұ ү һ і` (especially `ұ` or `і`) → kk.
     - `ң ө ү` only → ky.
     - `ҙ ҫ ҡ` → ba.
     - `җ` with `ә ө ү ң һ` → tt (or tk-Cyrillic if `җ` with `ң` and no `һ`; ambiguous).
     - `ҹ ҝ ј` with `ә` → az-Cyrillic.
     - otherwise ru.
3. Case handling: Turkish/Azerbaijani-aware case mapping (`İ↔i`, `I↔ı`) whenever tr/az/kk-2021/tt-Latin is detected, before ASCII folding.

**B. Output profiles (proposed). Each is a dict per language; pass `profile=` to select.**

| Profile | Purpose | Key behaviours |
|---|---|---|
| `icao_strict` | MRZ simulation | ICAO 6.A/6.B literally. For letters ICAO omits, use the per-language fallback table (Ə→A, Ә→A, Қ→K, Ң→N, Ө→O, Ұ→U, Ү→U, Ҳ→H, Ҷ→J, Ӣ→I, Ӯ→U, Җ→ZH, Ҙ→Z, Ҫ→S, Ҡ→K, Ӏ→∅). Optionally `Һ→C` (literal ICAO) vs `H` (recommended). Ü→U by default; flags for `UE`/`UXX`, `OE`, `AE`, `NXX`. Uppercase A–Z and `<`. |
| `ru_mvd` | Russian-form Cyrillic names (Russia; also Soviet-era docs of all states) | MVD 996 table (Й→I, Ю→IU, Я→IA, Ъ→IE, Ь→∅, Ё→E). Variant flag for the pre-2014 style (Y/YU/YA). |
| `passport_tr` | Turkish | ICAO simple (O, U). Alt OE/UE. |
| `passport_az` | Azerbaijani | Ə→A (alt E per the l/m/n/r/y rule). X→KH (evidence: ORKHAN). Ü→U, Ö→O, Ş→SH?, Ç→CH?, Q→? (low confidence; generate Q and G). |
| `passport_uz` | Uzbek | Two candidates: (1) Uzbek Latin stripped (Oʻ→O, Gʻ→G, X stays X, Q stays Q). (2) English style (X→KH, Gʻ→GH, Oʻ→O/U, J→J). |
| `passport_kz` | Kazakh | Russian/ICAO-like with Kazakh letters folded (Ә→A, Ғ→G, Қ→K, Ң→N, Ө→O, Ұ/Ү→U, Һ→H, І→I). Ye- for initial Е, Zh, Kh, YU/YA common. Optional `ss` intervocalic. Low confidence. |
| `passport_kg` | Kyrgyz | Same as kz-like, with Ж→ZH (alt J). Applicant choice since Resolution 651 (2026), so variants are essential. |
| `passport_tm` | Turkmen | ICAO fold of the national Latin (Ý→Y, Ž→Z, Ň→N, Ä→A, Ç→C, Ş→S); alt English (SH/CH/ZH). Low confidence. |
| `passport_tj` | Tajik | English-style from Cyrillic (Ғ→GH, Қ→Q, Ҳ→H, Ҷ→J, Ӣ→I, Ӯ→U, Х→KH). Alt Russian/ICAO (Ҷ→DZH via Дж). Low confidence. |
| `bgn_pcgn_<lang>` | Gazetteer-style, reversible-ish | Tables in §§3–11 verbatim (with diacritics). `ascii=True` folds diacritics. |
| `national_latin_<lang>` | Native Latin | az (1992); uz_1995, uz_2026; kk_2017, kk_2018, kk_2021; tk_1999; kaa; tt_zamanalif; ug_uly. |
| `english_phonetic` | Human-friendly English | SH/CH/KH/ZH/GH/J/Y; Ye-/Yu/Ya; ı→I; ə→A/E; ü→U; ö→O. |

**C. Matching key (proposed, lossy).** After ASCII folding, uppercase and:
- `KH|X|H → H`
- `DZH|DJ|ZH|J|C(tr/az) → J`
- `SH|SCH → S`
- `CH|TSCH|TCH → C`
- `GH|Q|K|G → K`, with an optional coarser `G≈K` level
- `YU|IU → U`
- `YA|IA → A`
- `YO|IO → O`
- `YE → E` at word start
- `OE → O`, `UE → U`, `AE → A`
- `Y|I|J(de) → I` as vowels
- `W|V → V`
- collapse double letters
- strip `'ʻʼ‘’`
- normalize the suffix set `{OV, EV, YEV, IEV, OW}` → `OV`, `{OVA, EVA, OWA}` → `OVA`, and `{ZODA, ZADE, ZADA, ZOD}` → `ZADE`
- remove patronymic markers and particles

Compare keys token by token, order-insensitively, and use edit distance on the keys for the remaining differences.

**D. Test vectors (expected outputs; derived from the cited tables).**

| Input | Lang | Profile | Expected |
|---|---|---|---|
| Şükrü Çağlar | tr | icao_strict | SUKRU CAGLAR |
| Şükrü | tr | icao_strict (OE/UE flag) | SUEKRUE |
| İsmail Işık | tr | icao_strict | ISMAIL ISIK |
| Məmmədov Orxan | az | passport_az | MAMMADOV ORKHAN (alt MEMMEDOV / ORXAN) |
| Hüseynli | az | passport_az | HUSEYNLI |
| Ҝәнҹә (Cyrillic Az) | az-Cyrl | national_latin_az | Gəncə |
| Xoʻjayev | uz | passport_uz | XOJAYEV; KHOJAYEV; KHODJAEV (ru_mvd via Ходжаев) |
| Ўринов | uz-Cyrl | icao_strict | URINOV (ICAO Ў=U); national: Oʻrinov → ORINOV |
| Мирзиёев | uz-Cyrl | ru_mvd | MIRZIEEV; national: Mirziyoyev |
| Ғафурова | uz-Cyrl | national_latin_uz_1995 / 2026 | Gʻafurova / Ğafurova → GAFUROVA / GHAFUROVA |
| Нұрсұлтан | kk | all | NURSULTAN |
| Әлия | kk | passport_kz | ALIYA (alt ALIIA, ÄLIYA) |
| Жапаров | ky | bgn_pcgn_ky | Japarov (ICAO: ZHAPAROV) |
| Ниязов / Nyýazow | tk | icao_strict | NIIAZOV / NYYAZOW; english: NIYAZOV |
| Ҷамшед Раҳмонов | tg | bgn_pcgn_tg | Jamshed Rahmonov; ru_mvd via Джамшед Рахмонов → DZHAMSHED RAKHMONOV |
| Шамиль | ru (Caucasus) | ru_mvd | SHAMIL |
| Хамзат | ru | ru_mvd | KHAMZAT |
| ХӀасан / Хlасан | ce | normalize→ХӀасан; bgn_pcgn_ce | hasan; ru_mvd (palochka dropped) → KHASAN |
| Гыйльмиев | tt | bgn_pcgn_tt | Ğilmiev; Russian form Гильмиев → GILMIEV |
| Ilham Tohti | ug | uyghur_cn_pinyin (dictionary) | YILIHAMU TUHETI |

**E. Packaging notes.**
- Ship the tables as data files (YAML/JSON) keyed by code point. Keep `source` and `as_of` fields per table, e.g., `pcgn_uzb_2000 (checked 2022-11)`, `uz_2026_law (senate 2026-09-10, unsigned?)`, `kk_2021_04`, `icao_9303_p3_2021`, `ru_mvd_996_2019`.
- Each output variant should carry a `confidence`/`weight` and a `provenance` tag, e.g., `observed_passport`, `official_table`, `heuristic`.
- Make the Uzbek alphabet year a parameter so that the 2026 Ş/Ç/Ö/Ğ letters are accepted on input now and can become the default once the law is in force.

### Gaps
- Several `passport_*` profiles (az, uz, kz, kg, tm, tj) rest on thin or indirect evidence. Before claiming "passport-accurate" output, validate them against real MRZ samples, e.g., PRADO specimen pages (blocked to automated fetch here) or the Keesing/Regula document libraries.
- I did not research Python library options (PyICU `Transliterator` with `tr`/`az` casing rules, `unidecode` behaviour for ə/ı/ʻ). Benchmark them against the tables above.
