// Shared tool definitions for agent frameworks (Vercel AI SDK, LangChain.js).
// Files are given as paths on the machine running the agent; results are written to outDir and returned as paths.
// IMPORTANT: with the hosted API (default) the files are sent to toolsthatdontupload.com, processed in memory
// for that one request and not stored. Pass baseUrl of an on-premises runner to keep files on your network.
import fs from 'node:fs'; import path from 'node:path';
import { z } from 'zod';
import { TTDU } from 'toolsthatdontupload';

export function makeTools({ apiKey, baseUrl, outDir = '.', allowDir } = {}) {
  const t = new TTDU({ apiKey: apiKey || process.env.TTDU_API_KEY, baseUrl });
  const root = allowDir ? path.resolve(allowDir) : null;
  const read = (p) => {
    const full = path.resolve(p);
    if (root && !(full === root || full.startsWith(root + path.sep))) throw new Error(`path outside the allowed folder: ${p}`);
    return { name: path.basename(full), data: new Uint8Array(fs.readFileSync(full)) };
  };
  const save = (files) => { fs.mkdirSync(outDir, { recursive: true }); return files.map((f) => { const p = path.resolve(outDir, f.name); fs.writeFileSync(p, f.bytes); return { path: p, name: f.name, mime: f.mime, size: f.size, sha256: f.sha256 }; }); };
  const where = 'Files are sent to Tools That Don\'t Upload (processed in memory for this request, not stored) unless a local runner is configured.';
  return [
    {
      name: 'ttdu_run_flow',
      description: `Run a saved file flow (ttdu.flow/v1 JSON with steps such as pdf.merge, pdf.compress, pdf.split) on local files and save the results. ${where}`,
      schema: z.object({
        flow: z.object({ schema: z.literal('ttdu.flow/v1'), steps: z.array(z.object({ tool: z.string(), scope: z.enum(['all', 'each']).optional(), options: z.record(z.string(), z.any()).optional(), outName: z.string().optional() }).passthrough()).min(1) }).passthrough().describe('The flow JSON'),
        files: z.array(z.string()).min(1).describe('Paths of the input files, in order'),
        vars: z.record(z.string(), z.string()).optional().describe('Values for the flow\'s vars, e.g. {"client":"ACME"}'),
      }),
      run: async ({ flow, files, vars }) => { const r = await t.runFlow(flow, files.map(read), vars); return { ok: true, steps: r.steps, notes: r.notes, files: save(r.files) }; },
    },
    {
      name: 'ttdu_hwp_to_markdown',
      description: `Convert a Korean HWP or HWPX document (local path) to Markdown, with tables as Markdown tables. ${where}`,
      schema: z.object({ file: z.string().describe('Path of the .hwp or .hwpx file') }),
      run: async ({ file }) => { const r = await t.hwpToMarkdown(read(file)); return { ok: true, format: r.format, stats: r.stats, markdown: r.markdown }; },
    },
    {
      name: 'ttdu_hwp_to_docx',
      description: `Convert a Korean HWP or HWPX document (local path) to an editable DOCX (paragraphs and tables) and save it. ${where}`,
      schema: z.object({ file: z.string().describe('Path of the .hwp or .hwpx file') }),
      run: async ({ file }) => { const r = await t.hwpToDocx(read(file)); return { ok: true, format: r.format, files: save(r.files) }; },
    },
  ];
}
