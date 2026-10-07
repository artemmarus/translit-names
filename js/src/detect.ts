/** Guess the script and language of a personal name from its letters (port of `detect.py`). */

import { scriptOf } from "./normalize.js";
import { cps, isAlpha, isAscii, pyRound } from "./unicode.js";

const RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя";
const CYRILLIC: Readonly<Record<string, readonly [string, number]>> = {
  ru: [RU, 3.0],
  uk: ["абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'\u2019\u02bc", 2.0],
  be: ["абвгдеёжзійклмнопрстуўфхцчшыьэюя'\u2019\u02bc", 1.5],
  bg: ["абвгдежзийклмнопрстуфхцчшщъьюя", 1.5],
  sr: ["абвгдђежзијклљмнњопрстћуфхцчџш", 1.2],
  mk: ["абвгдѓежзѕијклљмнњопрстќуфхцчџш", 1.0],
  kk: [RU + "әғқңөұүһі", 1.0],
  ky: [RU + "ңөү", 0.8],
  uz: ["абвгдеёжзийклмнопрстуфхцчшъьэюяўқғҳ", 0.8],
  tg: ["абвгғдеёжзиӣйкқлмнопрстуӯфхҳчҷшъэюя", 0.8],
  tt: [RU + "әөүҗңһ", 0.7],
  ba: [RU + "әөүғҡңҙҫһ", 0.6],
  ce: [RU + "ӏ", 0.6],
};
const CYRILLIC_MARKERS: Readonly<Record<string, Readonly<Record<string, number>>>> = {
  ґ: { uk: 3 }, є: { uk: 3 }, ї: { uk: 3 }, ў: { be: 3, uz: 1 }, ы: { ru: 0.5, be: 0.5 },
  і: { uk: 1, be: 1, kk: 0.5 }, ъ: { ru: 0.3, bg: 0.6 }, ђ: { sr: 3 }, ћ: { sr: 3 }, ѓ: { mk: 3 },
  ќ: { mk: 3 }, ѕ: { mk: 3 }, љ: { sr: 1, mk: 1 }, њ: { sr: 1, mk: 1 }, џ: { sr: 1, mk: 1 }, ј: { sr: 1, mk: 1 },
  ұ: { kk: 4 }, ә: { kk: 2, tt: 1.5, ba: 1.2 }, ғ: { kk: 1.5, uz: 1.5, tg: 1.5, ba: 1 },
  қ: { kk: 2, uz: 1.5, tg: 1.5 }, ң: { kk: 1.5, ky: 1.5, tt: 1, ba: 1 }, ө: { kk: 1.5, ky: 1.5, tt: 1, ba: 1 },
  ү: { kk: 1.5, ky: 1.5, tt: 1, ba: 1 }, һ: { kk: 1, tt: 1, ba: 1 }, ҳ: { uz: 2, tg: 2 }, ҷ: { tg: 4 },
  ӣ: { tg: 4 }, ӯ: { tg: 4 }, җ: { tt: 4 }, ҡ: { ba: 4 }, ҙ: { ba: 4 }, ҫ: { ba: 4 }, ӏ: { ce: 4 },
};

const AR_BASE = "ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىي";
const AR_NO_KY = AR_BASE.replace("ك", "").replace("ي", "");
const ARABIC: Readonly<Record<string, readonly [string, number]>> = {
  ar: [AR_BASE + "ٱ", 3.0],
  fa: [AR_NO_KY + "پچژگکیۀ", 2.0],
  ur: [AR_NO_KY + "پچژگکیٹڈڑںھہےۃ", 1.5],
  ps: [AR_NO_KY + "پچژګگکیټډړږښځڅڼېۍ", 1.0],
};
const ARABIC_MARKERS: Readonly<Record<string, Readonly<Record<string, number>>>> = {
  "ك": { ar: 1 }, "ي": { ar: 1 }, "ة": { ar: 1 }, "ى": { ar: 0.5 },
  "ی": { fa: 1, ur: 0.8, ps: 0.6 }, "ک": { fa: 1, ur: 0.8, ps: 0.4 },
  "پ": { fa: 1, ur: 1 }, "چ": { fa: 1, ur: 1 }, "ژ": { fa: 1.5 }, "گ": { fa: 1, ur: 1 },
  "ٹ": { ur: 4 }, "ڈ": { ur: 4 }, "ڑ": { ur: 4 }, "ں": { ur: 4 }, "ھ": { ur: 3 }, "ہ": { ur: 3 },
  "ے": { ur: 4 }, "ۃ": { ur: 2 }, "ټ": { ps: 4 }, "ډ": { ps: 4 }, "ړ": { ps: 4 }, "ږ": { ps: 4 },
  "ښ": { ps: 4 }, "ځ": { ps: 4 }, "څ": { ps: 4 }, "ڼ": { ps: 4 }, "ې": { ps: 4 }, "ۍ": { ps: 4 },
  "ګ": { ps: 4 }, "ۀ": { fa: 2 },
};

