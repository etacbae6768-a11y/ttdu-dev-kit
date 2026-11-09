# ttdu-files (command line)

```sh
npm install -g ttdu-files
ttdu-files flow merge.json a.pdf b.pdf --out results
ttdu-files flow invoice.json scan.pdf --var client=ACME
ttdu-files tool pdf.rotate scan.pdf --options '{"angle":90}' --scope each
ttdu-files hwp markdown notice.hwp > notice.md
ttdu-files hwp docx notice.hwpx --out results
```

Every output file's sha256 is checked before it is written. `--json` prints the answer as JSON. Exit codes: 0 ok, 2 usage, 3 the API refused the request, 4 limit or credits reached.

The CLI sends files to the hosted API by default and prints a one-line notice saying so (`--quiet` hides it). `--local` uses an on-premises runner on this computer instead (key from `--key`, `TTDU_LOCAL_KEY` or `./local-api-key.txt`).
## Where your files go

- **Hosted API (default, `https://toolsthatdontupload.com`)**: your files are **sent to our server** (a Cloudflare Worker) and processed in memory for that one request. We do not store the files, the results or the flow. The usual minimal request record applies: https://toolsthatdontupload.com/privacy/
- **On-premises runner** (`http://127.0.0.1:8790`, for business customers): files stay on that computer. Contact: https://toolsthatdontupload.com/business/
- Limits on the hosted API: one request = one file call (20 free a day with a free key, then 60 credits; 20 a day per IP address without a key), up to 20 files and 15 MB per request. HWP to PDF is not available on the hosted API (it answers `501 browser_only`; use https://dagotools.com/en/tools/hwp-to-pdf/ in the browser).
## License
MIT
