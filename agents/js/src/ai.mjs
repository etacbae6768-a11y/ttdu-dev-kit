// Vercel AI SDK (ai, Apache-2.0): const tools = ttduTools({ apiKey }); generateText({ model, tools, prompt })
import { tool } from 'ai';
import { makeTools } from './core.mjs';
export function ttduTools(opts = {}) { return Object.fromEntries(makeTools(opts).map((d) => [d.name, tool({ description: d.description, inputSchema: d.schema, execute: d.run })])); }
