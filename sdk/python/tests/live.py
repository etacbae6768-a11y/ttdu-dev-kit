"""usage: python tests/live.py <base_url> [api_key]  — compares results with test/expected.json (sha256)."""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
from toolsthatdontupload import TTDU, TTDUError
E = json.load(open(os.path.join(ROOT, "test", "expected.json"), encoding="utf-8"))
fx = lambda n: os.path.join(ROOT, "test", "fixtures", n)
base = sys.argv[1]; key = sys.argv[2] if len(sys.argv) > 2 else None
t = TTDU(base_url=base, api_key=key); local = "127.0.0.1" in base or "localhost" in base
only = os.environ.get("ONLY", "flow,md,docx,pdf").split(","); rows = []
def ok(n, c, i=""): rows.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (" " + str(i) if i else ""))
if "flow" in only:
    r = t.run_flow({"schema": "ttdu.flow/v1", "steps": [{"tool": "pdf.merge", "scope": "all", "options": {}}]}, [fx(n) for n in E["fixtures"]["merge"]])
    ok("py run_flow merge sha256", r["files"][0].sha256 == E["flow_merge_sha256"], r["files"][0].sha256)
if "md" in only:
    md = t.hwp_to_markdown(fx(E["fixtures"]["hwp"])); h = hashlib.sha256(md.encode("utf-8")).hexdigest(); ok("py hwp_to_markdown sha256", h == E["hwp_markdown_sha256"], h)
if "docx" in only:
    d = t.hwp_to_docx(fx(E["fixtures"]["hwp"])); ok("py hwp_to_docx sha256", d.sha256 == E["hwp_docx_sha256"], d.sha256)
if "pdf" in only:
    try:
        p = t.hwp_to_pdf(fx(E["fixtures"]["hwp"])); ok("py hwp_to_pdf (local runner) %PDF", local and p.data[:5] == b"%PDF-")
    except TTDUError as e:
        ok("py hwp_to_pdf hosted -> 501 browser_only", (not local) and e.status == 501 and e.code == "browser_only", e)
print(f"{sum(rows)}/{len(rows)}"); sys.exit(0 if all(rows) else 1)
