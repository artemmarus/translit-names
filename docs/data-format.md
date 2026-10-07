# Data format

All linguistic knowledge in `translit-names` lives in JSON files under
`src/translit_names/data/`. Code never hard-codes a transliteration table.

```
data/
  defaults.json            default scheme per language
  schemes/<id>.json        one transliteration scheme per file
  names/<group>.json       name lexicon (clusters of spellings)
```

## 1. Schemes (`data/schemes/<id>.json`)

A scheme converts text in one language/script into Latin script according to
one standard. The file name must equal `<id>.json`.

### Identifier

`<language>_<system>[_<variant>]`, lower case, underscores only.
`language` is the ISO 639-1 code (ISO 639-3 if there is no 639-1 code):
`ru_icao`, `ru_bgn_pcgn`, `ru_gost_7_79_b`, `uk_kmu_2010`, `bg_official`,
`ar_ala_lc`, `fa_ungegn`, `kk_latin_2021`, `uz_latin`, `latin_icao` (Latin
source, any language).

### Fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Identifier, equals the file name. |
| `title` | yes | Human-readable title, e.g. `"Russian — BGN/PCGN 1947"`. |
| `language` | yes | Source language code (`ru`, `uk`, `ar`, `fa`, …; `mul` for multi-language Latin folding). |
| `script` | yes | Source script, ISO 15924: `Cyrl`, `Arab`, `Latn`. |
| `kind` | yes | One of `passport`, `official`, `geographic`, `library`, `scholarly`, `practical`, `ascii`, `legacy`. |
| `status` | yes | `current`, `superseded`, `draft`, `informal`. |
| `year` | no | Year the system was adopted/introduced. |
| `ascii` | no | `true` if the output is guaranteed to be ASCII (checked by tests). |
| `reversible` | no | `true` if the system is designed to be reversible. |
| `authority` | no | Who defines it (law, order number, organisation). |
| `description` | yes | One or two sentences: where it is used, what is special. |
| `sources` | yes | List of URLs (primary sources first). |
| `notes` | no | List of strings: caveats, conflicts between sources. |
| `alphabet` | no | All letters of the source alphabet (lower case). Tests check every one has a mapping. |
| `extends` | no | Id of a parent scheme. Child `map`/`aliases`/`classes`/`options` are merged over the parent's (`null` deletes a parent entry); child `rules` are tried before the parent's (`"inherit_rules": false` drops them). `samples`, `notes`, `sources`, `description` are not inherited. |
| `classes` | no | Named character classes for contexts, e.g. `{"V": "аеёиоуыэюя"}`; refer to them as `{V}`. |
| `map` | yes* | Context-free mapping, lower-case keys → output. Keys may be several characters (`"зг"`). Value `""` deletes the character. |
| `rules` | no | Context-dependent rules (see below). |
| `aliases` | no | Character replacements applied to the input before matching, e.g. `{"’": "'", "ʼ": "'"}`. Upper-case variants are added automatically. |
| `case` | no | `auto` (default: restore case from source), `preserve` (output exactly as in map — Buckwalter), `upper`, `lower`. |
| `titlecase` | no | `true` for uncased source scripts (Arabic): capitalise each name part of the output. |
| `lowercase_words` | no | With `titlecase`: particles kept lower case unless they start the string. Entries ending in `-` are prefixes: `["al-", "ad-", "ibn", "bint"]`. |
| `geminate` | no | A combining mark meaning "double the previous consonant" (Arabic shadda, written `"\u0651"` in JSON). The engine repeats the previous letter's output. |
| `hook` | no | Name of a Python pre-processor. Only `"arabic"` exists (vocalisation via lexicon). |
| `options` | no | Options for the hook (see §3). |
| `post` | no | List of `{"pattern": <Python regex>, "replace": <string>}` applied to the output, in order. Use sparingly. |
| `fallback` | no | What to do with characters that have no mapping: `keep` (default), `drop`, `ascii` (fold to ASCII). |
| `samples` | yes | At least 3 `[source, expected_output]` pairs. **Prefer official examples quoted in the source document.** Every sample is a unit test. |

### Matching algorithm

1. Input is NFC-normalised, then `aliases` are applied.
2. At each position the engine collects all `rules` and `map` entries whose
   key matches the lower-cased input there. The **longest** key wins. Among
   keys of equal length, `rules` are tried in file order, then the `map`
   entry. The first one whose context conditions hold is applied.
3. If nothing matches, the character is kept (or dropped/folded, see `fallback`).
4. Output case is restored from the source: a lower-case source letter gives
   the value as written in the data; an upper-case one capitalises the first
   letter of the value (`Щ` → `Shch`, `Кс` → `X`); inside an all-caps word the
   whole value is upper-cased (`ЩЕРБАКОВ` → `SHCHERBAKOV`). **Write all keys
   and values in lower case.**

### Rules

```json
{"from": "е", "to": "ye", "after": "^{V}ъь"}
{"from": ["ий", "ый"], "to": "y", "end": true}
{"from": "я", "to": "ya", "start": true}
{"from": "с", "to": "ss", "after": "{V}", "before": "{V}"}
{"from": "ия", "to": "ia", "end": true}
```

