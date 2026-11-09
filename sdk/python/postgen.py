"""Post-generation fix for openapi-python-client 0.30.0: api modules use `Unset` in annotations without importing it."""
import pathlib, re
root = pathlib.Path(__file__).parent / "toolsthatdontupload" / "_api" / "api"
for p in root.rglob("*.py"):
    s = p.read_text(encoding="utf-8")
    if re.search(r"\bUnset\b", s) and not re.search(r"import[^\n]*\bUnset\b", s):
        s2 = s.replace("from ...types import UNSET, Response", "from ...types import UNSET, Response, Unset", 1)
        if s2 == s: raise SystemExit("cannot fix " + str(p))
        p.write_text(s2, encoding="utf-8"); print("fixed", p.relative_to(root))
