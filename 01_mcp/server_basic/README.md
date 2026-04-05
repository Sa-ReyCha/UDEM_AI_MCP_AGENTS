# MCP Server — Basic

A minimal MCP server built with **FastMCP** that exposes two tools for internet search and research.  
Supports two transport modes: **stdio** (local) and **HTTP** (remote via tunnel).

---

## Available Tools

### 1. `search_web` — Internet Search

Searches the web using **DuckDuckGo**. No API key required.  
Includes automatic retry with exponential backoff to handle rate-limiting.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | — | The search query string |
| `max_results` | `int` | `5` | Number of results to return (capped at 20) |

**Returns:** A list of results, each with `title`, `href`, and `body`.

```python
search_web(query="Model Context Protocol python", max_results=5)
```

---

### 2. `format_query` — Query Formatter / Rewriter

Takes a raw, informal query and reformats it for better search results.  
Use this **before** `search_web`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `raw_query` | `str` | — | The original, unformatted query |
| `style` | `str` | `"precise"` | Rewrite style (see table below) |
| `language` | `str` | `"en"` | Target language hint |

**Available styles:**

| Style | What it does | Input | Output |
|-------|-------------|-------|--------|
| `precise` | Strips filler/stop words, keeps key terms | `"tell me about machine learning"` | `"machine learning"` |
| `question` | Turns the query into a direct question | `"best practices python async"` | `"What is best practices python async?"` |
| `boolean` | Joins key terms with `AND` and quotes | `"python async performance"` | `"python" AND "async" AND "performance"` |
| `quoted` | Wraps the entire key phrase in quotes | `"climate change effects"` | `"climate change effects"` |

**Returns:** A dict with `original`, `formatted`, `style`, `language`, and `tips`.

```python
result  = format_query(raw_query="tell me about MCP agents", style="precise")
results = search_web(query=result["formatted"], max_results=5)
```

---

## Recommended Workflow

```
User prompt
      │
      ▼
format_query(raw_query, style="precise")
      │
      ▼
search_web(formatted_query, max_results=5)
      │
      ▼
Agent synthesises and returns answer
```

---

## How to Run

### Option A — stdio (default, Cline local)

```bash
# Activate the virtual environment
source .env_santi/bin/activate

# Install dependencies (first time only)
pip install -r 00_setup/requirements.txt

# Start the server (stdio mode — default)
python 01_mcp/server_basic/server.py
```

---

### Option B — HTTP server (for tunnel / remote access)

```bash
# Start the server in HTTP mode (listens on port 8000)
python 01_mcp/server_basic/server.py --transport http

# Custom host/port (optional)
python 01_mcp/server_basic/server.py --transport http --host 0.0.0.0 --port 8000
```

The server exposes the MCP endpoint at:
```
http://localhost:8000/mcp
```

#### Expose via tunnel

```bash
# ngrok
ngrok http 8000
# → https://abc123.ngrok.io/mcp

# Cloudflare Tunnel (no account needed for quick tests)
cloudflared tunnel --url http://localhost:8000
# → https://some-name.trycloudflare.com/mcp
```

---

### Option C — MCP Inspector (browser UI, no Cline needed)

The **MCP Inspector** lets you call and test your tools directly from the browser — great for development and demos.

```bash
# macOS — use python3 or the full venv path
npx @modelcontextprotocol/inspector python3 01_mcp/server_basic/server.py

# Recommended: use the venv Python so packages are found
npx @modelcontextprotocol/inspector .env_santi/bin/python 01_mcp/server_basic/server.py
```

> **`spawn python ENOENT` error?**  
> macOS does not ship a bare `python` binary — use `python3` or the full venv path above.

Open the URL printed in the terminal (usually `http://localhost:6274`). From there you can:

- Browse all registered tools (`search_web`, `format_query`)
- Fill in parameters and call tools manually
- Inspect the raw JSON request / response
- See the server logs in real time

---

## Connecting to Cline

### Mode 1 — Local stdio connection

**Use this when:** the server runs on the same machine as VS Code.

**Step 1** — In VS Code, click the **Cline icon** → click **MCP Servers** (plug icon) → **Edit MCP Settings**.

This opens:
```
~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

**Step 2** — Add the following entry (replace the paths with your actual repo location):

```json
{
  "mcpServers": {
    "basic-search-server": {
      "command": "/Users/santireycha/Documents/SAP LABS/UDEM_AI_MCP_AGENTS/.env_santi/bin/python",
      "args": ["01_mcp/server_basic/server.py"],
      "cwd": "/Users/santireycha/Documents/SAP LABS/UDEM_AI_MCP_AGENTS"
    }
  }
}
```

> **Tip:** Always use the full path to the venv Python (`.env_santi/bin/python`) so Cline
> finds `fastmcp` and `duckduckgo-search` without activating the environment manually.

**Step 3** — Save the file. Cline auto-restarts the server and shows `basic-search-server` as connected with both tools available.

---

### Mode 2 — Local HTTP connection (same machine, no tunnel)

**Use this when:** you want to run the server in HTTP mode but still connect from the same machine.

**Step 1** — Start the server in HTTP mode:

```bash
python 01_mcp/server_basic/server.py --transport http
# Server is now listening at http://localhost:8000/mcp
```

**Step 2** — In Cline MCP Settings, add:

```json
{
  "mcpServers": {
    "basic-search-server": {
      "disabled": false,
      "timeout": 60,
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

> ⚠️ `"disabled"` and `"timeout"` are **required** — without them Cline throws `Invalid MCP settings schema`.

**Step 3** — Save. Cline connects to the local HTTP server.

> **Important:** The server must be running before Cline tries to connect.
> Unlike stdio mode, Cline does **not** auto-start an HTTP server — you manage the process yourself.

---

### Mode 3 — Remote HTTP connection (via tunnel)

**Use this when:** the server runs on a remote machine, a VM, or you want to share it with teammates.

**Step 1** — Start the server in HTTP mode and expose it with a tunnel:

```bash
# Terminal 1 — start the server
python 01_mcp/server_basic/server.py --transport http

# Terminal 2 — expose it
ngrok http 8000
# copy the https URL, e.g. https://abc123.ngrok.io
```

**Step 2** — In Cline MCP Settings, add:

```json
{
  "mcpServers": {
    "basic-search-server": {
      "disabled": false,
      "timeout": 60,
      "type": "streamable-http",
      "url": "https://abc123.ngrok.io/mcp"
    }
  }
}
```

> ⚠️ `"disabled"` and `"timeout"` are **required** — without them Cline throws `Invalid MCP settings schema`.

Replace `https://abc123.ngrok.io` with the URL printed by your tunnel tool.

**Step 3** — Save. Cline connects over HTTPS to your tunneled server — no local Python needed on the client machine.

---

## Transport Comparison

| | stdio | HTTP local | HTTP + tunnel |
|---|---|---|---|
| Setup complexity | Low | Low-Medium | Medium |
| Requires local Python | Yes | Yes (server side) | No (client side) |
| Cline auto-starts server | ✅ Yes | ❌ No | ❌ No |
| Shareable with teammates | No | No | Yes |
| Survives VS Code restart | Auto-restarted by Cline | Must keep server running | Must keep server running |
| MCP Inspector compatible | ✅ (stdio mode) | ✅ `localhost:8000/mcp` | ✅ tunnel URL |
| Best for | Local dev / workshops | Local HTTP testing | Remote access / demos |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `fastmcp` | Framework for building MCP servers in Python |
| `duckduckgo-search` | Web search without an API key |
| `httpx` | Async HTTP client |
| `python-dotenv` | Load environment variables from `.env` |