| Key | Meaning |
|---|---|
| `from` | Lower-case source sequence, or a list of sequences sharing the same rule. |
| `to` | Output (lower case). |
| `start` | `true`: the match must begin a word. |
| `end` | `true`: the match must end a word. |
| `after` | Set of characters; the character immediately **before** the match must be in it. `^` in the set means "word start". |
| `not_after` | The character before the match must **not** be in the set (`^` = also fails at word start). |
| `before` | The character immediately **after** the match must be in the set. `$` means "word end". |
| `not_before` | The character after the match must not be in the set. |
| `note` | Free-text comment (ignored). |

A *word* is a run of letters and combining marks. Apostrophes (`' ’ ʼ ʻ ‘`)
count as word-internal when they sit between two letters, so in `Мар'яна` the
`я` is **not** word-initial and its "previous character" is `'`. Hyphens and
spaces separate words (`Анна-Яна` → `Anna-Yana` under KMU 2010).

Context is always evaluated on the **source** text, never on the output.

## 2. Name lexicon (`data/names/<group>.json`)

```json
{
  "description": "Common Arabic-origin given names",
  "sources": ["https://…"],
  "names": [
    {
      "id": "muhammad",
      "kind": "given",
      "gender": "m",
      "origin": "arabic",
      "english": "Muhammad",
      "native": {
        "ar": ["محمد"], "fa": ["محمد"], "ur": ["محمد"],
        "ru": ["Мухаммад", "Мухаммед", "Магомед", "Магомет", "Мохаммед"],
        "kk": ["Мұхаммед"], "tg": ["Муҳаммад"]
      },
      "vocalized": "مُحَمَّد",
      "latin": {
        "ar": ["Muhammad", "Mohammed", "Mohamed"],
        "ar_eg": ["Mohamed"], "ar_ma": ["Mohamed"], "ar_gulf": ["Mohammed"],
        "fa": ["Mohammad"], "ur": ["Muhammad"], "bn": ["Mohammad"],
        "tr": ["Mehmet", "Muhammed"], "az": ["Məhəmməd"], "uz": ["Muhammad"],
        "ms": ["Muhammad", "Mohamad"], "ru": ["Magomed", "Mukhammad"]
      },
      "variants": ["Muhammed", "Mohammad", "Mohamad", "Muhamad", "Mohamud", "Mehmed", "Mukhammed", "Mamed", "Mohd", "Md"],
      "short": [],
      "related": ["mahmud", "ahmad"]
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `id` | Unique, lower-case ASCII slug. Entries with the same id in different files are merged. |
| `kind` | `given`, `family`, `element` (name building blocks: `abd`, `bin`, `ibn`, `abu`, `umm`, `al`, `uddin`, `ullah`, `oglu`, `qizi`, `zadeh`), `compound` (multi-word names like `عبد الرحمن`). |
| `gender` | `m`, `f`, `u` (unknown/unisex). |
| `origin` | `arabic`, `persian`, `turkic`, `slavic`, `greek`, `hebrew`, `latin`, `germanic`, … |
| `english` | The single most common English spelling. |
| `native` | Native-script spellings keyed by language code (`ru`, `uk`, `be`, `bg`, `sr`, `mk`, `kk`, `ky`, `uz`, `tg`, `tt`, `ba`, `ce`, `az`, `ar`, `fa`, `ur`, `ps`, …). Latin-script languages (`pl`, `cs`, `tr`, `az`, `uz` …) put their national spelling here too, with diacritics. Arabic-script forms are written **without** vowel marks. |
| `vocalized` | Arabic-script form **with** full harakat (fatha/kasra/damma/sukun/shadda/tanwin). Required for Arabic-script names: it is what the standards (ALA-LC, DIN, BGN …) romanise. |
| `latin` | Conventional Latin spellings by language/region code, most common first. Region subtags: `ar_eg` (Egypt), `ar_ma` (Maghreb, French-influenced), `ar_gulf`, `ar_lev` (Levant). |
| `variants` | Additional attested Latin spellings (any source) for matching. ASCII where possible. |
| `equivalents` | Translation equivalents in other languages, **not** transliterations (`John` for Иван, `Michael` for Михаил, `Cyrus` for کوروش). Matched only weakly. |
| `short` | Diminutives/short forms (`Саша`, `Sasha` for Aleksandr). Used only for loose matching. |
| `related` | Ids of etymologically related but different names. |

## 3. Arabic-script hook options

Schemes with `"hook": "arabic"` accept `options`:

| Option | Default | Meaning |
|---|---|---|
| `lexicon` | `true` | Replace known names by their `vocalized` form before applying rules. |
| `practical` | — | List of lexicon `latin` keys, e.g. `["ar"]`. When set, known names are emitted directly in that conventional spelling (`محمد` → `Muhammad`). |
| `article` | `"al-"` | Article literal used for practical output (`الرشيد` → `al-Rashid`). |
| `vocalize` | `false` | Guess vowels for unknown names using Arabic name templates (فاعل → Khalid, فعيل → Karim, مفعول → Mahmud, أفعل → Ahmad …). |

Vowel marks present in the input are always respected.

## 4. Defaults (`data/defaults.json`)

```json
{"transliterate": {"ru": "ru_icao", "uk": "uk_kmu_2010"}}
```

`transliterate(text)` without a scheme detects the language and uses this map.
