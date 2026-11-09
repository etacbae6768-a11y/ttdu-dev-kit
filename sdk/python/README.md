# toolsthatdontupload (Python SDK)

Run saved file flows and convert Korean HWP/HWPX documents with the Tools That Don't Upload API. Python 3.11+.

```sh
pip install toolsthatdontupload
```

```python
from toolsthatdontupload import TTDU

t = TTDU()  # api_key=... optional, or TTDU_API_KEY
r = t.run_flow({"schema": "ttdu.flow/v1", "steps": [{"tool": "pdf.merge", "scope": "all", "options": {}}]}, ["a.pdf", "b.pdf"])
r["files"][0].save(".")            # sha256 already checked
print(t.hwp_to_markdown("notice.hwp"))
t.hwp_to_docx("notice.hwpx").save(".")
```

Methods: `run_flow(flow, files, vars=None)`, `run_tool(tool, files, options=None, scope="all")`, `hwp_to_text`, `hwp_to_markdown`, `hwp_to_docx`, `hwp_to_pdf` (on-premises runner only). Files can be paths, `(name, bytes)` or open files. Errors raise `TTDUError` (`status`, `code`, `problem`). `TTDU.local(key)` talks to an on-premises runner.

`toolsthatdontupload/_api` is generated from [`openapi/ttdu-files.openapi.json`](../../openapi/ttdu-files.openapi.json) with [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) (MIT), then `postgen.py` adds one missing import. Docs: https://toolsthatdontupload.com/docs/sdk/
## Where your files go

- **Hosted API (default, `https://toolsthatdontupload.com`)**: your files are **sent to our server** (a Cloudflare Worker) and processed in memory for that one request. We do not store the files, the results or the flow. The usual minimal request record applies: https://toolsthatdontupload.com/privacy/
- **On-premises runner** (`http://127.0.0.1:8790`, for business customers): files stay on that computer. Contact: https://toolsthatdontupload.com/business/
- Limits on the hosted API: one request = one file call (20 free a day with a free key, then 60 credits; 20 a day per IP address without a key), up to 20 files and 15 MB per request. HWP to PDF is not available on the hosted API (it answers `501 browser_only`; use https://dagotools.com/en/tools/hwp-to-pdf/ in the browser).
## License
MIT
