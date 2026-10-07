import { describe, expect, it } from "vitest";

import {
  Scheme,
  SchemeError,
  compare,
  defaultSchemeId,
  detectLanguage,
  fixMixedScript,
  fold,
  getLexicon,
  getScheme,
  isMatch,
  listSchemes,
  mrzName,
  mrzText,
  nameKey,
  nameKeys,
  parseMrzName,
  schemeSpecs,
  similarity,
  titlecaseName,
  transliterate,
  variants,
  variantsDetailed,
} from "../src/index.js";
import { pyPatternSource, pyReplacement } from "../src/pyregex.js";
import { pyRound } from "../src/unicode.js";

describe("schemes", () => {
  const specs = [...schemeSpecs().values()];

  it("bundles every scheme", () => {
    expect(listSchemes().length).toBeGreaterThanOrEqual(80);
  });

  it.each(specs.map((s) => [s.id, s] as const))("%s reproduces its official samples", (_id, spec) => {
    const scheme = getScheme(spec.id);
    for (const [src, expected] of spec.samples ?? []) expect(scheme.transliterate(src)).toBe(expected);
  });

  it("filters", () => {
    expect(listSchemes({ language: "uk" }).every((s) => s.language === "uk")).toBe(true);
    expect(listSchemes({ kind: "passport" }).every((s) => s.kind === "passport")).toBe(true);
  });

  it("accepts aliases of ids and language codes", () => {
    expect(getScheme("uk-kmu-2010").id).toBe("uk_kmu_2010");
    expect(getScheme("ru").id).toBe("ru_icao");
    expect(() => getScheme("xx_nope")).toThrow(RangeError);
  });

  it("every default points to an existing scheme", () => {
    expect(defaultSchemeId("az", "mrz", "Latn")).toBe("az_ascii");
    expect(defaultSchemeId("ru")).toBe("ru_icao");
    expect(defaultSchemeId("xx")).toBeNull();
  });
});

describe("transliterate", () => {
  it.each([
    ["Щербаков Юрий", "Shcherbakov Iurii"],
    ["Сергій Корольов", "Serhii Korolov"],
    ["Нұрсұлтан Назарбаев", "Nursultan Nazarbayev"],
    ["Эмомалӣ Раҳмон", "Emomali Rahmon"],
    ["Новак Ђоковић", "Novak Đoković"],
    ["محمد بن سلمان", "Muhammad bin Salman"],
    ["John Smith", "John Smith"],
  ])("%s → %s", (src, out) => {
    expect(transliterate(src)).toBe(out);
  });

  it("explicit scheme and language", () => {
    expect(transliterate("Щербаков Юрий", "ru_bgn_pcgn")).toBe("Shcherbakov Yuriy");
    expect(transliterate("Христо Стоичков", null, { language: "bg" })).toBe("Hristo Stoichkov");
    expect(transliterate("Олександр Згурський", null, { language: "uk" })).toBe("Oleksandr Zghurskyi");
    expect(transliterate("عبد الرحمن", "ar_ala_lc")).toBe("ʻAbd al-Raḥmān");
  });

  it("repairs mixed scripts", () => {
    expect(transliterate("Иванoв")).toBe("Ivanov");
    expect(fixMixedScript("Аlexey")).toBe("Alexey");
  });
});

describe("engine", () => {
  const uk = new Scheme({
    id: "t",
    map: { "з": "z", "г": "h", "а": "a", "я": "ia", "н": "n", "о": "o", "р": "r", "и": "y", "'": "" },
    rules: [
      { from: "я", to: "ya", start: true },
      { from: "зг", to: "zgh" },
    ],
  });

  it("context rules, apostrophes and case", () => {
    expect(uk.transliterate("Згорани")).toBe("Zghorany");
    expect(uk.transliterate("Яна-Яна")).toBe("Yana-Yana");
    expect(uk.transliterate("ЗГОРАНИ")).toBe("ZGHORANY");
  });

  it("rejects malformed specs", () => {
    expect(() => new Scheme({ id: "x", case: "weird" as never })).toThrow(SchemeError);
    expect(() => new Scheme({ id: "x", rules: [{ from: "a", to: "b", after: "{NOPE}" }] })).toThrow(SchemeError);
    expect(() => new Scheme({ id: "x", hook: "missing" })).toThrow(SchemeError);
  });

  it("titlecases particles", () => {
    expect(titlecaseName("hārūn al-rashīd", ["al-"])).toBe("Hārūn al-Rashīd");
    expect(titlecaseName("muḥammad ibn ʻabd allāh", ["ibn"])).toBe("Muḥammad ibn ʻAbd Allāh");
  });
});

