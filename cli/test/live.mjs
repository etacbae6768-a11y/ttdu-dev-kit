// usage: node test/live.mjs <--local|--hosted> — runs the CLI and compares output files with test/expected.json
import { execFileSync } from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import crypto from 'node:crypto'; import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)); const ROOT = path.resolve(HERE, '../..'); const BIN = path.join(HERE, '../bin/ttdu-files.mjs');
const E = JSON.parse(fs.readFileSync(path.join(ROOT, 'test/expected.json'), 'utf8')); const fx = (n) => path.join(ROOT, 'test/fixtures', n);
const mode = process.argv[2] || '--local'; const out = fs.mkdtempSync(path.join(os.tmpdir(), 'ttdu-cli-'));
const target = mode === '--local' ? ['--base-url', process.env.TTDU_LOCAL_URL, '--key', process.env.TTDU_LOCAL_KEY] : [];
const run = (args, expectFail) => { try { return { code: 0, out: execFileSync(process.execPath, [BIN, ...args, ...target], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }) }; } catch (e) { if (!expectFail) console.log(String(e.stderr || e.message).slice(0, 300)); return { code: e.status, out: String(e.stdout || ''), err: String(e.stderr || '') }; } };
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const rows = []; const ok = (n, c, i) => { rows.push(!!c); console.log((c ? 'PASS ' : 'FAIL ') + n + (i ? ' ' + i : '')); };
const only = (process.env.ONLY || 'flow,md,docx,pdf,err').split(',');
fs.writeFileSync(path.join(out, 'merge.json'), JSON.stringify({ schema: 'ttdu.flow/v1', steps: [{ tool: 'pdf.merge', scope: 'all', options: {} }] }));
if (only.includes('flow')) { run(['flow', path.join(out, 'merge.json'), ...E.fixtures.merge.map(fx), '--out', path.join(out, 'f'), '--quiet']); const p = path.join(out, 'f', 'merged.pdf'); ok('cli flow merge sha256', fs.existsSync(p) && sha(p) === E.flow_merge_sha256, fs.existsSync(p) ? sha(p) : 'missing'); }
if (only.includes('md')) { const r = run(['hwp', 'markdown', fx(E.fixtures.hwp)]); const h = crypto.createHash('sha256').update(r.out).digest('hex'); ok('cli hwp markdown (stdout) sha256', h === E.hwp_markdown_sha256, h); }
if (only.includes('docx')) { run(['hwp', 'docx', fx(E.fixtures.hwp), '--out', path.join(out, 'd'), '--quiet']); const p = path.join(out, 'd', 'loan.docx'); ok('cli hwp docx sha256', fs.existsSync(p) && sha(p) === E.hwp_docx_sha256, fs.existsSync(p) ? sha(p) : fs.readdirSync(path.join(out, 'd')).join(',')); }
if (only.includes('pdf')) { const r = run(['hwp', 'pdf', fx(E.fixtures.hwp), '--out', path.join(out, 'p'), '--quiet'], mode !== '--local'); if (mode === '--local') ok('cli hwp pdf (local runner)', r.code === 0 && fs.readdirSync(path.join(out, 'p')).some((n) => n.endsWith('.pdf'))); else ok('cli hwp pdf hosted -> exit 3 browser_only', r.code === 3 && /browser_only/.test(r.err), r.code); }
if (only.includes('err')) { const r = run(['flow', fx('a.pdf'), fx('a.pdf')], true); ok('cli bad flow file -> nonzero exit', r.code !== 0); const h = run(['--help']); ok('cli --help mentions where files go', h.code === 0 && /sent to our server/.test(h.out)); }
console.log(rows.filter(Boolean).length + '/' + rows.length); process.exit(rows.every(Boolean) ? 0 : 1);
