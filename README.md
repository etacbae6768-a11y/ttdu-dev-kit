# Tools That Don't Upload — developer kit

Everything to call the [file flows](https://toolsthatdontupload.com/docs/flows/) and [HWP/HWPX](https://toolsthatdontupload.com/docs/hwp/) API from code.

| Folder | Package | What |
|---|---|---|
| `openapi/` | — | OpenAPI 3.0 description (also at https://toolsthatdontupload.com/openapi/files.json) |
| `sdk/typescript` | npm `toolsthatdontupload` | TypeScript/JavaScript SDK (generated with @hey-api/openapi-ts, MIT) |
| `sdk/python` | PyPI `toolsthatdontupload` | Python SDK (generated with openapi-python-client, MIT) |
| `cli` | npm `ttdu-files` | Command line |
| `agents/js` | npm `ttdu-agent-tools` | Vercel AI SDK and LangChain.js tools |
| `agents/python` | PyPI `ttdu-agent-tools` | LlamaIndex and LangChain tools |

## Where your files go
With the hosted API (the default everywhere) **your files are sent to our server** (a Cloudflare Worker), processed in memory for that one request and not stored. Businesses can run the same API on their own computers (`http://127.0.0.1:8790`), where files stay on that computer.

## Tests
`test/expected.json` holds the sha256 of three results (PDF merge, HWPX to Markdown, HWPX to DOCX). `node scripts/test-all.mjs hosted [key]` runs every package against the hosted API and compares; `node scripts/contract.mjs` checks the OpenAPI description against live answers.

MIT License.