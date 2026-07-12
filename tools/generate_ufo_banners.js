#!/usr/bin/env node
/**
 * Generiert 3 UFO-Banner (1536x1024) mit DEMSELBEN UFO (fester Seed + feste
 * Referenz ufo_2.png, img2img denoise 0.6) und nur variierendem Hintergrund.
 * Basiert auf comfyui_ufo.json. Output nach ~/Downloads/ufo-banners/.
 */
const fs = require('fs');
const path = require('path');
const http = require('http');
const { randomUUID } = require('crypto');

const WORKFLOW = path.join(process.env.HOME, 'projekte', 'Nostr', 'publisher', 'comfyui_ufo.json');
const OUTPUT_DIR = path.join(process.env.HOME, 'ComfyUI', 'output');
const DEST_DIR = path.join(process.env.HOME, 'Downloads', 'ufo-banners');
const SEED = 777333;               // fest -> gleiches UFO in allen drei

const DENOISE = 0.72;              // etwas hoeher -> mehr Hintergrund-Variation
const NEG_EXTRA = ', multiple moons, two moons, extra moons, second moon, small moons, planets';
const VARIANTS = [
  { name: 'blog',   bg: 'dramatic vivid sunset sky, deep orange red and purple gradient at the horizon, dark starry blue at the top, single full moon top right' },
  { name: 'aktien', bg: 'clear deep midnight blue night sky, dense pristine starfield, cool moonlight, clean minimal, single full moon top right' },
  { name: 'bitcoin',bg: 'teal and cyan twilight over a calm reflective ocean, warm golden glow along the horizon line, single full moon top right' },
];

function httpRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch { resolve(data); } });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function run(variant) {
  const prompt = JSON.parse(fs.readFileSync(WORKFLOW, 'utf8'));
  prompt['6'].inputs.text = prompt['6'].inputs.text + ',\n' + variant.bg;
  prompt['7'].inputs.text = prompt['7'].inputs.text + NEG_EXTRA;
  prompt['3'].inputs.seed = SEED;                 // fester Seed -> gleiches UFO
  prompt['3'].inputs.denoise = DENOISE;
  prompt['9'].inputs.filename_prefix = 'UFOBanner_' + variant.name;

  const clientId = randomUUID();
  const body = JSON.stringify({ prompt, client_id: clientId });
  const submit = await httpRequest({
    hostname: 'localhost', port: 8188, path: '/prompt', method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
  }, body);
  const id = submit.prompt_id;
  if (!id) { console.error('Fehler:', JSON.stringify(submit)); return null; }
  process.stdout.write(`[${variant.name}] Job ${id} `);

  for (let i = 0; i < 90; i++) {
    await sleep(2000);
    const hist = await httpRequest({ hostname: 'localhost', port: 8188, path: `/history/${id}`, method: 'GET' });
    if (hist[id]) {
      const outputs = hist[id].outputs || {};
      for (const o of Object.values(outputs)) {
        if (o.images && o.images.length) {
          const img = o.images[0];
          const src = path.join(OUTPUT_DIR, img.filename);
          const dest = path.join(DEST_DIR, `${variant.name}-banner-neu.png`);
          fs.copyFileSync(src, dest);
          console.log(`-> ${dest}`);
          return dest;
        }
      }
    }
    process.stdout.write('.');
  }
  console.log(' TIMEOUT');
  return null;
}

(async () => {
  fs.mkdirSync(DEST_DIR, { recursive: true });
  for (const v of VARIANTS) await run(v);
  console.log('Fertig.');
})();
