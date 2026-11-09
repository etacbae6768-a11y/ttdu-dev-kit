// LangChain.js (@langchain/core, MIT): const tools = ttduLangChainTools({ apiKey }); model.bindTools(tools)
import { tool } from '@langchain/core/tools';
import { makeTools } from './core.mjs';
export function ttduLangChainTools(opts = {}) { return makeTools(opts).map((d) => tool(async (args) => JSON.stringify(await d.run(args)), { name: d.name, description: d.description, schema: d.schema })); }
