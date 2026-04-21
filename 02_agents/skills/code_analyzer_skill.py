"""
Code Analyzer Skill
====================
Scans a project folder and returns a high-level summary of its components.

This skill walks through the directory tree, reads source files, and builds
a structured prompt that an LLM can use to produce a high-level architecture
description of the codebase.

Functions exposed:
  1. analyze_code   — Scan a folder and return an LLM-ready analysis prompt
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# File extensions considered as "source code"
SOURCE_EXTENSIONS: set[str] = {
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".go", ".rs", ".rb", ".php",
    ".c", ".cpp", ".h", ".hpp", ".cs",
    ".swift", ".kt", ".scala",
    ".html", ".css", ".scss",
    ".yaml", ".yml", ".json", ".xml", ".toml",
    ".md", ".txt",
    ".sh", ".bash", ".zsh",
}

# Directories to always skip
SKIP_DIRS: set[str] = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "env", ".env", "dist", "build", ".next", ".nuxt",
    "target", "bin", "obj", ".idea", ".vscode",
}

# Maximum characters to read per file (to avoid huge files)
MAX_FILE_CHARS: int = 3000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _collect_source_files(folder_path: str) -> list[dict]:
    """Walk *folder_path* and return a list of {path, content} dicts."""
    files: list[dict] = []
    root = Path(folder_path).resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune directories we don't care about
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for fname in sorted(filenames):
            ext = Path(fname).suffix.lower()
            if ext not in SOURCE_EXTENSIONS:
                continue

            full = Path(dirpath) / fname
            rel = full.relative_to(root)

            try:
                content = full.read_text(encoding="utf-8", errors="replace")[
                    :MAX_FILE_CHARS
                ]
            except Exception:
                content = "<<unreadable>>"

            files.append({"path": str(rel), "content": content})

    return files


def _build_file_tree(folder_path: str) -> str:
    """Return a plain-text directory tree (files only, no content)."""
    lines: list[str] = []
    root = Path(folder_path).resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        level = len(Path(dirpath).relative_to(root).parts)
        indent = "  " * level
        lines.append(f"{indent}{Path(dirpath).name}/")
        sub_indent = "  " * (level + 1)
        for fname in sorted(filenames):
            lines.append(f"{sub_indent}{fname}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main skill function
# ---------------------------------------------------------------------------
def analyze_code(folder_path: str) -> dict:
    """
    Analyze the code inside *folder_path* and return a high-level component
    summary ready to be consumed by an LLM or returned directly as a tool
    response.

    Args:
        folder_path: Absolute or relative path to the project folder to
                     analyze.

    Returns:
        A dict with keys:
            folder       — the resolved folder path
            file_tree    — a plain-text directory tree
            file_count   — number of source files found
            prompt       — the analysis prompt (with code context embedded)
            components   — placeholder list; to be filled by the LLM
    """
    folder = str(Path(folder_path).resolve())

    if not Path(folder).is_dir():
        return {"error": f"'{folder}' is not a valid directory."}

    file_tree = _build_file_tree(folder)
    source_files = _collect_source_files(folder)

    # Build the embedded code context (trimmed)
    code_context_parts: list[str] = []
    for sf in source_files:
        code_context_parts.append(
            f"--- {sf['path']} ---\n{sf['content']}\n"
        )
    code_context = "\n".join(code_context_parts)

    # -----------------------------------------------------------------
    # The analysis prompt
    # -----------------------------------------------------------------
    prompt = f"""You are a senior software architect.  Analyze the following
codebase and return a **high-level component summary**.

For each component include:
  1. **Name** — a short, descriptive name.
  2. **Type** — e.g. Module, Service, Library, Config, Script, UI Component.
  3. **Responsibility** — one or two sentences describing what it does.
  4. **Key files** — the most important files that belong to this component.
  5. **Dependencies** — other components or external libraries it depends on.

Also provide:
  - An overall **Architecture Style** label (e.g. Monolith, Microservices,
    MVC, Event-Driven, etc.).
  - A short **Summary** paragraph of the whole project.

---
## Directory tree
```
{file_tree}
```

## Source files
{code_context}
---

Return the result as structured Markdown.
"""

    return {
        "folder": folder,
        "file_tree": file_tree,
        "file_count": len(source_files),
        "prompt": prompt,
        "components": [],  # to be filled by the LLM consuming the prompt
    }