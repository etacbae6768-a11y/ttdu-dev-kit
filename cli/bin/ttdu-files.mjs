#!/usr/bin/env node
// ttdu-files: run saved file flows and convert HWP/HWPX from the command line.
// Hosted API by default (files are SENT to toolsthatdontupload.com, processed in memory, not stored);
// --local talks to an on-premises runner on this computer (files stay here).
import fs from 'node:fs'; import path from 'node:path';
import { TTDU, TTDUError, HOSTED_URL, LOCAL_URL } from 'toolsthatdontupload';

const HELP = `ttdu-files — file flows and HWP conversion (Tools That Don't Upload)

Usage:
  ttdu-files flow <flow.json> <file...> [--var key=value ...] [--out <dir>]
  ttdu-files tool <tool.id> <file...> [--options '<json>'] [--scope all|each] [--out <dir>]
  ttdu-files hwp <text|markdown|docx|pdf> <file.hwp|.hwpx> [--out <dir>]

Where the files go:
  (default)        hosted API ${HOSTED_URL}: files are sent to our server, processed in
                   memory for that request and not stored. Key optional: --key or TTDU_API_KEY.
  --local          on-premises runner ${LOCAL_URL} (business customers): files stay on this
                   computer. Key: --key, TTDU_LOCAL_KEY or ./local-api-key.txt
  --base-url <url> any other address

Other options: --json (print the answer as JSON), --quiet, -h/--help, -v/--version
Results are written to --out (default: current folder); each file's sha256 is checked.`;

const argv = process.argv.slice(2);
const flags = { var: [] }; const pos = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '-h' || a === '--help') flags.help = true;
  else if (a === '-v' || a === '--version') flags.version = true;
  else if (a === '--local' || a === '--json' || a === '--quiet') flags[a.slice(2)] = true;
  else if (a === '--var') flags.var.push(argv[++i]);
  else if (/^--(out|key|base-url|options|scope)$/.test(a)) flags[a.slice(2)] = argv[++i];
  else if (a.startsWith('--')) die(`unknown option ${a}`, 2);
  else pos.push(a);
}
function die(msg, code = 1) { process.stderr.write(`ttdu-files: ${msg}\n`); process.exit(code); }
if (flags.version) { const p = JSON.parse(fs.readFileSync(new URL('../package.json', import.meta.url), 'utf8')); console.log(p.version); process.exit(0); }
if (flags.help || !pos.length) { console.log(HELP); process.exit(flags.help ? 0 : 2); }

const readFile = (p) => { if (!fs.existsSync(p)) die(`file not found: ${p}`); return { name: path.basename(p), data: new Uint8Array(fs.readFileSync(p)) }; };
let baseUrl = flags['base-url'] || (flags.local ? LOCAL_URL : HOSTED_URL);
let key = flags.key || (flags.local ? process.env.TTDU_LOCAL_KEY : process.env.TTDU_API_KEY);
if (flags.local && !key && fs.existsSync('local-api-key.txt')) key = fs.readFileSync('local-api-key.txt', 'utf8').trim();
const hosted = baseUrl.replace(/\/$/, '') === HOSTED_URL;
const say = (s) => { if (!flags.quiet && !flags.json) process.stderr.write(s + '\n'); };
if (hosted) say(`note: sending files to ${HOSTED_URL} (processed in memory, not stored). Use --local for an on-premises runner.`);
const t = new TTDU({ baseUrl, apiKey: key });
const outDir = flags.out || '.';
const save = (files) => { fs.mkdirSync(outDir, { recursive: true }); return files.map((f) => { const p = path.join(outDir, f.name); fs.writeFileSync(p, f.bytes); say(`wrote ${p} (${f.size} bytes, sha256 ${f.sha256})`); return { name: f.name, path: p, size: f.size, sha256: f.sha256 }; }); };
const strip = (r) => { const o = { ...r }; delete o.files; if (o.outputs) o.outputs = o.outputs.map(({ base64, ...x }) => x); return o; };

try {
  const [cmd, ...rest] = pos;
  if (cmd === 'flow') {
    if (rest.length < 2) die('flow needs <flow.json> and at least one file', 2);
    let flow; try { flow = JSON.parse(fs.readFileSync(rest[0], 'utf8')); } catch (e) { die(`cannot read flow ${rest[0]}: ${e.message}`); }
    const vars = {}; for (const v of flags.var) { const i = String(v).indexOf('='); if (i < 1) die(`--var needs key=value, got ${v}`, 2); vars[v.slice(0, i)] = v.slice(i + 1); }
    const r = await t.runFlow(flow, rest.slice(1).map(readFile), Object.keys(vars).length ? vars : undefined);
    const written = save(r.files);
    if (flags.json) console.log(JSON.stringify({ ...strip(r), written }, null, 1));
  } else if (cmd === 'tool') {
    if (rest.length < 2) die('tool needs <tool.id> and at least one file', 2);
    let options = {}; if (flags.options) { try { options = JSON.parse(flags.options); } catch (e) { die('--options is not valid JSON', 2); } }
    const r = await t.runTool(rest[0], rest.slice(1).map(readFile), options, flags.scope === 'each' ? 'each' : 'all');
    const written = save(r.files);
    if (flags.json) console.log(JSON.stringify({ ...strip(r), written }, null, 1));
  } else if (cmd === 'hwp') {
    const [op, file] = rest; if (!op || !file) die('hwp needs <text|markdown|docx|pdf> <file>', 2);
    const f = readFile(file); const stem = f.name.replace(/\.[^.]+$/, '');
    if (op === 'text') { const r = await t.hwpToText(f); if (flags.json) console.log(JSON.stringify(r, null, 1)); else if (flags.out) save([{ name: stem + '.txt', bytes: new TextEncoder().encode(r.text), size: new TextEncoder().encode(r.text).length, sha256: '' }]); else process.stdout.write(r.text + '\n'); }
    else if (op === 'markdown') { const r = await t.hwpToMarkdown(f); if (flags.json) console.log(JSON.stringify(r, null, 1)); else if (flags.out) { const b = new TextEncoder().encode(r.markdown); save([{ name: stem + '.md', bytes: b, size: b.length, sha256: '' }]); } else process.stdout.write(r.markdown); }
    else if (op === 'docx') { const r = await t.hwpToDocx(f); const written = save(r.files); if (flags.json) console.log(JSON.stringify({ ...strip(r), written }, null, 1)); }
    else if (op === 'pdf') { const r = await t.hwpToPdf(f); const written = save(r.files); if (flags.json) console.log(JSON.stringify({ written }, null, 1)); }
    else die(`unknown hwp operation ${op}`, 2);
  } else die(`unknown command ${cmd} (try --help)`, 2);
} catch (e) {
  if (e instanceof TTDUError) {
    if (flags.json) console.log(JSON.stringify({ ok: false, status: e.status, problem: e.problem }, null, 1));
    die(e.message + (e.code === 'browser_only' ? ' — on the hosted API, HWP to PDF runs in the browser: https://dagotools.com/en/tools/hwp-to-pdf/' : ''), e.status === 429 || e.status === 402 ? 4 : 3);
  }
  die(String(e && e.message || e));
}
