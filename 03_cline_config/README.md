![Image Place Holder](../docs/ITC_DAY.png)


# Cline Configuration

This directory contains the **MCP server configuration** and **system prompts** used to configure Cline (the AI coding agent in VS Code).

---

## Files

| File / Directory | Description |
|-----------------|-------------|
| `cline_mcp_config.json` | Template MCP server configuration for Cline |
| `system_prompts/developer_agent.md` | System prompt for a Developer Agent persona |
| `system_prompts/research_agent.md` | System prompt for a Research Agent persona |

---

## MCP Server Configuration (`cline_mcp_config.json`)

This is a **template** configuration file for Cline's MCP servers. It includes the three servers used in this workshop:

| Server | Type | Description |
|--------|------|-------------|
| `basic-search-server` | HTTP | Web search via DuckDuckGo (`01_mcp/server.py`) |
| `agents-server` | HTTP | Code analysis & diagram **generation** (`02_agents/server.py`) |
| `drawio` | stdio | Diagram **rendering** — opens diagrams in the draw.io editor ([jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)) |

> **Why 3 servers?** The `agents-server` *generates* diagram data (Mermaid text or draw.io XML) but cannot display it. The `drawio` server *renders* that data visually in the browser via tools like `open_drawio_mermaid` and `open_drawio_xml`. They work together:
>
> `analyze_code()` → `generate_diagram()` → `open_drawio_mermaid()` / `open_drawio_xml()`
>
> *(agents-server)* → *(agents-server)* → *(drawio server)*

### How to Use

1. **Copy** the template to your Cline settings location:
   ```
   macOS:   ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
   Linux:   ~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
   Windows: %APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
   ```

2. **Replace placeholders:**
   - `<REPO_ROOT>` → absolute path to this repository (e.g. `/Users/you/UDEM_AI_MCP_AGENTS`)

3. **Start the MCP servers** before using Cline:
   ```bash
   # Terminal 1 — Search server
   python 01_mcp/server.py --transport http

   # Terminal 2 — Agents server
   python 02_agents/server.py --transport http
   ```

   The `drawio` server is launched automatically by Cline via stdio.

### Draw.io Setup

The draw.io MCP server is already included in the repository under `dep/drawio-mcp/`. You only need to install its dependencies:

```bash
# Install dependencies (monorepo — install inside the mcp-tool-server sub-package)
cd dep/drawio-mcp/mcp-tool-server && npm install

# Copy shared files required at runtime (postprocessor, reference docs)
npm run prepack
```

> ⚠️ There is **no `package.json` at the `drawio-mcp/` root** — you must install from `mcp-tool-server/`.
>
> The `npm run prepack` step copies `postprocess.js` and reference markdown files from the monorepo root into the `src/` directory where `index.js` expects them. Without this step the server will crash with `Cannot find module './postprocessor/postprocess.js'`.

Then update `cline_mcp_config.json`: replace `<REPO_ROOT>` with the absolute path to this repository. The resulting path should look like:

```
/Users/you/UDEM_AI_MCP_AGENTS/dep/drawio-mcp/mcp-tool-server/src/index.js
```

> Alternatively, if you cloned `drawio-mcp` to a different location, set the `DRAWIO_MCP_PATH` environment variable in your `.env` file (see `.env.example`).

---

## System Prompts

System prompts define the **persona and capabilities** of the AI agent when using Cline. They tell the agent what tools are available and how to use them.

### Developer Agent (`system_prompts/developer_agent.md`)

A **Senior Software Developer** persona that:
- Scans codebases and identifies architectural components
- Generates architecture diagrams (Mermaid / draw.io)
- Opens diagrams directly in draw.io
- Searches the web for documentation and best practices

### Research Agent (`system_prompts/research_agent.md`)

A **Research Assistant** persona that:
- Optimizes search queries using different styles (precise, boolean, question, quoted)
- Searches the web via DuckDuckGo
- Synthesizes findings into structured summaries
- Can scan codebases for context before researching

### How to Use System Prompts

You can set a system prompt in Cline by:
1. Opening Cline in VS Code
2. Going to **Settings** → **Custom Instructions**
3. Pasting the content of the desired system prompt file

---

## Adding Your Own Servers

To add a new MCP server to the configuration:

1. Add a new entry to `cline_mcp_config.json` under `mcpServers`.
2. For **HTTP servers**, specify `"type": "streamableHttp"` and the `"url"`.
3. For **stdio servers**, specify `"type": "stdio"`, the `"command"`, and `"args"`.
4. Update the system prompts to reference the new server's tools.

![Image Place Holder](../docs/ITC_DAY.png)