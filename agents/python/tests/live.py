"""usage: python tests/live.py <base_url> [api_key] — calls each tool through the framework API (no model), checks sha256."""
import hashlib, json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path[:0] = [os.path.join(HERE, ".."), os.path.join(ROOT, "sdk", "python")]
from ttdu_agent_tools import llamaindex_tools, langchain_tools
E = json.load(open(os.path.join(ROOT, "test", "expected.json"), encoding="utf-8")); fx = lambda n: os.path.join(ROOT, "test", "fixtures", n)
base = sys.argv[1]; key = sys.argv[2] if len(sys.argv) > 2 else None; out = tempfile.mkdtemp(prefix="ttdu-pyagents-")
only = os.environ.get("ONLY", "li-flow,li-md,lc-md,lc-docx,lc-guard").split(","); rows = []
def ok(n, c, i=""): rows.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (" " + str(i) if i else ""))
li = {t.metadata.name: t for t in llamaindex_tools(api_key=key, base_url=base, out_dir=os.path.join(out, "li"))}
flow = {"schema": "ttdu.flow/v1", "steps": [{"tool": "pdf.merge", "scope": "all", "options": {}}]}
if "li-flow" in only:
    r = li["ttdu_run_flow"].call(flow=flow, files=[fx(n) for n in E["fixtures"]["merge"]]).raw_output
    ok("llamaindex ttdu_run_flow sha256", r["files"][0]["sha256"] == E["flow_merge_sha256"] and hashlib.sha256(open(r["files"][0]["path"], "rb").read()).hexdigest() == E["flow_merge_sha256"], r["files"][0]["sha256"])
if "li-md" in only:
    md = li["ttdu_hwp_to_markdown"].call(file=fx(E["fixtures"]["hwp"])).raw_output; h = hashlib.sha256(md.encode()).hexdigest(); ok("llamaindex ttdu_hwp_to_markdown sha256", h == E["hwp_markdown_sha256"], h)
lc = {t.name: t for t in langchain_tools(api_key=key, base_url=base, out_dir=os.path.join(out, "lc"), allow_dir=os.path.join(ROOT, "test"))}
if "lc-md" in only:
    md = lc["ttdu_hwp_to_markdown"].invoke({"file": fx(E["fixtures"]["hwp"])}); h = hashlib.sha256(md.encode()).hexdigest(); ok("langchain-py ttdu_hwp_to_markdown sha256", h == E["hwp_markdown_sha256"], h)
if "lc-docx" in only:
    r = lc["ttdu_hwp_to_docx"].invoke({"file": fx(E["fixtures"]["hwp"])}); ok("langchain-py ttdu_hwp_to_docx sha256", r["files"][0]["sha256"] == E["hwp_docx_sha256"], r["files"][0]["sha256"])
if "lc-guard" in only:
    try: lc["ttdu_hwp_to_markdown"].invoke({"file": os.path.join(os.path.expanduser("~"), "x.hwp")}); ok("langchain-py allow_dir blocks other paths", False)
    except Exception as e: ok("langchain-py allow_dir blocks other paths", "outside the allowed folder" in str(e))
print(f"{sum(rows)}/{len(rows)}"); sys.exit(0 if all(rows) else 1)
