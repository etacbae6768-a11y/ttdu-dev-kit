// Contract test: the OpenAPI spec is valid, and live answers match its schemas.
// usage: node scripts/contract.mjs [baseUrl] [--key KEY]   (anonymous by default; each call counts as one file call)
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
import SwaggerParser from '@apidevtools/swagger-parser';
import Ajv from 'ajv';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SPEC = path.join(HERE, '..', 'openapi', 'ttdu-files.openapi.json');
const FX = path.join(HERE, '..', 'test', 'fixtures');
const args = process.argv.slice(2); const BASE = (args.find((a) => /^https?:/.test(a)) || 'https://toolsthatdontupload.com').replace(/\/$/, '');
const KEY = args.includes('--key') ? args[args.indexOf('--key') + 1] : process.env.TTDU_API_KEY || '';
const api = await SwaggerParser.validate(JSON.parse(fs.readFileSync(SPEC, 'utf8')));
console.log('spec valid:', api.info.title, Object.keys(api.paths).length, 'paths');
// OpenAPI 3.0 "nullable" -> JSON Schema
const toJs = (s) => { if (Array.isArray(s)) return s.map(toJs); if (!s || typeof s !== 'object') return s; const o = {}; for (const [k, v] of Object.entries(s)) { if (k === 'nullable' || k === 'example' || k === 'format') continue; o[k] = toJs(v); } if (s.nullable && o.type) o.type = [o.type, 'null']; return o; };
const ajv = new Ajv({ strict: false, allErrors: true });
const schema = (name) => ajv.compile(toJs(api.components.schemas[name]));
const H = KEY ? { 'X-API-Key': KEY } : {};
const rows = []; const check = (name, ok, info) => { rows.push({ name, ok: !!ok, info }); console.log((ok ? 'PASS ' : 'FAIL ') + name + (info ? ' ' + info : '')); };
const pdfA = fs.readFileSync(path.join(FX, 'a.pdf')), pdfB = fs.readFileSync(path.join(FX, 'b.pdf')), hwp = fs.readFileSync(path.join(FX, 'loan.hwpx'));
async function call(p, body) { const r = await fetch(BASE + p, { method: 'POST', headers: H, body }); const ct = r.headers.get('content-type') || ''; const j = await r.json().catch(() => null); return { s: r.status, ct, j }; }
let fd = new FormData(); fd.append('flow', JSON.stringify({ schema: 'ttdu.flow/v1', steps: [{ tool: 'pdf.merge', scope: 'all', options: {} }] })); fd.append('files', new Blob([pdfA]), 'a.pdf'); fd.append('files', new Blob([pdfB]), 'b.pdf');
let r = await call('/v1/flows/run', fd); let v = schema('FlowRunResult'); check('flows/run 200 matches FlowRunResult', r.s === 200 && v(r.j), r.s + ' ' + JSON.stringify(v.errors || '').slice(0, 200) + ' sha=' + (r.j && r.j.outputs && r.j.outputs[0].sha256));
const flowSha = r.j && r.j.outputs && r.j.outputs[0].sha256;
fd = new FormData(); fd.append('file', new Blob([hwp]), 'loan.hwpx'); r = await call('/v1/hwp/text', fd); v = schema('HwpTextResult'); check('hwp/text 200 matches HwpTextResult', r.s === 200 && v(r.j), r.s + ' ' + JSON.stringify(v.errors || '').slice(0, 200));
r = await call('/v1/hwp/markdown', JSON.stringify({ name: 'loan.hwpx', base64: hwp.toString('base64') }).length && (() => { const f = new FormData(); f.append('file', new Blob([hwp]), 'loan.hwpx'); return f; })()); v = schema('HwpMarkdownResult'); check('hwp/markdown 200 matches HwpMarkdownResult', r.s === 200 && v(r.j), r.s);
const mdSha = r.j && r.j.markdown ? (await import('node:crypto')).createHash('sha256').update(r.j.markdown).digest('hex') : null;
fd = new FormData(); fd.append('file', new Blob([hwp]), 'loan.hwpx'); r = await call('/v1/hwp/pdf', fd);
if (BASE.includes('127.0.0.1')) { v = schema('FlowRunResult'); check('hwp/pdf on a local runner gives a PDF', r.s === 200 && v(r.j) && Buffer.from(r.j.outputs[0].base64, 'base64').subarray(0, 5).toString() === '%PDF-', String(r.s)); }
else { v = schema('Problem'); check('hwp/pdf 501 browser_only matches Problem', r.s === 501 && r.j.code === 'browser_only' && v(r.j), r.s + ' ' + r.ct); }
fd = new FormData(); fd.append('file', new Blob([hwp]), 'loan.hwpx'); r = await call('/v1/hwp/docx', fd); v = schema('HwpDocxResult'); check('hwp/docx 200 matches HwpDocxResult', r.s === 200 && v(r.j), String(r.s));
const docxSha = r.j && r.j.outputs ? r.j.outputs[0].sha256 : null;
const out = { at: new Date().toISOString(), base: BASE, keyed: !!KEY, pass: rows.filter((x) => x.ok).length, total: rows.length, rows, reference: { flow_merge_sha256: flowSha, hwp_markdown_sha256: mdSha, hwp_docx_sha256: docxSha } };
fs.mkdirSync(path.join(HERE, '..', 'test', 'results'), { recursive: true });
fs.writeFileSync(path.join(HERE, '..', 'test', 'results', 'contract-' + (BASE.includes('127.0.0.1') ? 'local' : 'hub') + '.json'), JSON.stringify(out, null, 1));
console.log(out.pass + '/' + out.total); process.exit(out.pass === out.total ? 0 : 1);
