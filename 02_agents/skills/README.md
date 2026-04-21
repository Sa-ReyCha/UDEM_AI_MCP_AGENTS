![Image Place Holder](../docs/ITC_DAY.png)

# Skills — Agents Module

This directory contains the **skills** used by the `02_agents/server.py` MCP server. Each skill is a self-contained Python module that implements a specific capability.

---

## Overview

| Skill | File | Description |
|-------|------|-------------|
| **Code Analyzer** | `code_analyzer_skill.py` | Scans a project folder and builds an LLM-ready prompt for high-level component analysis. |
| **Draw.io** | `drawio_skill.py` | Provides the draw.io MCP server configuration and helpers to generate Mermaid / XML diagrams. |

---

## 1. Code Analyzer Skill (`code_analyzer_skill.py`)

### Purpose

Walks through a codebase directory, reads source files, and produces a **structured prompt** that an LLM can consume to return a high-level architecture summary.

### Exposed Function

```python
analyze_code(folder_path: str) -> dict
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `folder_path` | `str` | Absolute or relative path to the project folder to analyze. |

**Returns** a dict with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `folder` | `str` | Resolved absolute path to the folder. |
| `file_tree` | `str` | Plain-text directory tree. |
| `file_count` | `int` | Number of source files found. |
| `prompt` | `str` | The full analysis prompt with embedded code context. |
| `components` | `list` | Empty list — placeholder to be filled by the LLM. |

### How It Works

1. **Directory scanning** — Recursively walks the folder, skipping common non-source directories (`node_modules`, `.git`, `__pycache__`, `venv`, etc.).
2. **File filtering** — Only reads files with recognized source extensions (`.py`, `.js`, `.ts`, `.java`, `.go`, `.yaml`, `.json`, `.md`, etc.).
3. **Content extraction** — Reads up to 3 000 characters per file to keep the prompt within reasonable token limits.
4. **Prompt building** — Assembles a prompt that instructs the LLM to return:
   - A list of **components** (name, type, responsibility, key files, dependencies).
   - An overall **Architecture Style** label.
   - A short **Summary** paragraph.

### Example Usage

```python
from skills.code_analyzer_skill import analyze_code

result = analyze_code("/path/to/my/project")
print(result["file_tree"])
print(result["prompt"])
```

---

## 2. Draw.io Skill (`drawio_skill.py`)

### Purpose

Encapsulates the **draw.io MCP server configuration** and provides helper functions to convert component analysis results into diagrams (Mermaid or draw.io XML format).

### Setup

The draw.io MCP server comes from the open-source repo [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp).

1. **Clone the repository** (or use the copy already in `dep/drawio-mcp/`):
   ```bash
   git clone https://github.com/jgraph/drawio-mcp.git
   ```

2. **Install dependencies** — this is a monorepo, so install inside the `mcp-tool-server` sub-package:
   ```bash
   cd drawio-mcp/mcp-tool-server && npm install
   ```
   > ⚠️ There is **no `package.json` at the repo root** — running `npm install` from `drawio-mcp/` directly will fail.

3. **Copy shared files** required at runtime:
   ```bash
   npm run prepack
   ```
   > This copies `postprocess.js` and reference markdown files from the monorepo root into the `src/` directory. Without this step the server crashes with `Cannot find module './postprocessor/postprocess.js'`.

4. **Set the environment variable** pointing to the server entry point:
   ```bash
   export DRAWIO_MCP_PATH="/absolute/path/to/drawio-mcp/mcp-tool-server/src/index.js"
   ```
   Or add it to your `.env` file (see `.env.example` in the project root).

### MCP Configuration

The configuration is built dynamically from the `DRAWIO_MCP_PATH` env var. The generated config looks like:

```json
{
  "drawio": {
    "disabled": false,
    "timeout": 60,
    "type": "stdio",
    "command": "node",
    "args": ["<value of DRAWIO_MCP_PATH>"]
  }
}
```

### Exposed Functions

#### `get_drawio_config() -> dict`

Returns the MCP configuration dict for the draw.io server. Used by the agent server to register or instantiate the draw.io connection.

---

#### `build_mermaid_from_components(components: list[dict]) -> str`

Converts a list of component dicts into a **Mermaid.js flowchart** definition.

**Component dict schema:**

```python
{
    "name": "ModuleName",
    "type": "Service",            # e.g. Module, Service, Library, Config
    "dependencies": ["OtherMod"]  # names of other components
}
```

**Example output:**

```
graph TD
    ModuleA["ModuleA<br/><i>Service</i>"]
    ModuleB["ModuleB<br/><i>Library</i>"]
    ModuleA --> ModuleB
```

---

#### `build_drawio_xml_from_components(components: list[dict]) -> str`

Converts a list of component dicts into a minimal **draw.io/mxGraph XML** diagram.

---

## How Skills Are Registered in the Server

The `02_agents/server.py` imports both skills and exposes them as MCP tools:

| MCP Tool | Skill Function | Description |
|----------|----------------|-------------|
| `analyze_code` | `code_analyzer_skill.analyze_code` | Scan a folder → get analysis prompt. |
| `generate_diagram` | `drawio_skill.build_mermaid_from_components` / `build_drawio_xml_from_components` | Components JSON → Mermaid or XML diagram. |
| `get_drawio_config` | `drawio_skill.get_drawio_config` | Get draw.io MCP server config. |

### Running the Server

```bash
# stdio mode (default — for Cline)
python 02_agents/server.py

# HTTP mode (for remote / tunnel access)
python 02_agents/server.py --transport http --port 8001
```

---

## Adding New Skills

1. Create a new Python file in this directory (e.g. `my_new_skill.py`).
2. Implement your skill functions with clear docstrings.
3. Import and register them as `@mcp.tool()` in `02_agents/server.py`.
4. Update this README with the new skill's documentation.

![Image Place Holder](../docs/ITC_DAY.png)