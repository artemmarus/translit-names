# South Slavic Cyrillic, Latin-script Slavic name romanization, and ICAO Doc 9303 name rules (status: October 2026)

Scope: Bulgarian, Serbian, Macedonian and Montenegrin Cyrillic; Polish, Czech, Slovak, Croatian, Bosnian, Slovene and Serbian Latin diacritics; ICAO Doc 9303 general name rules plus the complete Latin, Cyrillic and Arabic tables from Doc 9303 Part 3. These are working notes for the `translit-names` Python package. Tables are written to be lifted into package data.

Primary documents I downloaded and text-extracted, quoted below:
- ICAO Doc 9303 Part 3 (8th ed., 2021, consolidated with Amendments 1–2): https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf. The old URL `icao.int/publications/Documents/9303_p3_cons_en.pdf` now returns 404.
- ICAO Doc 9303 Part 4 (TD3/passports, consolidated with Amendment 2 of 20/2/26): https://www.icao.int/sites/default/files/publications/DocSeries/9303_p4_cons_en.pdf
- ICAO Doc 9303 Part 5 (TD1 cards): https://www.icao.int/sites/default/files/publications/DocSeries/9303_p5_cons_en.pdf
- Bulgarian Transliteration Act (text copy of ДВ бр. 19/2009): https://annual-ct.eu/bg/wp-content/uploads/2024/05/zakon_za_transliteraciata.pdf. The official lex.bg page (https://lex.bg/laws/ldoc/2135623094) returned errors.
- Bulgarian Regulation for Issuing Bulgarian Personal Documents (ПМС 13/2010, consolidated to ДВ 70/2016): https://www.mfa.bg/upload/648/08-Pr-ZBLD-bg.pdf

---

## Q1. ICAO Doc 9303: current edition (2026) and general rules for names (VIZ, MRZ, separators, punctuation, truncation)

### Takeaway
Doc 9303 is still the **Eighth Edition (2021)**. As of 2026 it is maintained by per-Part amendments, and I found no evidence of a 9th edition. In the MRZ, names use only A–Z and the filler `<`. The primary identifier is followed by `<<`. Name components are separated by a single `<`. Hyphens and commas between components become `<`. Apostrophes and all other punctuation are deleted with no filler. The TD3 (passport) name field is 39 characters and the TD1 (ID card) name field is 30. When a name is truncated, the field must end with a letter, and any name that fills the field exactly must be treated as possibly truncated. The VIZ may carry diacritics and the Latin national characters listed in Section 6.A.

### Cited Findings
**Edition and amendment status**
- Part 3 title page: "Doc 9303, Machine Readable Travel Documents, Eighth Edition, 2021, Part 3: Specifications Common to all MRTDs". Its record of amendments lists No. 1 dated 14/11/22 and No. 2 dated 20/3/24. — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Part 4 (passports) is also "Eighth Edition, 2021". Its record lists Amendment 1 dated 20/3/24 and Amendment 2 dated 20/2/26. The name-example pages (pp. 22–23) carry the marker "20/2/26 No. 2". — [ICAO Doc 9303 Part 4](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p4_cons_en.pdf)
- ICAO's 2026 catalogue supplement lists: Part 4 Amendment 2 (Specifications for MRPs), Part 8 Amendment 2 (Emergency Travel Documents, 6/2/26) and Part 11 Amendment 2 (Security Mechanisms, 23/2/26). It does not announce a new edition. — [ICAO catalogue 2026 supplement 04](https://www.icao.int/sites/default/files/publications/catalogue/cat_2026_sup04_en.pdf)
- **2026 change relevant to MRZ generation (Part 4 §4.4, "Document Codes")**: positions 1–2 of the passport MRZ now carry a harmonized second letter. The codes are PP national/ordinary, PE emergency, PD diplomatic, PO official/service, PR refugee, PT alien/non-citizen, PS stateless, PL laissez-passer and PM military, plus PU for single-sheet documents (Doc 9303-8). The schedule is: "Effective 1 January 2026, MRPs issued with a secondary document code shall be in accordance with Section 4.4"; "Effective 1 January 2028, all MRPs shall be issued with a secondary document code"; MRPs without a harmonized code "shall expire before 1 January 2038". The amended examples now start `PPUTO…` instead of `P<UTO…`. The accompanying note still reads "PP<UTO", which looks like an editorial slip because `PPUTO` is the five-character form. — [ICAO Doc 9303 Part 4](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p4_cons_en.pdf)

**VIZ rules (Part 3 §3.1, §3.4)**
- §3.1: "Latin-alphabet characters, i.e. A to Z and a to z, and Arabic numerals … shall be used to represent data in the VIZ. Diacritics are permitted. Latin-based national characters listed in Section 6.A … e.g. Þ and ẞ, may also be used in the VIZ without transliteration. When mandatory data elements are in a language that does not use the Latin alphabet, a transcription or transliteration shall also be provided." — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- §3.4: the name has a **primary identifier** and a **secondary identifier**. The issuing State decides which part is primary; it may be the family name, maiden name, married name, main name, surname, or the entire name when the name cannot be divided. Upper case is recommended, "except in the case of a prefix, e.g. 'von,' 'Mc' or 'de la,'", where mixed case is appropriate. The secondary identifier covers forenames, given names, initials and similar. In a single VIZ name field the two identifiers are separated by "a single comma (,)". Prefixes and suffixes (titles, qualifications, honours, hereditary status) should not appear unless the State considers them legally part of the name, in which case they go in the secondary identifier. Numerals should not appear; where a numeric naming convention is legal it is written in Roman numerals. "National characters may be used in the VIZ. If the national characters are not Latin-based, a transcription or transliteration into Latin characters shall be provided." — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

