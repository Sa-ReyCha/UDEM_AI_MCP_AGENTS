"""
MCP Server — Basic
==================
Tools exposed:
  1. search_web       — Search the internet using DuckDuckGo (no API key needed)
  2. format_query     — Rewrite / format a raw search query into a clean, effective one
"""

import time
import random
import argparse

from fastmcp import FastMCP
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException, RatelimitException

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------
mcp = FastMCP(
    name="basic-search-server",
    instructions=(
        "You are a research assistant. "
        "Use `format_query` to clean and improve a raw search query, "
        "then use `search_web` to retrieve results from the internet."
    ),
)


# ---------------------------------------------------------------------------
# Tool 1 — Web search
# ---------------------------------------------------------------------------
@mcp.tool()
def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the internet using DuckDuckGo and return the top results.

    Includes automatic retry with exponential backoff to handle
    DuckDuckGo rate-limiting (which can cause empty results).

    Args:
        query:       The search query string.
        max_results: Maximum number of results to return (default 5, max 20).

    Returns:
        A list of dicts with keys: title, href, body.
    """
    max_results = min(max_results, 20)
    max_retries = 4
    base_delay  = 2.0  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            if results:          # got something — return immediately
                return results
            # empty response — treat same as rate-limit and retry
            raise RatelimitException("Empty response from DuckDuckGo")

        except RatelimitException:
            if attempt == max_retries:
                return []        # give up after all retries
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
            time.sleep(delay)

        except DuckDuckGoSearchException as exc:
            # non-retryable search error
            return [{"error": str(exc)}]

    return []


# ---------------------------------------------------------------------------
# Tool 2 — Query formatter / rewriter
# ---------------------------------------------------------------------------
@mcp.tool()
def format_query(
    raw_query: str,
    style: str = "precise",
    language: str = "en",
) -> dict:
    """
    Rewrite and format a raw, informal search query into a clean, effective one.

    Styles available:
        - "precise"   : removes filler words, keeps only key terms
        - "question"  : turns the query into a well-formed question
        - "boolean"   : adds AND / OR / NOT operators for advanced search
        - "quoted"    : wraps the main concept in quotes for exact-match search

    Args:
        raw_query: The original, unformatted query.
        style:     One of "precise", "question", "boolean", "quoted".
        language:  Target language for the reformatted query (default "en").

    Returns:
        A dict with keys:
            original  — the original query
            formatted — the reformatted query
            style     — the style applied
            tips      — a short explanation of what was changed
    """
    # ---- helpers -----------------------------------------------------------
    FILLER_WORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can",
        "to", "of", "in", "on", "at", "by", "for", "with", "about",
        "what", "how", "why", "when", "where", "who", "which",
        "i", "me", "my", "we", "our", "you", "your", "tell", "give",
        "show", "find", "me", "some", "information", "about", "explain",
        "please", "help",
    }

    tokens = raw_query.strip().split()

    def strip_fillers(tokens):
        cleaned = [t for t in tokens if t.lower() not in FILLER_WORDS]
        return cleaned if cleaned else tokens  # fallback: keep original if all removed

    # ---- style logic -------------------------------------------------------
    style = style.lower()

    if style == "precise":
        key_terms = strip_fillers(tokens)
        formatted = " ".join(key_terms)
        tips = "Removed filler/stop words, keeping only the key terms."

    elif style == "question":
        base = " ".join(strip_fillers(tokens)).capitalize()
        # avoid double question mark
        formatted = f"What is {base}?" if not raw_query.strip().endswith("?") else raw_query.strip()
        tips = "Converted to a direct question format for better Q&A retrieval."

    elif style == "boolean":
        key_terms = strip_fillers(tokens)
        if len(key_terms) >= 2:
            formatted = " AND ".join(f'"{t}"' for t in key_terms)
        else:
            formatted = f'"{" ".join(key_terms)}"'
        tips = "Wrapped key terms in quotes and joined with AND for exact-match boolean search."

    elif style == "quoted":
        key_terms = strip_fillers(tokens)
        phrase = " ".join(key_terms)
        formatted = f'"{phrase}"'
        tips = "Wrapped the entire key phrase in quotes for exact-match search."

    else:
        formatted = raw_query.strip()
        tips = f"Unknown style '{style}'. Returning the original query unchanged."

    return {
        "original": raw_query.strip(),
        "formatted": formatted,
        "style": style,
        "language": language,
        "tips": tips,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="basic-search-server MCP")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode: 'stdio' for Cline local (default) or 'http' for HTTP server + tunnel",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind when using HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on when using HTTP transport (default: 8000)",
    )
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
