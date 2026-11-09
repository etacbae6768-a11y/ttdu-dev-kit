// Tools That Don't Upload — TypeScript SDK for the file flows and HWP API.
// The low-level functions in ./gen are generated from openapi/ttdu-files.openapi.json by @hey-api/openapi-ts (MIT).
// IMPORTANT: with the hosted API (default base URL) your files are sent to our server, processed in memory for
// that one request and not stored. With an on-premises runner (business customers) files stay on that computer.
import { createClient, createConfig, type Client } from './gen/client/index.js';
import { runFlow, hwpToText, hwpToMarkdown, hwpToDocx, hwpToPdf } from './gen/sdk.gen.js';
import type { Flow, FlowRunResult, HwpTextResult, HwpMarkdownResult, HwpDocxResult, OutputFile, Problem } from './gen/types.gen.js';

export type { Flow, FlowRunResult, HwpTextResult, HwpMarkdownResult, HwpDocxResult, OutputFile, Problem };
export const HOSTED_URL = 'https://toolsthatdontupload.com';
export const LOCAL_URL = 'http://127.0.0.1:8790';

/** A file to send: raw bytes plus a name (the extension matters, e.g. ".pdf", ".hwpx"). */
export interface InputFile { name: string; data: Uint8Array | ArrayBuffer | Blob; mime?: string }
/** An output file with its bytes decoded and the server's sha256 checked. */
export interface Output extends OutputFile { bytes: Uint8Array }

export class TTDUError extends Error {
  status: number; code?: string; problem: Problem | unknown;
  constructor(status: number, problem: Problem | unknown) {
    const p = (problem || {}) as Problem;
    super(`${status} ${p.title || 'Error'}${p.code ? ' (' + p.code + ')' : ''}: ${p.detail || ''}`.trim());
    this.name = 'TTDUError'; this.status = status; this.code = p.code; this.problem = problem;
  }
}

export interface TTDUOptions {
  /** Default: the hosted API. Use LOCAL_URL (or your runner's address) for an on-premises runner. */
  baseUrl?: string;
  /** Optional on the hosted API (free key: https://toolsthatdontupload.com/api-keys/); required on a runner. */
  apiKey?: string;
  fetch?: typeof fetch;
}

const toB64 = async (d: InputFile['data']): Promise<string> => {
  const u8 = d instanceof Uint8Array ? d : d instanceof ArrayBuffer ? new Uint8Array(d) : new Uint8Array(await (d as Blob).arrayBuffer());
  let s = ''; for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, Array.from(u8.subarray(i, i + 0x8000)));
  return btoa(s);
};
const fromB64 = (b: string): Uint8Array => { const s = atob(b); const u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return u; };
const sha256 = async (u: Uint8Array): Promise<string> => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', u as BufferSource)), (x) => x.toString(16).padStart(2, '0')).join('');
async function decode(outputs: OutputFile[] = []): Promise<Output[]> {
  const out: Output[] = [];
  for (const o of outputs) { const bytes = fromB64(o.base64); const h = await sha256(bytes); if (h !== o.sha256) throw new TTDUError(0, { title: 'Checksum mismatch', status: 0, detail: `${o.name}: sha256 ${h} != ${o.sha256}` }); out.push({ ...o, bytes }); }
  return out;
}

export class TTDU {
  readonly baseUrl: string; private client: Client;
  constructor(opts: TTDUOptions = {}) {
    this.baseUrl = (opts.baseUrl || HOSTED_URL).replace(/\/$/, '');
    this.client = createClient(createConfig({ baseUrl: this.baseUrl, fetch: opts.fetch, auth: opts.apiKey || undefined }));
  }
  /** An on-premises runner (business customers): files stay on that computer. */
  static local(apiKey: string, baseUrl = LOCAL_URL): TTDU { return new TTDU({ baseUrl, apiKey }); }
  private async call<T>(p: Promise<{ data?: T; error?: unknown; response: Response }>): Promise<T> {
    const r = await p; if (r.error !== undefined || !r.response.ok) throw new TTDUError(r.response.status, r.error); return r.data as T;
  }
  /** Run a saved flow (ttdu.flow/v1). Files run in the order given. */
  async runFlow(flow: Flow, files: InputFile[], vars?: Record<string, string>): Promise<FlowRunResult & { files: Output[] }> {
    const body = { flow, files: await Promise.all(files.map(async (f) => ({ name: f.name, mime: f.mime, base64: await toB64(f.data) }))), ...(vars ? { vars } : {}) };
    const r = await this.call<FlowRunResult>(runFlow({ client: this.client, body }) as never);
    return { ...r, files: await decode(r.outputs) };
  }
  /** Run one tool: a flow with a single step. */
  runTool(tool: string, files: InputFile[], options: Record<string, unknown> = {}, scope: 'all' | 'each' = 'all') {
    return this.runFlow({ schema: 'ttdu.flow/v1', steps: [{ tool, scope, options }] }, files);
  }
  private async hwpBody(file: InputFile) { return { name: file.name, base64: await toB64(file.data) }; }
  async hwpToText(file: InputFile): Promise<HwpTextResult> { return this.call<HwpTextResult>(hwpToText({ client: this.client, body: await this.hwpBody(file) }) as never); }
  async hwpToMarkdown(file: InputFile): Promise<HwpMarkdownResult> { return this.call<HwpMarkdownResult>(hwpToMarkdown({ client: this.client, body: await this.hwpBody(file) }) as never); }
  async hwpToDocx(file: InputFile): Promise<HwpDocxResult & { files: Output[] }> { const r = await this.call<HwpDocxResult>(hwpToDocx({ client: this.client, body: await this.hwpBody(file) }) as never); return { ...r, files: await decode(r.outputs) }; }
  /** Only on an on-premises runner; the hosted API answers 501 browser_only (use https://dagotools.com/en/tools/hwp-to-pdf/). */
  async hwpToPdf(file: InputFile): Promise<{ files: Output[] }> { const r = await this.call<{ outputs: OutputFile[] }>(hwpToPdf({ client: this.client, body: await this.hwpBody(file) }) as never); return { files: await decode(r.outputs) }; }
}
export default TTDU;

