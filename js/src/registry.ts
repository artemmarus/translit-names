/** Loading and lookup of the bundled transliteration schemes (port of `_registry.py`). */

import { arabicHook } from "./arabic.js";
import DEFAULTS from "./data/defaults.js";
import SCHEME_FILES from "./data/schemes.js";
import { Scheme, SchemeError, type WordHook } from "./engine.js";
import type { DefaultsConfig, SchemeSpec } from "./types.js";

const HOOKS: Readonly<Record<string, WordHook>> = { arabic: arabicHook };
const MERGED_KEYS = new Set(["map", "aliases", "classes", "options"]);
const NOT_INHERITED = new Set(["samples", "notes", "sources", "description"]);

let specs: Map<string, SchemeSpec> | null = null;
const compiled = new Map<string, Scheme>();

function resolve(sid: string, raw: ReadonlyMap<string, SchemeSpec>, chain: readonly string[]): SchemeSpec {
  if (chain.includes(sid)) throw new SchemeError(`inheritance cycle: ${[...chain, sid].join(" -> ")}`);
  const spec = raw.get(sid) as SchemeSpec;
  const parentId = spec.extends;
  if (!parentId) return { ...spec };
  if (!raw.has(parentId)) throw new SchemeError(`${sid}: extends unknown scheme ${JSON.stringify(parentId)}`);
  const parent = resolve(parentId, raw, [...chain, sid]) as unknown as Record<string, unknown>;
  const merged: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(parent)) if (!NOT_INHERITED.has(k)) merged[k] = v;
  const inherit = spec.inherit_rules ?? true;
  for (const [key, value] of Object.entries(spec)) {
    if (MERGED_KEYS.has(key)) {
      const combined: Record<string, unknown> = { ...((parent[key] as Record<string, unknown>) ?? {}) };
      for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
        // a JSON object key that is re-set must move to the end, as in a Python dict update
        if (!(k in combined)) combined[k] = v;
        else combined[k] = v;
      }
      merged[key] = Object.fromEntries(Object.entries(combined).filter(([, v]) => v !== null));
    } else if (key === "rules") {
      merged["rules"] = [...(value as unknown[]), ...(inherit ? ((parent["rules"] as unknown[]) ?? []) : [])];
    } else {
      merged[key] = value;
    }
  }
  if (!("rules" in spec) && !inherit) merged["rules"] = [];
  delete merged["inherit_rules"];
  return merged as unknown as SchemeSpec;
}

function loadSpecs(): Map<string, SchemeSpec> {
  if (specs) return specs;
  const raw = new Map<string, SchemeSpec>();
  for (const spec of SCHEME_FILES) {
    if (!spec.id) throw new SchemeError("scheme without 'id'");
    raw.set(spec.id, spec);
  }
  const out = new Map<string, SchemeSpec>();
  for (const sid of raw.keys()) out.set(sid, resolve(sid, raw, []));
  specs = out;
  return out;
}

const canon = (sid: string): string => sid.trim().toLowerCase().replace(/[-\s.]/g, "_");

/** Resolved JSON specs of every bundled scheme, keyed by id. */
export function schemeSpecs(): ReadonlyMap<string, SchemeSpec> {
  return loadSpecs();
}

/** The parsed `defaults.json`. */
export function defaultsConfig(): DefaultsConfig {
  return DEFAULTS;
}

/**
 * Compiled scheme by id (`"ru_icao"`, `"uk-kmu-2010"` …).  A bare language
 * code (`"ru"`) returns that language's default scheme.
 */
export function getScheme(schemeId: string): Scheme {
  const all = loadSpecs();
  let sid = canon(schemeId);
  if (!all.has(sid)) {
    const def = DEFAULTS.transliterate[sid];
    if (def) sid = def;
    else throw new RangeError(`unknown scheme ${JSON.stringify(schemeId)}; see listSchemes()`);
  }
  let scheme = compiled.get(sid);
  if (!scheme) {
    scheme = new Scheme(all.get(sid) as SchemeSpec, HOOKS);
    compiled.set(sid, scheme);
  }
  return scheme;
}

export interface ListSchemesOptions {
  language?: string;
  kind?: string;
  status?: string;
  script?: string;
}

/** List bundled schemes (sorted by id), optionally filtered. */
export function listSchemes(options: ListSchemesOptions = {}): Scheme[] {
  const out: Scheme[] = [];
  const ids = [...loadSpecs().keys()].sort();
  for (const sid of ids) {
    const spec = loadSpecs().get(sid) as SchemeSpec;
    if (options.language && spec.language !== options.language) continue;
    if (options.kind && spec.kind !== options.kind) continue;
    if (options.status && (spec.status ?? "current") !== options.status) continue;
    if (options.script && spec.script !== options.script) continue;
    out.push(getScheme(sid));
  }
  return out;
}

/**
 * Default scheme id for a language and purpose (`"transliterate"`, `"mrz"`,
 * `"match"`), optionally restricted to a source script.
 */
export function defaultSchemeId(language: string, purpose = "transliterate", script?: string | null): string | null {
  const all = loadSpecs();
  const sections: Record<string, string>[] = [((DEFAULTS[purpose] as Record<string, string>) ?? {})];
  if (purpose !== "transliterate") sections.push(DEFAULTS.transliterate);
  for (const table of sections) {
    const keys = script ? [`${language}-${script}`, language] : [language];
    for (const key of keys) {
      const sid = table[key];
      if (sid && all.has(sid) && (!script || all.get(sid)?.script === script)) return sid;
    }
  }
  return null;
}
