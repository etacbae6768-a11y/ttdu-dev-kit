// Runs every package test against one target. usage:
//   node scripts/test-all.mjs local            (starts a local runner; needs the private ttdu-platform checkout)
//   node scripts/test-all.mjs hosted [apiKey]  (each package makes 3-4 file calls on the hosted API)
import { execFileSync } from 'node:child_process'; import path from 'node:path'; import fs from 'node:fs'; import { fileURLToPath } from 'node:url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [mode, key] = process.argv.slice(2);
const base = mode === 'local' ? process.env.TTDU_LOCAL_URL : 'https://toolsthatdontupload.com';
const k = mode === 'local' ? process.env.TTDU_LOCAL_KEY : (key || process.env.TTDU_API_KEY || '');
if (mode === 'local' && !base) { execFileSync(process.execPath, [path.join(ROOT, 'scripts/with-local.mjs'), process.execPath, path.join(ROOT, 'scripts/test-all.mjs'), 'local'], { stdio: 'inherit' }); process.exit(0); }
const py = process.platform === 'win32' ? 'python' : 'python3';
const jobs = [['contract', process.execPath, ['scripts/contract.mjs', base, ...(k ? ['--key', k] : [])]], ['ts-sdk', process.execPath, ['sdk/typescript/test/live.mjs', base, k]], ['py-sdk', py, ['sdk/python/tests/live.py', base, k]], ['cli', process.execPath, ['cli/test/live.mjs', mode === 'local' ? '--local' : '--hosted']], ['agents-js', process.execPath, ['agents/js/test/live.mjs', base, k]], ['agents-py', py, ['agents/python/tests/live.py', base, k]]];
const res = [];
for (const [name, cmd, args] of jobs) { let out = '', code = 0; try { out = execFileSync(cmd, args.filter((x) => x !== undefined && x !== ''), { cwd: ROOT, encoding: 'utf8', shell: process.platform === 'win32' && cmd === py, env: { ...process.env, TTDU_API_KEY: mode === 'local' ? '' : k } }); } catch (e) { code = e.status || 1; out = String(e.stdout || '') + String(e.stderr || ''); } const lines = out.split(/\r?\n/).filter((l) => /^(PASS|FAIL)/.test(l)); res.push({ name, code, pass: lines.filter((l) => l.startsWith('PASS')).length, total: lines.length, lines }); console.log(`${code ? 'FAIL' : 'ok  '} ${name} ${lines.filter((l) => l.startsWith('PASS')).length}/${lines.length}`); }
fs.mkdirSync(path.join(ROOT, 'test/results'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'test/results', `all-${mode}.json`), JSON.stringify({ at: new Date().toISOString(), mode, base, results: res }, null, 1));
process.exit(res.every((r) => !r.code) ? 0 : 1);
