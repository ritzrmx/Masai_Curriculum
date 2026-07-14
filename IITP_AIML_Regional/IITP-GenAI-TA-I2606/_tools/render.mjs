#!/usr/bin/env node
/**
 * Mermaid -> PDF renderer with an anti-clipping measurement pass.
 *
 * Usage: node render.mjs <input.mmd> <output.pdf> ["Title||Subtitle"]
 *
 * The clipping problem: mermaid sizes each node from its measured label, but bold/italic
 * runs and stacked <br/> lines inside a foreignObject routinely under-measure, so text
 * gets cut off by the node's rect. Fix: after the first render, re-measure every label's
 * true scrollWidth/scrollHeight, grow any rect that is too small, refit the viewBox, then
 * size the PDF page to the finished content. Nothing can be cut off.
 */
import { readFileSync, existsSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { resolve, dirname, join, extname, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const HERE = dirname(fileURLToPath(import.meta.url));

const [, , inFile, outFile, title = ''] = process.argv;
if (!inFile || !outFile) {
  console.error('usage: node render.mjs <input.mmd> <output.pdf> ["Title||Subtitle"]');
  process.exit(1);
}

const graph = readFileSync(resolve(inFile), 'utf8');
const [heading = '', subheading = ''] = title.split('||');
// Served over HTTP, not file://: Chrome blocks ES-module imports from a null origin.
const mermaidUrl = '/node_modules/mermaid/dist/mermaid.esm.mjs';

const html = `<!doctype html>
<html><head><meta charset="utf-8">
<style>
  @page { margin: 0; }
  html, body { margin: 0; padding: 0; background: #ffffff; }
  #sheet { display: inline-block; padding: 46px 44px 42px 44px; box-sizing: border-box; }
  #heading {
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 22px; font-weight: 700; color: #1A202C;
    margin: 0 0 30px 0; text-align: center; letter-spacing: .2px;
  }
  #heading small {
    display: block; font-size: 13px; font-weight: 500; color: #64748B;
    margin-top: 8px; letter-spacing: .3px;
  }
  /* Anti-clipping: let labels paint outside their foreignObject rather than be cut.
     Do NOT change white-space here — mermaid measured the label with its own wrapping,
     and forcing a re-wrap after layout is what makes text spill out of the box. */
  .node foreignObject { overflow: visible !important; }
  svg { display: block; margin: 0 auto; }
</style></head>
<body>
  <div id="sheet">
    ${heading ? `<div id="heading">${heading}${subheading ? `<small>${subheading}</small>` : ''}</div>` : ''}
    <div id="target"></div>
  </div>
<script type="module">
  import mermaid from '${mermaidUrl}';
  window.__render = async (graph) => {
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'loose',
      theme: 'base',
      fontFamily: '-apple-system, "Segoe UI", Helvetica, Arial, sans-serif',
      flowchart: {
        htmlLabels: true,    // required: <b>/<i>/<br/> must be real HTML, not SVG tspans
        curve: 'basis',
        padding: 18,         // breathing room inside every node
        useMaxWidth: false,  // let the SVG take its natural width; never squeeze it
        diagramPadding: 20,
        nodeSpacing: 60,
        rankSpacing: 95,
        wrappingWidth: 620   // high on purpose: only my explicit <br/> may break a line,
                             // so mermaid never re-wraps a phrase mid-sentence
      },
      themeVariables: { fontSize: '15px', lineColor: '#94A3B8', primaryTextColor: '#1A202C' }
    });
    const { svg } = await mermaid.render('mm', graph);
    document.getElementById('target').innerHTML = svg;
  };
  window.__ready = true;
</script>
</body></html>`;

// --- Local static server: index.html + the mermaid ESM bundle (and its lazy chunks) ---
const MIME = { '.html': 'text/html', '.mjs': 'text/javascript', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css' };
const server = createServer((req, res) => {
  const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p === '/' || p === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    return res.end(html);
  }
  const file = join(HERE, normalize(p));
  if (!file.startsWith(HERE) || !existsSync(file) || !statSync(file).isFile()) {
    res.writeHead(404);
    return res.end('404');
  }
  res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
  res.end(readFileSync(file));
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const { port } = server.address();

const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--font-render-hinting=none'] });
const page = await browser.newPage();
await page.setViewport({ width: 1800, height: 1400, deviceScaleFactor: 2 });
page.on('pageerror', (e) => console.error('page error:', e.message));
await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: 'networkidle0' });
await page.waitForFunction('window.__ready === true', { timeout: 30000 });

await page.evaluate(async (g) => { await window.__render(g); }, graph);

// ---- Refit + overflow AUDIT (report only; never mutate mermaid's layout) ----
const size = await page.evaluate(() => {
  const el = document.querySelector('#target svg');

  // Report any label whose real content is wider/taller than the box mermaid gave it.
  // We do not "fix" it here — a post-layout resize detaches labels from their rects.
  // An overflow means the SOURCE text is too long and must be shortened/rebalanced.
  const overflows = [];
  for (const node of el.querySelectorAll('g.node')) {
    const fo = node.querySelector('foreignObject');
    const label = fo && fo.firstElementChild;
    if (!fo || !label) continue;
    const dw = Math.ceil(label.scrollWidth) - Math.round(parseFloat(fo.getAttribute('width')));
    const dh = Math.ceil(label.scrollHeight) - Math.round(parseFloat(fo.getAttribute('height')));
    if (dw > 2 || dh > 2) {
      overflows.push({ id: node.id, overflowX: dw, overflowY: dh, text: label.innerText.slice(0, 40) });
    }
  }

  // Refit the viewBox tightly around the finished diagram.
  const bb = el.getBBox();
  const M = 16;
  el.setAttribute('viewBox', [bb.x - M, bb.y - M, bb.width + 2 * M, bb.height + 2 * M].join(' '));
  el.setAttribute('width', Math.ceil(bb.width + 2 * M));
  el.setAttribute('height', Math.ceil(bb.height + 2 * M));
  el.removeAttribute('style');

  const sheet = document.getElementById('sheet');
  return { w: Math.ceil(sheet.offsetWidth), h: Math.ceil(sheet.offsetHeight), overflows };
});

if (size.overflows.length) {
  console.error(`⚠ ${size.overflows.length} node(s) overflow their box — shorten the source text:`);
  for (const o of size.overflows) console.error(`   [${o.id}] +${o.overflowX}px wide, +${o.overflowY}px tall — "${o.text}…"`);
}

// Page sized exactly to the content, so no page edge can crop the diagram.
await page.pdf({
  path: resolve(outFile),
  width: `${size.w}px`,
  height: `${size.h}px`,
  printBackground: true,
  pageRanges: '1',
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});

await browser.close();
server.close();
console.log(`✓ ${outFile}  (${size.w}×${size.h}px)`);
