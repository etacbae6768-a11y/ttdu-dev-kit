# ttdu-agent-tools (Vercel AI SDK, LangChain.js)

Three tools for agents: `ttdu_run_flow`, `ttdu_hwp_to_markdown`, `ttdu_hwp_to_docx`. The agent passes **file paths** on the machine running it; results are saved to `outDir` and returned as paths with sha256. Use `allowDir` to limit which folder the tools may read.

```js
import { ttduTools } from 'ttdu-agent-tools/ai';             // Vercel AI SDK (ai, Apache-2.0)
const { text } = await generateText({ model, tools: ttduTools({ outDir: './out', allowDir: './inbox' }), prompt: 'Convert ./inbox/notice.hwp to Markdown' });

import { ttduLangChainTools } from 'ttdu-agent-tools/langchain'; // LangChain.js (@langchain/core, MIT)
const model = chatModel.bindTools(ttduLangChainTools({ outDir: './out', allowDir: './inbox' }));
```
## Where your files go

- **Hosted API (default, `https://toolsthatdontupload.com`)**: your files are **sent to our server** (a Cloudflare Worker) and processed in memory for that one request. We do not store the files, the results or the flow. The usual minimal request record applies: https://toolsthatdontupload.com/privacy/
- **On-premises runner** (`http://127.0.0.1:8790`, for business customers): files stay on that computer. Contact: https://toolsthatdontupload.com/business/
- Limits on the hosted API: one request = one file call (20 free a day with a free key, then 60 credits; 20 a day per IP address without a key), up to 20 files and 15 MB per request. HWP to PDF is not available on the hosted API (it answers `501 browser_only`; use https://dagotools.com/en/tools/hwp-to-pdf/ in the browser).
## License
MIT
