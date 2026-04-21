# UDEM AI Workshop — MCP Agents with Cline & VS Code

## Overview

This repository accompanies a hands-on workshop focused on building AI agents powered by the **Model Context Protocol (MCP)**. Participants will walk through the entire process of setting up, building, and configuring their own MCP server, then connect it to **Cline** inside **Visual Studio Code** to create an AI agent that understands their project context.

Whether you are looking to automate repetitive tasks, integrate custom tools, or understand how AI agents are changing the development landscape, this session provides a practical, end-to-end experience.

---

## What We Will Cover

1. **The Setup** — Getting Visual Studio Code, Cline, and your Python environment ready.
2. **Understanding MCP** — Why the Model Context Protocol is the foundational layer for your AI agent.
3. **Building Your Server** — Creating and extending an MCP server to expose custom tools and functionality.
4. **Agent Skills** — Adding modular skills (code analysis, diagram generation) on top of MCP.
5. **Cline Configuration** — Connecting your LLM API and MCP servers to Cline.
6. **Live Demo** — Building a stock price tool from scratch using Specification Driven Development (SDD).

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Visual Studio Code | Latest stable release |
| Python | 3.10 or higher |
| Node.js | 18+ (for draw.io MCP server) |
| Cline | VS Code extension (preferred AI agent interface) |
| LLM API Key | Any supported provider: OpenAI, Anthropic, Google Gemini, or local via Ollama |

---

## Repository Structure

```
UDEM_AI_MCP_AGENTS/
├── 00_setup/          Setup guides, dependencies, and API key configuration
├── 01_mcp/            MCP server — web search tool (DuckDuckGo) with stdio & HTTP transport
├── 02_agents/         Agent server — code analysis + diagram generation (Mermaid / draw.io XML)
│   └── skills/        Modular skill modules (code_analyzer, drawio)
├── 03_cline_config/   Cline MCP configuration template and system prompts
├── 04_live_demo/      SDD spec for building a stock price MCP server from scratch
├── dep/               External dependencies (draw.io MCP server)
├── agent/             Agent templates and reference docs
└── docs/              Images and supplementary documentation
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Sa-ReyCha/UDEM_AI_MCP_AGENTS.git
cd UDEM_AI_MCP_AGENTS

# 2. Set up your environment variables
cp .env.example .env
# Edit .env and configure DRAWIO_MCP_PATH (see .env.example for instructions)

# 3. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install Python dependencies
pip install -r 00_setup/requirements.txt

# 5. Start an MCP server
python 01_mcp/server.py --transport http          # Web search server on port 8000
python 02_agents/server.py --transport http        # Agents server on port 8001

# 6. Open VS Code and connect Cline to your servers
code .
```

For detailed setup instructions, see [`00_setup/README.md`](./00_setup/README.md).
For API key guides, see [`00_setup/openai_api_key_guide.md`](./00_setup/openai_api_key_guide.md) or [`00_setup/anthropic_api_key_guide.md`](./00_setup/anthropic_api_key_guide.md).

---

## MCP Servers Overview

| Server | Directory | Port | Transport | Tool(s) |
|--------|-----------|------|-----------|---------|
| **Search** | `01_mcp/` | 8000 | stdio / HTTP | `search_web` — DuckDuckGo web search |
| **Agents** | `02_agents/` | 8001 | stdio / HTTP | `analyze_code`, `generate_diagram`, `get_drawio_config` |
| **Draw.io** | `dep/drawio-mcp/` | — | stdio | `open_drawio_xml`, `open_drawio_mermaid`, `open_drawio_csv` |
| **Stock Price** *(live demo)* | `04_live_demo/` | 8002 | HTTP | `get_stock_price` *(to be built during the workshop)* |

---

## Workshop Flow

```
00_setup  →  01_mcp  →  02_agents  →  03_cline_config  →  04_live_demo
```

Each module is self-contained and builds on the previous one. Participants may navigate to any module independently once the initial setup is complete.

---

## License

This project is intended for educational use as part of the UDEM AI Workshop series.