// news-image-20261117 entry (Node 22, standard library only).
// The image is drawn in code by draw.py (Pillow) and shipped as
// entry.png beside this file; this program copies it to the output
// directory. Outside the grader's container, MAKEFUN_OUTPUT_DIR
// stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) {
  throw new Error('entry.png missing next to main.ts');
}
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(source, dest);
// Deterministic by construction: a plain byte copy, so two runs
// always write identical bytes. Verify the copy landed whole.
if (statSync(dest).size !== statSync(source).size) {
  throw new Error('entry.png copy is incomplete');
}
