"""Thin agent-framework tools for Tools That Don't Upload (LlamaIndex, LangChain).

Files are given as paths on the machine running the agent; results are written to ``out_dir``.
IMPORTANT: with the hosted API (default) the files are sent to toolsthatdontupload.com, processed in memory for
that one request and not stored. Pass ``base_url`` of an on-premises runner to keep files on your network.
"""
from __future__ import annotations

import os
from typing import Any

from toolsthatdontupload import HOSTED_URL, TTDU

__version__ = "0.1.0"
WHERE = "Files are sent to Tools That Don't Upload (processed in memory for this request, not stored) unless a local runner is configured."


class _Core:
    def __init__(self, api_key: str | None = None, base_url: str = HOSTED_URL, out_dir: str = ".", allow_dir: str | None = None):
        self.t = TTDU(base_url=base_url, api_key=api_key)
        self.out_dir = out_dir
        self.root = os.path.realpath(allow_dir) if allow_dir else None

    def _path(self, p: str) -> str:
        full = os.path.realpath(p)
        if self.root and not (full == self.root or full.startswith(self.root + os.sep)):
            raise ValueError(f"path outside the allowed folder: {p}")
        return full

    def _save(self, files) -> list[dict[str, Any]]:
        os.makedirs(self.out_dir, exist_ok=True)
        return [{"path": os.path.abspath(f.save(self.out_dir)), "name": f.name, "size": f.size, "sha256": f.sha256} for f in files]

    def run_flow(self, flow: dict, files: list[str], vars: dict | None = None) -> dict:
        r = self.t.run_flow(flow, [self._path(p) for p in files], vars)
        return {"ok": True, "steps": r.get("steps"), "notes": r.get("notes"), "files": self._save(r["files"])}

    def hwp_to_markdown(self, file: str) -> str:
        return self.t.hwp_to_markdown(self._path(file))

    def hwp_to_docx(self, file: str) -> dict:
        return {"ok": True, "files": self._save([self.t.hwp_to_docx(self._path(file))])}


def llamaindex_tools(**kw) -> list:
    """LlamaIndex (llama-index-core, MIT) FunctionTools."""
    from llama_index.core.tools import FunctionTool

    c = _Core(**kw)

    def ttdu_run_flow(flow: dict, files: list[str], vars: dict | None = None) -> dict:
        """Run a saved file flow (ttdu.flow/v1 JSON with steps such as pdf.merge) on local file paths and save the results."""
        return c.run_flow(flow, files, vars)

    def ttdu_hwp_to_markdown(file: str) -> str:
        """Convert a Korean HWP or HWPX document (local path) to Markdown, with tables as Markdown tables."""
        return c.hwp_to_markdown(file)

    def ttdu_hwp_to_docx(file: str) -> dict:
        """Convert a Korean HWP or HWPX document (local path) to an editable DOCX and save it."""
        return c.hwp_to_docx(file)

    return [FunctionTool.from_defaults(fn=f, description=(f.__doc__ or "") + " " + WHERE) for f in (ttdu_run_flow, ttdu_hwp_to_markdown, ttdu_hwp_to_docx)]


def langchain_tools(**kw) -> list:
    """LangChain (langchain-core, MIT) StructuredTools."""
    from langchain_core.tools import StructuredTool

    c = _Core(**kw)
    return [
        StructuredTool.from_function(func=c.run_flow, name="ttdu_run_flow", description="Run a saved file flow (ttdu.flow/v1) on local file paths and save the results. " + WHERE),
        StructuredTool.from_function(func=c.hwp_to_markdown, name="ttdu_hwp_to_markdown", description="Convert a Korean HWP or HWPX document (local path) to Markdown. " + WHERE),
        StructuredTool.from_function(func=c.hwp_to_docx, name="ttdu_hwp_to_docx", description="Convert a Korean HWP or HWPX document (local path) to an editable DOCX and save it. " + WHERE),
    ]
