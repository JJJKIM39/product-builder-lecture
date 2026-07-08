// GitHub Pages 등 정적 호스팅은 확장자로 Content-Type을 판단하므로,
// next/og가 생성하는 확장자 없는 opengraph-image 파일에 .png를 붙이고
// HTML 내 참조 URL도 함께 고쳐준다.
import { readdirSync, renameSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { join } from "node:path";

const OUT_DIR = new URL("../out", import.meta.url).pathname;

function walk(dir, cb) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) walk(full, cb);
    else cb(full);
  }
}

let renamed = 0;
walk(OUT_DIR, (file) => {
  if (file.endsWith("/opengraph-image")) {
    renameSync(file, `${file}.png`);
    renamed++;
  }
});

let patched = 0;
walk(OUT_DIR, (file) => {
  if (!file.endsWith(".html")) return;
  const content = readFileSync(file, "utf8");
  const next = content.replaceAll("opengraph-image?", "opengraph-image.png?");
  if (next !== content) {
    writeFileSync(file, next);
    patched++;
  }
});

console.log(`renamed ${renamed} OG image files, patched ${patched} HTML files`);
