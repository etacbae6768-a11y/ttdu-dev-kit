# toolsthatdontupload (TypeScript / JavaScript SDK)

Run saved file flows and convert Korean HWP/HWPX documents with the Tools That Don't Upload API. Node 18+, Deno, Bun and browsers (any runtime with `fetch`).

```sh
npm install toolsthatdontupload
```

```js
import fs from 'node:fs';
import { TTDU } from 'toolsthatdontupload';

const t = new TTDU({ apiKey: process.env.TTDU_API_KEY }); // key optional
const r = await t.runFlow(
  { schema: 'ttdu.flow/v1', steps: [{ tool: 'pdf.merge', scope: 'all', options: {} }] },
  [{ name: 'a.pdf', data: fs.readFileSync('a.pdf') }, { name: 'b.pdf', data: fs.readFileSync('b.pdf') }],
);
fs.writeFileSync(r.files[0].name, r.files[0].bytes); // sha256 already checked

const md = await t.hwpToMarkdown({ name: 'notice.hwp', data: fs.readFileSync('notice.hwp') });
console.log(md.markdown);
```

Methods: `runFlow(flow, files, vars?)`, `runTool(toolId, files, options?, scope?)`, `hwpToText`, `hwpToMarkdown`, `hwpToDocx`, `hwpToPdf` (on-premises runner only). Errors throw `TTDUError` with `status`, `code` and the problem details. `TTDU.local(key)` talks to an on-premises runner.

The low-level functions in `src/gen` are generated from [`openapi/ttdu-files.openapi.json`](../../openapi/ttdu-files.openapi.json) with [@hey-api/openapi-ts](https://github.com/hey-api/openapi-ts) (MIT). Docs: https://toolsthatdontupload.com/docs/sdk/
## Where your files go

- **Hosted API (default, `https://toolsthatdontupload.com`)**: your files are **sent to our server** (a Cloudflare Worker) and processed in memory for that one request. We do not store the files, the results or the flow. The usual minimal request record applies: https://toolsthatdontupload.com/privacy/
- **On-premises runner** (`http://127.0.0.1:8790`, for business customers): files stay on that computer. Contact: https://toolsthatdontupload.com/business/
- Limits on the hosted API: one request = one file call (20 free a day with a free key, then 60 credits; 20 a day per IP address without a key), up to 20 files and 15 MB per request. HWP to PDF is not available on the hosted API (it answers `501 browser_only`; use https://dagotools.com/en/tools/hwp-to-pdf/ in the browser).
## License
MIT
