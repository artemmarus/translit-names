/** Shapes of the shared JSON data (see docs/data-format.md in the repository). */

export interface RuleSpec {
  from: string | string[];
  to: string;
  start?: boolean;
  end?: boolean;
  after?: string | string[];
  not_after?: string | string[];
  before?: string | string[];
  not_before?: string | string[];
  note?: string;
}

export interface SchemeSpec {
  id: string;
  title?: string;
  language?: string;
  script?: string;
  target_script?: string;
  kind?: string;
  status?: string;
  year?: number;
  ascii?: boolean;
  reversible?: boolean;
  authority?: string;
  description?: string;
  sources?: string[];
  notes?: string[];
  alphabet?: string;
  extends?: string;
  inherit_rules?: boolean;
  classes?: Record<string, string>;
  map?: Record<string, string | null>;
  rules?: RuleSpec[];
  aliases?: Record<string, string | null>;
  case?: "auto" | "preserve" | "upper" | "lower";
  titlecase?: boolean;
  lowercase_words?: string[];
  geminate?: string;
  hook?: string;
  options?: Record<string, unknown>;
  post?: { pattern: string; replace: string }[];
  fallback?: "keep" | "drop" | "ascii";
  samples?: [string, string][];
}

export interface NameSpec {
  id: string;
  kind?: string;
  gender?: string;
  origin?: string;
  english?: string;
  native?: Record<string, string | string[]>;
  latin?: Record<string, string | string[]>;
  variants?: string[];
  equivalents?: string[];
  short?: string[];
  vocalized?: string;
  related?: string[];
}

export interface LexiconFile {
  file: string;
  names: NameSpec[];
}

export interface DefaultsConfig {
  description?: string;
  transliterate: Record<string, string>;
  mrz?: Record<string, string>;
  match?: Record<string, string>;
  [purpose: string]: Record<string, string> | string | undefined;
}

export interface VariantRuleSpec {
  pattern: string;
  alts: string[];
  weight: number;
}

export interface VariantRulesFile {
  description?: string;
  [family: string]: VariantRuleSpec[] | string | undefined;
}
