# ttdu-agent-tools (LlamaIndex, LangChain)

```python
from ttdu_agent_tools import llamaindex_tools, langchain_tools
tools = llamaindex_tools(out_dir="out", allow_dir="inbox")   # llama-index-core (MIT): FunctionTool
tools = langchain_tools(out_dir="out", allow_dir="inbox")    # langchain-core (MIT): StructuredTool
```

Tools: `ttdu_run_flow(flow, files, vars)`, `ttdu_hwp_to_markdown(file)`, `ttdu_hwp_to_docx(file)`. Files are paths on the machine running the agent; `allow_dir` limits which folder they may come from.
## Where your files go

- **Hosted API (default, `https://toolsthatdontupload.com`)**: your files are **sent to our server** (a Cloudflare Worker) and processed in memory for that one request. We do not store the files, the results or the flow. The usual minimal request record applies: https://toolsthatdontupload.com/privacy/
- **On-premises runner** (`http://127.0.0.1:8790`, for business customers): files stay on that computer. Contact: https://toolsthatdontupload.com/business/
- Limits on the hosted API: one request = one file call (20 free a day with a free key, then 60 credits; 20 a day per IP address without a key), up to 20 files and 15 MB per request. HWP to PDF is not available on the hosted API (it answers `501 browser_only`; use https://dagotools.com/en/tools/hwp-to-pdf/ in the browser).
## License
MIT
