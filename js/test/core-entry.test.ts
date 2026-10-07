// The /core entry point works without the lexicon (separate module graph in
// this test file: vitest isolates test files).
import { describe, expect, it } from "vitest";

import { getLexicon, mrzName, similarity, transliterate, variants } from "../src/core.js";

describe("translit-names/core (no lexicon)", () => {
  it("has an empty lexicon", () => {
    expect(getLexicon().size).toBe(0);
  });

  it("still transliterates, builds MRZ and matches", () => {
    expect(transliterate("Щербаков Юрий")).toBe("Shcherbakov Iurii");
    expect(mrzName("Щербаков", "Юрий")).toBe("SHCHERBAKOV<<IURII<<<<<<<<<<<<<<<<<<<<<");
    expect(similarity("Mukhammed", "Mohamed")).toBeGreaterThanOrEqual(0.9);
    expect(variants("Юрий", { limit: 5 })).toContain("Yuriy");
  });

  it("vocalises Arabic names by template", () => {
    expect(transliterate("خالد")).toBe("Khalid");
  });
});