describe("MRZ (ICAO Doc 9303 examples)", () => {
  it.each([
    ["ERIKSSON", "ANNA MARIA", "ERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"],
    ["SMITH-JONES", "SUSIE MARGARET", "SMITH<JONES<<SUSIE<MARGARET<<<<<<<<<<<<"],
    ["O'CONNOR", "ENYA SIOBHAN", "OCONNOR<<ENYA<SIOBHAN<<<<<<<<<<<<<<<<<<"],
    ["AL-BASRI", "HUDA MUHAMMAD JAWAD", "AL<BASRI<<HUDA<MUHAMMAD<JAWAD<<<<<<<<<<"],
    ["NILAVADHANANANDA", "ARNPOL PETCH CHARONGUANG", "NILAVADHANANANDA<<ARNPOL<PETCH<CHARONGU"],
    ["Щербаков", "Юрий", "SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<"],
  ])("%s, %s", (s, g, out) => {
    expect(mrzName(s, g)).toBe(out);
  });

  it("strategies and helpers", () => {
    expect(mrzName("NILAVADHANANANDA", "CHAYAPA DEJTHAMRONG KRASUANG", { strategy: "initials" })).toBe(
      "NILAVADHANANANDA<<CHAYAPA<DEJTHAMRONG<K",
    );
    const td1 = mrzName("BENNELONG WOOLOOMOOLOO WARRANDYTE WARNAMBOOL", "DINGO POTOROO", { length: 30 });
    expect(td1).toHaveLength(30);
    expect(/[A-Z]$/.test(td1)).toBe(true);
    expect(mrzText("Müller", { german: true })).toBe("MUELLER");
    expect(parseMrzName("AL<BASRI<<HUDA<MUHAMMAD<<<")).toEqual(["AL BASRI", "HUDA MUHAMMAD"]);
  });
});

describe("matching", () => {
  it.each([
    ["Щербаков Юрий", "Yuri Scherbakov"],
    ["Хрущёв", "Chruschtschow"],
    ["Мухаммед Али", "Mohammed Ali"],
    ["Магомед", "Mehmet"],
    ["حسين", "Hüseyin"],
    ["عبد الرحمن", "Abderrahmane"],
    ["Ivanov Ivan Ivanovich", "IVAN IVANOV"],
    ["Abdul Rahman", "Abdulrahman"],
  ])("%s ~ %s", (a, b) => {
    expect(similarity(a, b)).toBeGreaterThanOrEqual(0.88);
  });

  it.each([
    ["Hasan", "Husayn"],
    ["Said", "Zayd"],
    ["Alexander Smith", "Alexandra Smith"],
    ["John Smith", "Ivan Petrov"],
  ])("%s ≠ %s", (a, b) => {
    expect(similarity(a, b)).toBeLessThan(0.88);
  });

  it("explains weak relations", () => {
    expect(compare("Michael", "Михаил").pairs[0]?.reason).toBe("equivalent");
    expect(compare("Саша", "Александр").pairs[0]?.reason).toBe("diminutive");
    expect(isMatch("Мухаммед", "Mohammed")).toBe(true);
    expect(isMatch("Мухаммед", "Mohammed", { threshold: 0.999 })).toBe(false);
  });

  it("keys", () => {
    expect(nameKeys("Mohammed")).toEqual(["MHMT"]);
    expect(nameKey("Ivan Ivanov")).toBe(nameKey("Иванов Иван"));
  });
});

describe("variants", () => {
  it("covers every passport generation", () => {
    const out = variants("Юрий", { limit: 12 });
    expect(out[0]).toBe("Iurii");
    for (const v of ["Yuriy", "Yuri", "Yury"]) expect(out).toContain(v);
  });

  it("uses the lexicon for Arabic names", () => {
    const out = variants("محمد", { limit: 8 });
    expect(out[0]).toBe("Muhammad");
    expect(out).toEqual(expect.arrayContaining(["Mohammed", "Mohamed", "Mohammad"]));
  });

  it("returns sorted scores with sources", () => {
    const vs = variantsDetailed("Хусейн", { limit: 10 });
    expect(vs.map((v) => v.score)).toEqual([...vs.map((v) => v.score)].sort((a, b) => b - a));
    expect(vs[0]?.sources.length).toBeGreaterThan(0);
  });
});

describe("misc", () => {
  it("detects languages", () => {
    expect(detectLanguage("Олександр Їжакевич").language).toBe("uk");
    expect(detectLanguage("عمران خان ٹیپو").language).toBe("ur");
    expect(detectLanguage("İlham Əliyev").language).toBe("az");
    expect(detectLanguage("John Smith").language).toBe("en");
  });

  it("folds Latin letters", () => {
    expect(fold("Łódź Ærø Þór Məmmədov İstanbul")).toBe("Lodz Aeroe Thor Mammadov Istanbul");
    expect(fold("Ä Ö Ü", { german: true })).toBe("AE OE UE");
  });

  it("lexicon", () => {
    const lex = getLexicon();
    expect(lex.size).toBeGreaterThan(1000);
    expect(lex.lookup("Магомед").map((e) => e.id)).toContain("muhammad");
    expect(lex.lookup("Вольдемарище")).toEqual([]);
  });

  it("Python helpers", () => {
    expect(pyRound(0.03125, 4)).toBe(0.0312); // ties to even, like Python
    expect(pyRound(0.98765, 3)).toBe(0.988);
    expect(pyRound(2.5, 0)).toBe(2);
    expect(pyReplacement("\\1-x$")).toBe("$1-x$$");
    expect(new RegExp(pyPatternSource("\\bab\\w+"), "u").test("ā abč")).toBe(true);
  });
});
