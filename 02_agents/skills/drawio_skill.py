"""
Draw.io Skill
==============
Provides the draw.io MCP server configuration and helper utilities
to generate diagrams from code analysis results.

The draw.io MCP server is a Node.js process that exposes tools to open
and render diagrams in draw.io format (XML, CSV, or Mermaid).

Setup:
    1. Clone the draw.io MCP server repository::

        git clone https://github.com/jgraph/drawio-mcp.git

    2. Install its dependencies::

        cd drawio-mcp && npm install

    3. Set the environment variable ``DRAWIO_MCP_PATH`` pointing to the
       server entry point::

        export DRAWIO_MCP_PATH="/absolute/path/to/drawio-mcp/mcp-tool-server/src/index.js"

    If ``DRAWIO_MCP_PATH`` is not set, a warning is shown at import time.

Functions exposed:
  1. get_drawio_config                — Return the draw.io MCP server configuration
  2. build_mermaid_from_components    — Convert components into a Mermaid.js flowchart
  3. build_drawio_xml_from_components — Convert components into draw.io XML
"""

import os
import warnings

# ---------------------------------------------------------------------------
# Draw.io MCP Server Configuration (agnostic via env var)
# ---------------------------------------------------------------------------
_DEFAULT_DRAWIO_PATH = "drawio-mcp/mcp-tool-server/src/index.js"

DRAWIO_MCP_PATH: str = os.environ.get("DRAWIO_MCP_PATH", _DEFAULT_DRAWIO_PATH)

if DRAWIO_MCP_PATH == _DEFAULT_DRAWIO_PATH:
    warnings.warn(
        "DRAWIO_MCP_PATH environment variable is not set. "
        "Using default relative path. "
        "Please clone the repo and set the variable:\n"
        "  git clone https://github.com/jgraph/drawio-mcp.git\n"
        '  export DRAWIO_MCP_PATH="/absolute/path/to/drawio-mcp/mcp-tool-server/src/index.js"',
        stacklevel=2,
    )

# Source repository for reference
DRAWIO_MCP_REPO = "https://github.com/jgraph/drawio-mcp.git"


def get_drawio_config() -> dict:
    """
    Return the MCP configuration dict for the draw.io server.

    The path to the draw.io MCP entry point is read from the
    ``DRAWIO_MCP_PATH`` environment variable.

    Returns:
        A dict matching the Cline MCP settings schema for the drawio server.
    """
    return {
        "drawio": {
            "disabled": False,
            "timeout": 60,
            "type": "stdio",
            "command": "node",
            "args": [DRAWIO_MCP_PATH],
        }
    }


def get_drawio_repo() -> str:
    """Return the git clone URL for the draw.io MCP server."""
    return DRAWIO_MCP_REPO


# ---------------------------------------------------------------------------
# Helper — Build a Mermaid diagram from component analysis
# ---------------------------------------------------------------------------
def build_mermaid_from_components(components: list[dict]) -> str:
    """
    Convert a list of high-level components into a Mermaid.js flowchart
    definition that can be rendered by the draw.io MCP tool
    ``open_drawio_mermaid``.

    Each component dict is expected to have at least:
        - name: str
        - type: str
        - dependencies: list[str]   (names of other components)

    Args:
        components: List of component dicts (as produced by the code
                    analyzer skill or manually assembled).

    Returns:
        A Mermaid.js graph definition string.

    Example output::

        graph TD
            ModuleA["ModuleA<br/><i>Service</i>"]
            ModuleB["ModuleB<br/><i>Library</i>"]
            ModuleA --> ModuleB
    """
    lines: list[str] = ["graph TD"]

    # Sanitize node ids (remove spaces, special chars)
    def _node_id(name: str) -> str:
        return name.replace(" ", "_").replace("-", "_").replace(".", "_")

    # Add nodes
    for comp in components:
        nid = _node_id(comp.get("name", "Unknown"))
        label = comp.get("name", "Unknown")
        comp_type = comp.get("type", "")
        lines.append(f'    {nid}["{label}<br/><i>{comp_type}</i>"]')

    # Add edges (dependencies)
    for comp in components:
        src = _node_id(comp.get("name", "Unknown"))
        for dep_name in comp.get("dependencies", []):
            dst = _node_id(dep_name)
            lines.append(f"    {src} --> {dst}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helper — Build draw.io XML from component analysis
# ---------------------------------------------------------------------------
def build_drawio_xml_from_components(components: list[dict]) -> str:
    """
    Convert a list of high-level components into a minimal draw.io XML
    diagram that can be rendered by the draw.io MCP tool ``open_drawio_xml``.

    Args:
        components: List of component dicts.

    Returns:
        A draw.io/mxGraph XML string.
    """
    cells: list[str] = []
    x, y = 40, 40
    cell_id = 2  # 0 and 1 are reserved by mxGraph

    for comp in components:
        label = comp.get("name", "Unknown")
        comp_type = comp.get("type", "")
        display = f"{label}\\n({comp_type})" if comp_type else label
        cells.append(
            f'      <mxCell id="{cell_id}" value="{display}" '
            f'style="rounded=1;whiteSpace=wrap;html=1;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="160" height="60" as="geometry"/>'
            f"</mxCell>"
        )
        cell_id += 1
        x += 200
        if x > 600:
            x = 40
            y += 100

    xml = f"""<mxfile>
  <diagram name="Architecture">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{chr(10).join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

    return xml