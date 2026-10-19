// Ve anh PNG/SVG tu file .bpmn bang bpmn-js (Playwright).
// Chay: node tools/render_bpmn.js <file.bpmn>   (can goi playwright: NODE_PATH tro toi node_modules co playwright)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const src = path.resolve(process.argv[2]);
  const xml = fs.readFileSync(src, 'utf8');
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 2600, height: 900 }, deviceScaleFactor: 1 });
  await pg.setContent(`<!doctype html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="https://unpkg.com/bpmn-js@17.11.1/dist/assets/bpmn-js.css">
    <style>body{margin:0;background:#fff}#c{width:2600px;height:900px}</style></head>
    <body><div id="c"></div><script src="https://unpkg.com/bpmn-js@17.11.1/dist/bpmn-viewer.development.js"></script></body></html>`);
  await pg.waitForFunction(() => window.BpmnJS);
  const svg = await pg.evaluate(async (x) => {
    const v = new BpmnJS({ container: '#c' });
    const r = await v.importXML(x);
    v.get('canvas').zoom('fit-viewport');
    const { svg } = await v.saveSVG();
    return JSON.stringify({ svg, warnings: r.warnings.length });
  }, xml);
  const o = JSON.parse(svg);
  fs.writeFileSync(src.replace(/\.bpmn$/, '.svg'), o.svg);
  await pg.waitForTimeout(500);
  await pg.locator('#c').screenshot({ path: src.replace(/\.bpmn$/, '.png') });
  console.log('warnings:', o.warnings);
  await b.close();
})();
