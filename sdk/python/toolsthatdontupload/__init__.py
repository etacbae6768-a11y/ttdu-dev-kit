"""Tools That Don't Upload — Python SDK for the file flows and HWP/HWPX API.

The low-level client in ``toolsthatdontupload._api`` is generated from ``openapi/ttdu-files.openapi.json`` by
openapi-python-client (MIT). IMPORTANT: with the hosted API (the default base URL) your files are sent to our
server, processed in memory for that one request and not stored. With an on-premises runner (business customers)
files stay on that computer.
"""
from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from ._api.client import AuthenticatedClient, Client
from ._api.api.flows import run_flow as _run_flow
from ._api.api.hwp import hwp_to_docx as _hwp_docx, hwp_to_markdown as _hwp_md, hwp_to_pdf as _hwp_pdf, hwp_to_text as _hwp_text
from ._api.models.flow_run_json import FlowRunJson
from ._api.models.hwp_to_docx_json_body import HwpToDocxJsonBody
from ._api.models.hwp_to_markdown_json_body import HwpToMarkdownJsonBody
from ._api.models.hwp_to_pdf_json_body import HwpToPdfJsonBody
from ._api.models.hwp_to_text_json_body import HwpToTextJsonBody

__version__ = "0.1.0"
HOSTED_URL = "https://toolsthatdontupload.com"
LOCAL_URL = "http://127.0.0.1:8790"
__all__ = ["TTDU", "TTDUError", "Output", "HOSTED_URL", "LOCAL_URL"]


class TTDUError(Exception):
    """Error answer (RFC 9457 problem details): ``status``, ``code`` and the full ``problem`` dict."""

    def __init__(self, status: int, problem: Mapping[str, Any] | None):
        self.status = status
        self.problem = dict(problem or {})
        self.code = self.problem.get("code")
        super().__init__(f"{status} {self.problem.get('title', 'Error')}" + (f" ({self.code})" if self.code else "") + f": {self.problem.get('detail', '')}")


@dataclass
class Output:
    name: str
    mime: str
    size: int
    sha256: str
    data: bytes

    def save(self, folder: str = ".") -> str:
        path = os.path.join(folder, self.name)
        with open(path, "wb") as f:
            f.write(self.data)
        return path


def _file(f: Any) -> tuple[str, bytes]:
    """Accepts a path, (name, bytes) or an object with .name and .read()."""
    if isinstance(f, (str, os.PathLike)):
        with open(f, "rb") as h:
            return os.path.basename(str(f)), h.read()
    if isinstance(f, tuple):
        return str(f[0]), bytes(f[1])
    return os.path.basename(getattr(f, "name", "file")), f.read()


def _outputs(items: Iterable[Mapping[str, Any]]) -> list[Output]:
    out = []
    for o in items or []:
        data = base64.b64decode(o["base64"])
        h = hashlib.sha256(data).hexdigest()
        if h != o["sha256"]:
            raise TTDUError(0, {"title": "Checksum mismatch", "detail": f"{o['name']}: {h} != {o['sha256']}"})
        out.append(Output(o["name"], o["mime"], o["size"], o["sha256"], data))
    return out


class TTDU:
    """Client. ``TTDU()`` uses the hosted API; ``TTDU.local(key)`` an on-premises runner."""

    def __init__(self, base_url: str = HOSTED_URL, api_key: str | None = None, timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        api_key = api_key or os.environ.get("TTDU_API_KEY") or None
        if api_key:
            self._c = AuthenticatedClient(base_url=self.base_url, token=api_key, prefix="", auth_header_name="X-API-Key", timeout=timeout)
        else:
            self._c = Client(base_url=self.base_url, timeout=timeout)

    @classmethod
    def local(cls, api_key: str, base_url: str = LOCAL_URL) -> "TTDU":
        return cls(base_url=base_url, api_key=api_key)

    def _call(self, fn, body) -> dict[str, Any]:
        r = fn.sync_detailed(client=self._c, body=body)
        import json
        try:
            data = json.loads(r.content or b"{}")
        except ValueError:
            data = {"title": "Not JSON", "detail": r.content[:200].decode("utf-8", "replace")}
        if int(r.status_code) >= 400 or not data.get("ok", False):
            raise TTDUError(int(r.status_code), data)
        return data

    def run_flow(self, flow: Mapping[str, Any], files: Iterable[Any], vars: Mapping[str, str] | None = None) -> dict[str, Any]:
        """Run a saved flow (ttdu.flow/v1). Returns the answer plus ``files`` (list of Output, sha256 checked)."""
        payload: dict[str, Any] = {"flow": dict(flow), "files": [{"name": n, "base64": base64.b64encode(b).decode()} for n, b in map(_file, files)]}
        if vars:
            payload["vars"] = dict(vars)
        data = self._call(_run_flow, FlowRunJson.from_dict(payload))
        data["files"] = _outputs(data.get("outputs", []))
        return data

    def run_tool(self, tool: str, files: Iterable[Any], options: Mapping[str, Any] | None = None, scope: str = "all") -> dict[str, Any]:
        """Run one tool: a flow with a single step."""
        return self.run_flow({"schema": "ttdu.flow/v1", "steps": [{"tool": tool, "scope": scope, "options": dict(options or {})}]}, files)

    def _hwp(self, fn, model, file) -> dict[str, Any]:
        name, data = _file(file)
        return self._call(fn, model.from_dict({"name": name, "base64": base64.b64encode(data).decode()}))

    def hwp_to_text(self, file: Any) -> dict[str, Any]:
        return self._hwp(_hwp_text, HwpToTextJsonBody, file)

    def hwp_to_markdown(self, file: Any) -> str:
        return self._hwp(_hwp_md, HwpToMarkdownJsonBody, file)["markdown"]

    def hwp_to_docx(self, file: Any) -> Output:
        return _outputs(self._hwp(_hwp_docx, HwpToDocxJsonBody, file)["outputs"])[0]

    def hwp_to_pdf(self, file: Any) -> Output:
        """Only on an on-premises runner; the hosted API answers 501 browser_only."""
        return _outputs(self._hwp(_hwp_pdf, HwpToPdfJsonBody, file)["outputs"])[0]
