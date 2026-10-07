# Romanizing Arabic-script personal names (Arabic language): standards, real-world practice, and variant generation (status as of Oct 2026)

Scope: notes for the `translit-names` Python package. The package has three jobs: (1) romanize under selectable standards, (2) produce a practical, passport-style English spelling, (3) generate realistic spelling variants for search and matching.
Source handling: the primary PDFs (LOC ALA-LC 2012, BGN/PCGN 2019 presentation, the UNGEGN WGRS Arabic report v5.0 2018, ICAO Doc 9303 Part 3 7th ed., the IJMES chart and guide, and Freeman et al. 2006) were downloaded and text-extracted. Tables below are transcribed from those extractions. Where a value comes from a secondary source (Wikipedia, interscript, search snippets), it is labelled.

---

## 1. Full character mapping tables for ALA-LC, IJMES, DIN 31635, ISO 233 / 233-2, BGN/PCGN 1956, UNGEGN 2017, Buckwalter and ICAO Doc 9303

### Takeaway
The scholarly systems (ALA-LC, IJMES, DIN, ISO) and the geographic-names systems (BGN/PCGN, UNGEGN) share consonant identities. They differ in four things: how emphatics are marked (dot below, cedilla, or macron below), whether they use digraphs (th/kh/dh/sh/gh) or single letters with diacritics, how they treat the article (sun-letter assimilation, hyphen, capitalization), and how they render ة and ى. Buckwalter and ICAO MRZ are reversible letter-for-letter schemes: they carry no vowels unless harakat are present, and ICAO marks the letters with no simple Latin equivalent with an "X" escape. Collision warning: the same Latin glyph means different Arabic letters in different standards. ẖ is ح in UNGEGN 2017 but خ in ISO 233. ṯ is ط in UNGEGN 2017 but ث in DIN/ISO. ḏ is ض in UNGEGN 2017 but ذ in DIN/ISO. The package therefore needs one table per standard, never a shared "diacritic" table.

### Cited Findings

