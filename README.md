# UDEM AI Workshop — MCP Agents with Cline & VS Code

## Overview

This repository accompanies a hands-on workshop focused on building AI agents powered by the **Model Context Protocol (MCP)**. Participants will walk through the entire process of setting up, building, and configuring their own MCP server, then connect it to **Cline** inside **Visual Studio Code** to create an AI agent that understands their project context.

Whether you are looking to automate repetitive tasks, integrate custom tools, or understand how AI agents are changing the development landscape, this session provides a practical, end-to-end experience.

---

## What We Will Cover

1. **The Setup** — Getting Visual Studio Code, Cline, and your Python environment ready.
2. **Understanding MCP** — Why the Model Context Protocol is the foundational layer for your AI agent.
3. **Building Your Server** — Creating and extending an MCP server to expose custom tools and functionality.
4. **Agent Configuration** — Connecting your LLM API to Cline for optimized performance.
5. **Live Testing** — Putting your agent to work and troubleshooting in real time.

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Visual Studio Code | Latest stable release |
| Python | 3.10 or higher |
| Cline | VS Code extension (preferred AI agent interface) |
| LLM API Key | Any supported provider: OpenAI, Anthropic, Google Gemini, or local via Ollama |

---

## Repository Structure

```
UDEM_AI_MCP_AGENTS/
├── 00_setup/          Setup guides, dependencies, and API key configuration
├── 01_mcp/            MCP server — basic and extended implementations
├── 02_agents/         Agent skills and multi-step workflows
├── 03_cline_config/   Cline configuration and system prompts
├── 04_live_demo/      Demo scenarios and troubleshooting reference
└── docs/              Diagrams and supplementary documentation
```

Refer to [ARCHITECTURE.md](./ARCHITECTURE.md) for the full structural plan and module descriptions.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Sa-ReyCha/UDEM_AI_MCP_AGENTS.git
cd UDEM_AI_MCP_AGENTS

# 2. Set up your environment variables
cp .env.example .env
# Open .env and add your LLM API key

# 3. Install Python dependencies
pip install -r 00_setup/requirements.txt

# 4. Start the MCP server
python 01_mcp/server_basic/server.py

# 5. Open VS Code and connect Cline to your server
code .
```

For detailed setup instructions, see [`00_setup/README.md`](./00_setup/README.md).  
For API key configuration, refer to [`00_setup/api_key_config.pdf`](./00_setup/api_key_config.pdf).

---

## Workshop Flow

```
00_setup  ->  01_mcp  ->  02_agents  ->  03_cline_config  ->  04_live_demo
```

Each module is self-contained and builds on the previous one. Participants may navigate to any module independently once the initial setup is complete.

---

## License

This project is intended for educational use as part of the UDEM AI Workshop series.