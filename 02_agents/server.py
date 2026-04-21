"""
MCP Server — Agents
====================
Tools exposed:
  1. analyze_code        — Scan a project folder and return a high-level
                           component summary (prompt + file context).
  2. generate_diagram    — Build a Mermaid or draw.io XML diagram from a
                           list of components.
  3. get_drawio_config   — Return the draw.io MCP server configuration so
                           that Cline (or another orchestrator) can
                           instantiate a connection to the draw.io server.

Skills used:
  - skills.code_analyzer_skill  (code analysis prompt builder)
  - skills.drawio_skill         (draw.io config & diagram helpers)
"""

import argparse
import json
import sys
from pathlib import Path

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Ensure the skills package is importable regardless of how the server
# is launched (e.g.  ``python 02_agents/server.py``  from the repo root).
# ---------------------------------------------------------------------------
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from skills.code_analyzer_skill import analyze_code as _analyze_code  # noqa: E402
from skills.drawio_skill import (  # noqa: E402
    build_drawio_xml_from_components,
    build_mermaid_from_components,
    get_drawio_config as _get_drawio_config,
)

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------
mcp = FastMCP(
    name="agents-server",
    instructions=(
        "You are a code-analysis and diagramming assistant.\n"
        "Use `analyze_code` to scan a project folder and get a high-level\n"
        "component summary.  Then use `generate_diagram` to turn the\n"
        "component list into a Mermaid or draw.io XML diagram.\n"
        "Use `get_drawio_config` to retrieve the draw.io MCP server\n"
        "configuration if you need to open a diagram in draw.io."
    ),
)


# ---------------------------------------------------------------------------
# Tool 1 — Code analysis
# ---------------------------------------------------------------------------
@mcp.tool()
def analyze_code(folder_path: str) -> dict:
    """
    Scan *folder_path* and return a high-level component summary of the
    codebase.  The response contains a ready-to-use analysis prompt with
    embedded code context that can be forwarded to an LLM.

    Args:
        folder_path: Absolute or relative path to the project folder.

    Returns:
        A dict with keys: folder, file_tree, file_count, prompt, components.
    """
    return _analyze_code(folder_path)


# ---------------------------------------------------------------------------
# Tool 2 — Diagram generator
# ---------------------------------------------------------------------------
@mcp.tool()
def generate_diagram(
    components_json: str,
    output_format: str = "mermaid",
) -> dict:
    """
    Generate a diagram from a JSON array of components.

    Each component object should have:
        - name:         str
        - type:         str  (e.g. Module, Service, Library …)
        - dependencies: list[str]  (names of other components)

    Args:
        components_json: A JSON string representing a list of component dicts.
        output_format:   "mermaid" (default) or "xml" (draw.io XML).

    Returns:
        A dict with keys:
            format  — the chosen output format
            diagram — the diagram definition string
    """
    try:
        components = json.loads(components_json)
    except json.JSONDecodeError as exc:
        return {"error": f"Invalid JSON: {exc}"}

    if not isinstance(components, list):
        return {"error": "components_json must be a JSON array."}

    fmt = output_format.lower().strip()

    if fmt == "mermaid":
        diagram = build_mermaid_from_components(components)
    elif fmt in ("xml", "drawio"):
        diagram = build_drawio_xml_from_components(components)
    else:
        return {"error": f"Unknown format '{output_format}'. Use 'mermaid' or 'xml'."}

    return {"format": fmt, "diagram": diagram}


# ---------------------------------------------------------------------------
# Tool 3 — Draw.io MCP configuration
# ---------------------------------------------------------------------------
@mcp.tool()
def get_drawio_config() -> dict:
    """
    Return the MCP configuration for the draw.io server.

    This allows an orchestrator (e.g. Cline) to know how to start or
    connect to the draw.io MCP server.

    Returns:
        A dict matching the Cline MCP settings schema for the drawio server.
    """
    return _get_drawio_config()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="agents-server MCP")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode: 'stdio' for Cline local (default) or 'http' for HTTP server",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind when using HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port to listen on when using HTTP transport (default: 8001)",
    )
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")