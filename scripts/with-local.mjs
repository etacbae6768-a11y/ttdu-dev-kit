// Starts a local `ttdu serve` (needs the private ttdu-platform checkout; not shipped) and runs a command against it.
// usage: node scripts/with-local.mjs <cmd> [args...]   -> env TTDU_LOCAL_URL, TTDU_LOCAL_KEY
import { spawn } from 'node:child_process'; import os from 'node:os'; import path from 'node:path'; import fs from 'node:fs';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..');
const PLATFORM = (process.env.TTDU_PLATFORM || path.resolve(ROOT, '..', 'ttdu-platform')).replace(/\\/g, '/');
process.env.TTDU_KEY_FILE = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'ttdu-local-')), 'local-api-key.txt');
if (!process.env.TTDU_SITE) { const S = path.resolve(ROOT, '..', 'ttdu-integration', 'staging').replace(/\\/g, '/') + '/'; const d = fs.readdirSync(S).filter((n) => /^live-\d+$/.test(n) && fs.existsSync(S + n + '/module-runners')).sort(); process.env.TTDU_SITE = S + d[d.length - 1]; }
const { startServe } = await import('file:///' + PLATFORM + '/apps/office-runner/serve.mjs');
const srv = await startServe({ port: Number(process.env.TTDU_LOCAL_PORT || 8792), quiet: true });
const [cmd, ...a] = process.argv.slice(2);
const p = spawn(cmd, a, { stdio: 'inherit', shell: process.platform === 'win32', env: { ...process.env, TTDU_LOCAL_URL: srv.url, TTDU_LOCAL_KEY: srv.key } });
p.on('close', async (code) => { await srv.close(); process.exit(code); });