**Sources and status of each standard**
- ALA-LC Arabic table: the "2012 version" (earlier versions 2011 and 1997) is the current LOC PDF — [LOC ALA-LC Arabic](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- BGN/PCGN 1956 system: adopted by BGN in 1946 and PCGN in 1956. The "Revised Presentation 2019" was "checked for validity and accuracy – November 2022". It is applied to geographical names of Bahrain, Egypt, Iraq, Jordan, Kuwait, Libya, Oman, Qatar, Saudi Arabia, Syria, UAE, Yemen, the West Bank and Gaza. It is **not** used for Algeria, Chad, Comoros, Djibouti, Lebanon, Mauritania, Morocco, Sudan or Tunisia, "where the spellings used on official Roman-script sources are used" — [BGN/PCGN Arabic (gov.uk)](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- The UN-recommended system was approved in 2017 (res. XI/3). It is based on the 2007 Beirut "Unified Arabic Transliteration System" as amended in Beirut 2008 and Riyadh 2017, and it replaces the UN 1972 system (res. II/8). It is recommended only within Arabic-speaking countries "where this system is officially adopted", and there is evidence of partial implementation in Jordan, Oman and Saudi Arabia. Algeria, Djibouti, Mauritania, Morocco and Tunisia render names in the "traditional manner" following French orthography — [UNGEGN WGRS report, Arabic, v5.0 (2018)](https://www.eki.ee/wgrs/rom1_ar.pdf)
- BGN/PCGN 1956 is "almost identical" to UN 1972. The only differences are the article (BGN: capitalized initially, no hyphen, e.g. "Al Başrah, Ar Riyāḑ"; UN 1972 table: lowercase plus hyphen, "al-Başrah") and the -iyyah ending (BGN: -īyah). UN 2017 differs from UN 1972 in two ways: ظ = d͟h instead of z̧, and the macron below replaces the cedilla — [UNGEGN WGRS report](https://www.eki.ee/wgrs/rom1_ar.pdf)
- DIN 31635 (1982) is based on the DMG rules adopted by the 1935 Rome Orientalist Congress. It uses one sign per letter and no digraphs. The article is written with sun-letter assimilation, ة is -h, or -t in construct, and nunation is ignored — [Wikipedia: DIN 31635](https://en.wikipedia.org/wiki/DIN_31635)
- ISO 233:1984 is a strict letter-to-letter system. Vowels are transliterated only when written with diacritics. ISO 233-2:1993 is a "simplified" system in which words are vocalized before romanization. It is used in French and North African libraries and recommended by ISSN for key titles — [Wikipedia: ISO 233](https://en.wikipedia.org/wiki/ISO_233)
- IJMES uses its own chart for Arabic, Persian and Turkish. For personal names, place names, and party/organization names, "diacritics should not be added… However, ʿayn and hamza should be preserved… (except for initial hamza, which is dropped)" — [IJMES chart](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [IJMES guide](https://www.cambridge.org/core/journals/international-journal-of-middle-east-studies/information/author-resources/ijmes-translation-and-transliteration-guide)
- IJMES policy on famous names has changed over time. The archived 2014 guide said IJMES "no longer follows 'accepted English spellings'… e.g., Jamal ʿAbd al-Nasir" — [IJMES guide, archived 2014](https://web.archive.org/web/20141021063826/http://ijmes.chass.ncsu.edu/IJMES_Translation_and_Transliteration_Guide.htm). The current Cambridge-hosted guide says IJMES follows "accepted English spellings" for prominent figures, e.g. "Gamal Abdel Nasser" — [IJMES guide (current)](https://www.cambridge.org/core/journals/international-journal-of-middle-east-studies/information/author-resources/ijmes-translation-and-transliteration-guide)
- ICAO Doc 9303 Part 3, Section 6, Table C "Transliteration of Arabic Script" (MRZ only) and Appendix B (informative) were read from the Seventh Edition, 2015, with amendment pages dated 16/09/16. The official ICAO URL currently returns 404/Cloudflare. The text was read from a copy hosted at [itftennis.atlassian.net (Doc 9303 Part 3, 7th ed.)](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); official location: [ICAO Doc 9303 p3](https://www.icao.int/publications/Documents/9303_p3_cons_en.pdf)
- Buckwalter is ASCII and strictly one-to-one: و is always w, and ؤ is &. XML-safe variants replace < > &, as I O W. Buckwalter originated in the ALPNET project in 1988 — [Wikipedia: Buckwalter transliteration](https://en.wikipedia.org/wiki/Buckwalter_transliteration). CAMeL Tools publishes BW, Safe-BW, XML-BW and HSB tables — [CAMeL Tools encoding schemes](https://camel-tools.readthedocs.io/en/latest/reference/encoding_schemes.html)

**Master consonant/letter table**

Values come from: ALA-LC from the LOC 2012 PDF; IJMES from the IJMES chart; DIN from Wikipedia DIN 31635 and ICAO App. B; ISO 233 from Wikipedia ISO 233, ICAO App. B and UNGEGN report notes; BGN/PCGN from the 2019 presentation Table 1/2; UNGEGN 2017 from the WGRS report (special characters verified by code point); Buckwalter from ICAO App. B and the CAMeL table; ICAO MRZ from Doc 9303-3 §6 Table C. All URLs are given above.

| Arabic | U+ | ALA-LC | IJMES | DIN 31635 | ISO 233:1984 | BGN/PCGN | UNGEGN 2017 | Buckwalter | ICAO MRZ |
|---|---|---|---|---|---|---|---|---|---|
| ء | 0621 | ’ (U+02BC) medial/final; **not shown word-initially** | ʾ (initial dropped) | ʾ | ˌ (bare hamza, U+02CC) | ’ (U+2019); not word-initial | ’; not word-initial | ' | XE |
| آ | 0622 | ā initial; ’ā medial | — | ʾā | ʾâ | Ā initial; ’ā medial | ā | \| | XAA |
| أ | 0623 | seat not shown; hamza rule as ء | ʾ / dropped initial | ʾ | ˈ (hamza on seat, U+02C8) | as ء | as ء | > | XAE |
| ؤ | 0624 | ’ | ʾ | ʾ | ˈ | ’ | ’ | & | U |
| إ | 0625 | not shown initially (gives i-) | dropped initial | ʾ / i- | (hamza below = alif) | as ء | as ء | < | I |
| ئ | 0626 | ’ | ʾ | ʾ | ˈ | ’ (e.g. Bi’r) | ’ | } | XI |
| ا | 0627 | ā (long vowel); seat/wasla not shown | ā | ā | ʾ (U+02BE), so ā = aʾ | ā | ā (letter not romanized itself) | A | A |
| ٱ | 0671 | not represented | — | — | — | ’ (classical only) | — | { | XXA |
| ب | 0628 | b | b | b | b | b | b | b | B |
| ت | 062A | t | t | t | t | t | t | t | T |
| ث | 062B | th | th (Pers./Turk. s) | ṯ | ṯ | th | th | v | XTH |
| ج | 062C | j | j (Ott./Mod. Turk. c) | ǧ | ǧ | j | j | j | J |
| ح | 062D | ḥ | ḥ | ḥ | ḥ | ḩ (U+1E29) | ẖ (U+1E96) | H | XH |
| خ | 062E | kh | kh | ḫ | ẖ (U+1E96) | kh | kh | x | XKH |
| د | 062F | d | d | d | d | d | d | d | D |
| ذ | 0630 | dh | dh (Pers./Turk. z) | ḏ | ḏ | dh | dh | * | XDH |
| ر | 0631 | r | r | r | r | r | r | r | R |
| ز | 0632 | z | z | z | z | z | z | z | Z |
| س | 0633 | s | s | s | s | s | s | s | S |
| ش | 0634 | sh | sh (Turk. ş) | š | š | sh | sh | $ | XSH |
| ص | 0635 | ṣ | ṣ | ṣ | ṣ | ş (U+015F) | s̱ (s+U+0331) | S | XSS |
| ض | 0636 | ḍ | ḍ (Pers./Ott. ż; Mod. Turk. z) | ḍ | ḍ | ḑ (U+1E11) | ḏ (U+1E0F) | D | XDZ |
| ط | 0637 | ṭ | ṭ (Mod. Turk. t) | ṭ | ṭ | ţ (U+0163) | ṯ (U+1E6F) | T | XTT |
| ظ | 0638 | ẓ | ẓ (Mod. Turk. z) | ẓ | ẓ | z̧ (z+U+0327) | d͟h (d+U+035F+h) | Z | XZZ |
| ع | 0639 | ‘ (ʻ U+02BB) | ʿ (U+02BF) | ʿ | ʿ (U+02BF) | ‘ (U+2018) | ‘ | E | E |
| غ | 063A | gh | gh (Turk. g/ğ) | ġ | ġ | gh | gh | g | G |
| ف | 0641 | f (Maghrebi ڢ also f) | f | f | f | f | f | f | F |
| ق | 0642 | q (Maghrebi ڧ also q) | q (Ott. ḳ; Mod. Turk. k) | q | q | q | q | q | Q |
| ك | 0643 | k | k | k | k | k | k | k | K |
| ل | 0644 | l | l | l | l | l | l | l | L |
| م | 0645 | m | m | m | m | m | m | m | M |
| ن | 0646 | n | n | n | n | n | n | n | N |
| ه | 0647 | h | h | h | h | h | h | h | H |
| و | 0648 | w; ū | w; ū (Pers. v/u; Turk. v) | w; ū | w; (uw) | w; ū | w; ū | w | W |
| ي | 064A | y; ī | y; ī | y; ī | y; (iy) | y; ī | y; ī | y | Y |
| ى | 0649 | á | ā | ā | ỳ | á | á | Y | XAY |
| ة | 0629 | h; t in construct; tan adverbial | a; at in construct | h; t in construct | ẗ (U+1E97) | ah / at (iḑāfah); āh after alif | h; t in construct | p | XTA; **XAH at the end of a name component** |
| ـ (tatweel) | 0640 | omitted | omitted | omitted | omitted | omitted | omitted | _ | not encoded |

Sources for this table: [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf), [IJMES chart](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf), [Wikipedia DIN 31635](https://en.wikipedia.org/wiki/DIN_31635), [Wikipedia ISO 233](https://en.wikipedia.org/wiki/ISO_233), [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf), [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf), [CAMeL encoding schemes](https://camel-tools.readthedocs.io/en/latest/reference/encoding_schemes.html), [ICAO 9303-3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2), [Wikipedia Romanization of Arabic comparison table](https://en.wikipedia.org/wiki/Romanization_of_Arabic)

**Vowel signs, other diacritics, ligatures, article**

| Sign | U+ | ALA-LC | IJMES | DIN | ISO 233 | BGN/PCGN | UNGEGN 2017 | Buckwalter | ICAO MRZ |
|---|---|---|---|---|---|---|---|---|---|
| fatḥa َ | 064E | a | a | a | a | a | a | a | not encoded |
| kasra ِ | 0650 | i | i | i | i | i | i | i | not encoded |
| ḍamma ُ | 064F | u | u | u | u | u | u | u | not encoded |
| ـَا | — | ā | ā | ā | aʾ ("a'") | ā | ā | aA | A |
| ـِي | — | ī | ī | ī | iy | ī | ī | iy | Y |
| ـُو | — | ū | ū | ū | uw | ū | ū | uw | W |
| ـَيْ | — | ay | ay or ai | ay | ay | ay | ay | ayo | Y |
| ـَوْ | — | aw | aw or au | aw | aw | aw | aw | awo | W |
| sukūn ْ | 0652 | not shown | — | — | º (per ICAO App. B) | not romanized | not romanized | o | not encoded |
| shadda ّ | 0651 | double the letter/digraph; special: ـُوّ = ūw, ـَوّ = aww, medial ـِيّ = īy, final ـِيّ = ī, ـَيّ = ayy | -iyy (final ī), -uww (final ū) | double | ¯ per ICAO App. B (interscript implementation doubles instead) | double; but final -iyy = ī, -iyyah = **īyah**, -iyyīn = īyīn | double (-iyyah kept) | ~ | doubled (e.g. عبّاس → EBBAS) |
| tanwīn ً ٍ ٌ | 064B/D/C | an/in/un only for defective-root nouns and adverbial use; else ignored | — | ignored | á / í / ú | an/in/un "when necessary"; not in modern names | ignored (Jabal, not Jabalun) | F / K / N | not encoded |
| dagger alif ٰ | 0670 | ā (long vowels always marked even if written defectively: Allāh, dhālika) | — | ā | ā | ā (Allāh) | ā | ` | not encoded |
| لا lām-alif | 0644+0627 | lā | lā | lā | lā | lā (Note 10) | lā | lA | LA |
| ال article | — | **al-** always, lowercase, hyphen, **no sun-letter assimilation** (al-Shams); li+al = lil- | al- and -l- (wa-l-), no assimilation | al- with assimilation (aš-Šams) | letter-by-letter | **Al** initial capital, no hyphen, **assimilated** (Ar Riyāḑ, Ash Shām); medial "al" lowercase | **assimilated**, always capitalized (Ash Shāriqah, Minyat Aḏ Ḏinniyyah) | Al | AL (no assimilation) |
| digraph separator | — | prime ʹ (Adʹham, akramatʹhā) | — | n/a | n/a | middle dot k·h, d·h, s·h, t·h; a·h for non-ة "ah" | middle dot (S·haylah, Ad·ham) | n/a | n/a |

Sources: [LOC rules 6–21](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf); [IJMES chart](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [BGN/PCGN Notes 3–11 & Special Rules](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf); [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf); [ICAO 9303-3 Table C + App. B](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [Wikipedia DIN 31635](https://en.wikipedia.org/wiki/DIN_31635)

**ALA-LC rules that matter for names (verbatim substance, LOC 2012)**
- Rule 8(a): hamza in initial position, including after a prefix or the article, is not represented. Medial and final hamza are written ’ (e.g. mas’alah, dā’im) — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 7: ة is h when indefinite or after the article (ṣalāh, al-Risālah), t in construct (Wizārat al-Tarbiyah), and tan when adverbial — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 6: ى (alif maqṣūrah) is á, as in Muṣṭafá and Yaḥyá. Final ـِيّ in the nisbah and in fāʿīl forms from defective roots is ī, not īy (al-Miṣrī, Raḍī al-Dīn); compare al-Miṣrīyah — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 17: "al" is always "al" regardless of the preceding vowel (Abū al-Wafā’), and the l is never assimilated (Abū al-Layth al-Samarqandī). Exception: li + article = lil- (lil-Shirbīnī) — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 18: English capitalization, except that the article al is lowercase in all positions — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 19: long vowels are always marked, even when written defectively: Ibrāhīm for both إبرهيم and إبراهيم; Dā’ūd for both داود and داؤود — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 23: الله is Allāh; also billāh, lillāh, bismillāh — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 24: irregular names: طه Ṭāhā; يس / يسن Yāsīn; **عمرو ‘Amr** (silent final و); بهجة / بهجت Bahjat — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- Rule 25: ابن and بن are both "ibn" in all positions. Exception: "modern names, typically North African, in which the element بن is pronounced bin": Bin Khiddah, Bin-‘Abd Allāh (بنعبد الله). Rule 20(c) hyphenates bin to the next element when the Arabic writes them as one word — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)
- ALA-LC non-Arabic letters: گ g, ڴ ñ, چ ch/zh, پ p, ژ zh, ڤ / ۋ / ڥ v — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)

**BGN/PCGN rules that matter for names (2019 presentation)**
- Special Rule 4: names that are noun phrases are written as separate words, and the medial article is "al", not "ul": ‘Abd Allāh, ‘Abd ar Raḩmān, Dhū al Faqār — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Special Rule 5: بن written without alif between two proper nouns is **Bin** ("‘Umar Bin al Khaţţāb"); ابن with alif is **Ibn** — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Special Rules 6–8: Turkish Paşa is Bāshā. Bey stays "Bey" in Egyptian names; elsewhere بك is Bak and بيك is Bayk. Colloquial Sīdī is preferred to Sayyidī. Colloquial Bū is not "corrected" to Abū — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Special Rule 2: li + article = lil (Mişr liţ Ţayarān; lil Maghāzil); bi + article = bil/bid (Al Qaryah bid Duwayr) — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Note 11: initial او is Ū in non-Arabic-origin words and Aw otherwise; initial اي is Ī; medial/final āw / āy — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Table 3 (non-standard letters): پ p, چ ch, ڤ v, ڨ g (Tunisian), گ g ("used principally in Iraq"), ڭ g (Moroccan) — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Table 4: Arabic-Indic digits ٠–٩ become 0–9, and numbers are written left to right — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)

**ICAO Doc 9303-3 specifics (7th ed.)**
- Table C covers Arabic plus Persian, Urdu and Pashto letters. ٹ XXT, ټ XRT, پ P, ځ XKE, څ XXH, چ XC, ڈ XXD, ډ XDR, ڑ XXR, ړ XRR, ږ XRX, ژ XJ, ښ XXS, ک (keheh) XKK, ګ XXK, ڭ XNG, گ XGG, ں XNN, ڼ XXN, ھ XDO, ۀ XYH, ہ XXG, ۂ XGE, ۃ XTG, ی (Farsi yeh) XYA, ۍ XXY, ې Y, ے XYB, ۓ XBE. ڜ, ڢ, ڧ and ڨ are "Not encoded" — [ICAO 9303-3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- App. B.5.3: "X" is an escape character placed **before** the letter it modifies (XTH), unlike the Latin-diacritic convention (NXX for Ñ). Operators are told to ignore X characters and to expect missing vowels. The MRZ does not reflect sun-letter assimilation: "AL-RAZI" may be "AR-RAZI" in the VIZ. On shadda: "Search algorithms should take into account that the 'shadda' may not always be present" — [ICAO 9303-3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- App. B.5.5: the X-scheme is based on Buckwalter. ح (XH) and ه (H) were swapped on Interpol's advice. ة is XTA generally but XAH when it ends a name component, "because feminine names often use teh marbuta… e.g. فاطمة (Fatimah). Search algorithms should take these two possibilities into account". Farsi yeh (ی) "could be transliterated as 'Y' or 'XAY'" — [ICAO 9303-3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- Worked example, ابو بكر محمد بن زكريا الرازي: VIZ "Abū Bakr Mohammed ibn Zakarīa al-Rāzi"; phonetic MRZ "ABU<BAKR<MOHAMMED<IBN<ZAKARIA<AL<RAZI"; X-scheme MRZ "ABW<BKR<MXHMD<BN<ZKRYA<ALRAZY"; Buckwalter "Abw<bAkr<mHmd<bn<zkryAY<AlrAzY" (sic) — [ICAO 9303-3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- A machine-readable ICAO map exists in interscript (`icao-fas-Arab-Latn-9303.isc`), but it disagrees with the primary text: ة → "P", and the harakat produce output. **Do not use it as ground truth** — [interscript ICAO map](https://github.com/interscript/maps/blob/main/maps/icao-fas-Arab-Latn-9303.isc)

**Buckwalter (complete; reversible)**

ء `'` · آ `|` · أ `>` · ؤ `&` · إ `<` · ئ `}` · ا `A` · ب `b` · ة `p` · ت `t` · ث `v` · ج `j` · ح `H` · خ `x` · د `d` · ذ `*` · ر `r` · ز `z` · س `s` · ش `$` · ص `S` · ض `D` · ط `T` · ظ `Z` · ع `E` · غ `g` · ـ `_` · ف `f` · ق `q` · ك `k` · ل `l` · م `m` · ن `n` · ه `h` · و `w` · ى `Y` · ي `y` · ً `F` · ٌ `N` · ٍ `K` · َ `a` · ُ `u` · ِ `i` · ّ `~` · ْ `o` · ٰ `` ` `` · ٱ `{` · پ `P` · چ `J` · ڤ `V` · گ `G`.
Safe-BW replaces non-alphanumerics: ء C, آ M, أ O, ؤ W, إ I, ئ Q, ذ V, ش c, ٰ e, ٱ L, ڤ B. HSB uses Unicode letters: ة ħ, ث θ, ذ ð, ش š, ع ς, غ γ, ى ý, and so on — [CAMeL Tools encoding schemes](https://camel-tools.readthedocs.io/en/latest/reference/encoding_schemes.html); [ICAO 9303-3 App. B.5.2](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)

**ISO 233-2 (1993) details known from secondary sources**
- In interscript's implementation, ISO 233-2 uses ā, ī, ū for long vowels (not the aʾ/iy/uw of ISO 233:1984), keeps ẗ for ة, ỳ for ى, and the consonants ṯ ǧ ḥ ẖ ḏ š ṣ ḍ ṭ ẓ ‘ ġ. Maghrebi ڢ is f and ڨ is q. The article is written "al-", with "bi-" and "li-l-" prefixes — [interscript iso-ara-Arab-Latn-233-2-1993](https://github.com/interscript/maps/blob/main/maps/iso-ara-Arab-Latn-233-2-1993.isc). This was not verified against the ISO text, which is paywalled.

**ODNI / US Intelligence Community standard ICS 630-01 (2015), a "practical" ASCII standard for Arabic personal names**
- It uses the 26 English letters plus an apostrophe. Short and long vowels are not distinguished (Samir). Shadda is doubled except for ‘ayn and digraph letters (al-Qadhafi, not al-Qadhdhafi; Mubashir, not Mubashshir). Hamza and ‘ayn are both ’. ة is t in construct and h otherwise. The article follows spelling, not pronunciation ('Abd-alRahman, not 'Abd-ar-Rahman). Diphthongs are y/w (Haytham, Faysal, Tawfiq). Name elements are hyphenated (’Abd- al Rahman, Abu-al-Bashar, Bin-Ladin), except Allah compounds ('Abdallah, Nasrallah, never 'Abdullah) and the family marker Al (Al Thani). "al" is not "ul" (Nur-al-Din). بن is Bin, or Ibn when written with alif. Colloquial Bu is not standardized to Abu. MSA spelling overrides local pronunciation (Egyptian "Gamal" is written "Jamal"). Already-known spellings are kept in parentheses (e.g. "Muhammad Khulud (Mohamed Khulood)") — [interscript odni-ara-Arab-Latn-2015 (quotes ICS-630-01 Annex A)](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc)

### Inferences
- Implement each standard as a separate rule set over a **vocalized** internal representation, with tokens like C, V, shadda, ة-state and article flags, rather than as a character map. ALA-LC, BGN and UN all need context such as construct state for ة, word-initial hamza, sun letters, and final -iyy.
- BGN/PCGN and UN 1972 share all letters. UN 2017 is a letter-level diff (ح ẖ, ص s̱, ض ḏ, ط ṯ, ظ d͟h) plus article capitalization and -iyyah. DIN and Hans Wehr are close to ISO 233-2 in practice. IJMES equals ALA-LC except ة = a/at, optional au/ai, no macrons/dots in names, and ʿ/ʾ (not ‘/’).
- Store diacritic outputs in NFC, but generate ASCII fallbacks by stripping combining marks (NFD, then drop Mn). Be aware that BGN's ţ/ş/ḑ/ḩ/z̧ (cedilla) and UN's macron-below letters strip to the same ASCII as ALA-LC's dot-below letters. That is good for matching but irreversible.
- For an "ICAO" mode, offer two outputs: (a) phonetic VIZ/MRZ (ABU<BAKR<MOHAMMED…), which most states actually use, and (b) the ICAO X-scheme. The X-scheme needs no vocalization and is a good stable **matching key** because it is reversible.

### Gaps
- The full ISO 233:1984 and ISO 233-2:1993 texts (paywalled) and the DIN 31635:2011 text were not accessed. Hamza-seat handling in ISO 233 (whether the seat letter is also transliterated) and ISO 233 shadda handling (macron vs doubling) are uncertain because the ICAO App. B table and the interscript implementation disagree.
- Not verified whether Doc 9303 **8th edition (2021)** keeps Table C and Appendix B unchanged. The official PDF could not be fetched (404/Cloudflare).
- The UNGEGN 2017 Annex tables (E/CONF.105/137/CRP.137) were not fetched. The values here come from the WGRS summary report v5.0 (2018).

---

## 2. Vocalization: the core problem and how tools handle it

### Takeaway
Arabic names are normally written without short vowels or shadda. Every non-reversible romanization therefore needs a vocalization step first. Primary standards (BGN/PCGN, UNGEGN, ODNI) explicitly assume a human or a dictionary supplies the "proper pointing". Commercial name systems (CJKI ARAN/DAN) use a lexicon first, fuzzy lexicon lookup second, and rule-based generation last. General-purpose diacritizers (CAMeL Tools, Mishkal, Farasa, neural models) are tuned to running text and have non-trivial error rates, which strongly favours a **name dictionary + fallback** design.

### Cited Findings
- BGN/PCGN: "Uniform results… are difficult to obtain, since vowel points and diacritical marks are generally omitted… knowledge of its standard Arabic-script spelling including proper pointing… [is] essential" — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- ICAO: محمد is written with four consonants, "Mhmd". Vowels "are added at the discretion of the translator", and harakat "are normally omitted" — [ICAO 9303-3 App. B.1](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- ODNI ICS-630-01: linguists use "on-line tools and name dictionaries to determine the exact Arabic and the appropriate transliteration". The system is to be used "in conjunction with on-line tools, name dictionaries, and lists containing conventional spellings of names of well-known individuals" — [interscript ODNI map](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc)
- Halpern's ARAN pipeline: (1) transliterate to Buckwalter, (2) exact lookup in the Database of Arabic Names (DAN), (3) fuzzy DAN lookup, (4) algorithmic candidate generation, (5) output a candidate list. Modules: ADAN diacritizer, ATAN phonemic, AXAN graphemic, APAN phonetic, AVAN variant generator. Example: إبراهيم produces popular forms "Ibrahiim, Ibrahim, Ebraheem, Ebrahiim…" and pure-generation candidates "ibraahiim, ibaraahiim, ibiraahiim, iburaahiim". Fuzzy matching such as "ignoring hamza and collapsing 'alif with 'alif maqSuura is a bit risky". DAN had ~180,000 variants at the time of that paper — [Halpern, Challenges and Pitfalls of Arabic Romanization and Arabization](https://www.cjki.org/arabic/arannana.pdf)
- Halpern's literature summary: Arbabi et al. (1994) built a knowledge-base plus neural-network diacritizer with a 3.1% error rate that "rejects 55% of the names as unprocessable". Gal's HMM had a 14% error rate. Elshafei et al. (2006) reported 5.5% — [Halpern (CJKI)](https://www.cjki.org/arabic/arannana.pdf)
- DAN later grew. The DAN paper says it "currently contains over five million entries" of romanized names mapped to Arabic — [Halpern, Lexicon-Driven Approach](https://www.cjki.org/reference/danpaper.pdf). The CJKI XOFAC brochure, an undated document, says 2.4 million entries — [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf). The figures come from different dates.
- CAMeL Tools (v1.6.0 docs, © 2018–2026, NYU Abu Dhabi):
  - `MLEDisambiguator.pretrained()` defaults to the 'calima-msa-r13' model. It does a word-based MLE lookup, then falls back to analyzer pos-lex probabilities, and returns analyses that include the diacritized form.
  - `BERTUnfactoredDisambiguator` is based on Inoue, Khalifa & Habash (ACL Findings 2022).
  - Also provided: `dediac_ar`, the normalizers `normalize_alef_ar`, `normalize_alef_maksura_ar`, `normalize_teh_marbuta_ar` and `normalize_unicode` (NFKC by default), and CLI transliteration schemes ar2bw / ar2safebw / ar2xmlbw / ar2hsb and their reverses.
  - Install with `pip install camel-tools`; data is installed with `camel_data -i light|defaults|all`.
  - Sources: [MLE](https://camel-tools.readthedocs.io/en/latest/api/disambig/mle.html); [BERT](https://camel-tools.readthedocs.io/en/latest/api/disambig/bert.html); [normalize](https://camel-tools.readthedocs.io/en/latest/api/utils/normalize.html); [dediac](https://camel-tools.readthedocs.io/en/latest/api/utils/dediac.html); [camel_transliterate](https://camel-tools.readthedocs.io/en/latest/cli/camel_transliterate.html); [getting started](https://camel-tools.readthedocs.io/en/latest/getting_started.html)
- Diacritizer comparisons (from search summaries; full papers not read): an evaluation of six diacritization models in Annals of Computer Science and Information Systems vol. 43 (FedCSIS) reports CAMeL Tools and Mishkal with comparatively higher error rates than Shakkelha and Fine-Tashkeel — [annals-csis.org Vol. 43](https://annals-csis.org/Volume_43/drp/4862.html). An earlier paper reports the neural Shakkala at DER 2.88% vs 13.78% for the best non-neural tool (Mishkal) — [arXiv:1905.01965](https://arxiv.org/abs/1905.01965v1). A third study found Farasa outperforming MADAMIRA — [jlcl.org](https://jlcl.org/article/download/213/211)
- Halpern lists ambiguity sources beyond short vowels:
  - long ā can be written ا, آ or ى;
  - long vowels are sometimes omitted (dagger alif);
  - shadda is omitted (محمد gives no clue that m is doubled);
  - hamza seats vary;
  - ى/ي alternate ("especially in Egypt");
  - ه/ة alternate;
  - compound names are written solid or open (عبدالرحيم / عبد الرحيم);
  - the bare string مو has ~40 consonant-vowel permutations.
  - Sources: [Halpern ARAN](https://www.cjki.org/arabic/arannana.pdf); [Halpern DAN](https://www.cjki.org/reference/danpaper.pdf)
- ALA-LC Rule 19 shows that defective spellings must be normalized to the full vocalized lemma (إبرهيم and إبراهيم both give Ibrāhīm; داود and داؤود both give Dā’ūd) — [LOC](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf)

### Inferences
- Recommended architecture:
  1. Normalize (section 9).
  2. Compute a consonantal **skeleton key**: alef forms → ا, ى → ي, ة → ه, strip harakat and tatweel.
  3. Look up a curated name lexicon: skeleton → list of (vocalized form with shadda, frequency, gender, region notes, conventional spellings).
  4. If the input is partially vocalized, filter candidates by the given harakat.
  5. Fallback: optional CAMeL MLE `diac` (extra dependency), then a heuristic vocalizer using name morphological templates. Common name patterns such as faʿīl (Saʿīd, Rashīd, Karīm), fāʿil (Khālid, Ṭāriq), mafʿūl (Maḥmūd), mufaʿʿal (Muḥammad) and faʿʿāl (Ḥassān) can be matched against the root letters and ي/ا/و positions.
  6. Return candidates ranked by prior.
- Keep vocalization ambiguity explicit in the API (e.g. `romanize(..., all_readings=True)`). The classic collision حسن Ḥasan vs حسّان Ḥassān both become "Hassan" in English (section 8).
- CAMeL Tools is heavy (C++ deps, data downloads), so make it an optional extra (`translit-names[camel]`) rather than a hard dependency.

### Gaps
- No published accuracy figures for diacritizers on **personal names specifically** were found. All comparisons found are on running text.
- Licensing and availability of large Arabic name lexicons (CJKI DAN is commercial) was not researched. An open-source substitute (e.g. names mined from Wikidata with Arabic and English labels) was not evaluated.

---

## 3. Arabic name structure (ism, nasab, laqab, kunya, nisba, Āl) and its effect on romanization and matching

### Takeaway
A full classical name is ism + nasab chain (ibn/bint) + kunya (Abū/Umm) + laqab + nisba (al-…ī). Modern documents usually reduce this to given name + father's name + grandfather's name + family/tribal name. Particles like ibn/bin/ben, Abū/Abu/Abou/Bou, Umm and al-/Āl must be tokenized as separate, optional, variant-bearing elements. Two-word theophoric given names (ʿAbd + X) must never be split into "Abdul" + surname.

### Cited Findings
- Ism is the given name. Nasab is the patronymic via ibn ("son of", colloquially bin) or bint ("daughter of"); Fischer (1995) notes ibn/bint are omitted "in almost all Arab countries". Laqab is an epithet or honorific, today largely the family name (e.g. Ṣalāḥ al-Dīn, Nūr al-Dīn). Nisba is a tribal/place/profession adjective (al-Halabi "from Aleppo", al-Khayyat "the tailor"). Kunya is Abū/Umm + child's name (Abu Nidal) — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- Dynastic "Āl" (آل, family/clan) is distinct from the article ال. If the Arabic has آل as a separate word, write "Al" capitalized with a space and no hyphen ("Bandar bin Abdulaziz Al Saud"). أهل is "Ahl". Dynasty membership does not imply Āl (Bashar al-Assad) — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- ODNI also treats "Al" (lineage/family marker) as unhyphenated (Al Thani) — [interscript ODNI](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc)
- Common errors: "Abdul" is not a name by itself ("Mr. Rahman" is wrong for Abdul-Rahman). Habībullāh is wrongly split into forename Habib + surname Ullah. Jalālu-d-dīn is wrongly split into "Jalal Uddin" / "Mr. Uddin" — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- Muhammad is so frequent that South and Southeast Asia abbreviate it "Md.", "Mohd.", "Muhd." or "M.", and people are then called by their second name — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- Chicago Manual of Style indexing: alphabetize under Abu, Abd and ibn, but not under al-/el- (use the following element) — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- Grammatical case alters particles: Abū becomes Abī in genitive iḍāfah (Shāri‘ Abī Bakr). The same applies to Banū/Banī and Dhū/Dhī. BGN keeps the authoritative written form — [BGN/PCGN Special Rule 11](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- بن/ابن: ALA-LC always uses "ibn" except modern North African "Bin" — [LOC rule 25](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf). BGN and ODNI use "Bin" when written without alif and "Ibn" when written with alif — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf); [ODNI](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc)
- ICAO notes "ibn" as "bin" and "al" as "el" multiply variants: 32 variants of Mohammed × Zakaria/Zakariya × ibn/bin × al/el give "256 alternatives" — [ICAO 9303-3 App. B.2.2](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- Real OFAC data shows Maghrebi particles. "Mohamed Ben Belgacem AOUADI" has OFAC alias "Mohamed Ben Belkacem AOUADI". CJKI found attested aliases "Muhammad Bin Belgacem AWADI" and "Mohamed Ben Belgacem AL AOUADI": Ben/Bin, g/k for ق, ou/aw for و, and an optional article — [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf)
- Compound name elements (عبد, ابو, بن) are written either attached or detached (عبدالرحيم vs عبد الرحيم). عبد العزيز has eight Arabic-script variants — [Halpern DAN paper](https://www.cjki.org/reference/danpaper.pdf)

### Inferences
- Token classes to model:
  - `PARTICLE_NASAB` {بن, ابن, بنت, ولد (Maghreb/Mauritania)}
  - `PARTICLE_KUNYA` {ابو, أبو, ابي, أبي, ابا, بو, ام, أم}
  - `ARTICLE` {ال attached}
  - `FAMILY_MARKER` {آل}
  - `THEOPHORIC_HEAD` {عبد}
  - `COMPOUND_TAIL` {الدين, الله, …}
  - `NISBA` (ending ـي after the article)
- Romanization of particles by profile:
  - nasab: ibn / bin / ben / b. / bint / binti (Malay)
  - kunya: Abu / Abou / Abo / Bou / Bu / Ebu (Turkish); Umm / Um / Oum / Om
  - article: al / el / ul / Al / El / assimilated forms
- For matching, particles should be optional or low-weight tokens. The nasab chain makes token-order and token-count mismatches common (passport may show 4 names, list entry 2).
- Detect آل **before** alef normalization. NFKC does not touch آ, but `normalize_alef_ar`-style folding turns آل into ال and loses the distinction between "Al Saud" (family) and "al-Saud" (article).

### Gaps
- No primary national civil-registry spec was found describing which name slots (first/father/grandfather/family) map to passport primary/secondary identifiers, country by country.

---

## 4. The definite article al-: sun letters, surface forms, capitalization and hyphenation, passport rendering, and dropping it in matching

### Takeaway
Sun letters are the 14 letters ت ث د ذ ر ز س ش ص ض ط ظ ل ن. Standards split on assimilation. ALA-LC, IJMES, ODNI and the ICAO MRZ keep "al" (al-Shams, al-Rahman). BGN/PCGN, UNGEGN and DIN assimilate (ash-Shams / Ash Shams, ar-Rahman). Popular and passport forms add al/el/ul, hyphen/space/solid, and Al/AL/El/EL. Matching should treat the article as optional and fold all its forms.

### Cited Findings
- BGN sun letters: "t, th, d, dh, r, z, s, sh, ş, ḑ, ţ, z̧, l, or n". The l is assimilated "in pronunciation and romanization" (Ar Riyāḑ, not Al Riyāḑ). The initial article is capitalized with no hyphen (Ash Shāriqah); the medial article is lowercase (Tall al Laḩm). If sources conflict on including the article, prefer the form with it — [BGN/PCGN Special Rule 1](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- UN 2017: assimilation (Ash Shāriqah), and the article is "always written with a capital initial", even medially (Minyat Aḏ Ḏinniyyah) — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf)
- ALA-LC: "al" is always hyphenated, always lowercase, never assimilated (Abū al-Layth al-Samarqandī) — [LOC rules 17–18](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf). IJMES writes the article "al- and -l-" — [IJMES chart](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf)
- The Survey of Egypt System always writes the article "el-" (El-Kafr el-Qadîm, Sharm el-Sheikh) — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf)
- The article's vowel is unstressed "and can be transliterated by almost any vowel, often by u" (Abdul Qadir, Abdul Rahman) — [Wikipedia: Abd al-Rahman](https://en.wikipedia.org/wiki/Abd_al-Rahman); [Wikipedia: Abdul Qadir](https://en.wikipedia.org/wiki/Abdul_Qadir)
- Wikipedia's chat-alphabet column gives el/al/æl for ال. UN/ALA-LC prefer lowercase plus hyphen (al-Baṣrah, ar-Riyāḍ); BGN/PCGN prefers "Al Baṣrah, Ar Riyāḍ" — [Wikipedia: Romanization of Arabic](https://en.wikipedia.org/wiki/Romanization_of_Arabic)
- ICAO MRZ: hyphens become a single filler "<", so AL-SAYED is written AL<SAYED. Apostrophes are dropped without a filler, and other punctuation is dropped. The ICAO phonetic example writes the article as its own component (…<AL<RAZI). The X-scheme writes it attached (ALRAZY) and does not assimilate — [ICAO 9303-3 §4.6, App. B](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- ICAO counts al/el as one of the binary variant dimensions that drive the 256-alternatives example — [ICAO 9303-3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- Indexing practice ignores al-/el- (Chicago) — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- Attested surface forms in name variant lists include: Al-Rashid, ar-Rashid, Al-Rasheed — [Wikipedia: Rashid](https://en.wikipedia.org/wiki/Rashid); Al-Waleed, al-Walid — [Wikipedia: Waleed](https://en.wikipedia.org/wiki/Waleed); Nur ad-Din, Nur-ud-Din, Nur al-Din, Noureddine — [Wikipedia: Nur al-Din](https://en.wikipedia.org/wiki/Nur_al-Din); Salah ad-Din, Salahu’d-Din, Ṣalāḥ ud-Dīn, Salah ed-Din — [Wikipedia: Salah ad-Din (name)](https://en.wikipedia.org/wiki/Salah_ad-Din_(name))

### Inferences
- The article generator should cross:
  - vowel ∈ {a, e, u, i(rare), ∅}
  - assimilation ∈ {none (al-Rahman), assimilated (ar-Rahman), doubled consonant without l (arrahman, as in Abdurrahman)}
  - joiner ∈ {"-", " ", "" (solid), "’" (Salahu’d-Din)}
  - case ∈ {al, Al, AL, el, El, EL}
- Expected passport-style outputs for السيد: AL SAYED, AL-SAYED, ALSAYED, EL SAYED, EL-SAYED, ELSAYED, AS SAYED, ASSAYED, ES SAYED, plus base variants SAYED/SAYYED/SAYID/SAEED-type spellings from the vowel rules. These are generated by rule from the cited conventions, not attested as a list.
- Matching: normalize by (a) removing a leading article token (al, el, ul, il, plus the 14 assimilated forms like as/ash/ad/ar/an/at/az/es/ed/er/en/et/ez) **only if** the remainder starts with the corresponding consonant, and (b) splitting solid forms (Alsayed → al + sayed; Abdulrahman → abd + al + rahman). Keep the article-stripped form as a secondary key, scored slightly below an exact match. BGN's "prefer the form with the article" rule supports treating presence/absence as a soft difference.
- Guard against false article detection: names that genuinely start with "Al"/"El" (e.g. Alia, Elias, Alam) must not lose their first syllable. Only strip when the Arabic source has ال, or when the Latin token is followed by a hyphen or space.

### Gaps
- No primary statistics were found on how often specific states print the article solid vs hyphen vs space in passports. No country-specific passport rule on article rendering was found (for example, whether Egyptian passports systematically use "EL").

---

## 5. Theophoric and compound names (ʿAbd al-X, X al-Dīn, X-allāh): forms and variant-generation rules

### Takeaway
ʿAbd + al + divine-attribute and X + al-Dīn/-allāh compounds produce the largest variant families: Abd al-Rahman alone has more than a dozen attested romanizations, and CJKI counts more than 1,100 for ʿAbd al-Raḥīm and ʿAbd al-Razzāq. Variation comes from the article vowel (a/e/u/i), sun-letter assimilation, spacing/hyphenation/solid writing, final French "-e", and the vowels and consonants of the second element.

### Cited Findings
- Abd al-Rahman (عبد الرحمن, occasionally عبد الرحمان): "Alternative transliterations include Abdelrahman, Abd al-Rahman, Abdul Rahman, Abdur Rahman, Abdurrahman or Abdrrahman, Abd ar-Rahman, Abdulrahman, Abdur Rehman, Abdul Rehman, Abidur Rahman… all subject to variant spacing and hyphenation" — [Wikipedia: Abd al-Rahman](https://en.wikipedia.org/wiki/Abd_al-Rahman)
- Abdullah variants: "Abdallah, Abdellah, Abdollah, Abdullah and many others" — [Wikipedia: Abdullah (name)](https://en.wikipedia.org/wiki/Abdullah_(name)). ODNI prescribes 'Abdallah (not 'Abdullah) and 'Abd al Rahman/'Abd-al-Rahman with no assimilation, and Nur al Din — [interscript ODNI](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc). BGN: ‘Abd Allāh, ‘Abd ar Raḩmān — [BGN/PCGN](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- Nur al-Din: نور is Nur/Noor/Nor/Nour/Nuer, and دين is Din/Deen/Dine. Popular forms: Nuraddin, Nureddin, Noureddin, Noureddine, Nooradeen, Nordeen, Nourdin, Noordine, Nordine, Nuradin, Nurdin, Nooruldeen. Scientific forms: Nur ad-Din, Nur-ud-Din, Nur al-Din — [Wikipedia: Nur al-Din](https://en.wikipedia.org/wiki/Nur_al-Din)
- Abdul Qadir: the second part can be "Qader, Kadir, Qadir, Kader, Gadir or in other ways, and the whole name subject to variable spacing and hyphenation" — [Wikipedia: Abdul Qadir](https://en.wikipedia.org/wiki/Abdul_Qadir)
- Salah ad-Din: Salahu’d-Din, Ṣalāḥ ud-Dīn, Salah ed-Din — [Wikipedia: Salah ad-Din (name)](https://en.wikipedia.org/wiki/Salah_ad-Din_(name))
- CJKI: عبدالرحيم and عبدالرزاق "have over 1100 variants". عبد العزيز عودة (OFAC "Abd Al Aziz AWDA") has "over 4000 Arabic and Roman variants". Hatim Ahmad BARAKAT has ~130,000 actual and potential full-name variants — [Halpern DAN paper](https://www.cjki.org/reference/danpaper.pdf); [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf)
- "Abdul" is not a standalone name, and "Uddin"/"Ullah" are not surnames — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)
- ʿAbd is usually not combined with the Prophet's names, though some areas accept it. Christians use Abdul-Massih (عبد المسيح) — [Wikipedia: Arabic name](https://en.wikipedia.org/wiki/Arabic_name)

### Inferences
- Variant-generation grammar for `عبد` + `ال` + `X` (rule-derived from the attested forms above; N = the first consonant of X):
  - **Head**: Abd, Abdu, Abdo (Egypt), Abid (rare, e.g. "Abidur"), Ebd (rare)
  - **Article**: al, el, ul, il, or assimilated vowel+N (ar/er/ur/ir before r; as/es/us before s; ash/esh/ush before sh; ad/ed/ud before d; an/en/un before n; at/et/ut before t; az/ez/uz before z)
  - **Joiner** between head and article: "", " ", "-", "-ul-"-style double hyphen
  - **Joiner** between article and X: "", " ", "-"
  - **Contractions**: Abdul + X, Abdel + X, Abdal + X, Abdol + X (Persian); assimilated solid forms Abdurrahman, Abderrahmane, Abdessalam, Abdennour, Abdelkader. When X starts with a sun letter, also generate the "Abdur Rahman" / "Abdus Salam" / "Abdush Shakur" family.
  - **French/Maghreb tail**: append "e" after a final nasal or consonant (Abderrahmane, Noureddine, Abdelkrim, Abdelhamide is rare). Use ou for u and ch for sh, and drop the vowel in Abdelkrim (كريم → krim).
  - **Allah compounds** (عبد الله, نصر الله, فتح الله, حبيب الله, …): -allah / -ullah / -ellah / -illah / -ollah (Persian) / -alla / -ulla (Central Asia). Joiners: solid, space ("Abdul Lah" is rare) or hyphen. Never generate "Allah" as a separate surname token for matching.
  - **X al-Dīn compounds** (نور الدين, صلاح الدين, شمس الدين, سيف الدين, عز الدين, علاء الدين, بهاء الدين, جمال الدين, خير الدين, …):
    - head: Nur/Noor/Nour; Salah/Saladin; Shams/Chams; Saif/Sayf/Seif; Izz/Ezz/Izz/Iz; Ala/Alaa/Aladdin; Baha/Bahaa; Jamal/Gamal/Djamal/Djamel; Khair/Khayr/Kheir/Hayr;
    - article+din: ad-Din, ud-Din, ed-Din, eddine (Maghreb), eddin, uddin (South Asia), al-Din, -addin, -adin, -deen, -dine; solid or spaced.
- Cap the cross-product and rank by attested frequency. Each slot has 3–10 options, so the product easily exceeds 1,000 (consistent with CJKI's counts). The package should return a top-k list for display and use **pattern/skeleton matching** (section 10) rather than enumerating every variant for search.
- Parse in reverse too: when an input Latin name contains Abdul/Abdel/Abdur/Abdus/Abd-/Abd al-, re-segment it into (head, article, X) before comparing.

### Gaps
- No corpus-derived frequency ranking of compound variants (e.g. Abdulrahman vs Abdelrahman share by country) was found in a primary or open source.

---

## 6. Regional practice differences and a per-letter variation table

### Takeaway
Popular spellings follow the orthography of the colonial or education language and local pronunciation. English-influenced (Gulf, Levant, Iraq, Sudan, South Asia): sh, kh, j, ee/oo. Egyptian: g for ج, e/o vowels, el-, -a. French-influenced (Maghreb, Lebanon, West Africa): ou, ch, dj, gu, ss, final -e, Ben. Turkish, Persian, Urdu, Malay, Russian/Caucasian and Somali forms re-spell Arabic names through their own orthographies (Mehmet, Hossein, Usman, Achmad, Magomed, Maxamed). The variant generator should be profile-based, with per-letter equivalence classes.

### Cited Findings

**French-based IGN 1973 ("Variant B of the Amended Beirut System") equivalences to the UN system**: a = a/e/é/è (by local pronunciation); ā = â/ê; ī = î/ê; i = i/e; u = ou/o; ū = oû/ô; j = dj/j; q = q/g/gu ("gu before e and i"); s = s/ss ("ss between vowels"); ṣ = ṣ/ç; sh = ch; w = ou; y = i/ï/y (y initially or between vowels); n = n/ne (ne word-finally after a, e, i, o); ’ (hamza) not romanized; ‘ (ʿayn) = ’ or "aa" ("aa is specific to Lebanon") — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf)

**Survey of Egypt System (SES) equivalences**: ā = â (a); -ah (ة) = -a; aw = ô (au); ay = ei (ai); dh = dh (z); j = g (j); q = q (k); th = th (t); ẓ = ẓ (d); s = s (c); ī = î; ū = û. The article is always el- — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf)

- ALA-LC, BGN/PCGN, UNGEGN and DIN 31635 "use a normal g for ج when romanizing Egyptian names". They also "use the French-based ou for u in Francophone Arabic speaking countries in names and toponyms" — [Wikipedia: Romanization of Arabic, notes 12–13](https://en.wikipedia.org/wiki/Romanization_of_Arabic)
- English vs German: "Omar Khayyam" vs "Omar Chajjam" for عمر خيام — [ICAO 9303-3 App. B.3.1](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2). ش is sh in English, ch in French and sch in German — [Wikipedia: Romanization of Arabic](https://en.wikipedia.org/wiki/Romanization_of_Arabic). The Spanish scholarly system has ǧ > ŷ, ḫ > j, ġ > g — [Wikipedia: Romanization of Arabic](https://en.wikipedia.org/wiki/Romanization_of_Arabic)
- ق realizations attested on the web for القذافي: q (Qaddafi 77,900), g (Gaddafi 219,000), gh (13,100), k (68,300), kh (7,380), c (34), j (31) — [Halpern DAN paper](https://www.cjki.org/reference/danpaper.pdf). ق is pronounced [g] in many dialects, including Libya's — [Freeman et al. 2006](https://aclanthology.org/N06-1060.pdf)
- Freeman et al. note that "Those dialects that produce ق as a [g] will as a rule not produce ج as [g] and vice versa" — [Freeman et al. 2006](https://aclanthology.org/N06-1060.pdf)
- IJMES Persian and Turkish values for Arabic letters: ث s; ذ z; ض ż (Pers./Ott.), z (Mod. Turk.); ظ ẓ/z; ح h (Mod. Turk.); خ h (Turk.); ج c (Turk.); ش ş (Turk.); غ g/ğ (Turk.); ق ḳ (Ott.), k (Mod. Turk.); و v (Turk.), v/u (Pers.); ك k/g/ñ/n/y/ğ (Turk.); short vowels a/e, u/ü/o/ö, ı/i (Turk.); diphthongs ev, ey (Turk.) — [IJMES chart](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf)
- Arabizi/chat-alphabet values (informal, dialect-based): ث s/th/t; ج j/g/dj/gh/gi/ż/ž; ح 7/h; خ kh/7'/5/j; ذ z/dh/th/d/ð; ش sh/ch/$/ș/š; ص s/9; ض d/9'; ط t/6; ظ z/dh/6'/th; ع 3; غ gh/3'/8; ق 2/g/q/8/9; و w/ou/oo/u/o; ي y/i/ee/ei/ai; ة a/e(h), et/at; ال el/al/æl; fatḥa a/e/é; kasra i/e/é; ḍamma ou/o/u; ay ay/ai/ey/ei; aw aw/aou — [Wikipedia: Romanization of Arabic](https://en.wikipedia.org/wiki/Romanization_of_Arabic)

**Per-letter variation table for the generator**

Sources are marked per row. "Rule-derived" means the value is inferred from the cited conventions rather than listed verbatim in one source.

| Arabic | Canonical (practical EN) | Realistic variants | Region/language driver | Sources |
|---|---|---|---|---|
| ق | q | k, g, gh, kh, c, ' (glottal; rule-derived), gu (Fr., before e/i) | g: Gulf/Bedouin/Libya/Upper Egypt; k: Turkish/Persian/French (Kadhafi); gu: French | [Halpern](https://www.cjki.org/reference/danpaper.pdf); [Freeman](https://aclanthology.org/N06-1060.pdf); [UNGEGN IGN](https://www.eki.ee/wgrs/rom1_ar.pdf); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf) |
| ج | j | g (Egypt: Gamal), dj (Fr.: Djamel), c (Turk.: Cemal), zh/ž, gi | Egypt g; Maghreb/Fr. dj; Turkish c | [SES/IGN](https://www.eki.ee/wgrs/rom1_ar.pdf); [Wikipedia Arabizi](https://en.wikipedia.org/wiki/Romanization_of_Arabic); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf) |
| ث | th | t (Egypt/Levant urban), s (Persian/Turkish/Urdu: Osman/Usman) | | [SES](https://www.eki.ee/wgrs/rom1_ar.pdf); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [Wikipedia: Uthman](https://en.wikipedia.org/wiki/Uthman_(name)) |
| ذ | dh | z (Egypt/Persian/Turkish), d, th | | [SES](https://www.eki.ee/wgrs/rom1_ar.pdf); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [Arabizi](https://en.wikipedia.org/wiki/Romanization_of_Arabic) |
| ظ | z | dh (UN 2017 d͟h; Gulf), th, d (SES "ẓ (d)") | | [UNGEGN](https://www.eki.ee/wgrs/rom1_ar.pdf); [Arabizi](https://en.wikipedia.org/wiki/Romanization_of_Arabic) |
| ض | d | dh (rule-derived, Gulf), z (Persian/Turkish ż/z: e.g. Rıza/Reza for رضا, rule-derived) | | [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf) |
| ص / س | s | ss (Fr. intervocalic), c / ç (Fr. conventional), sc (rare) | French | [UNGEGN IGN](https://www.eki.ee/wgrs/rom1_ar.pdf); [Freeman CEQ](https://aclanthology.org/N06-1060.pdf) |
| ش | sh | ch (Fr.: Chakib, Chams), sch (Ger.), ş (Turk.), š, $ | | [UNGEGN IGN](https://www.eki.ee/wgrs/rom1_ar.pdf); [Wikipedia](https://en.wikipedia.org/wiki/Romanization_of_Arabic) |
| ح | h | (collapses with ه), kh (Russian/Caucasian: Akhmed, Akhmat, Mukhammad, Mokhmad), ch (Dutch/Indonesian/Cape: Achmad, Achmed, Achmat), x (Somali: Maxamed), g (Dagestani "Magomed"), 7 (Arabizi) | Russian-, Dutch-, Somali-mediated | [Wikipedia: Ahmad](https://en.wikipedia.org/wiki/Ahmad); [Wikipedia: Muhammad (name)](https://en.wikipedia.org/wiki/Muhammad_(name)) |
| خ | kh | ch (German: "Omar Chajjam"), h (Turkish/Bosnian: Halit, Halid), j (Spanish scholarly ḫ > j), k (Freeman CEQ), 5 / 7' (Arabizi) | | [ICAO App. B](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [Wikipedia: Khalid](https://en.wikipedia.org/wiki/Khalid); [Wikipedia: Romanization of Arabic](https://en.wikipedia.org/wiki/Romanization_of_Arabic) |
| غ | gh | g, ğ (Turk.), r/rh (Fr. uvular; rule-derived), 8 | | [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [Arabizi](https://en.wikipedia.org/wiki/Romanization_of_Arabic) |
| ع | ' / ‘ / ʿ or ∅ | omitted (most passports), a/e/o vowel colouring, aa (Lebanon), 3 | | [UNGEGN IGN](https://www.eki.ee/wgrs/rom1_ar.pdf); [Freeman CEQ](https://aclanthology.org/N06-1060.pdf) |
| ء/أ/إ/ؤ/ئ | ∅ or ' | ∅, ', vowel only (Faiz/Fayez for فائز), e for initial إ in Persian/Turkish/Egyptian (Ebrahim, Esmail) | | [ICAO App. B.5.5](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [Wikipedia: Ibrahim](https://en.wikipedia.org/wiki/Ibrahim_(name)) |
| و (consonant) | w | ou (Fr.: Oualid, Ouali), v (Turk./Bosnian/Persian: Velid), u | | [Wikipedia: Waleed](https://en.wikipedia.org/wiki/Waleed); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf) |
| و (ū) | u | oo (Gulf/S. Asia: Moosa), ou (Fr./Levant: Mousa, Youssef), o, ô/oû (Fr./SES) | | [Wikipedia: Musa](https://en.wikipedia.org/wiki/Musa_(name)); [Wikipedia: Yusuf](https://en.wikipedia.org/wiki/Yusuf); [SES/IGN](https://www.eki.ee/wgrs/rom1_ar.pdf) |
| ي (ī) | i | ee (Saeed, Waleed, Kareem, Ibraheem), ie (Walied), ei, î, y | | [Wikipedia: Waleed](https://en.wikipedia.org/wiki/Waleed); [Wikipedia: Ibrahim](https://en.wikipedia.org/wiki/Ibrahim_(name)) |
| ـَيْ (ay) | ay / ai | ei, ey, e, ai (Zainab, Hussain), é | | [Wikipedia: Hussein](https://en.wikipedia.org/wiki/Hussein); [Wikipedia: Zaynab](https://en.wikipedia.org/wiki/Zaynab); [SES](https://www.eki.ee/wgrs/rom1_ar.pdf) |
| ـَوْ (aw) | aw | au, ow, o/ô (SES), ou (Fr.: Toufik, rule-derived) | | [SES](https://www.eki.ee/wgrs/rom1_ar.pdf); [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf) |
| ة (final) | a / ah | a, ah, at, e (Turkish: Ayşe, Hatice, Fadime), eh (Persian/Levant: Fatemeh, Hamzeh), et/at (construct/Turkish) | | [ICAO XTA/XAH](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [Wikipedia: Fatima](https://en.wikipedia.org/wiki/Fatima_(given_name)); [Wikipedia: Hamza](https://en.wikipedia.org/wiki/Hamza_(name)) |
| short a | a | e (Ahmed, Mohammed, Hesham), o (Persian: Abdollah), ä | | [Wikipedia: Ahmad](https://en.wikipedia.org/wiki/Ahmad); [Wikipedia: Hisham](https://en.wikipedia.org/wiki/Hisham) |
| short u | u | o (Mohammed, Omar, Mostafa), ou (Fr.: Moustafa), ü/ö (Turk.) | | [Wikipedia: Mustafa](https://en.wikipedia.org/wiki/Mustafa) |
| short i | i | e (Hesham, Esmail, Ebrahim), ı (Turk.) | | [Wikipedia: Hisham](https://en.wikipedia.org/wiki/Hisham); [Wikipedia: Ismail](https://en.wikipedia.org/wiki/Ismail_(name)) |
| long ā | a | aa (Bilaal, Belaal, Barakaat), â (Fr./SES) | | [Wikipedia: Bilal](https://en.wikipedia.org/wiki/Bilal_(name)); [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf) |
| shadda | double | single (Mohamed, Hasan, Hatem vs Hattem), double where none exists (Hattem) | | [ICAO App. B.5.5.11](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf) |
| final د | d | t (Turkish/Central Asian: Mehmet, Ahmet; "in some countries it is common to replace the final d with t") | Turkic | [ICAO App. B.2.1](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [Wikipedia: Ahmad](https://en.wikipedia.org/wiki/Ahmad) |
| ب | b | p (Turkish word-final, IJMES "b or p"); for Latin→Arabic, p and v map to b and f | | [IJMES](https://www.cambridge.org/core/services/aop-file-manager/file/57d83390f6ea5a022234b400/TransChart.pdf); [Freeman](https://aclanthology.org/N06-1060.pdf) |

**Freeman et al. (MITRE, 2006) Arabic→English character equivalence classes (CEQ), as used in a modified Levenshtein**: hamza forms and ا → {', a, e, i, o, u}; ب → {b, p, v}; ة → {a, e}; ت → {t}; ث → {t}; ج → {j, g}; ح → {h}; خ → {k}; د → {d}; ذ → {d}; ص → {s}; ض → {d}; ط → {t}; ظ → {z, d}; ع → {', `, c, a, e, i, o, u}; غ → {g}; ف → {f, v}; ق → {q, g, k}; ك → {k, c, s}; و → {w, u, o}; ي → {y, i, e, j}; ى → {a, e, i, o, u}; fatḥa → {a, e}; kasra → {i, e}; ḍamma → {u, o}. Digraphs are first normalized (sh, th, dh, kh), then English-side rules are applied: ph→f, sch→sh, ch→tsh (with a second pass ch→k), x→ks, drop silent final e and silent gh, collapse doubled letters, remove hyphens and spaces. CEQ raised F-score from ~48% to ~72%, and all enhancements together reached ~80%. Peak threshold was ~85% with CEQ — [Freeman, Condon & Ackerman 2006](https://aclanthology.org/N06-1060.pdf)

**Cross-language "re-spellings" attested for common names (useful for the Turkish, Persian, South Asian, Malay, African and Russian profiles)**
- Muhammad: Mehmed/Mehmet, Mehemmed, Memet (Turkish); Mamadou (West Africa); Magomed, Mukhammad, Mokhmad (Caucasus/Russian); Maxamed (Somali); Mochamad (Indonesian); Muhammadu (Hausa); Md./Mohd. (South/Southeast Asia) — [Wikipedia: Muhammad (name)](https://en.wikipedia.org/wiki/Muhammad_(name))
- Ahmad: Ahmet (Turkish), Achmad/Achmed/Achmat (Dutch/Indonesian/Cape), Akhmed/Akhmat (Russian/Caucasus), Ahmadu/Amadou/Amadu (West Africa) — [Wikipedia: Ahmad](https://en.wikipedia.org/wiki/Ahmad)
- Uthman: Osman (Turkic/Bosnian), Usman (Persian/Urdu), Ousmane (Francophone West Africa) — [Wikipedia: Uthman (name)](https://en.wikipedia.org/wiki/Uthman_(name))
- Fatima: Fadumo (Somali), Fadime/Fatma (Turkish), Fatemeh (Persian), Patimat/Petimat (Caucasus), Fotima (Uzbek), Fadma/Fatna (Maghreb) — [Wikipedia: Fatima (given name)](https://en.wikipedia.org/wiki/Fatima_(given_name))
- Khadija: Hatice (Turkish), Hadja, Khatija, Tijah (Malay) — [Wikipedia: Khadija](https://en.wikipedia.org/wiki/Khadija)
- Khalid: Halid (Bosnian), Halit (Turkish), Xalîd (Kurdish) — [Wikipedia: Khalid](https://en.wikipedia.org/wiki/Khalid)
- Hamza: Khamzat (Chechen), Hamzeh, Humza — [Wikipedia: Hamza (name)](https://en.wikipedia.org/wiki/Hamza_(name))
- Abu Bakr: Abu Bakar (Malay), Abu Bekr, Ebubekir (Turkish), Aboubacar, Abubakar — [Wikipedia: Abu Bakr (name)](https://en.wikipedia.org/wiki/Abu_Bakr_(name))

### Inferences
- Define profiles as ordered rule sets over the vocalized form: `en_gulf` (Mohammed, Abdulla(h), Al Xxx), `en_levant`, `en_iraq`, `egypt` (g, e/o vowels, El-, Abdel, -a), `maghreb_fr` (ou, ch, dj, gu, ss, final -e, Ben, Bel/Bou), `lebanon_fr`, `turkish`, `persian`, `south_asian`, `malay_indonesian`, `russian_caucasian`, `west_african_fr`, `somali`. Generate variants by applying the alternative choices for each letter or slot under each profile, then union and rank.
- Freeman's CEQ is directly reusable as a scoring matrix, both cross-script (Arabic skeleton vs Latin) and Latin-vs-Latin via the Arabic skeleton. A Latin→Arabic-skeleton "back-projection" key, e.g. Mohamed/Muhammad/Mehmet → m-h-m-d, is the most robust matching key.
- ق ↔ g and ج ↔ g are mutually exclusive by dialect (Freeman). Use this to prune the cross-product: within one name, don't generate both ق→g and ج→g for the same profile.

### Gaps
- No open, frequency-weighted dataset of popular romanizations by country was found (CJKI DAN is commercial).
- Babel Street/Rosette's article "You say Jamāl, he writes Djamel: influences on Western transliteration of Arabic names" returned 404 when fetched, so its content was not used.

---

## 7. Passport practice by country and ICAO guidance

### Takeaway
ICAO mandates a Latin rendering in the VIZ but leaves the scheme to the issuing state. Its Arabic table is a **recommended**, X-escaped MRZ transliteration, and in practice most states print phonetic spellings in both VIZ and MRZ. No Arab state's personal-name passport transliteration rulebook was found publicly. Evidence points to registry-fixed English spellings (e.g. Saudi civil records editable via Absher), legacy colonial-era Latin forms in the Maghreb (Algeria's 1981 decree froze the Latin forms on a national list of family names), and unsuccessful regional standardization attempts (Saudi Arabia 2003/2006, UAE 2009).

### Cited Findings
- ICAO VIZ: "When mandatory data elements are in a national language that does not use the Latin alphabet, a transliteration shall also be provided". Diacritics are optional in the VIZ. "It is at the discretion of the issuing State as to whether this is a phonetic transcription, or a copy of the MRZ transliteration". States that keep approved Latin forms in registers "may wish to continue to enter the approved Latin transcription in the VIZ" — [ICAO 9303-3 §3, App. B.3](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- ICAO MRZ: only A–Z and "<". Diacritics are not permitted. Primary and secondary identifiers are separated by "<<", components by "<". Apostrophes are removed with components joined; a hyphen becomes "<". Titles and prefixes are omitted unless legally part of the name. Names are truncated per the form-factor rules — [ICAO 9303-3 §4.6](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- ICAO's stated goal for the Arabic MRZ scheme: "only one possible representation for the name… to avoid ambiguity and make database and alert list searching as accurate as possible". The phonetic approach means "database searches can become useless" — [ICAO 9303-3 App. B.2.2, B.5.1](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- Saudi Arabia, from search snippets only (pages not fetched): Saudi driving licences and passports carry fixed English transliterations of names — [Cultural Atlas (SBS): Saudi naming](https://culturalatlas.sbs.com.au/saudi-arabian-culture/saudi-arabian-culture-naming). Citizens can request a correction of the English name in civil records electronically via Absher's "Tawasul" service by submitting a passport copy. Employers can update the English-translated names of Arab-national domestic workers via Absher. These come from search snippets of Ajel English news items; which claim belongs to which article was not verified — [Ajel 1](https://english.ajel.sa/news/ov2elpmci); [Ajel 2](https://english.ajel.sa/news/gb3noz23d); [Ajel 3](https://english.ajel.sa/news/rynjhilmh)
- Gulf standardization attempts: Saudi Arabia held conferences in 2003 and 2006, and researchers developed patented automatic transliteration software, but enforcement was hard because names were already registered in passports and property documents (suggestion: apply standards to "the coming generation"). The UAE held a 2009 symposium whose scholars recommended a "computer-friendly system, based on standard Arabic rather than colloquial pronunciation" — [The National, 24 Feb 2013](https://thenationalnews.com/uae/other-countries-grapple-with-same-issue-1.331487)
- The UN 2017 system shows "partial implementation in Jordan, Oman and Saudi Arabia". This concerns geographical names, not passports — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf)
- Algeria, Décret n° 81-28 of 7 March 1981:
  - communes compile all family names into a national list;
  - all names are transcribed into Arabic "sur la base de la traduction phonétique des noms", with an annexed table classifying Latin letters that admit several phonemes;
  - "Les noms figurant en caractères latins sur la liste nationale ne peuvent subir aucune modification";
  - civil-status officers may correct phonemes on request using the annex table.
  - Décret 81-26 (same date) created a national lexicon of first names.
  - Source: [Décret 81-28 (CEFAN, Université Laval)](https://www.axl.cefan.ulaval.ca/afrique/algerie_decret-81-28-1981.htm)
- Algeria had no official romanization system for geographical names, and one was under discussion. Morocco's official romanization for Arabic-script geographical names dates from 17 June 1932, with changes planned. Tunisia adopted the amended Beirut system in 1983, then reverted to traditional rendering. Mauritania uses a simplified IGN system — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf)
- Egypt has no single standard source. The Survey of Egypt System (g for ج, el-, -a, ei/ô) is the documented traditional Egyptian romanization — [UNGEGN WGRS](https://www.eki.ee/wgrs/rom1_ar.pdf). "Mohamed" (single m) is widely reported as the Egyptian-style passport spelling, and passport renewals reportedly re-spell names (e.g. Mohammed→Mohamed, A→E) without the Arabic changing. These are search-snippet claims from practitioner and forum pages, so confidence is low — [VisaJourney forum](https://visajourney.com/forums/topic/550459-the-names-are-killing-us); [IDScan blog](https://idscan.net/blog/transliteration-issues-in-identity-verification/)
- ODNI explicitly normalizes Egyptian "Gamal" to IC-standard "Jamal". This shows that Egyptian document spellings systematically diverge from MSA-based standards — [interscript ODNI](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc)

### Inferences
- The "passport-style" mode should be a **profile + lexicon** output, not a standard. Uppercase A–Z, no diacritics, ʿ/ʾ dropped, the article as a separate token or attached according to profile, and an ICAO-MRZ serializer (`<`, `<<`, punctuation rules, truncation).
- Supported country profiles: SA/AE/KW/QA/BH/OM (English, MOHAMMED, ABDULLAH/ABDULAZIZ solid, AL as a separate token), JO/PS/LB/SY/IQ (English with e/o vowels; LB is often French), EG (G, MOHAMED, EL, ABDEL, -A), MA/DZ/TN (French: MOHAMED, ABDELKADER, BEN, OU, CH, DJ, -E), LY (G for ق common), SD (English). These profile contents are inferences from the regional conventions in section 6, not documented state rules.
- For Maghreb records, the Latin form is often primary (Algeria's frozen list), so Arabic→Latin generation may not reproduce the legal Latin name. Matching must therefore rely on variant/skeleton similarity, not exact generation.

### Gaps
- No official, public personal-name transliteration regulations were found for Saudi Arabia, the UAE, Egypt, Jordan, Iraq, Syria, Morocco or Tunisia. Whether such internal rules exist, e.g. in Saudi Absher/NIC, UAE ICP or the Egyptian Civil Status Organization, could not be verified.
- Iraq, Syria, Jordan and the UAE: no source on current passport spelling practice was found.
- The Algerian annex table (Latin letter → phoneme classes) was not available on the page fetched.
- The Moroccan civil-status law's provisions on Latin transcription of names were not located.

---

## 8. Common Arabic first names (~40) with realistic variant sets

### Takeaway
High-frequency names have large, well-documented variant families: محمد has "one of the highest numbers of English spelling variants in the world", ~200 popular transcriptions according to CJKI, and 16–32 according to ICAO. The table below combines attested variant lists (Wikipedia infobox and lead lists; ICAO; CJKI) with rule-derived additions, clearly marked. Watch for homographs: unvocalized forms that map to two different names.

### Cited Findings
- ICAO lists 16 variants for محمد from the "Database of Arabic Name Variants": Muhammad, Moohammad, Moohamad, Mohammad, Mohamad, Muhamad, Mohamed, Mohammed, Mohemmed, Muhemmed, Muhamed, Muhammed, Moohammed, Mouhammed. ICAO adds that "In some countries it is common to replace the final 'd' with 't'… a total of 32 variations" — [ICAO 9303-3 App. B.2.1](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- محمد is transcribed "in some 200 different ways" — [Halpern ARAN](https://www.cjki.org/arabic/arannana.pdf); "in over 100 ways" — [Halpern DAN](https://www.cjki.org/reference/danpaper.pdf)
- Homograph: two different names, حسن (Ḥasan) and حسّان (Ḥassān), are both romanized "Hassan" — [Wikipedia: Hassan (given name)](https://en.wikipedia.org/wiki/Hassan_(given_name)). Similarly عمرو ‘Amr (silent final و) vs عمر ‘Umar — [LOC rule 24](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf). Also خاتم/حاتم: CJKI shows "Khadem/Hadim Ahmed Barakat" as XOFAC variants of Hatim (حاتم) — [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf)

**Name table.** Legend: **A** = attested in the cited source for that row. *R* = rule-derived from the section 6 conventions (not verbatim in a source). ALA-LC forms follow LOC rules. Vocalized Arabic is the standard lexical form.

| # | Arabic (vocalized) | ALA-LC | Attested variants (A) | Rule-derived additions (R) | Source for A |
|---|---|---|---|---|---|
| 1 | مُحَمَّد | Muḥammad | Muhammad, Mohammed, Mohamed, Mohammad, Mohamad, Muhammed, Muhamad, Muhamed, Mohemmed, Muhemmed, Moohammad, Moohamad, Moohammed, Mouhammed, Mahmad, Mahammad, Mahammed, Mahamed, Muhammadu, Muhammet, Mehmed, Mehmet, Memet, Mehemmed, Mamadou, Magomed, Mukhammad, Mokhmad, Maxamed, Mochamad, Mohamud, Mamed, Md., Mohd. | Mouhamed, Mohamet, Muhamet | [ICAO](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2); [Wikipedia](https://en.wikipedia.org/wiki/Muhammad_(name)) |
| 2 | أَحْمَد | Aḥmad | Ahmad, Ahmed, Ahmmad, Achmad, Achmat, Achmed, Akhmat, Akhmed, Achmet, Ahmat, Ahmet, Ahmadu, Amadou, Ahmot, Amadu | Ehmed, Hamad (≠ حمد) | [Wikipedia: Ahmad](https://en.wikipedia.org/wiki/Ahmad) |
| 3 | عَلِيّ | ‘Alī | Ali, Aly, Ally, Alli, Alley, Allie, Aliy, Aliyy, Alee | 'Ali, Aliyu (Hausa) | [Wikipedia: Ali (name)](https://en.wikipedia.org/wiki/Ali_(name)) |
| 4 | حُسَيْن | Ḥusayn | Hussein, Hossein, Hussain, Hossain, Huseyn, Hüseyin, Husayn, Husein, Hussin, Hoessein, Houcine, Hocine, Husain, Houssin, Hosein | Hussien, Husien, Housein | [Wikipedia: Hussein](https://en.wikipedia.org/wiki/Hussein) |
| 5 | حَسَن | Ḥasan | Hassan, Hasan, al-Ḥasan; related Alassane, Lassana | Hassen (Maghreb), Hacen, Hasen | [Wikipedia: Hassan (given name)](https://en.wikipedia.org/wiki/Hassan_(given_name)) |
| 6 | عُمَر | ‘Umar | Omar, Umar (per Wikipedia "Omar (name)" page; list not enumerated) | Omer, Ömer, Oumar, Omari | [Wikipedia: Omar (name)](https://en.wikipedia.org/wiki/Omar_(name)) |
| 7 | يُوسُف | Yūsuf | Yusuf, Yousef, Yousif, Youssef, Youssif, Yousuf, Yoosuf, Yusef, Yusup, Jusuf | Youcef (Alg.), Yossef, Yousseph, Yusif | [Wikipedia: Yusuf](https://en.wikipedia.org/wiki/Yusuf) |
| 8 | إِبْرَاهِيم | Ibrāhīm | Ibrahim, Ibraheem, Ebrahim, Ebraheem, Ibrahiim, Ebrahiim | Brahim (Maghreb), İbrahim, Ibrahima | [Wikipedia: Ibrahim](https://en.wikipedia.org/wiki/Ibrahim_(name)); [Halpern](https://www.cjki.org/arabic/arannana.pdf) |
| 9 | إِسْمَاعِيل | Ismā‘īl | Ismail, Esmail | Ismael, Ismaeel, Ismayil, Smail (Maghreb), İsmail | [Wikipedia: Ismail](https://en.wikipedia.org/wiki/Ismail_(name)) |
| 10 | خَالِد | Khālid | Khalid; Halid, Halit, Xalîd; fem. Khalida | Khaled, Khalead, Kaled | [Wikipedia: Khalid](https://en.wikipedia.org/wiki/Khalid) |
| 11 | عَبْد الله | ‘Abd Allāh | Abdullah, Abdallah, Abdellah, Abdollah | Abdulla, Abdalla, Abd Allah, Abdoulaye (W. Afr.) | [Wikipedia: Abdullah](https://en.wikipedia.org/wiki/Abdullah_(name)) |
| 12 | عَبْد العَزِيز | ‘Abd al-‘Azīz | Abd Al Aziz (OFAC form) | Abdulaziz, Abdelaziz, Abdul Aziz, Abdul-Aziz, Abd el-Aziz, Abdulazeez, Abdelazize (rare Fr.) | [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf) |
| 13 | عَبْد الرَّحْمٰن | ‘Abd al-Raḥmān | Abdelrahman, Abd al-Rahman, Abdul Rahman, Abdur Rahman, Abdurrahman, Abdrrahman, Abd ar-Rahman, Abdulrahman, Abdur Rehman, Abdul Rehman, Abidur Rahman | Abderrahmane, Abderrahman, Abdel Rahman, Abdirahman (Somali) | [Wikipedia: Abd al-Rahman](https://en.wikipedia.org/wiki/Abd_al-Rahman) |
| 14 | مُصْطَفَى | Muṣṭafá | Mustafa, Mostafa, Mostapha, Moustafa, Moustapha, Mustapha, Mustafi | Mustafaa | [Wikipedia: Mustafa](https://en.wikipedia.org/wiki/Mustafa) |
| 15 | مَحْمُود | Maḥmūd | Mahmud, Mahmoud | Mahmood, Mehmood (S. Asia), Mahmut (Turk.) | [Wikipedia: Mahmud](https://en.wikipedia.org/wiki/Mahmud) |
| 16 | سَعِيد | Sa‘īd | (Wikipedia Saʽid page; list not enumerated) | Said, Saeed, Saied, Sayed (≠ سيد), Saïd (Fr.), Sait (Turk.) | [Wikipedia: Saʽid](https://en.wikipedia.org/wiki/Sa%CA%BDid) |
| 17 | فَاطِمَة | Fāṭimah | Fatima, Fatimah, Fathima, Fadumo, Fadime, Fadima, Fatma, Fatme, Fatemeh, Fathama, Fadma, Fatna, Fatim, Fotima, Patimat, Petimat | Fatema, Fatiha (≠ فاتحة) | [Wikipedia: Fatima](https://en.wikipedia.org/wiki/Fatima_(given_name)); [ICAO](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2) |
| 18 | عَائِشَة | ‘Ā’ishah | Aishah, Aishat, Aiisha, Aishaa, Aysha, Ayshat, Ayshe, Ayşe, Aisha | Aicha (Fr.), Aïcha, Ayesha (S. Asia) | [Wikipedia: Aisha (given name)](https://en.wikipedia.org/wiki/Aisha_(given_name)) |
| 19 | خَدِيجَة | Khadījah | Khadijah, Khadeeja, Khadeejah, Khatija, Khatijah, Katijah, Hadja, Hatice, Tijah | Khadija, Khadidja (Alg.), Kadidja | [Wikipedia: Khadija](https://en.wikipedia.org/wiki/Khadija) |
| 20 | زَيْنَب | Zaynab | Zainab, Zaenab, Zayneb, Zeinab, Zenab, Zineb, Zinab, Zynab, Zaineb, Zeynab, Zeynep | — | [Wikipedia: Zaynab](https://en.wikipedia.org/wiki/Zaynab) |
| 21 | مَرْيَم | Maryam | (no list in source) | Mariam, Meryem (Turk.), Meriem (Maghreb), Mariyam | — |
| 22 | نُور | Nūr | (element) Nur, Noor, Nor, Nour, Nuer | Nura/Noura for نورة | [Wikipedia: Nur al-Din](https://en.wikipedia.org/wiki/Nur_al-Din) |
| 23 | لَيْلَى | Laylá | (related Lila, Layal) | Layla, Leila, Laila, Leyla, Lailah | [Wikipedia: Leila (name)](https://en.wikipedia.org/wiki/Leila_(name)) |
| 24 | يَاسْمِين | Yāsmīn | (no list in source) | Yasmin, Yasmine, Yasmeen, Jasmin | — |
| 25 | حَمْزَة | Ḥamzah | Humza, Hamzah, Hamzeh, Hamsah, Khamzat, Hamëz | Hamza, Hamzat | [Wikipedia: Hamza](https://en.wikipedia.org/wiki/Hamza_(name)) |
| 26 | بِلَال | Bilāl | Bilel, Billel, Belal, Bilaal, Belaal | Bilal | [Wikipedia: Bilal](https://en.wikipedia.org/wiki/Bilal_(name)) |
| 27 | طَارِق | Ṭāriq | Tarık, Tarek, Tarik, Tareq, Tariq, Tareek, Tyreek | Tarak (Tun.) | [Wikipedia: Tariq](https://en.wikipedia.org/wiki/Tariq) |
| 28 | جَمَال | Jamāl | Jamal (popular), Gamal (Egyptian) | Djamel, Djamal, Cemal (Turk.), Jamaal | [Halpern ARAN](https://www.cjki.org/arabic/arannana.pdf); [ODNI](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc) |
| 29 | كَرِيم | Karīm | (Wikipedia Kareem page; no list) | Karim, Kareem, Kerim (Turk.), Krim (Maghreb, in Abdelkrim) | [Wikipedia: Kareem](https://en.wikipedia.org/wiki/Kareem) |
| 30 | رَشِيد | Rashīd | Al-Rashid, ar-Rashid, Al-Rasheed (as surname) | Rashid, Rasheed, Rachid (Fr.), Reşit (Turk.) | [Wikipedia: Rashid](https://en.wikipedia.org/wiki/Rashid) |
| 31 | وَلِيد | Walīd | Al-Waleed, al-Walid, Walid, Walied, Oualid, Velid | Waleed | [Wikipedia: Waleed](https://en.wikipedia.org/wiki/Waleed) |
| 32 | هِشَام | Hishām | Hesham, Hicham | Hisham, Hishaam | [Wikipedia: Hisham](https://en.wikipedia.org/wiki/Hisham) |
| 33 | زِيَاد | Ziyād | Ziad, Zyad, Zeyad, Zijad, Ziyad | Ziade | [Wikipedia: Ziyad](https://en.wikipedia.org/wiki/Ziyad) |
| 34 | سَمِير | Samīr | Samir, Sameer | Semir, Smir | [Wikipedia: Samir](https://en.wikipedia.org/wiki/Samir) |
| 35 | فَيْصَل | Fayṣal | Faisel, Faysal, Fayçal, Foysal | Faisal, Feisal, Faiçal | [Wikipedia: Faisal](https://en.wikipedia.org/wiki/Faisal) |
| 36 | سُلْطَان | Sulṭān | (no list in source) | Sultan, Soltan, Soultane | — |
| 37 | أَمِينَة | Amīnah | Aminah, Aminat, Aminas, Aminna, Amiina, Amine, Aminata, Amina | Ameena | [Wikipedia: Amina](https://en.wikipedia.org/wiki/Amina) |
| 38 | هُدَى | Hudá | (no list in source) | Huda, Hoda (Egypt), Houda (Fr.), Hudaa | — |
| 39 | مُوسَى | Mūsá | Mosa, Moosa, Mousa, Moussa | Musa, Mussa | [Wikipedia: Musa](https://en.wikipedia.org/wiki/Musa_(name)) |
| 40 | عُثْمَان | ‘Uthmān | Uthman, Osman, Usman, Ousmane | Othman, Otman (Maghreb) | [Wikipedia: Uthman](https://en.wikipedia.org/wiki/Uthman_(name)) |
| 41 | أَبُو بَكْر | Abū Bakr | Abu Bakar, Abu Bekr, Ebubekir, Aboubacar, Abubakar | Abou Bakr, Boubacar, Aboubakr | [Wikipedia: Abu Bakr (name)](https://en.wikipedia.org/wiki/Abu_Bakr_(name)) |
| 42 | إِدْرِيس | Idrīs | Idrees | Idris, Driss (Maghreb) | [Wikipedia: Idris](https://en.wikipedia.org/wiki/Idris_(name)) |
| 43 | حَاتِم | Ḥātim | Hatim, Hatam, Hatem, Hattem, Hotem, Hetem | — | [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf) |
| 44 | نُور الدِّين | Nūr al-Dīn | see section 5 | — | [Wikipedia: Nur al-Din](https://en.wikipedia.org/wiki/Nur_al-Din) |

### Inferences
- Ship a curated YAML/JSON lexicon keyed by consonant skeleton. Fields: vocalized form, ALA-LC/BGN/IJMES outputs (precomputed by the rule engine for tests), a `practical` default per profile, `attested_variants` with source tags, gender, and homograph flags (حسن/حسّان, عمر/عمرو, سعيد/سيد-type confusions).
- The table also provides **regression tests**: e.g. `romanize("مُصْطَفَى", "ala_lc") == "Muṣṭafá"`, and `"Mostapha" in variants("مصطفى")`.

### Gaps
- No source gave variant lists for Maryam, Yasmin, Sultan, Huda, Jamal, Karim, Said/Saeed or Omar in a fetchable structured form. Those rows rely on rule-derived forms.
- No country-specific frequency data (e.g. the share of "Mohamed" vs "Mohammed" in Egyptian vs Gulf passports) was found.

---

## 9. Arabic Unicode normalization before transliteration

### Takeaway
Before any lookup, apply NFKC (folds presentation forms and ligatures such as ﻻ and ﷲ), remove tatweel and invisible format characters, map Persian/Urdu letter variants to Arabic, and convert Arabic-Indic digits. Do **not** blindly fold alef/hamza/ى/ة or strip harakat in the canonical path. Do those only when building matching keys, because standards need hamza seats, آ (for Āl), ى vs ي and ة.

### Cited Findings
- Verified with Python `unicodedata` (Unicode 13 data), consistent with the [Unicode Arabic chart](https://www.unicode.org/charts/PDF/U0600.pdf):
  - آ U+0622 = 0627+0653 (NFD); أ U+0623 = 0627+0654; إ U+0625 = 0627+0655; ؤ U+0624 = 0648+0654; ئ U+0626 = 064A+0654. NFC/NFKC recompose them. **NFD followed by stripping combining marks (Mn) deletes the hamza/madda.**
  - NFKC maps presentation forms: ﻻ U+FEFB → ل+ا; ﻵ U+FEF5 → ل+آ; ﻷ U+FEF7 → ل+أ; ﻹ U+FEF9 → ل+إ; ﷲ U+FDF2 → ا+ل+ل+ه; ﺍ U+FE8D → ا; ﮎ U+FB8E → ک.
  - NFKC does **not** map ٱ U+0671, ی U+06CC, ک U+06A9, ہ U+06C1, ھ U+06BE, ى U+0649, ة U+0629, tatweel U+0640, or the digits U+0660–0669 / U+06F0–06F9. Python `int()` accepts the digits (`int('١٢٣') == 123`).
  - Harakat U+064B–0652 and U+0670 are category Mn; tatweel U+0640 is Lm; ZWNJ U+200C is Cf.
- ICAO treats tatweel as "Not encoded" and harakat/sukun/dagger alif as not transliterated. Farsi yeh (ی U+06CC) "is functionally identical to the standard 'yeh' (ي) but in the isolated and final forms is graphically identical to… 'alef maksura' (ى)", and matching should account for this. Pashto yeh ې is functionally ي — [ICAO 9303-3 §6 and App. B.5.6](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- In Egypt, Sudan and sometimes elsewhere, final ي is written ى (dotless) for both /-iː/ and /-aː/ — [Wikipedia: Romanization of Arabic, note 9](https://en.wikipedia.org/wiki/Romanization_of_Arabic). Halpern also notes ي/ى alternation "especially in Egypt" and ه/ة alternation — [Halpern DAN paper](https://www.cjki.org/reference/danpaper.pdf)
- Maghrebi ڢ (f) and ڧ (q) are romanized f and q — [LOC note 2](https://www.loc.gov/catdir/cpso/romanization/arabic.pdf). Note: Wikipedia states Maghrebi feh/qaf are traditionally written with the dot placement ڢ and ڧ — [Wikipedia: Romanization of Arabic, note 8](https://en.wikipedia.org/wiki/Romanization_of_Arabic). Tunisian ڨ, Iraqi گ and Moroccan ڭ are g — [BGN/PCGN Table 3](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/320079/Arabic_Romanization.pdf)
- CAMeL Tools provides `normalize_unicode` (NFKC by default), `normalize_alef_ar`, `normalize_alef_maksura_ar` (ى→ي), `normalize_teh_marbuta_ar` (ة→ه) and `dediac_ar` — [CAMeL normalize](https://camel-tools.readthedocs.io/en/latest/api/utils/normalize.html); [CAMeL dediac](https://camel-tools.readthedocs.io/en/latest/api/utils/dediac.html)
- The Buckwalter community notes that transliteration pipelines must decide on removing kashida (tatweel), removing short vowels, normalizing spelling, and converting Eastern Arabic numerals — [Wikipedia: Buckwalter transliteration](https://en.wikipedia.org/wiki/Buckwalter_transliteration)

### Inferences
Recommended `normalize()` stages. Stages 1–6 are always applied. Stage 7 is applied only for matching keys.
1. `unicodedata.normalize("NFKC", s)` to fold presentation forms and ligatures (ﷲ, ﻻ, ﻷ, ﻹ, ﻵ). Then NFC.
2. Remove: tatweel U+0640; ZWNJ U+200C, ZWJ U+200D, LRM U+200E, RLM U+200F, ALM U+061C, LRE/RLE/PDF/LRO/RLO U+202A–202E, LRI/RLI/FSI/PDI U+2066–2069, BOM U+FEFF, soft hyphen U+00AD; Quranic annotation marks U+06D6–06ED (optional).
3. Map Persian/Urdu/Pashto letters to Arabic for Arabic-language processing: ی U+06CC → ي (but → ى if the lexicon says alif maqsura); ې U+06D0 → ي; ک U+06A9 → ك; ہ U+06C1 → ه; ھ U+06BE → ه; ۀ U+06C0 → ه + hamza (or ة); ە U+06D5 → ه; ۃ U+06C3 → ة; ٱ U+0671 → ا (record wasla); ٲ/ٳ → ا. Keep پ چ ژ گ ڤ ڨ ڭ as foreign-sound letters with mappings p, ch/zh, zh, g, v, g, g.
4. Digits: U+0660–0669 and U+06F0–06F9 → 0–9.
5. Punctuation: ، U+060C → ","; ؛ U+061B → ";"; ؟ U+061F → "?"; ٪ → "%".
6. Keep harakat if present (U+064B–0652, 0670, 0653–0655). They feed vocalization and the Buckwalter/ISO outputs. NFC already puts them in canonical order. Verified combining classes: fatḥatān 27, ḍammatān 28, kasratān 29, fatḥa 30, ḍamma 31, kasra 32, shadda 33, sukūn 34, dagger alif 35, maddah/hamza above 230, hamza below 220. So "م + shadda + fatḥa" is reordered to "م + fatḥa + shadda", and parsers must accept shadda **after** the vowel.
7. Matching key only: strip harakat; أ إ آ ٱ → ا (but tag آل first); ى → ي; ة → ه; ؤ → و; ئ → ي; ء → ∅; optionally collapse doubled letters and remove the article ال.

### Gaps
- No authoritative spec was found on the canonical order of shadda vs vowel marks in input data from real registries (combined vs separate). The NFC claim above relies on standard Unicode canonical ordering, not on a registry source.

---

## 10. Industry and academic name-matching practice for Arabic names (OFAC, UN, Rosette/Babel Street, IBM, academic)

### Takeaway
Production systems combine (a) large lexicons of name variants (CJKI DAN/XOFAC, Rosette's Arabic name lexicon), (b) normalization and back-projection to a common representation (Latin or Buckwalter skeleton), and (c) fuzzy scoring: Jaro-Winkler, Soundex and Levenshtein with character equivalence classes, applied per token and to the whole string. OFAC's public tool documents Jaro-Winkler + Soundex at both full-string and per-name-part level. MITRE showed that Arabic-specific equivalence classes give the largest single gain in a Levenshtein matcher.

### Cited Findings
- OFAC Sanctions List Search: fuzzy logic applies only to the name field. The two algorithms are "Jaro-Winkler, a string difference algorithm, and Soundex, a phonetic algorithm". Technique 1 compares the full name string with Jaro-Winkler. Technique 2 splits the input into name parts, scores each part with Jaro-Winkler and Soundex, and computes a composite. The higher of the two scores is returned. A minimum score of 100 means exact match — [OFAC Sanctions List Search FAQ (archived 2020)](https://webarchive.library.unt.edu/web/20201218003925mp_/https://home.treasury.gov/policy-issues/financial-sanctions/sanctions-list-search-tool)
- MITRE (Freeman, Condon, Ackerman, HLT-NAACL 2006): Levenshtein with Arabic→English character equivalence classes (CEQ, table in section 6), plus normalization, vowel handling, a separate pass for "ch", and light stemming. Baseline string metrics on 29 names: Needleman-Wunsch/Levenshtein F = 0.73, Smith-Waterman 0.60, Jaro 0.40, SLIM 0.16. With CEQ, F rose from ~48% to ~72%; all enhancements gave ~80%. Opposite in spirit to Soundex/Editex, which collapse character classes — [Freeman et al. 2006](https://aclanthology.org/N06-1060.pdf)
- CJKI (Halpern):
  - The XOFAC database contains "millions of potential and actual variants not found in OFAC". Example: ~130,000 variants of "Hatim Ahmad BARAKAT", ranked by product of web frequencies of component variants; only 1 of the top 15 appeared in OFAC.
  - The goal "is to achieve maximum recall", and comprehensive variant coverage "has no negative effects (except possibly for system resources)".
  - Real aliases missing from OFAC were found (e.g. "Hattem Ahmed Barakat").
  - Sources: [CJKI XOFAC](https://www.cjk.org/wp-content/uploads/2020/12/xofacv.pdf)
- CJKI argues for a lexicon-driven approach: a database of names and variants built with an Orthographical Rule Base compiled from a large name corpus (a bilingually aligned phone directory), because statistical methods alone are inadequate — [Halpern DAN paper](https://www.cjki.org/reference/danpaper.pdf); [Halpern ARAN](https://www.cjki.org/arabic/arannana.pdf)
- ICAO advises search algorithms to account for optional shadda, ة as XTA/XAH, ی as Y/XAY, and missing vowels; operators should ignore X characters — [ICAO 9303-3 App. B](https://itftennis.atlassian.net/wiki/download/attachments/1272938619/Passport%20Standards.pdf?api=v2)
- ODNI ICS-630-01 says not to erase forensic variants: keep the as-found spelling in parentheses after the IC-standard form, plus the Arabic original if known — [interscript ODNI](https://github.com/interscript/maps/blob/main/maps/odni-ara-Arab-Latn-2015.isc)
- Babel Street (Rosette), from search snippets only (pages not fetched): Rosette Name Indexer does cross-script, cross-cultural fuzzy matching via a "patented two-pass process". For Arabic, it relies "on a lexicon of Arabic names and their corresponding transliterations, falling back on phonetic transliteration rules", with all names rendered in Latin script before matching — [Babel Street: Understanding Rosette Name Indexer](https://www.babelstreet.com/landing/understanding-rosette-name-indexer). In 2006 the MITRE work normalized Arabic via Basis Technology's "Artrans" transliteration tool (kh/sh/th/dh digraphs) — [Freeman et al. 2006](https://aclanthology.org/N06-1060.pdf)

### Inferences
- Two-layer matcher for `translit-names`:
  1. **Candidate generation / blocking** with multiple keys per name token:
     - Arabic skeleton (normalized, unvocalized Buckwalter);
     - Latin back-projection skeleton (Latin → collapse digraphs sh/ch/kh/th/dh/gh/dj/ou/oo/ee → classes; drop vowels and h-after-consonant; map q/k/g/c → K, j/g/dj → J, s/ç/c(+e/i) → S, z/dh/th(ظ) → Z, w/ou/v → W, y/i/ee → Y; collapse doubles; strip the article);
     - a phonetic key (e.g. Double Metaphone);
     - optionally the ICAO X-scheme of the Arabic, when Arabic is available.
  2. **Scoring**: a token-level CEQ-weighted Levenshtein or Jaro-Winkler, with optional-token handling for particles (al/el, bin/ibn/ben, abu/bou, abd-compounds re-segmented) and token-order-insensitive alignment for nasab chains. Also take the max of full-string and per-token composite scores (the OFAC pattern).
- Variant generation (for displaying aliases or expanding queries against systems you don't control) and similarity matching (for your own index) should be separate features. Generation explodes combinatorially (CJKI: 10⁵ variants per full name). Skeleton keys plus CEQ scoring cover the same space cheaply.

### Gaps
- IBM's name-matching products (InfoSphere Global Name Recognition / Global Name Analytics) were not researched. No IBM primary documentation on its Arabic handling was obtained in this session.
- UN Security Council Consolidated List practice for Arabic names (e.g. whether it publishes original-script names and how aliases are structured) was not verified.
- Babel Street/Rosette technical documentation on Arabic was not fetched beyond the search snippet.
