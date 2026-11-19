// Front Page 19 Nov 2026 — copies the rendered front page to the output dir.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");
mkdirSync(out, { recursive: true });
copyFileSync(join(here, "entry.png"), join(out, "entry.png"));