const LATIN_MARKERS: Readonly<Record<string, Readonly<Record<string, number>>>> = {
  ł: { pl: 4 }, ą: { pl: 4 }, ę: { pl: 4 }, ś: { pl: 3 }, ź: { pl: 3 }, ż: { pl: 4 }, ń: { pl: 3 },
  ř: { cs: 4 }, ů: { cs: 4 }, ě: { cs: 4 }, ď: { cs: 2, sk: 2 }, ť: { cs: 2, sk: 2 }, ň: { cs: 1.5, sk: 1.5, tk: 1 },
  ľ: { sk: 4 }, ĺ: { sk: 4 }, ŕ: { sk: 4 }, ô: { sk: 2 }, đ: { sh: 4 }, ć: { sh: 2, pl: 2 },
  č: { sh: 1.5, sl: 1.5, cs: 1.5, sk: 1.5 }, š: { sh: 1.5, sl: 1.5, cs: 1.5, sk: 1.5 },
  ž: { sh: 1.5, sl: 1.5, cs: 1.5, sk: 1.5, tk: 1 }, ǆ: { sh: 4 }, ǉ: { sh: 4 }, ǌ: { sh: 4 },
  ğ: { tr: 2, az: 2 }, ı: { tr: 2, az: 2, kk: 1 }, ş: { tr: 1.5, az: 1.5, tk: 1.5, kk: 1 },
  ç: { tr: 1.5, az: 1.5, tk: 1.5 }, ə: { az: 5 }, ö: { tr: 1, az: 1, tk: 1 }, ü: { tr: 1, az: 1, tk: 1 },
  ä: { tk: 2, sk: 1, kk: 1 }, ý: { tk: 2, cs: 1, sk: 1 }, ū: { kk: 3 }, ñ: { kk: 2 },
  "\u02bb": { uz: 4 }, "\u2018": { uz: 1 }, â: { tr: 0.5 },
};
const LATIN_PRIOR: Readonly<Record<string, number>> = {
  tr: 1.0, pl: 1.0, cs: 0.8, sh: 0.8, az: 0.8, uz: 0.8, sk: 0.6, sl: 0.6, tk: 0.5, kk: 0.4,
};

/** Result of `detectLanguage()`. */
export interface Detection {
  language: string;
  script: string;
  confidence: number;
  candidates: [string, number][];
}

/** Dominant script: `Cyrl`, `Arab`, `Latn`, `Grek` or `Zyyy`. */
export function detectScript(text: string): string {
  const counts = new Map<string, number>();
  for (const c of text.normalize("NFC")) {
    const s = scriptOf(c);
    if (s !== "Zyyy") counts.set(s, (counts.get(s) ?? 0) + 1);
  }
  let best = "Zyyy";
  let bestN = 0;
  for (const [s, n] of counts) {
    if (n > bestN) {
      best = s;
      bestN = n;
    }
  }
  return best;
}

function score(
  letters: Map<string, number>,
  alphabets: Readonly<Record<string, readonly [string, number]>>,
  markers: Readonly<Record<string, Readonly<Record<string, number>>>>,
): Map<string, number> {
  const scores = new Map<string, number>();
  for (const [lang, [alphabet, prior]] of Object.entries(alphabets)) {
    let missing = 0;
    for (const [ch, n] of letters) if (!alphabet.includes(ch)) missing += n;
    scores.set(lang, prior - 6.0 * missing);
  }
  for (const ch of letters.keys()) {
    for (const [lang, bonus] of Object.entries(markers[ch] ?? {})) {
      if (scores.has(lang)) scores.set(lang, (scores.get(lang) as number) + bonus);
    }
  }
  return scores;
}

