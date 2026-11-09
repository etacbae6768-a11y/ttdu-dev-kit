// usage: node test/live.mjs <baseUrl> [key] — calls each tool through the framework's own API (no model) and checks sha256
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import crypto from 'node:crypto'; import { fileURLToPath } from 'node:url';
import { ttduTools } from '../src/ai.mjs'; import { ttduLangChainTools } from '../src/langchain.mjs';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..'); const E = JSON.parse(fs.readFileSync(path.join(ROOT, 'test/expected.json'), 'utf8')); const fx = (n) => path.join(ROOT, 'test/fixtures', n);
const [baseUrl, apiKey] = process.argv.slice(2); const only = (process.env.ONLY || 'ai-flow,ai-md,lc-md,lc-docx,lc-guard').split(',');
const rows = []; const ok = (n, c, i) => { rows.push(!!c); console.log((c ? 'PASS ' : 'FAIL ') + n + (i ? ' ' + i : '')); };
const out = fs.mkdtempSync(path.join(os.tmpdir(), 'ttdu-agents-'));
const flow = { schema: 'ttdu.flow/v1', steps: [{ tool: 'pdf.merge', scope: 'all', options: {} }] };
const ai = ttduTools({ baseUrl, apiKey, outDir: path.join(out, 'ai') });
if (only.includes('ai-flow')) { const r = await ai.ttdu_run_flow.execute({ flow, files: E.fixtures.merge.map(fx) }, { toolCallId: 't1', messages: [] }); ok('vercel-ai ttdu_run_flow sha256', r.files[0].sha256 === E.flow_merge_sha256 && crypto.createHash('sha256').update(fs.readFileSync(r.files[0].path)).digest('hex') === E.flow_merge_sha256, r.files[0].sha256); }
if (only.includes('ai-md')) { const r = await ai.ttdu_hwp_to_markdown.execute({ file: fx(E.fixtures.hwp) }, { toolCallId: 't2', messages: [] }); const h = crypto.createHash('sha256').update(r.markdown).digest('hex'); ok('vercel-ai ttdu_hwp_to_markdown sha256', h === E.hwp_markdown_sha256, h); }
const lc = Object.fromEntries(ttduLangChainTools({ baseUrl, apiKey, outDir: path.join(out, 'lc'), allowDir: path.join(ROOT, 'test') }).map((t) => [t.name, t]));
if (only.includes('lc-md')) { const r = JSON.parse(await lc.ttdu_hwp_to_markdown.invoke({ file: fx(E.fixtures.hwp) })); const h = crypto.createHash('sha256').update(r.markdown).digest('hex'); ok('langchain ttdu_hwp_to_markdown sha256', h === E.hwp_markdown_sha256, h); }
if (only.includes('lc-docx')) { const r = JSON.parse(await lc.ttdu_hwp_to_docx.invoke({ file: fx(E.fixtures.hwp) })); ok('langchain ttdu_hwp_to_docx sha256', r.files[0].sha256 === E.hwp_docx_sha256, r.files[0].sha256); }
if (only.includes('lc-guard')) { let blocked = false; try { await lc.ttdu_hwp_to_markdown.invoke({ file: path.join(os.homedir(), 'x.hwp') }); } catch (e) { blocked = /outside the allowed folder/.test(e.message); } ok('langchain allowDir blocks other paths (no request sent)', blocked); let bad = false; try { await lc.ttdu_run_flow.invoke({ flow: { schema: 'x', steps: [] }, files: [] }); } catch (e) { bad = true; } ok('langchain schema rejects bad input', bad); }
console.log(rows.filter(Boolean).length + '/' + rows.length); process.exit(rows.every(Boolean) ? 0 : 1);
