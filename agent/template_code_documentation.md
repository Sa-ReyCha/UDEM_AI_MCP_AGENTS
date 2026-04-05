# Code Documentation Template
## Based on `01_mcp/server_basic/server.py` style

This document defines the documentation conventions used throughout this project.
All new Python files must follow these patterns for consistency.

---

## 1. Module-Level Docstring

Every `.py` file must start with a module docstring using the following structure:

```python
"""
<Module Title> — <Subtitle or Category>
==========================================
<Brief description of what this module does.>

Tools / Functions exposed:
  1. tool_or_function_name   — Short one-line description
  2. tool_or_function_name   — Short one-line description
"""
```

**Rules:**
- Title followed by a separator line of `=` characters (same length as the title).
- List every public tool or function with a short description.
- Keep it to a maximum of 5–8 lines.

---

## 2. Section Separators

Use this exact separator style to divide logical sections inside a file:

```python
# ---------------------------------------------------------------------------
# Section Name
# ---------------------------------------------------------------------------
```

**Common section names used in this project:**
| Section name | Purpose |
|---|---|
| `Server instance` | FastMCP / server initialization |
| `Tool 1 — <name>` | First tool definition |
| `Tool 2 — <name>` | Second tool definition |
| `Helpers` | Private utility functions |
| `Entry point` | `if __name__ == "__main__":` block |

---

## 3. Function / Tool Docstrings

Every public function or MCP tool must have a docstring following this structure:

```python
def my_function(param1: str, param2: int = 5) -> list[dict]:
    """
    One-line summary of what this function does.

    Optional: one or two lines expanding on behavior, edge cases,
    or important implementation notes (e.g., retry logic, fallback behavior).

    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter (default N, max M).

    Returns:
        Description of the return value and its structure.
        E.g., "A list of dicts with keys: title, href, body."
    """
```

**Rules:**
- First line: short imperative summary (no period at end, e.g. *"Search the internet…"*).
- Blank line after the summary before the expanded description.
- `Args:` section: one line per parameter, aligned with a colon separator.
- `Returns:` section: describe the type and shape of the return value.
- Use plain English — no RST/Sphinx markers like `:param:` or `:type:`.

---

## 4. Inline Sub-Section Comments (Inside Functions)

For long functions with distinct internal phases, use this mini-separator:

```python
# ---- subsection label --------------------------------------------------
```

**Example from `format_query`:**

```python
# ---- helpers -----------------------------------------------------------
FILLER_WORDS = { ... }

# ---- style logic -------------------------------------------------------
if style == "precise":
    ...
```

**Rules:**
- Use 4 dashes (`----`) before the label and fill to column ~72 with dashes after.
- Use only when a function has 2+ clearly distinct phases.
- Label should be lowercase, 1–3 words.

---

## 5. Inline Comments

```python
max_results = min(max_results, 20)   # cap to avoid abuse
if results:                           # got something — return immediately
    return results
```

**Rules:**
- Place inline comments at the end of the line, separated by two spaces.
- Use an em dash (`—`) to separate a short label from its explanation when needed.
- Do **not** state the obvious (e.g., `i += 1  # increment i`).

---

## 6. Constants and Configuration Blocks

```python
# Constants / config
MAX_RETRIES = 4
BASE_DELAY  = 2.0   # seconds — base for exponential backoff
```

**Rules:**
- Group related constants together after the imports section.
- Align the `=` sign when defining multiple related constants (optional but preferred).
- Add a short inline comment if the unit or purpose is not obvious.

---

## 7. Entry Point Block

```python
# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="<server-name> MCP")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode: 'stdio' for Cline local (default) or 'http' for HTTP server + tunnel",
    )
    # ... additional args ...
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
```

**Rules:**
- Always wrap `mcp.run()` inside the `if __name__ == "__main__":` guard.
- Always support both `stdio` and `http` transports via `--transport` argument.
- Include `--host` and `--port` arguments when HTTP transport is supported.

---

## 8. Imports Order

Follow this ordering (PEP 8):

```python
# 1. Standard library
import time
import random
import argparse

# 2. Third-party packages
from fastmcp import FastMCP
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException, RatelimitException

# 3. Local / project modules  (if any)
from .utils import my_helper
```

---

## 9. Quick Checklist for New Files

- [ ] Module-level docstring with title, separator, and tools list
- [ ] Section separators `# ---...---` before each logical block
- [ ] Every public function has a docstring with `Args:` and `Returns:`
- [ ] Inline sub-section comments for functions longer than ~30 lines
- [ ] Imports ordered: stdlib → third-party → local
- [ ] Entry point wrapped in `if __name__ == "__main__":` with `--transport` argument
- [ ] No commented-out dead code committed

---

*Template based on `01_mcp/server_basic/server.py` — keep this file updated as new conventions are adopted.*