const UK_HINTS = ["ськ", "цьк", "зьк", "ньк", "ьо"];

function ukrainianHint(text: string): number {
  const low = text.toLowerCase();
  return UK_HINTS.reduce((acc, h) => acc + (low.includes(h) ? 1.5 : 0), 0);
}

function bulgarianHint(text: string): number {
  const low = cps(text.toLowerCase());
  let bonus = 0;
  low.forEach((ch, i) => {
    if (ch === "ъ") {
      const nxt = low[i + 1] ?? " ";
      if (!"еёюя".includes(nxt)) bonus += 2.5;
    }
  });
  return bonus;
}

function counter(chars: Iterable<string>): Map<string, number> {
  const m = new Map<string, number>();
  for (const c of chars) m.set(c, (m.get(c) ?? 0) + 1);
  return m;
}

/**
 * Guess the language of a name: `ru`, `uk`, `kk`, `ar`, `fa`, `ur`, `tr`,
 * `pl` …  Plain ASCII Latin text gives `"en"`; Latin text with diacritics
 * that match no profile gives `"mul"`.  `hint` breaks ties in its favour.
 */
export function detectLanguage(text: string, options: { hint?: string } = {}): Detection {
  const t = text.normalize("NFC");
  const script = detectScript(t);
  const all = cps(t.toLowerCase()).filter((c) => isAlpha(c) || "'\u2019\u02bc\u02bb\u2018".includes(c));
  let scores: Map<string, number>;
  if (script === "Cyrl") {
    const letters = counter(all.filter((c) => scriptOf(c) === "Cyrl" || "'\u2019\u02bc".includes(c)));
    scores = score(letters, CYRILLIC, CYRILLIC_MARKERS);
    scores.set("bg", (scores.get("bg") as number) + bulgarianHint(t));
    scores.set("uk", (scores.get("uk") as number) + ukrainianHint(t));
  } else if (script === "Arab") {
    scores = score(counter(all.filter((c) => scriptOf(c) === "Arab")), ARABIC, ARABIC_MARKERS);
  } else if (script === "Latn") {
    const letters = counter(all);
    scores = new Map(Object.keys(LATIN_PRIOR).map((k) => [k, 0.0]));
    for (const ch of letters.keys()) {
      for (const [lang, bonus] of Object.entries(LATIN_MARKERS[ch] ?? {})) {
        scores.set(lang, (scores.get(lang) ?? 0) + bonus);
      }
    }
    const low = t.toLowerCase();
    if (["o\u2018", "g\u2018", "o\u02bb", "g\u02bb"].some((s) => low.includes(s))) {
      scores.set("uz", (scores.get("uz") ?? 0) + 4);
    }
    if (![...scores.values()].some((v) => v > 0)) {
      const lang = isAscii(t) ? "en" : "mul";
      return { language: lang, script, confidence: lang === "en" ? 0.5 : 0.3, candidates: [[lang, 1.0]] };
    }
    for (const [lang, prior] of Object.entries(LATIN_PRIOR)) {
      if ((scores.get(lang) ?? 0) > 0) scores.set(lang, (scores.get(lang) as number) + prior * 0.1);
    }
  } else {
    return { language: "und", script, confidence: 0.0, candidates: [] };
  }
  if (options.hint && scores.has(options.hint)) {
    scores.set(options.hint, (scores.get(options.hint) as number) + 1.5);
  }
  const ranked = [...scores.entries()].sort((a, b) => b[1] - a[1]);
  const [best, bestScore] = ranked[0] as [string, number];
  const second = ranked.length > 1 ? (ranked[1] as [string, number])[1] : bestScore - 3;
  const margin = bestScore - second;
  const confidence = bestScore > -3 ? Math.max(0.05, Math.min(0.99, 0.5 + margin / 6.0)) : 0.05;
  return {
    language: best,
    script,
    confidence: pyRound(confidence, 3),
    candidates: ranked.slice(0, 5).map(([k, v]) => [k, pyRound(v, 3)]),
  };
}
