/**
 * Character helpers with Python `str` semantics, so that the TypeScript port
 * behaves exactly like the Python reference implementation.
 *
 * Strings are processed as arrays of code points (`Array.from`), never as
 * UTF-16 code units.
 */

const RE_ALPHA = /^\p{L}$/u;
const RE_LETTER_OR_MARK = /^[\p{L}\p{Mn}\p{Mc}]$/u;
const RE_MN = /^\p{Mn}$/u;
const RE_UPPER = /^\p{Uppercase}$/u;
const RE_LOWER = /^\p{Lowercase}$/u;
const RE_TITLE = /^\p{Lt}$/u;
const RE_ALNUM = /^[\p{L}\p{N}]$/u;
const RE_SPACE = /^\s$/u;
// eslint-disable-next-line no-control-regex
const RE_ASCII = /^[\u0000-\u007f]*$/;

/** Split into code points. */
export const cps = (s: string): string[] => Array.from(s);

/** Python `ch.isalpha()` for one character. */
export const isAlpha = (c: string): boolean => RE_ALPHA.test(c);

/** Letters and (spacing or non-spacing) combining marks. */
export const isLetterOrMark = (c: string): boolean => RE_LETTER_OR_MARK.test(c);

/** Unicode category Mn (non-spacing mark). */
export const isMn = (c: string): boolean => RE_MN.test(c);

/** Python `unicodedata.combining(c) != 0` (approximated by category Mn). */
export const isCombining = isMn;

/** Python `ch.isalnum()` for one character. */
export const isAlnum = (c: string): boolean => RE_ALNUM.test(c);

/** Python `ch.isspace()` for one character. */
export const isSpace = (c: string): boolean => RE_SPACE.test(c);

/** Python `s.isascii()`. */
export const isAscii = (s: string): boolean => RE_ASCII.test(s);

/** Python `ch.isupper()` for a single character. */
export const isUpper1 = (c: string): boolean => RE_UPPER.test(c);

/** Python `ch.istitle()` for a single character (category Lt). */
export const isTitle1 = (c: string): boolean => RE_TITLE.test(c);

/** Python `ch.islower()` for a single character. */
export const isLower1 = (c: string): boolean => RE_LOWER.test(c);

/** Python `s.isupper()`: at least one cased character and none lower/title case. */
export function pyIsUpper(s: string): boolean {
  let cased = false;
  for (const c of s) {
    if (RE_LOWER.test(c) || RE_TITLE.test(c)) return false;
    if (!cased && RE_UPPER.test(c)) cased = true;
  }
  return cased;
}

/** Python `s.islower()`. */
export function pyIsLower(s: string): boolean {
  let cased = false;
  for (const c of s) {
    if (RE_UPPER.test(c) || RE_TITLE.test(c)) return false;
    if (!cased && RE_LOWER.test(c)) cased = true;
  }
  return cased;
}

/** Python `ch.lower() != ch.upper()`. */
export const isCased = (c: string): boolean => c.toLowerCase() !== c.toUpperCase();

/** Lower-case one character without changing the length (`İ` → `i`). */
export function lower1(c: string): string {
  const low = c.toLowerCase();
  const arr = cps(low);
  return arr.length === 1 ? low : (arr[0] ?? low);
}

/** Python `s.strip(chars)`. */
export function strip(s: string, chars: string): string {
  const arr = cps(s);
  let i = 0;
  let j = arr.length;
  while (i < j && chars.includes(arr[i] as string)) i++;
  while (j > i && chars.includes(arr[j - 1] as string)) j--;
  return arr.slice(i, j).join("");
}

/** Python `s.rstrip(chars)`. */
export function rstrip(s: string, chars: string): string {
  const arr = cps(s);
  let j = arr.length;
  while (j > 0 && chars.includes(arr[j - 1] as string)) j--;
  return arr.slice(0, j).join("");
}

/** Python `s.split()` (whitespace, no empty strings). */
export const splitWs = (s: string): string[] => s.split(/\s+/u).filter((x) => x !== "");

/** Python `s.capitalize()` for the ASCII strings it is used on. */
export const capitalize = (s: string): string => {
  const arr = cps(s);
  if (!arr.length) return s;
  return (arr[0] as string).toUpperCase() + arr.slice(1).join("").toLowerCase();
};

/**
 * Python's `round(x, n)`: correctly rounded, ties to even, on the exact
 * binary value of `x` (Math.round would round 0.03125 to 0.0313; Python
 * gives 0.0312).
 */
export function pyRound(x: number, n: number): number {
  if (!Number.isFinite(x)) return x;
  const neg = x < 0;
  const s = Math.abs(x).toFixed(Math.min(100, n + 40));
  const [intPart, frac = ""] = s.split(".");
  const keep = frac.slice(0, n);
  const rest = frac.slice(n);
  let digits = (intPart ?? "0") + keep;
  const first = rest.charCodeAt(0) - 48;
  const tail = rest.slice(1);
  let up = false;
  if (first > 5) up = true;
  else if (first === 5) {
    if (/[1-9]/.test(tail)) up = true;
    else up = ((digits.charCodeAt(digits.length - 1) - 48) & 1) === 1;
  }
  if (up) {
    const arr = digits.split("").map(Number);
    let k = arr.length - 1;
    while (k >= 0) {
      if ((arr[k] as number) < 9) {
        arr[k] = (arr[k] as number) + 1;
        break;
      }
      arr[k] = 0;
      k--;
    }
    if (k < 0) arr.unshift(1);
    digits = arr.join("");
  }
  const intLen = digits.length - n;
  const out = Number(n > 0 ? `${digits.slice(0, intLen)}.${digits.slice(intLen)}` : digits);
  return neg ? -out : out;
}

/** Python-style string comparison by code point (UTF-16 order differs only outside the BMP). */
export function cmpStr(a: string, b: string): number {
  if (a === b) return 0;
  const aa = cps(a);
  const bb = cps(b);
  const n = Math.min(aa.length, bb.length);
  for (let i = 0; i < n; i++) {
    const x = (aa[i] as string).codePointAt(0) as number;
    const y = (bb[i] as string).codePointAt(0) as number;
    if (x !== y) return x < y ? -1 : 1;
  }
  return aa.length < bb.length ? -1 : aa.length > bb.length ? 1 : 0;
}
