// usage: node test/live.mjs <baseUrl> [apiKey]  — compares results with test/expected.json (sha256)
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto'; import { fileURLToPath } from 'node:url';
import { TTDU, TTDUError } from '../dist/index.js';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const E = JSON.parse(fs.readFileSync(path.join(ROOT, 'test/expected.json'), 'utf8'));
const fx = (n) => ({ name: n, data: new Uint8Array(fs.readFileSync(path.join(ROOT, 'test/fixtures', n))) });
const [base, key] = process.argv.slice(2); const t = new TTDU({ baseUrl: base, apiKey: key || process.env.TTDU_API_KEY });
const local = /127\.0\.0\.1|localhost/.test(base); const rows = []; const ok = (n, c, i) => { rows.push({ n, c: !!c }); console.log((c ? 'PASS ' : 'FAIL ') + n + (i ? ' ' + i : '')); };
const only = (process.env.ONLY || 'flow,md,docx,pdf').split(',');
if (only.includes('flow')) { const r = await t.runFlow({ schema: 'ttdu.flow/v1', steps: [{ tool: 'pdf.merge', scope: 'all', options: {} }] }, E.fixtures.merge.map(fx)); ok('ts runFlow merge sha256', r.files[0].sha256 === E.flow_merge_sha256, r.files[0].sha256); }
if (only.includes('md')) { const r = await t.hwpToMarkdown(fx(E.fixtures.hwp)); const h = crypto.createHash('sha256').update(r.markdown).digest('hex'); ok('ts hwpToMarkdown sha256', h === E.hwp_markdown_sha256, h); }
if (only.includes('docx')) { const r = await t.hwpToDocx(fx(E.fixtures.hwp)); ok('ts hwpToDocx sha256', r.files[0].sha256 === E.hwp_docx_sha256, r.files[0].sha256); }
if (only.includes('pdf')) { try { const r = await t.hwpToPdf(fx(E.fixtures.hwp)); ok('ts hwpToPdf (local runner) %PDF', local && Buffer.from(r.files[0].bytes.subarray(0, 5)).toString() === '%PDF-'); } catch (e) { ok('ts hwpToPdf hosted -> 501 browser_only', !local && e instanceof TTDUError && e.status === 501 && e.code === 'browser_only', e.message); } }
console.log(rows.filter((x) => x.c).length + '/' + rows.length); process.exit(rows.every((x) => x.c) ? 0 : 1);
