![Image Place Holder](../docs/ITC_DAY.png)

# MCP Server — Agents

An MCP server built with **FastMCP** that exposes tools for **code analysis** and **diagram generation**.  
It uses modular **skills** (self-contained Python modules) to implement each capability.  
Supports two transport modes: **stdio** (local) and **HTTP** (remote via tunnel).

---

## Available Tools

### 1. `analyze_code` — Code Analysis

Scans a project folder, reads source files, and returns a high-level component summary with an LLM-ready analysis prompt.

| Parameter | Type | Description |
|-----------|------|-------------|
| `folder_path` | `str` | Absolute or relative path to the project folder to analyze |

**Returns:** A dict with `folder`, `file_tree`, `file_count`, `prompt`, and `components`.

```python
analyze_code(folder_path="/path/to/my/project")
```

**How it works:**
1. Recursively walks the directory, skipping non-source folders (`node_modules`, `.git`, `__pycache__`, etc.).
2. Reads files with recognized source extensions (`.py`, `.js`, `.ts`, `.java`, `.go`, `.yaml`, `.json`, `.md`, etc.).
3. Extracts up to 3 000 characters per file to stay within token limits.
4. Builds a structured prompt instructing the LLM to return components, architecture style, and a summary.

---

### 2. `generate_diagram` — Diagram Generator

Converts a JSON array of components into a **Mermaid.js** flowchart or a **draw.io XML** diagram.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `components_json` | `str` | — | A JSON string representing a list of component dicts |
| `output_format` | `str` | `"mermaid"` | `"mermaid"` or `"xml"` (draw.io XML) |

Each component object should have:

| Key | Type | Description |
|-----|------|-------------|
| `name` | `str` | Short, descriptive name |
| `type` | `str` | e.g. Module, Service, Library, Config |
| `dependencies` | `list[str]` | Names of other components it depends on |

**Returns:** A dict with `format` and `diagram`.

```python
generate_diagram(
    components_json='[{"name": "API", "type": "Service", "dependencies": ["DB"]}]',
    output_format="mermaid"
)
```

---

### 3. `get_drawio_config` — Draw.io MCP Configuration

Returns the MCP configuration for the draw.io server so that an orchestrator (e.g. Cline) can instantiate a connection to render diagrams.

**Returns:** A dict matching the Cline MCP settings schema for the drawio server.

> Requires the `DRAWIO_MCP_PATH` environment variable to be set. See the [Skills README](skills/README.md) for setup instructions.

---

## Recommended Workflow

```
Project folder path
        │
        ▼
analyze_code(folder_path)
        │
        ▼
LLM processes the prompt and returns components
        │
        ▼
generate_diagram(components_json, output_format="mermaid")
        │
        ▼
(Optional) get_drawio_config() → open diagram in draw.io
```

---

## Skills Architecture

This server uses a **skills-based architecture**. Each skill is a self-contained Python module in the `skills/` directory:

| Skill | File | Description |
|-------|------|-------------|
| **Code Analyzer** | `skills/code_analyzer_skill.py` | Scans a project folder and builds an LLM-ready analysis prompt |
| **Draw.io** | `skills/drawio_skill.py` | Provides draw.io MCP config and helpers to generate Mermaid / XML diagrams |

See the [Skills README](skills/README.md) for detailed documentation on each skill.

---

## How to Run

### Option A — stdio (default, Cline local)

```bash
# Activate the virtual environment
source .env_santi/bin/activate

# Install dependencies (first time only)
pip install -r 00_setup/requirements.txt

# Start the server (stdio mode — default)
python 02_agents/server.py
```

---

### Option B — HTTP server (for tunnel / remote access)

```bash
# Start the server in HTTP mode (listens on port 8001)
python 02_agents/server.py --transport http

# Custom host/port (optional)
python 02_agents/server.py --transport http --host 0.0.0.0 --port 8001
```

The server exposes the MCP endpoint at:
```
http://localhost:8001/mcp
```

---

### Option C — MCP Inspector (browser UI, no Cline needed)

The **MCP Inspector** lets you call and test your tools directly from the browser — great for development and demos.

#### C.1 — STDIO mode (single command)

```bash
# macOS — use python3 or the full venv path
npx @modelcontextprotocol/inspector python3 02_agents/server.py

# Recommended: use the venv Python so packages are found
npx @modelcontextprotocol/inspector .env_santi/bin/python 02_agents/server.py
```

> **Important:** In the browser UI, make sure the **Transport Type** dropdown is set to **"STDIO"** (not "Streamable HTTP"), then click **Connect**.

> **`spawn python ENOENT` error?**  
> macOS does not ship a bare `python` binary — use `python3` or the full venv path above.

#### C.2 — Streamable HTTP mode (two terminals)

If you prefer to test the HTTP transport, start the server first and then open the Inspector separately:

```bash
# Terminal 1 — start the server in HTTP mode
python3 02_agents/server.py --transport http

# Terminal 2 — open the Inspector (no server command needed)
npx @modelcontextprotocol/inspector
```

In the browser UI, set:
- **Transport Type**: `Streamable HTTP`
- **URL**: `http://localhost:8001/mcp`

Then click **Connect**.

---

Open the URL printed in the terminal (usually `http://localhost:6274`). From there you can browse and test all registered tools.

---

## Connecting to Cline

### stdio connection (local)

```json
{
  "mcpServers": {
    "agents-server": {
      "command": "/path/to/venv/bin/python",
      "args": ["02_agents/server.py"],
      "cwd": "/path/to/UDEM_AI_MCP_AGENTS"
    }
  }
}
```

### HTTP connection (local or tunnel)

```json
{
  "mcpServers": {
    "agents-server": {
      "disabled": false,
      "timeout": 60,
      "type": "streamable-http",
      "url": "http://localhost:8001/mcp"
    }
  }
}
```

> ⚠️ `"disabled"` and `"timeout"` are **required** — without them Cline throws `Invalid MCP settings schema`.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DRAWIO_MCP_PATH` | Optional | Absolute path to the draw.io MCP server entry point (`index.js`). Required only if you want to use the draw.io integration. See [Skills README](skills/README.md). |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `fastmcp` | Framework for building MCP servers in Python |
| `python-dotenv` | Load environment variables from `.env` |

![Image Place Holder](../docs/ITC_DAY.png)