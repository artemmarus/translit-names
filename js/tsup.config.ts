import { defineConfig } from "tsup";

export default defineConfig({
  entry: { index: "src/index.ts", core: "src/core.ts" },
  format: ["esm", "cjs"],
  dts: true,
  clean: true,
  sourcemap: false,
  target: "es2020",
  splitting: true,
  treeshake: true,
});
