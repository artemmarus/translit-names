/**
 * Translation of the Python regular expressions stored in the shared JSON
 * data (scheme `post` rules, variant rules) into JavaScript.
 *
 * Python's `\w`, `\b` and `\d` are Unicode-aware; JavaScript's are ASCII-only
 * even with the `u` flag, so they are rewritten with Unicode property
 * escapes.  Replacement strings use `\1` / `\g<name>` in Python and `$1` /
 * `$<name>` in JavaScript.
 */

const W = "\\p{L}\\p{N}_";
const SYNTAX = "^$\\.*+?()[]{}|/";

function hex(c: string): string {
  const cp = c.codePointAt(0) as number;
  return cp > 0xffff ? `\\u{${cp.toString(16)}}` : `\\u${cp.toString(16).padStart(4, "0")}`;
}

/** Convert a Python `re` pattern to an equivalent JavaScript `RegExp` source. */
export function pyPatternSource(src: string): string {
  let out = "";
  let i = 0;
  let inClass = false;
  while (i < src.length) {
    const c = src[i] as string;
    if (c === "\\") {
      const n = src[i + 1];
      if (n === undefined) throw new SyntaxError(`trailing backslash in ${JSON.stringify(src)}`);
      if (n === "u" || n === "x" || n === "U" || n === "N") {
        // \uXXXX, \xXX: same meaning in both dialects (with the u flag)
        if (n === "U") {
          out += `\\u{${src.slice(i + 2, i + 10).replace(/^0+/, "")}}`;
          i += 10;
          continue;
        }
        out += c + n;
        i += 2;
        continue;
      }
      if (inClass) {
        if (n === "w") out += W;
        else if (n === "d") out += "\\p{Nd}";
        else if (n === "s" || n === "S" || /[0-9a-zA-Z]/.test(n)) {
          if (n === "W" || n === "D") throw new SyntaxError(`unsupported \\${n} in a class: ${src}`);
          out += c + n;
        } else if (SYNTAX.includes(n) || n === "-") out += c + n;
        else out += hex(n);
        i += 2;
        continue;
      }
      switch (n) {
        case "w":
          out += `[${W}]`;
          break;
        case "W":
          out += `[^${W}]`;
          break;
        case "d":
          out += "\\p{Nd}";
          break;
        case "D":
          out += "\\P{Nd}";
          break;
        case "b":
          out += `(?:(?<=[${W}])(?![${W}])|(?<![${W}])(?=[${W}]))`;
          break;
        case "B":
          out += `(?:(?<=[${W}])(?=[${W}])|(?<![${W}])(?![${W}]))`;
          break;
        case "A":
          out += "^";
          break;
        case "Z":
          out += "$";
          break;
        default:
          if (/[0-9a-zA-Z]/.test(n) || SYNTAX.includes(n)) out += c + n;
          else out += hex(n);
      }
      i += 2;
      continue;
    }
    if (inClass) {
      if (c === "]") inClass = false;
      out += c;
      i++;
      continue;
    }
    if (c === "[") {
      if (src.startsWith("[^\\W\\d_]", i)) {
        out += "[\\p{L}\\p{No}\\p{Nl}]";
        i += 8;
        continue;
      }
      inClass = true;
      out += c;
      i++;
      if (src[i] === "^") {
        out += "^";
        i++;
      }
      if (src[i] === "]") {
        out += "\\]";
        i++;
      }
      continue;
    }
    if (src.startsWith("(?P<", i)) {
      out += "(?<";
      i += 4;
      continue;
    }
    if (src.startsWith("(?P=", i)) {
      const end = src.indexOf(")", i);
      out += `\\k<${src.slice(i + 4, end)}>`;
      i = end + 1;
      continue;
    }
    if (c === "{") {
      const q = /^\{\d+(?:,\d*)?\}/.exec(src.slice(i));
      if (q) {
        out += q[0];
        i += q[0].length;
      } else {
        out += "\\{";
        i++;
      }
      continue;
    }
    if (c === "}") {
      out += "\\}";
      i++;
      continue;
    }
    out += c;
    i++;
  }
  return out;
}

/** Compile a Python pattern. `flags` are JavaScript flags (`u` is always added). */
export function pyRegExp(src: string, flags = ""): RegExp {
  return new RegExp(pyPatternSource(src), flags.includes("u") ? flags : `${flags}u`);
}

/** Convert a Python replacement template to a JavaScript one. */
export function pyReplacement(r: string): string {
  let out = "";
  for (let i = 0; i < r.length; i++) {
    const c = r[i] as string;
    if (c === "$") {
      out += "$$";
      continue;
    }
    if (c === "\\" && i + 1 < r.length) {
      const n = r[i + 1] as string;
      if (/[0-9]/.test(n)) {
        let j = i + 1;
        let num = "";
        while (j < r.length && /[0-9]/.test(r[j] as string) && num.length < 2) num += r[j++];
        out += `$${num}`;
        i = j - 1;
        continue;
      }
      if (n === "g" && r[i + 2] === "<") {
        const end = r.indexOf(">", i);
        const name = r.slice(i + 3, end);
        out += /^\d+$/.test(name) ? `$${name}` : `$<${name}>`;
        i = end;
        continue;
      }
      const simple: Record<string, string> = { n: "\n", t: "\t", r: "\r", "\\": "\\" };
      if (n in simple) {
        out += simple[n];
        i++;
        continue;
      }
      out += c + n;
      i++;
      continue;
    }
    out += c;
  }
  return out;
}