**MRZ rules (Part 3 §4.6)**
- MRZ names "shall be printed using upper-case OCR-B characters … without diacritical marks". The issuing State "shall transliterate national characters using only the allowed OCR-B characters and/or truncate". Section 6 supplies the tables for Latin, Cyrillic and Arabic. — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- "The primary identifier shall be followed by two filler characters (<<)". The secondary identifier starts at the next position. Multiple components within either identifier are separated by "a single filler character (<)". Filler `<` runs from after the last name component to the end of the field. "In all other cases [i.e. unless the field overflows], the name shall not be truncated." — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Prefixes and suffixes "(such as Dr., Sir, Jr., Sr., II and III) shall not be included in the MRZ except where the issuing State considers these to be legally part of the name". In that case they are components of the secondary identifier. "Numeric characters shall not be used in the name fields of the MRZ." — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Punctuation, quoted rule by rule:
  - Apostrophe: "This shall be omitted; name components separated by the apostrophe shall be combined, and no filler character shall be inserted". Example: VIZ `D'ARTAGNAN` → MRZ `DARTAGNAN`.
  - Hyphen: represented "by a single filler character (<)". Example: `MARIE-ELISE` → `MARIE<ELISE`.
  - Comma separating primary from secondary identifier: omitted and replaced by `<<`. Example: `ERIKSSON, ANNA MARIA` → `ERIKSSON<<ANNA<MARIA`.
  - Any other comma: a single `<`. Example: `ANNA, MARIA` → `ANNA<MARIA`.
  - "All other punctuation characters shall be omitted … (i.e. no filler character shall be inserted…)".
  
  — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Appendix B: the MRP name field has 39 positions "and only the OCR-B subset of A-Z and < may be used". National characters "shall not, therefore, appear in the MRZ". — [ICAO Doc 9303 Part 3, App. B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Appendix B §B.4.1: "Most of the national characters have their diacritical marks omitted… There are a group of nine characters that are treated specially, for example, the character 'Ñ' can be transliterated into the MRZ as 'NXX'". Example: `Térèsa CAÑON` → `CANXXON<<TERESA`. — [ICAO Doc 9303 Part 3, App. B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

**TD3 passport name field and truncation (Part 4 §4.2.2–4.2.3)**
- Line 1 positions 6–44 = 39 characters. If all components plus separators fit in 39 characters, every component is included and the rest is filled with `<` to position 44. — [ICAO Doc 9303 Part 4](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p4_cons_en.pdf)
- Truncation rule, quoted: "Characters shall be removed from one or more components of the primary identifier until three character positions are freed, and two filler characters (<<) and the first character of the first component of the secondary identifier can be inserted. The last character (position 44) shall be an alphabetic character (A through Z). This indicates that truncation may have occurred. Further truncation of the primary identifier may be carried out to allow characters of the secondary identifier to be included, provided that the name field shall end with an alphabetic character". Also: "Where long names extend to the last character position in the name field, the presence of an alphabetic character means that the name must be treated as though truncation had occurred." — [ICAO Doc 9303 Part 4](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p4_cons_en.pdf)
- Official TD3 examples, copied exactly from the Amendment-2 text:

| Case | VIZ | MRZ line 1 |
|---|---|---|
| usual | ERIKSSON, ANNA MARIA | `PPUTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<` |
| central primary | HENG, DEBORAH MING LO | `PPUTOHENG<<DEBORAH<MING<LO<<<<<<<<<<<<<<<<<<` |
| hyphen | SMITH-JONES, SUSIE MARGARET | `PPUTOSMITH<JONES<<SUSIE<MARGARET<<<<<<<<<<<<` |
| apostrophe | O'CONNOR, ENYA SIOBHAN | `PPUTOOCONNOR<<ENYA<SIOBHAN<<<<<<<<<<<<<<<<<<` |
| multi-component | VAN DER MUELLEN, MARTIN | `PPUTOVAN<DER<MUELLEN<<MARTIN<<<<<<<<<<<<<<<<` |
| Arabic article | AL-BASRI, HUDA MUHAMMAD JAWAD | `PPUTOAL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<<<<<<<` |
| two surnames | VILARCHAO FERNANDEZ, JOSE RAMON | `PPUTOVILARCHAO<FERNANDEZ<<JOSE<RAMON<<<<<<<<` |
| no secondary | ARKFREITH | `PPUTOARKFREITH<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<` |
| no secondary, 2 comps | SATRIYA SUDARPA | `PPUTOSATRIYA<SUDARPA<<<<<<<<<<<<<<<<<<<<<<<<` |
| secondary → initials | NILAVADHANANANDA, CHAYAPA DEJTHAMRONG KRASUANG | `PPUTONILAVADHANANANDA<<CHAYAPA<DEJTHAMRONG<K` |
| secondary truncated | NILAVADHANANANDA, ARNPOL PETCH CHARONGUANG | `PPUTONILAVADHANANANDA<<ARNPOL<PETCH<CHARONGU` |
| primary → initials | BENNELONG WOOLOOMOOLOO WARRANDYTE WARNAMBOOL, DINGO POTOROO | `PPUTOBENNELONG<WOOLOOMOOLOO<WARRANDYTE<W<<DI` |
| primary truncated | (same) | `PPUTOBENNELONG<WOOLOOM<WARRAND<WARNAM<<DINGO` |
| primary fixed-length | (same) | `PPUTOBENNEL<WOOLOO<WARRAN<WARNAM<<DINGO<POTO` |
| exact fit, not truncated | PAPANDROPOULOUS, JONATHON WARREN TREVOR | `PPUTOPAPANDROPOULOUS<<JONATHON<WARREN<TREVOR` (must still be assumed possibly truncated) |

  — [ICAO Doc 9303 Part 4](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p4_cons_en.pdf)

**TD1 (ID-card) name field (Part 5)**
- The name occupies line 3, 30 characters. Truncation follows the same idea, and the "following methods provide a number of options available for use at the discretion of the issuing State". Examples:
  - `NILAVADHANANANDA<<CHAYAPA<DE<K`
  - `BENNELONG<WOOLOOMOOLOO<W<W<<DI`
  - `BENNE<WOOLO<WARRA<WARNA<<DIN<P`
  - exact fit: `PAPANDROPOULOUS<<JONATHON<ALEC`
  
  — [ICAO Doc 9303 Part 5](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p5_cons_en.pdf)

### Inferences
- Name-to-MRZ pipeline that follows from §4.6:
  1. Map national characters with Section 6 (or the national table).
  2. Uppercase.
  3. Delete apostrophes and other punctuation, joining the pieces.
  4. Turn hyphens, spaces and non-separator commas into `<`.
  5. Collapse runs (an implementation choice, so "A - B" does not produce `<<<`).
  6. Join primary and secondary with `<<`.
  7. Pad with `<` to 39 (TD3) or 30 (TD1).
  8. If the result is too long, truncate per Part 4/5, keeping the last character alphabetic.
- Truncation is not deterministic: ICAO gives several equally valid methods. The package should expose a strategy parameter (`initials`, `truncate_components`, `fixed_length`). Matching code should treat any name that ends exactly at the field boundary as a prefix match.
- The Part 4 Amendment 2 (2026) document-code change (P< → PP and the others) affects MRZ generation and parsing but not name transliteration.

### Gaps
- I did not read the TD2 (Part 6) or visa (Part 7) name-field lengths in the primary text. They are commonly 31 (TD2/MRV-B) and 39 (MRV-A), but this is unverified here.
- The full list of the "nine characters treated specially" (App. B §B.4.1) is not printed as a list. From Section 6.A the multi-letter or alternative forms are Ä, Å, Æ, Ñ, Ö, Ø, Ü, Þ, Ĳ, Œ and ẞ; which nine ICAO means is not stated.
- I did not check for an ICAO TAG/TRIP working paper proposing a new transliteration table after 2024.

---

## Q2. ICAO Doc 9303 Part 3, Section 6.A — "Transliteration of Multinational Latin-based Characters" (complete, verbatim)

### Takeaway
The table is upper-case only and has 92 rows, ending at U+017D plus U+1E9E. Almost every letter maps to its base letter. The exceptions are Ä→AE/A, Å→AA/A, Æ→AE, Ñ→N/NXX, Ö→OE/O, Ø→OE, Ü→UE/UXX/U, Þ→TH, Ĳ→IJ, Œ→OE and ẞ→SS. Ð (Eth) and Đ (D stroke) both map to **D**. Ł maps to L. The table does **not** cover Ə, Ș/Ț (comma-below), Ǆ/Ǉ/Ǌ digraph code points, Ǵ/Ḱ, Vietnamese letters, or combining sequences.

### Cited Findings
Verbatim rows from Doc 9303 Part 3 §6.A (columns: Unicode, national character, description, recommended transliteration) — [ICAO Doc 9303 Part 3 §6.A](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf):

| Unicode | Char | Description | MRZ |
|---|---|---|---|
| 00C0 | À | A grave | A |
| 00C1 | Á | A acute | A |
| 00C2 | Â | A circumflex | A |
| 00C3 | Ã | A tilde | A |
| 00C4 | Ä | A diaeresis | AE or A |
| 00C5 | Å | A ring above | AA or A |
| 00C6 | Æ | ligature AE | AE |
| 00C7 | Ç | C cedilla | C |
| 00C8 | È | E grave | E |
| 00C9 | É | E acute | E |
| 00CA | Ê | E circumflex | E |
| 00CB | Ë | E diaeresis | E |
| 00CC | Ì | I grave | I |
| 00CD | Í | I acute | I |
| 00CE | Î | I circumflex | I |
| 00CF | Ï | I diaeresis | I |
| 00D0 | Ð | Eth | D |
| 00D1 | Ñ | N tilde | N or NXX |
| 00D2 | Ò | O grave | O |
| 00D3 | Ó | O acute | O |
| 00D4 | Ô | O circumflex | O |
| 00D5 | Õ | O tilde | O |
| 00D6 | Ö | O diaeresis | OE or O |
| 00D8 | Ø | O stroke | OE |
| 00D9 | Ù | U grave | U |
| 00DA | Ú | U acute | U |
| 00DB | Û | U circumflex | U |
| 00DC | Ü | U diaeresis | UE or UXX or U |
| 00DD | Ý | Y acute | Y |
| 00DE | Þ | Thorn (Iceland) | TH |
| 0100 | Ā | A macron | A |
| 0102 | Ă | A breve | A |
| 0104 | Ą | A ogonek | A |
| 0106 | Ć | C acute | C |
| 0108 | Ĉ | C circumflex | C |
| 010A | Ċ | C dot above | C |
| 010C | Č | C caron | C |
| 010E | Ď | D caron | D |
| 0110 | Đ (printed with the Ð glyph) | D stroke | D |
| 0112 | Ē | E macron | E |
| 0114 | Ĕ | E breve | E |
| 0116 | Ė | E dot above | E |
| 0118 | Ę | E ogonek | E |
| 011A | Ě | E caron | E |
| 011C | Ĝ | G circumflex | G |
| 011E | Ğ | G breve | G |
| 0120 | Ġ | G dot above | G |
| 0122 | Ģ | G cedilla | G |
| 0124 | Ĥ | H circumflex | H |
| 0126 | Ħ | H stroke | H |
| 0128 | Ĩ | I tilde | I |
| 012A | Ī | I macron | I |
| 012C | Ĭ | I breve | I |
| 012E | Į | I ogonek | I |
| 0130 | İ | I dot above | I |
| 0131 | ı (printed as "I") | I without dot (Turkey) | I |
| 0132 | Ĳ | ligature IJ | IJ |
| 0134 | Ĵ | J circumflex | J |
| 0136 | Ķ | K cedilla | K |
| 0139 | Ĺ | L acute | L |
| 013B | Ļ | L cedilla | L |
| 013D | Ľ | L caron | L |
| 013F | Ŀ | L middle dot | L |
| 0141 | Ł | L stroke | L |
| 0143 | Ń | N acute | N |
| 0145 | Ņ | N cedilla | N |
| 0147 | Ň | N caron | N |
| 014A | Ŋ | Eng | N |
| 014C | Ō | O macron | O |
| 014E | Ŏ | O breve | O |
| 0150 | Ő | O double acute | O |
| 0152 | Œ | ligature OE | OE |
| 0154 | Ŕ | R acute | R |
| 0156 | Ŗ | R cedilla | R |
| 0158 | Ř | R caron | R |
| 015A | Ś | S acute | S |
| 015C | Ŝ | S circumflex | S |
| 015E | Ş | S cedilla | S |
| 0160 | Š | S caron | S |
| 0162 | Ţ | T cedilla | T |
| 0164 | Ť | T caron | T |
| 0166 | Ŧ | T stroke | T |
| 0168 | Ũ | U tilde | U |
| 016A | Ū | U macron | U |
| 016C | Ŭ | U breve | U |
| 016E | Ů | U ring above | U |
| 0170 | Ű | U double acute | U |
| 0172 | Ų | U ogonek | U |
| 0174 | Ŵ | W circumflex | W |
| 0176 | Ŷ | Y circumflex | Y |
| 0178 | Ÿ | Y diaeresis | Y |
| 0179 | Ź | Z acute | Z |
| 017B | Ż | Z dot above | Z |
| 017D | Ž | Z caron | Z |
| 1E9E | ẞ | double s (Germany) | SS |

- Secondary-source conflict: English Wikipedia lists "ð → DH" as a permitted alternative and gives German/Nordic examples such as Gößmann → GOESSMANN. The ICAO table itself gives **Ð (00D0) → D**, with no DH alternative. — [Wikipedia: Machine-readable passport](https://en.wikipedia.org/wiki/Machine-readable_passport); contradicted by [ICAO Doc 9303 Part 3 §6.A](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

### Inferences
- **Letters missing from the ICAO table that the package must handle explicitly**:
  - Ə/ə (U+018F/0259, Azerbaijani; commonly A)
  - Ș/Ț comma-below (U+0218/021A, Romanian; map to S/T like the cedilla forms)
  - Ǆ ǅ ǆ Ǉ ǈ ǉ Ǌ ǋ ǌ (U+01C4–01CC; NFKD → D+Ž etc. → DZ/LJ/NJ)
  - Ǵ/Ḱ (Macedonian scholarly; G/K, or GJ/KJ to match passports)
  - Uzbek ʻ (U+02BB) in Oʻ/Gʻ: punctuation-like, so ICAO "other punctuation" → omit
  - Vietnamese Ơ/Ư and stacked diacritics: NFD-strip
  - lowercase ß: Python `str.upper()` already gives "SS"
  - Turkish dotless ı: map to I before uppercasing; Python `'ı'.upper()` = 'I', which is fine
- Unicode NFD/NFKD stripping is **not sufficient**. Ł, Đ, Ð, Ø, Æ, Œ, Þ, ß/ẞ, Ħ, Ŧ, Ŋ and ı have no canonical decomposition to base letter + combining mark. A practical design is: explicit table first (ICAO rows plus the extras above), then NFKD-and-strip-combining-marks as a fallback, then reject anything outside A–Z.
- Package data should store the ICAO alternatives as ordered lists, for example `"Ä": ["AE", "A"]`, `"Ü": ["UE", "UXX", "U"]`, `"Ñ": ["N", "NXX"]`. That lets a "German-style" profile and a "plain" profile share one table, and lets name matching generate every variant.

### Gaps
- ICAO publishes no lowercase rows. Lowercase must be uppercased first. That is safe for every row except U+0131 ı and the İ/i Turkish casing issue.

---

## Q3. ICAO Doc 9303 Part 3, Section 6.B — "Transliteration of Cyrillic Characters" (complete, verbatim, with errata)

### Takeaway
The ICAO Cyrillic table is a Russian-centred default with per-language exceptions. Its Bulgarian, Serbian and Macedonian entries contain several errors and gaps:
- Serbian Г is given as H.
- Code 0402 is printed with the Ћ glyph.
- Macedonian GJ is attached to Ғ (0492) instead of Ѓ (0403).
- Ь, Ѓ and Ћ (040B) are missing.

Bulgaria and North Macedonia issue passports from national tables. Serbia and Montenegro use Gaj's Latin in the VIZ. Implementers should use national tables and keep ICAO as a fallback.

### Cited Findings
Verbatim rows from Doc 9303 Part 3 §6.B (columns: Unicode, national character, recommended transliteration). Glyph and code checks were done on the PDF text layer — [ICAO Doc 9303 Part 3 §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf):

| Unicode (as printed) | Char (as printed) | Recommended transliteration (verbatim) |
|---|---|---|
| 0401 | Ё | E (except Belorussian = IO) |
| 0402 | Ћ (**glyph is U+040B; code 0402 is actually Ђ**) | D |
| 0404 | Є | IE (except if Ukrainian first character, then =YE) |
| 0405 | Ѕ | DZ |
| 0406 | І | I |
| 0407 | Ї | I (except if Ukrainian first character, then =YI) |
| 0408 | Ј | J |
| 0409 | Љ | LJ |
| 040A | Њ | NJ |
| 040C | Ќ | K (except in the language spoken in the former Yugoslav Republic of Macedonia = KJ) |
| 040E | ў (lower-case glyph U+045E printed) | U |
| 040F | Џ | DZ (except in the language spoken in the former Yugoslav Republic of Macedonia = DJ) |
| 0410 | А | A |
| 0411 | Б | B |
| 0412 | В | V |
| 0413 | Г | G (except Belorussian, Serbian, and Ukrainian = H) |
| 0414 | Д | D |
| 0415 | Е | E |
| 0416 | Ж | ZH (except Serbian = Z) |
| 0417 | З | Z |
| 0418 | И | I (except Ukrainian = Y) |
| 0419 | Й | I (except if Ukrainian first character, then =Y) |
| 041A | К | K |
| 041B | Л | L |
| 041C | М | M |
| 041D | Н | N |
| 041E | О | O |
| 041F | П | P |
| 0420 | Р | R |
| 0421 | С | S |
| 0422 | Т | T |
| 0423 | У | U |
| 0424 | Ф | F |
| 0425 | Х | KH (except Serbian and in the language spoken in the former Yugoslav Republic of Macedonia = H) |
| 0426 | Ц | TS (except Serbian and in the language spoken in the former Yugoslav Republic of Macedonia = C) |
| 0427 | Ч | CH (except Serbian = C) |
| 0428 | Ш | SH (except Serbian = S) |
| 0429 | Щ | SHCH (except Bulgarian = SHT) |
| 042A | Ъ | IE |
| 042B | Ы | Y |
| 042D | Э | E |
| 042E | Ю | IU (except if Ukrainian first character, then =YU) |
| 042F | Я | IA (except if Ukrainian first character, then =YA) |
| 046A | Ѫ | U |
| 0474 | "V" (Latin V printed; U+0474 is Ѵ izhitsa) | Y |
| 0490 | Ґ | G |
| 0492 | Ғ | G (except in the language spoken in the former Yugoslav Republic of Macedonia = GJ) |
| 04BA | Һ | C |

- Rows absent from the table: 0403 Ѓ, 040B Ћ, 042C Ь, 0400 Ѐ, 040D Ѝ and all lower-case forms. — [ICAO Doc 9303 Part 3 §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- In Serbian (Gaj's Latin ↔ Cyrillic), Г corresponds to G, not H. — [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet)

### Inferences
- Taking the ICAO "except Serbian" values (Ж→Z, Ч→C, Ш→S, Х→H, Ц→C, Ђ(0402)→D) gives the same result as writing in Gaj's Latin and then stripping diacritics with Section 6.A (Ž→Z, Č→C, Š→S, Đ→D). The one exception is Г→H, which looks like an ICAO error copied from the Belarusian/Ukrainian rule. The package should not apply Г→H to Serbian.
- The Macedonian exceptions (Ќ→KJ, Џ→DJ, Х→H, Ц→C, plus intended Ѓ→GJ) match the North Macedonian 2008 passport system exactly (see Q6). The ICAO entry for GJ is attached to the wrong code point (0492 instead of 0403).
- The ICAO defaults for Bulgarian (Й→I, Ъ→IE, Ю→IU, Я→IA, Х→KH, Ь undefined) conflict with Bulgarian national law (see Q4). Only Щ→SHT is carved out for Bulgarian.
- Package data should store the ICAO Cyrillic table as published (`icao9303_cyrillic.json`, with an `erratum` field per affected row) and separately store "corrected" per-language derivatives.

### Gaps
- I found no ICAO corrigendum fixing these Cyrillic-table errors. The 2022 and 2024 amendments to Part 3 did not change these rows, as of the consolidated PDF.

---

## Q4. ICAO Doc 9303 Part 3, Section 6.C — "Transliteration of Arabic Script" plus Appendix B extras (complete)

### Takeaway
ICAO's Arabic MRZ scheme is a reversible, consonant-only transliteration built on Buckwalter. `X` is an escape prefix for letters with no single A–Z equivalent. Short vowels are not encoded and shadda doubles the letter. Teh marbuta is XTA generally and XAH at the end of a name component.

### Cited Findings
Section 6.C table, verbatim. Arabic glyphs in the PDF text layer partly use presentation forms, so the Unicode column is authoritative — [ICAO Doc 9303 Part 3 §6.C](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf):

| Unicode | Name | MRZ |
|---|---|---|
| 0621 | hamza | XE |
| 0622 | alef with madda above | XAA |
| 0623 | alef with hamza above | XAE |
| 0624 | waw with hamza above | U |
| 0625 | alef with hamza below | I |
| 0626 | yeh with hamza above | XI |
| 0627 | alef | A |
| 0628 | beh | B |
| 0629 | teh marbuta | XTA/XAH (note 2) |
| 062A | teh | T |
| 062B | theh | XTH |
| 062C | jeem | J |
| 062D | hah | XH |
| 062E | khah | XKH |
| 062F | dal | D |
| 0630 | thal | XDH |
| 0631 | reh | R |
| 0632 | zain | Z |
| 0633 | seen | S |
| 0634 | sheen | XSH |
| 0635 | sad | XSS |
| 0636 | dad | XDZ |
| 0637 | tah | XTT |
| 0638 | zah | XZZ |
| 0639 | ain | E |
| 063A | ghain | G |
| 0640 | tatwheel | (Not encoded) |
| 0641 | feh | F |
| 0642 | qaf | Q |
| 0643 | kaf | K |
| 0644 | lam | L |
| 0645 | meem | M |
| 0646 | noon | N |
| 0647 | heh | H |
| 0648 | waw | W |
| 0649 | alef maksura | XAY |
| 064A | yeh | Y |
| 064B | fathatan | (Not encoded) |
| 064C | dammatan | (Not encoded) |
| 064D | kasratan | (Not encoded) |
| 064E | fatha | (Not encoded) |
| 064F | damma | (Not encoded) |
| 0650 | kasra | (Not encoded) |
| 0651 | shadda | [DOUBLE] (note 3) |
| 0652 | sukun | (Not encoded) |
| 0670 | superscript alef | (Not encoded) |
| 0671 | alef wasla | XXA |
| 0679 | tteh | XXT |
| 067C | teh with ring | XRT |
| 067E | peh | P |
| 0681 | hah with hamza above | XKE |
| 0685 | hah with 3 dots above | XXH |
| 0686 | tcheh | XC |
| 0688 | ddal | XXD |
| 0689 | dal with ring | XDR |
| 0691 | rreh | XXR |
| 0693 | reh with ring | XRR |
| 0696 | reh with dot below and dot above | XRX |
| 0698 | jeh | XJ |
| 069A | seen with dot below and dot above | XXS |
| 069C | seen with 3 dots below and 3 dots above | (Not encoded) |
| 06A2 | feh with dot moved below | (Not encoded) |
| 06A7 | qaf with dot above | (Not encoded) |
| 06A8 | qaf with 3 dots above | (Not encoded) |
| 06A9 | keheh | XKK |
| 06AB | kaf with ring | XXK |
| 06AD | ng | XNG |
| 06AF | gaf | XGG |
| 06BA | noon ghunna | XNN |
| 06BC | noon with ring | XXN |
| 06BE | heh doachashmee | XDO |
| 06C0 | heh with yeh above | XYH |
| 06C1 | heh goal | XXG |
| 06C2 | heh goal with hamza above | XGE |
| 06C3 | teh marbuta goal | XTG |
| 06CC | farsi yeh | XYA |
| 06CD | yeh with tail | XXY |
| 06D0 | yeh | Y |
| 06D2 | yeh barree | XYB |
| 06D3 | yeh barree with hamza above | XBE |

- Note 2 (verbatim): "XTA is used generally, except if teh marbuta occurs at the end of the name component, in which case XAH is used." — [ICAO Doc 9303 Part 3 §6.C](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Note 3 (verbatim): "Shadda denotes doubling: Latin character or sequence is repeated e.g. عباس becomes EBBAS; فضة becomes FXDZXDZXAH." — [ICAO Doc 9303 Part 3 §6.C](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Appendix B adds two letters "commonly used for foreign names": **06A4 veh → V** and **06A5 feh with 3 dots below → XF**. — [ICAO Doc 9303 Part 3 App. B §B.5.4](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Appendix B notes:
  - **06CC farsi yeh** "could be transliterated as 'Y' or 'XAY'" (note 4).
  - **06D0 Pashto yeh** "is functionally identical to the standard yeh" (note 5).
  - Hah and heh "have been swapped at the advice of Interpol": hah = XH, heh = H.
  - Alef maksura is XAY ("the former XY is incompatible").
  - Alef wasla is XXA ("the former XA is incompatible").
  - Maghrebi letters 069C, 06A2, 06A7 and 06A8 are "obsolete and not transliterated".
  
  — [ICAO Doc 9303 Part 3 App. B §B.5.5–B.5.8](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- `X` escape rationale: "the character 'X' is used as an 'escape' character … only one 'X' is used, and it is used before the character it modifies rather than after (e.g. 'XTH' versus 'NXX')". Human operators are to "ignore any 'X' characters". — [ICAO Doc 9303 Part 3 App. B §B.5.3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Worked examples (App. B §B.5.7, §B.5.9):
  - ابو بكر محمد بن زكريا الرازي → `ABW<BKR<MXHMD<BN<ZKRYA<ALRAZY`
  - Gamal Abdel Nasser → `JMAL<EBD<ALNAXSSR`
  - Isma'il Izz-ud-din → `ISMAEYL<EZZ<ALDYN`
  - Jamillah Na'ima → `JMYLXAH<NEYMXAH`
  - Abdul Aziz bin Mithab → `EBD<ALEZYZ<BN<MTEB`
  - Hari Al-Schamma → `HARY<ALXSHMAE`
  - al-'Abbās 'Abdu'llāh ibn Muhammad as-Saffāh → `ALEBAS<EBD<ALLXH<BN<MXHMD<ALSFAXH`
  
  The sun-letter article is not assimilated ("AL-RAZI" may be "AR-RAZI" in the VIZ). — [ICAO Doc 9303 Part 3 App. B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

### Inferences
- ICAO's own examples are not fully consistent:
  - Note 3 gives EBBAS (shadda doubled), but the "Abbās" example gives ALEBAS (shadda absent from the input).
  - "Allah" is shown as ALLXH, which App. B §B.5.5.11 calls a special case.
  
  Matching code should allow optional doubling and XTA/XAH alternation, as ICAO itself advises.
- In practice few states use this X-escape scheme in real MRZs. Most print a phonetic Latin transcription, for example JAMAL rather than JMAL. The table is best stored as an `icao9303_arabic_mrz` scheme, not as the default English rendering.

### Gaps
- I did not establish which issuing states actually implement the ICAO Arabic X-scheme. Other researchers cover Arabic-specific practice.

---

## Q5. Bulgarian: the Streamlined System under the Transliteration Act (ДВ бр. 19/2009), passports, exceptions, UN/BGN/PCGN

### Takeaway
The Transliteration Act (promulgated in State Gazette No. 19 of 13 March 2009) fixes the table in **Art. 4**, letter combinations in **Art. 5(1)**, word-final **-ия → -ia** in **Art. 5(2)**, and "Bulgaria" in Art. 6. Identity documents and passports are governed separately by the **Regulation for Issuing Bulgarian Personal Documents (ПМС 13/2010)**. Its Art. 2(1) requires "English transliteration" per Appendix 1, which uses the same letters, uppercase, with the -ия note limited to personal names and settlement names. Art. 2(2) lets citizens request a **different** Latin spelling of "characteristic letters and letter combinations" in their **first** ID document; later changes require official documents or a court decision. The UN adopted the system in 2012 (resolution X/7) and BGN/PCGN in 2013.

### Cited Findings
**Statutory table (Transliteration Act, Art. 4)** and **ID-document table (Regulation App. 1)**:

| Cyrillic | Unicode (upper/lower) | Act Art. 4 | Regulation App. 1 (passports, uppercase) | ICAO §6.B generic | Differences in older/other systems |
|---|---|---|---|---|---|
| А а | 0410/0430 | A a | A | A | — |
| Б б | 0411/0431 | B b | B | B | — |
| В в | 0412/0432 | V v | V | V | — |
| Г г | 0413/0433 | G g | G | G | — |
| Д д | 0414/0434 | D d | D | D | — |
| Е е | 0415/0435 | E e | E | E | — |
| Ж ж | 0416/0436 | Zh zh | ZH | ZH | UN 1977: ž |
| З з | 0417/0437 | Z z | Z | Z | — |
| И и | 0418/0438 | I i | I | I | — |
| Й й | 0419/0439 | Y y | Y | **I** | UN 1977: j; BDS 1596:73: J |
| К к | 041A/043A | K k | K | K | — |
| Л л | 041B/043B | L l | L | L | — |
| М м | 041C/043C | M m | M | M | — |
| Н н | 041D/043D | N n | N | N | — |
| О о | 041E/043E | O o | O | O | — |
| П п | 041F/043F | P p | P | P | — |
| Р р | 0420/0440 | R r | R | R | — |
| С с | 0421/0441 | S s | S | S | — |
| Т т | 0422/0442 | T t | T | T | — |
| У у | 0423/0443 | U u | U | U | — |
| Ф ф | 0424/0444 | F f | F | F | — |
| Х х | 0425/0445 | H h | H | **KH** | BGN/PCGN 1952: kh |
| Ц ц | 0426/0446 | Ts ts | TS | TS | UN 1977: c; pre-2009 ID docs: C (see conflict below) |
| Ч ч | 0427/0447 | Ch ch | CH | CH | UN 1977: č |
| Ш ш | 0428/0448 | Sh sh | SH | SH | UN 1977: š |
| Щ щ | 0429/0449 | Sht sht | SHT | SHT (Bulgarian exception) | UN 1977: št |
| Ъ ъ | 042A/044A | A a | A | **IE** | BGN/PCGN 1952: ŭ; UN 1977: ǎ |
| Ь ь | 042C/044C | Y y | Y | (not in table) | BGN/PCGN 1952: ʹ (apostrophe) |
| Ю ю | 042E/044E | Yu yu | YU | **IU** | UN 1977: ju; BDS 1596:73: JU |
| Я я | 042F/044F | Ya ya | YA | **IA** | UN 1977: ja; BDS 1596:73: JA |

Sources for the table:
- Act Art. 4: [Закон за транслитерацията, ДВ 19/2009 (text)](https://annual-ct.eu/bg/wp-content/uploads/2024/05/zakon_za_transliteraciata.pdf)
- App. 1: [Правилник за издаване на българските лични документи](https://www.mfa.bg/upload/648/08-Pr-ZBLD-bg.pdf)
- ICAO: [ICAO Doc 9303 Part 3 §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- UN 1977 / BGN 1952: [UN WGRS report on Bulgarian, Feb 2013](https://arhiiv.eki.ee/wgrs/rom1_bg.htm)
- BDS 1596:73: [UNGEGN E/CONF.101/12](https://unstats.un.org/UNSD/geoinfo/UNGEGN/docs/10th-uncsgn-docs/econf/E_CONF.101_12_Romanization%20System%20in%20Bulgaria.pdf)

- **Art. 5(1)** letter combinations: "дж" → "dzh"; "дз" → "dz"; "ьо" → "yo"; "йо" → "yo". **Art. 5(2)**: "Буквеното съчетание 'ия', когато е в края на думата, се изписва и предава чрез 'ia'". **Art. 6**: България → Bulgaria "в съответствие с установената традиция". — [Закон за транслитерацията](https://annual-ct.eu/bg/wp-content/uploads/2024/05/zakon_za_transliteraciata.pdf)
- Act examples: Стара планина → Stara planina; Централен Балкан → Tsentralen Balkan; **София-юг → Sofia-yug**; Перник-север → Pernik-sever; Златни пясъци → Zlatni pyasatsi; Горна Оряховица → Gorna Oryahovitsa (Arts. 7–8). Art. 9: foreign names from Latin-script languages keep their original form; names from non-Latin languages follow that language's transliteration system. — [Закон за транслитерацията](https://annual-ct.eu/bg/wp-content/uploads/2024/05/zakon_za_transliteraciata.pdf)
- **Scope of the Act**: Art. 2 covers executive-branch bodies and other constitutional bodies. It also binds anyone who transliterates geographical names, historical personalities, cultural realia and Bulgarian-origin terms, as well as publishers of dictionaries and textbooks. Art. 3 makes it mandatory for legal-entity name additions, trademarks with historical names and geographical indications. **The Act text contains no article dealing specifically with personal names of living citizens or identity documents.** It was adopted by the 40th National Assembly on 27 Feb 2009. — [Закон за транслитерацията](https://annual-ct.eu/bg/wp-content/uploads/2024/05/zakon_za_transliteraciata.pdf)
- Bulgaria's 2012 UN submission says the Act standardizes romanization "in official documents: identity cards, foreign-travel passports, driving licences etc." It promulgated by Decree No. 59 of 9 March 2009 in State Gazette No. 19 of 13 March 2009. — [UNGEGN E/CONF.101/12 (submitted by Bulgaria)](https://unstats.un.org/UNSD/geoinfo/UNGEGN/docs/10th-uncsgn-docs/econf/E_CONF.101_12_Romanization%20System%20in%20Bulgaria.pdf)
- **Passports and ID documents**: Regulation Art. 2(1) (verbatim): "Имената и месторождението на българските граждани в българските лични документи се изписват на кирилица и на латиница чрез английска транслитерация съгласно приложение № 1." The App. 1 note (verbatim): "Съчетанието от буквите 'ия' в края на собствените имена на граждани и на наименованията на населени места се предава чрез 'ia'." — [Правилник за издаване на българските лични документи (ПМС 13/08.02.2010, ДВ 12/2010, consolidated to ДВ 70/2016)](https://www.mfa.bg/upload/648/08-Pr-ZBLD-bg.pdf)
- **Exceptions in the Regulation** (verbatim):
  - Art. 2(2): "По искане на българските граждани имената им, съдържащи характерни букви и буквосъчетания, могат да бъдат изписани на латиница по начин, различен от английската транслитерация, в първи документ за самоличност. Промяна в следващ документ може да се извърши само след представяне на официални документи, съдържащи исканото изписване, или след представяне на съдебно решение."
  - Art. 2(3): a return to the standard App. 1 transliteration may be made in a subsequent document without such evidence.
  - Art. 2(4): Art. 2(3) does not apply if MoI records show the person was registered as an offender abroad under the previous Latin spelling.
  - Art. 2(6): when a document is issued with changed transliteration, "се обявяват за невалидни всички български лични документи на лицето, издадени с предходна транслитерация".
  
  — [Правилник за издаване на българските лични документи](https://www.mfa.bg/upload/648/08-Pr-ZBLD-bg.pdf)
- Wikipedia likewise says the "freedom of using different Roman transliterations of personal names is guaranteed by Article 2(2) of the governmental 2010 Regulation", giving Simeon Djankov as an example. — [Wikipedia: Romanization of Bulgarian](https://en.wikipedia.org/wiki/Romanization_of_Bulgarian)
- Conflicting secondary source: a Bulgarian blog says there are no exceptions for previous or foreign documents and gives examples Георги → Georgi, Жоро → Zhoro (not Joro), Христо → Hristo, Мария → Maria, and Илиян → Iliyan (mid-word -ия is not affected). The exceptions claim is contradicted by Regulation Art. 2(2). — [pishi.bg](https://pishi.bg/blog/imena-na-latinitsa-zakon/); contradicted by [Правилник Art. 2(2)](https://www.mfa.bg/upload/648/08-Pr-ZBLD-bg.pdf)
- **History**:
  - BDS 1596:73 (effective 1 Jan 1975) was the base.
  - Decree No. 61 of 2 April 1999 attached an ID-document table that changed Й from J to Y, Ю from JU to YU and Я from JA to YA.
  - Per Bulgaria's UN paper, "The transliteration table in the Transliteration Act introduced a change concerning the Bulgarian letter 'Ц', which until then was Romanized by 'C' and from now on will be transliterated as 'TS'."
  
  — [UNGEGN E/CONF.101/12](https://unstats.un.org/UNSD/geoinfo/UNGEGN/docs/10th-uncsgn-docs/econf/E_CONF.101_12_Romanization%20System%20in%20Bulgaria.pdf). Partly contradicted by Wikipedia, which says the 1999 ID system was amended in 2000 to become identical to the 1995 Antarctic system (ts for ц). Wikipedia also says the -ia exception was introduced in 2006 for proper names and geographical names and extended by the 2009 Act to all word-final -ия. — [Wikipedia: Romanization of Bulgarian](https://en.wikipedia.org/wiki/Romanization_of_Bulgarian)
- **UN / BGN/PCGN**: "approved in 2012 (resolution X/7)", "based on the system finalized and officially adopted in Bulgaria in 2009". The WGRS rule reads: "The characters -ия at the end of a word are romanized -ia." The report adds that "the romanization table is not fully reversible as certain romanization equivalents are ambiguous". BGN/PCGN 1952 used kh, ŭ, ʹ and -iya. — [UN WGRS report, Feb 2013 (v4.0)](https://arhiiv.eki.ee/wgrs/rom1_bg.htm). BGN and PCGN adopted the system in 2013, replacing their 1952 system. — [Wikipedia: Romanization of Bulgarian](https://en.wikipedia.org/wiki/Romanization_of_Bulgarian), [BGN/PCGN page summary (search result)](https://en.wikipedia.org/wiki/BGN/PCGN_romanization)

### Inferences
- **Algorithm**: map letter by letter with Art. 4, then apply word-final -ия → -ia.
  - Art. 5(1) needs no special code: д+ж → d+zh = "dzh", д+з = "dz", ь+о → y+o = "yo", й+о → y+o = "yo".
  - Word boundaries for -ия should include end of string, space and hyphen (София-юг → Sofia-yug), and probably apostrophes.
  - Case: output Zh/Ts/Ch/Sh/Sht/Yu/Ya in title case when the source letter is uppercase and the next letter is lowercase, and all caps for an all-uppercase input (passport style ZHIVKOV).
- **MRZ**: the App. 1 output is already pure A–Z, so a Bulgarian MRZ is presumably the uppercase App. 1 string, not the ICAO generic Cyrillic output. For example, Йорданова would be YORDANOVA, not IORDANOVA.
- **Matching variants to generate** for Bulgarian-origin names:
  - Й: Y/J/I
  - Ц: TS/C (pre-2009 per the UN paper)
  - Х: H/KH
  - Ъ: A/U/Ŭ
  - Ю/Я: YU/JU/IU and YA/JA/IA
  - word-final -ИЯ: IA/IYA
  - Ж: ZH/J (French-style "Joro" as noted by pishi.bg)
  - Щ: SHT/SHCH
  - plus any user-chosen spelling under Art. 2(2)
- Reverse transliteration (Latin → Cyrillic) is ambiguous: "a" can be а or ъ, "y" can be й or ь, and "sht" can be щ or ш+т. A reverse function must return candidates, not a single answer.

### Gaps
- I could not open lex.bg for an up-to-date consolidated Regulation text after ДВ 70/2016. Later amendments (for example around the 2023–2024 changes to the Bulgarian Personal Documents Act for new eID cards) may have renumbered or changed Art. 2. This needs checking.
- I found no primary specimen showing a Bulgarian passport MRZ, so the uppercase App. 1 = MRZ claim is inferred.
- I did not verify the ISO 9:1995 Bulgarian table in this session.

---

## Q6. Serbian: Cyrillic → Gaj's Latin, passport VIZ/MRZ, English conventions (Đoković → Djokovic)

### Takeaway
Serbian Cyrillic maps one-to-one onto Gaj's Latin, with three digraph letters: Lj, Nj, Dž. Serbian passports print personal data in Serbian **Latin with diacritics**. Since biometric passports (2008/09), Đ is printed as **Đ**, not Dj, in the personal-data (visual) zone. The MRZ strips diacritics (Č/Ć→C, Š→S, Ž→Z). For **Đ in the MRZ**, I found no authoritative Serbian source: ICAO's table gives D, and Montenegro's rule is explicitly D. The English/ASCII convention is **Dj**: Đoković → Djokovic, Đorđe → Djordje.

### Cited Findings
**Serbian Cyrillic ↔ Gaj's Latin (complete, 30 letters)**, with the ICAO entry, the MRZ and the English convention:

| Cyrillic | Gaj Latin | Unicode (Latin upper) | ICAO §6.B (Serbian) | MRZ (Latin → §6.A) | Common English/ASCII |
|---|---|---|---|---|---|
| А а | A a | — | A | A | a |
| Б б | B b | — | B | B | b |
| В в | V v | — | V | V | v |
| Г г | G g | — | "H" (ICAO error; should be G) | G | g |
| Д д | D d | — | D | D | d |
| Ђ ђ | Đ đ | 0110/0111 | D (row "0402") | D (ICAO) — Serbian practice unverified | **dj** |
| Е е | E e | — | E | E | e |
| Ж ж | Ž ž | 017D/017E | Z | Z | z |
| З з | Z z | — | Z | Z | z |
| И и | I i | — | I | I | i |
| Ј ј | J j | — | J | J | j |
| К к | K k | — | K | K | k |
| Л л | L l | — | L | L | l |
| Љ љ | Lj lj | 01C7/01C8/01C9 (digraph code points) or L+J | LJ | LJ | lj |
| М м | M m | — | M | M | m |
| Н н | N n | — | N | N | n |
| Њ њ | Nj nj | 01CA/01CB/01CC or N+J | NJ | NJ | nj |
| О о | O o | — | O | O | o |
| П п | P p | — | P | P | p |
| Р р | R r | — | R | R | r |
| С с | S s | — | S | S | s |
| Т т | T t | — | T | T | t |
| Ћ ћ | Ć ć | 0106/0107 | (040B not listed) | C | c |
| У у | U u | — | U | U | u |
| Ф ф | F f | — | F | F | f |
| Х х | H h | — | H | H | h |
| Ц ц | C c | — | C | C | c |
| Ч ч | Č č | 010C/010D | C | C | c |
| Џ џ | Dž dž | 01C4/01C5/01C6 or D+Ž | DZ | DZ | dz |
| Ш ш | Š š | 0160/0161 | S | S | s |

Sources for the table:
- Correspondence and digraph code points: [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet)
- ICAO column: [ICAO Doc 9303 Part 3 §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- MRZ column: [ICAO §6.A](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

- Dž, Lj and Nj "are considered to be single letters" (single phonemes), but the same letter sequences can occur across morpheme boundaries without being digraphs (nadživjeti = d+ž). — [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet)
- ASCII convention: "ošišana abeceda" ("shorn Latin") drops the diacritics of č ć š ž and writes đ as "dj". It is common in SMS, email and web use, and cannot be reversed to Cyrillic without manual work. Đ "is still sometimes represented by ⟨dj⟩", as in "Novak Djokovic", though "strictly Đ should be used". — [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet). "When a true ⟨đ⟩ is not available or desired, it is transcribed as ⟨dj⟩ in modern Serbo-Croatian, and as ⟨gj⟩ in Macedonian." — [Wikipedia: D with stroke](https://en.wikipedia.org/wiki/D_with_stroke)
- **Serbian passports, VIZ**: a 2009 Ministry of Interior (MUP) statement, quoted verbatim: "svaki građanin koji u svom imenu ili prezimenu ima slovo đ ono u pasoš biti upisano kao latinično slovo u srpskom jeziku đ, a ne kao dj". It cites Art. 26 of the Law on Travel Documents: forms are filled in in Serbian using Latin script, with names "in original form" as in the birth register. The MUP also notes the MRZ "can contain only alphabet letters, numbers and the special character <". — [Danas, 29 May 2009](https://www.danas.rs/drustvo/komplikovano-slovo-dj-u-pasosu/)
- Old blue (SFRY/FRY) passports wrote Đorđe Đorđević with "DJ". The new red biometric passport uses "Đ", which caused mismatches with work permits that read "Djordjević". — [Novosti, 28 May 2009](https://www.novosti.rs/vesti/naslovna/aktuelno.69.html:241172-Dj-za-nove-nevolje)
- **Serbian ID card MRZ**: "The only characters used are those of Serbian Latin alphabet, except for letters with diacritics (ŠĐĆČŽ — they are replaced by the appropriate letter without a diacritical mark)". This implies Đ→D, but the article does not say so explicitly. — [Wikipedia: Serbian identity card](https://en.wikipedia.org/wiki/Serbian_identity_card)
- The Serbian Wikipedia passport article confirms that personal data are printed in Serbian Latin script but gives no MRZ diacritic rule. — [sr.wikipedia: Пасош Србије](https://sr.wikipedia.org/sr-ec/%D0%9F%D0%B0%D1%81%D0%BE%D1%88_%D0%A1%D1%80%D0%B1%D0%B8%D1%98%D0%B5)

### Inferences
- **Default MRZ profile for Serbian**: Cyrillic → Gaj Latin → ICAO §6.A, giving Đ→D, Ć/Č→C, Š→S, Ž→Z, Dž→DZ. For example, ĐOKOVIĆ, NOVAK → `DOKOVIC<<NOVAK`.
- **Default English profile**: Đ→Dj, giving DJOKOVIC. The package should offer both and generate both for matching, because which one appears in Serbian MRZs is unresolved.
- Do not apply ICAO's "Serbian Г = H".
- Collision warning: "DJ" in a Macedonian passport means Џ, whereas in Serbian/Croatian English convention it means Ђ/Đ. "DZ" in an ICAO-style Serbian MRZ means Џ. Cross-language reverse mapping must be language-tagged.

### Gaps
- **No primary source found for how Serbian passports print Đ in the MRZ (D vs DJ).** Search snippets conflict, and PRADO (SRB-AP-02001) returned 403. This is the main open item. The next places to check are a PRADO specimen MRZ or Serbia's "Pravilnik o obrascu pasoša".
- I did not verify a BGN/PCGN Serbian table. It is generally identical to Gaj's Latin.

---

## Q7. Macedonian: official 2008 passport system, BGN/PCGN 2013, ISO 9, ICAO

### Takeaway
North Macedonian passports and IDs use a diacritic-free digraph system adopted in 2008: Ѓ→GJ, Ж→ZH, Ѕ→DZ, Ј→J, Љ→LJ, Њ→NJ, Ќ→KJ, Х→H, Ц→C, Ч→CH, Џ→DJ, Ш→SH. It coincides with ICAO's Macedonian exceptions. BGN/PCGN (2013 agreement, checked November 2023) uses the diacritic forms ǵ, ž, dz, ḱ, č, dž and š.

### Cited Findings
**Comparison table (31 letters)**:

| Cyrillic | Unicode (upper) | Official 2008 (passports/IDs) | ICAO §6.B | BGN/PCGN 2013 | ISO 9:1995 | ALA-LC |
|---|---|---|---|---|---|---|
| А | 0410 | A | A | a | A | A |
| Б | 0411 | B | B | b | B | B |
| В | 0412 | V | V | v | V | V |
| Г | 0413 | G | G | g | G | G |
| Д | 0414 | D | D | d | D | D |
| Ѓ | 0403 | **GJ** | GJ (listed under 0492 by mistake) | ǵ (01F5) | Ǵ | Ǵ |
| Е | 0415 | E | E | e | E | E |
| Ж | 0416 | **ZH** | ZH | ž | Ž | Ž |
| З | 0417 | Z | Z | z | Z | Z |
| Ѕ | 0405 | **DZ** | DZ | dz / ǳ (01F3) | Ẑ | Dz |
| И | 0418 | I | I | i | I | I |
| Ј | 0408 | J | J | j | J̌ | J |
| К | 041A | K | K | k | K | K |
| Л | 041B | L | L | l | L | L |
| Љ | 0409 | **LJ** | LJ | lj | L̂ | Lj |
| М | 041C | M | M | m | M | M |
| Н | 041D | N | N | n | N | N |
| Њ | 040A | **NJ** | NJ | nj | N̂ | Nj |
| О | 041E | O | O | o | O | O |
| П | 041F | P | P | p | P | P |
| Р | 0420 | R | R | r | R | R |
| С | 0421 | S | S | s | S | S |
| Т | 0422 | T | T | t | T | T |
| Ќ | 040C | **KJ** | KJ | ḱ (1E31) | Ḱ | Ḱ |
| У | 0423 | U | U | u | U | U |
| Ф | 0424 | F | F | f | F | F |
| Х | 0425 | **H** | H | h | H | H |
| Ц | 0426 | **C** | C | c | C | C |
| Ч | 0427 | **CH** | CH | č | Č | Č |
| Џ | 040F | **DJ** | DJ | dž | D̂ | Dž |
| Ш | 0428 | **SH** | SH | š | Š | Š |
| ʼ (modifier apostrophe) | 02BC | — | — | ’ (2019) | — | — |

Sources for the table:
- Official 2008, ISO 9 and ALA-LC: [Wikipedia: Romanization of Macedonian](https://en.wikipedia.org/wiki/Romanization_of_Macedonian)
- BGN/PCGN: [BGN/PCGN Romanization of Macedonian Cyrillic, 2013 Agreement (checked Nov 2023)](https://assets.publishing.service.gov.uk/media/636cd3738fa8f53587ffb1d6/ROMANIZATION_OF_MACEDONIAN_2022_final.pdf)
- ICAO: [ICAO Doc 9303 Part 3 §6.B](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

- "Such a diacritic-free system, with digraphs ch, sh, zh, dz, dj, gj, kj, lj, nj has been adopted since 2008 for use in official documents such as passports, ID cards and driver's licenses". The article cites ICAO Doc 9303 as the basis. — [Wikipedia: Romanization of Macedonian](https://en.wikipedia.org/wiki/Romanization_of_Macedonian)
- BGN/PCGN examples:
  - Ѓавато → Ǵavato
  - Ќафасан → Ḱafasan
  - Џепчиште → Džepčište
  - Ѕвегор → Dzvegor
  - ’Ржаново → ’Ržanovo
  
  This system replaces the BGN/PCGN 1981 agreement. Digraph letters ǲ/ǳ, ǈ/ǉ, ǋ/ǌ and ǅ/ǆ "can also be reproduced with individual letters". — [BGN/PCGN Macedonian 2013](https://assets.publishing.service.gov.uk/media/636cd3738fa8f53587ffb1d6/ROMANIZATION_OF_MACEDONIAN_2022_final.pdf)
- Macedonian forms of George: Gjorgji (Ѓорѓи), Gjorgje (Ѓорѓе), Gjorgjija (Ѓорѓија), Gjoko (Ѓоко), written with the gj convention. — [Wikipedia: George (given name)](https://en.wikipedia.org/wiki/George_(given_name))

### Inferences
- For Macedonian, "official", "passport VIZ" and "MRZ" are the same string up to case. The package can treat `mk_official_2008` as the ICAO MRZ scheme.
- Macedonian Ѐ/ѐ (U+0400/0450) and Ѝ/ѝ (U+040D/045D) are accent-marked homograph differentiators that appear only occasionally. Map them to E and I.
- Older or alternative spellings to accept when matching: Ѓ as G, Đ, Gj or Dj; Ќ as K, Ć, Kj or Ch; Џ as Dž, Dzh or Dj; Ж as Ž, Zh or J; Ц as C or Ts. For example, Ѓорѓи may appear as Gjorgji, Gjorgi, Djordji or Georgi.

### Gaps
- I did not retrieve the legal instrument (number and date of the 2008 government decision or rulebook) that adopted the passport system. Its legal basis was not verified in a primary North Macedonian source.
- The UN-recommended status of the Macedonian system (and whether it is UN 1977) was not verified.

---

## Q8. Montenegrin extras (Ś, Ź, С́, З́) and Montenegro's MRZ rule

### Takeaway
Montenegrin, standardized in 2009, adds Ś/С́ and Ź/З́ to the Serbo-Croatian inventory, and their use is optional. Montenegro's 2008 MRZ regulation explicitly maps **Đ→D, Ž→Z, Ć→C, Č→C, Š→S**. ICAO maps Ś→S and Ź→Z.

### Cited Findings
- Latin alphabet: A B C Č Ć D Dž Đ E F G H I J K L Lj M N Nj O P R S Š **Ś** T U V Z Ž **Ź**. Cyrillic: А Б В Г Д Ђ Е Ж З **З́** И Ј К Л Љ М Н Њ О П Р С **С́** Т Ћ У Ф Х Ц Ч Џ Ш. Ś/С́ = /ɕ/ and Ź/З́ = /ʑ/, both borrowed from Polish. Introduced by ministerial decree of 9 July 2009. The Cyrillic forms use a combining acute. Traditional spellings remain standard, so the new letters are optional. — [Wikipedia: Montenegrin alphabet](https://en.wikipedia.org/wiki/Montenegrin_alphabet)
- Montenegro "Pravilnik o sadržaju mašinski čitljivog zapisa" (10 April 2008, published 18 April 2008), Art. 5(4), verbatim: "Slova latiničnog pisma unose se na sljedeći način, i to: Đ kao D, Ž kao Z, Ć kao C, Č kao C i Š kao S." — [Government of Montenegro (gov.me) document](https://wapi.gov.me/download/389da702-a26d-455c-a4e5-15fe4975d37a?version=1.0)
- ICAO §6.A: 015A Ś → S; 0179 Ź → Z. — [ICAO Doc 9303 Part 3](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)

### Inferences
- Cyrillic С́ is С (U+0421) + U+0301, and З́ is З (U+0417) + U+0301. No precomposed code points exist. The transliterator must handle the combining sequence before single-character lookup (NFD-normalize, then match the longest sequence first): С́→Ś, З́→Ź. The MRZ/ASCII forms are S and Z.
- Montenegro is the strongest primary evidence that ex-Yugoslav practice in the MRZ is Đ→**D**, not DJ.

### Gaps
- I did not check whether the 2008 Montenegrin regulation has been replaced, or whether newer rules mention Ś/Ź.

---

## Q9. Latin-script Slavic diacritics: (a) ICAO MRZ, (b) national passport practice, (c) English/ASCII renderings

### Takeaway
For every Polish, Czech, Slovak, Croatian, Bosnian, Serbian-Latin and Slovene diacritic letter, ICAO §6.A gives a single base letter. Slovak Ä is the only one with an option (AE or A). The Gaj digraph code points Ǆ/Ǉ/Ǌ are not in the ICAO table and decompose to DZ/LJ/NJ. Confirmed national MRZ practice: Poland strips diacritics (CURUŚ → CURUS), Czech MRZ uses only A–Z/0–9/<, Montenegro maps Đ→D, Croatia defers to ISO/ICAO, and Serbia strips diacritics with the Đ question open. English/ASCII practice matches ICAO except Đ, which is usually "Dj".

### Cited Findings
**Master table** (ICAO column verbatim from §6.A):

| Letter (upper/lower) | Unicode upper | Languages | ICAO §6.A MRZ | Typical English/ASCII |
|---|---|---|---|---|
| Ą ą | 0104 | pl | A | a |
| Á á | 00C1 | cs, sk | A | a |
| Ä ä | 00C4 | sk | AE or A | a (see inference) |
| Ć ć | 0106 | pl, hr, bs, sr, me | C | c |
| Č č | 010C | cs, sk, hr, bs, sr, me, sl | C | c |
| Ď ď | 010E | cs, sk | D | d |
| Đ đ | 0110 | hr, bs, sr, me | D | dj (Djokovic) |
| Dž dž (Ǆ ǅ ǆ) | 01C4/01C5/01C6 (or D+Ž) | hr, bs, sr, me; sk (as two letters dz/dž) | not listed (D + Ž → DZ) | dz |
| É é | 00C9 | cs, sk | E | e |
| Ě ě | 011A | cs | E | e |
| Ę ę | 0118 | pl | E | e |
| Í í | 00CD | cs, sk | I | i |
| Ĺ ĺ | 0139 | sk | L | l |
| Ľ ľ | 013D | sk | L | l |
| Ł ł | 0141 | pl | L | l |
| Lj lj (Ǉ ǈ ǉ) | 01C7/01C8/01C9 (or L+J) | hr, bs, sr, me | not listed → LJ | lj |
| Ń ń | 0143 | pl | N | n |
| Ň ň | 0147 | cs, sk | N | n |
| Nj nj (Ǌ ǋ ǌ) | 01CA/01CB/01CC (or N+J) | hr, bs, sr, me | not listed → NJ | nj |
| Ó ó | 00D3 | pl, cs, sk | O | o |
| Ô ô | 00D4 | sk | O | o |
| Ŕ ŕ | 0154 | sk | R | r |
| Ř ř | 0158 | cs | R | r |
| Ś ś | 015A | pl, me | S | s |
| Š š | 0160 | cs, sk, hr, bs, sr, me, sl | S | s |
| Ť ť | 0164 | cs, sk | T | t |
| Ú ú | 00DA | cs, sk | U | u |
| Ů ů | 016E | cs | U | u |
| Ý ý | 00DD | cs, sk | Y | y |
| Ź ź | 0179 | pl, me | Z | z |
| Ż ż | 017B | pl | Z | z |
| Ž ž | 017D | cs, sk, hr, bs, sr, me, sl | Z | z |

Sources for the table:
- ICAO column: [ICAO Doc 9303 Part 3 §6.A](https://www.icao.int/sites/default/files/publications/DocSeries/9303_p3_cons_en.pdf)
- Digraph code points and Đ→dj: [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet)
- Slovene uses Gaj's alphabet without ć and đ and treats lj/nj as two letters: [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet)

**National MRZ practice found**
- **Poland**: "Narodowe znaki diakrytyczne są transliterowane na odpowiednie znaki alfabetu łacińskiego". Example: Adam Jerzy Bachleda-Curuś → `BACHLEDA<CURUS<<ADAM<JERZY<<<`. — [pl.wikipedia: MRZ](https://pl.wikipedia.org/wiki/MRZ)
- **Czech Republic**: "Veškeré údaje se kódují výhradně velkými písmeny anglické abecedy, arabskými číslicemi a znakem '<'. Pro vkládání dalších znaků jsou definované transkripce (např. 'Ä' → 'AE')." No Czech-specific examples are given. — [cs.wikipedia: Strojově čitelná oblast dokladů](https://cs.wikipedia.org/wiki/Strojov%C4%9B_%C4%8Diteln%C3%A1_oblast_doklad%C5%AF)
- **Croatia**: Pravilnik NN 4/2010, Art. 8: "Upis podataka u vizualnu i strojno čitljivu zonu putovnice mora se obavljati sukladno međunarodnim standardima za strojno čitanje putne isprave". There is no explicit letter table. — [Narodne novine 4/2010](https://narodne-novine.nn.hr/clanci/sluzbeni/2010_01_4_104.html)
- **Montenegro**: Đ→D, Ž→Z, Ć→C, Č→C, Š→S (Art. 5(4), 2008). — [gov.me regulation](https://wapi.gov.me/download/389da702-a26d-455c-a4e5-15fe4975d37a?version=1.0)
- **Serbia**: ID-card MRZ replaces ŠĐĆČŽ with the letter without diacritic; the Đ question is open (see Q6). — [Wikipedia: Serbian identity card](https://en.wikipedia.org/wiki/Serbian_identity_card)
- **Bosnia and Herzegovina**: a search snippet of the 2002 ID-card rulebook (Sl. glasnik BiH 39/02) states Đ→D, Ž→Z, Ć→C, Č→C, Š→S in the MRZ. The PDF could not be opened (connection reset), so this is **unverified**. — [Pravilnik o obrascu lične karte, Sl. glasnik BiH 39/02](https://propisi.ks.gov.ba/sites/propisi.ks.gov.ba/files/sl_glasnik_bih_39_02_pravilnik_licne_karte.pdf)
- German- and Nordic-style expansions (Ä→AE, Ö→OE, Ü→UE, Å→AA) are typical of German-speaking and Nordic issuers. — [Wikipedia: Machine-readable passport](https://en.wikipedia.org/wiki/Machine-readable_passport)

### Inferences
- **Default ASCII fold** (`to_ascii(name, lang)`): use the ICAO single-letter value for every letter in the table, with these overrides:
  - Đ/đ → "Dj"/"dj" in the `english` profile and "D" in the `icao_mrz` profile.
  - Slovak Ä → "A". Slovak ä is not a German-style umlaut, and AE is mainly a German/Nordic convention. This is my inference; I found no Slovak passport specimen.
  - Gaj digraph code points → decompose: Ǆ→DŽ→DZ, ǅ→Dž→Dz, ǉ→lj, and so on. Title-case forms (U+01C5, U+01C8, U+01CB) must map to "Dz", "Lj", "Nj".
- Typical English renderings simply drop diacritics: Łukasz → Lukasz, Wałęsa → Walesa, Dvořák → Dvorak, Jiří → Jiri, Đorđe → Djordje (or Dorde in an ICAO MRZ). These follow from the table, not from a separate source.
- **Do not** use NFKD stripping alone. Ł and Đ survive NFKD unchanged and would then be dropped or rejected.

### Gaps
- I found no primary specimen MRZ or regulation for Slovak, Slovene, Czech or Polish passports that spells out letter mappings. All are presumed ICAO-default (diacritic stripping). Whether any of these issuers uses Ä→AE (Slovak) is unverified.
- Common phonetic anglicizations, such as Polish "Ł → W" spellings in diaspora names or Czech Ř → "Rz", were not researched or sourced.

---

## Q10. Gendered surname forms (Polish, Czech/Slovak, Bulgarian, Macedonian, Serbo-Croatian) and the Czech 2022 law

### Takeaway
Polish (-ski/-ska, -cki/-cka), Czech/Slovak (-ský/-ská, -ová), Bulgarian (-ov/-ova, -ev/-eva, -ski/-ska) and Macedonian (-ski/-ska, -ov/-ova) surnames change with gender. Serbo-Croatian and Bosnian -ić/-vić names do not. Since **1 January 2022**, Czech women may register the masculine (unsuffixed) form of their surname on request, without justification. Name matching should therefore normalize female forms to a shared stem.

### Cited Findings
- Polish surnames have gendered forms -ski/-ska and -cki/-cka. Czech and Slovak -ová "makes a feminine adjective out of a surname", for example Krejčí → Krejčová. -ský/-ská is used in both languages. Bulgarian uses -ov/-ova, -ev/-eva and -ski/-ska. Macedonian uses -ski/-ska and -ov/-ova. Serbian, Croatian and Bosnian -ić/-vić are invariant by gender. — [Wikipedia: Slavic name suffixes](https://en.wikipedia.org/wiki/Slavic_name_suffixes)
- Czech law: "Od 1. ledna 2022" women may "bez jakýchkoli dalších zákonných podmínek zvolit", choosing an inflected or uninflected surname; "Stačí o zápis bez jakéhokoli zdůvodnění požádat". This applies at marriage (on the woman's request) and at birth registration ("na základě žádosti rodičů"). Previously it was allowed only for foreign women, Czech citizens of non-Czech nationality, those living abroad, or those married to foreigners. — [Právní prostor, 10 Jan 2022](https://pravniprostor.cz/aktuality/od-ledna-mohou-zeny-pouzivat-prijmeni-v-neprechylenem-tvaru-bez-jakychkoli-dalsich-podminek)
- The Senate approved the amendment to the Law on Registers of Births, First Names and Surnames in July 2021, and it then went for presidential signature. Parents may also give daughters the masculine form. — [Radio Prague International, 3 Jul 2021](https://english.radio.cz/node/8722097)

### Inferences
- Matching normalizer rules, applied to ASCII-folded forms:
  - **Polish**: -SKA→-SKI, -CKA→-CKI, -DZKA→-DZKI. Example: Kowalska ↔ Kowalski.
  - **Czech/Slovak**: -SKA→-SKY (Novotná/Novotný pattern: -NA→-NY), -OVA → strip -OVA. Then compare against the male stem, allowing for a dropped final -A or -E: Svoboda → Svobodová, Novák → Nováková. Slovak follows the same -ová pattern.
  - **Czech after 2022**: a woman may hold the male form outright (Nováková or Novák), so both must match.
  - **Bulgarian/Macedonian** (after transliteration): -OVA→-OV, -EVA→-EV, -SKA→-SKI. Examples: Ivanova ↔ Ivanov, Petkovska ↔ Petkovski.
  - **Serbian/Croatian -IĆ**: no change.
- Over-normalization risk: some names end in -ova or -ska naturally, so the normalizer should produce candidate keys rather than overwrite the input.

### Gaps
- The amending act number (for example the act amending Act No. 301/2000 Sb. on registers, names and surnames) and the exact section (§69) were not confirmed from the Sbírka zákonů.
- Bulgarian patronymic middle names (father's name + -ов/-ев, -ова/-ева, for example Иван Петров Иванов) and Russian-style -ович forms in Bulgarian were not sourced in this session.

---

## Q11. Common anglicized/variant forms of popular first names and variation patterns

### Takeaway
Variation comes from four sources: (1) which romanization era or system was used (BDS-1973/ICAO/BGN vs the 2009 Streamlined System for Bulgarian; diacritics vs Dj for Serbo-Croatian); (2) ICAO MRZ stripping; (3) English convention (Đ→Dj); and (4) translation to the English cognate (George). The package should generate candidates from (1)–(3) mechanically and from (4) using a curated cognate dictionary.

### Cited Findings
- Forms of George:
  - Bulgarian Георги (Georgi)
  - Macedonian Ѓорѓи (Gjorgji), Ѓорѓе (Gjorgje), Gjorgjija, Gjoko
  - Serbo-Croatian Đorđe (Ђорђе), Đorđo, Đukan, Đurađ, Đurđe, Đoko, Đoka, Đuro, Đura, Georgije (Георгије), Juraj, Jure, Jurica
  - Slovene Jure, Jurij
  - Polish Jerzy (Jur, Jurek, Juras)
  - Czech Jiří
  - Slovak Juraj
  
  — [Wikipedia: George (given name)](https://en.wikipedia.org/wiki/George_(given_name))
- Bulgarian examples under the 2009 law: Георги → Georgi, Жоро → Zhoro (not Joro), Христо → Hristo, Мария → Maria, Илиян → Iliyan. — [pishi.bg](https://pishi.bg/blog/imena-na-latinitsa-zakon/)
- The Й→Y, Ю→YU, Я→YA spellings date from the 1999 ID-document table. Before that (BDS 1596:73) they were J, JU, JA. — [UNGEGN E/CONF.101/12](https://unstats.un.org/UNSD/geoinfo/UNGEGN/docs/10th-uncsgn-docs/econf/E_CONF.101_12_Romanization%20System%20in%20Bulgaria.pdf)
- Djokovic is the conventional English form for Đoković. — [Wikipedia: Gaj's Latin alphabet](https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet)

### Inferences
These candidate sets are derived mechanically from the sourced tables above:
- **Йордан**: Yordan (2009 Act / 1999 table), Jordan (BDS 1596:73 Й→J), Iordan (ICAO generic Й→I). Jordan also coincides with the English/biblical cognate.
- **Георги**: Georgi (Act), with English cognate George. Georgiy/Georgy/Georgii are Russian-style (ICAO/BGN Russian) spellings sometimes applied to Bulgarians. This is an inference; the Russian tables are covered by other researchers.
- **Христо**: Hristo (Act), Khristo (ICAO/BGN 1952 Х→KH).
- **Мария**: Maria (word-final -ия → -ia), Mariya (pre-2006 / BGN 1952 -iya).
- **Цветан**: Tsvetan (Act), Cvetan (pre-2009 per the UNGEGN paper Ц→C; UN 1977 c).
- **Đorđe/Ђорђе**: Djordje (English), Dorde (ICAO MRZ), Đorđe (VIZ), George (cognate). The Macedonian counterpart Ѓорѓи gives Gjorgji/Gjorgi.
- **Jiří**: Jiri (ASCII/MRZ), cognate George.
- **Wojciech**: no diacritics, so it is unchanged in ASCII/MRZ.
- **Jovan/Јован**: Jovan (Gaj = MRZ).

### Gaps
- Anglicized forms such as Wojciech → "Voytek"/"Albert", Jovan → "John", and Polish Łukasz → "Luke" were not sourced. They need a curated cognate list, for example from Wiktionary or a given-name database, which other researchers or later work should source.
- I did not research frequency data showing which variants are most common in real-world records (airline PNRs, sanctions lists).
