# SDD Spec: Stock Price MCP Server (Live Demo)

> **Methodology:** Specification Driven Development (SDD)  
> **Target directory:** `04_live_demo/`  
> **Files to create:** `server.py`, `skills/yfinance_skill.py`

---

## 1. Specification First

### 1.1 Overview

Build a **standalone MCP server** inside `04_live_demo/` that exposes a single tool: **`get_stock_price`**.  
The tool accepts a company ticker symbol and returns the latest stock market price.

The server must support **HTTP Streamable** transport so it can be tested with the MCP Inspector or connected to Cline via `streamableHttp`.

### 1.2 Requirements

| ID | Requirement |
|----|-------------|
| R1 | Create `04_live_demo/server.py` — a FastMCP server with HTTP transport (port `8002`) |
| R2 | Create `04_live_demo/skills/yfinance_skill.py` — skill module with `get_stock_price(ticker)` |
| R3 | The tool accepts a **stock ticker symbol** (e.g. `AAPL`, `MSFT`, `TSLA`) as input |
| R4 | The tool returns the **latest price**, company name, ticker, and currency |
| R5 | Use the `yfinance` Python library (no API key required) |
| R6 | Handle invalid/empty tickers gracefully with a clear error message |
| R7 | Add `yfinance` to `00_setup/requirements.txt` if not already present |

### 1.3 Acceptance Criteria

```
Given: a valid stock ticker "AAPL"
When:  the user calls get_stock_price(ticker="AAPL")
Then:  the response is a dict containing:
       - ticker: "AAPL"
       - name: "Apple Inc."
       - price: <current price as float>
       - currency: "USD"
```

```
Given: an invalid stock ticker "XYZNOTREAL123"
When:  the user calls get_stock_price(ticker="XYZNOTREAL123")
Then:  the response is a dict containing:
       - error: "Could not find data for ticker 'XYZNOTREAL123'."
```

```
Given: an empty ticker ""
When:  the user calls get_stock_price(ticker="")
Then:  the response is a dict containing:
       - error: "Ticker symbol is required."
```

### 1.4 Expected Behavior

**Input:**
```json
{
  "ticker": "AAPL"
}
```

**Output:**
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "price": 198.52,
  "currency": "USD"
}
```

### 1.5 Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Empty ticker `""` | Return `{"error": "Ticker symbol is required."}` |
| Ticker with spaces `" AAPL "` | Strip whitespace and process normally |
| Lowercase ticker `"aapl"` | Convert to uppercase and process normally |
| Delisted/invalid ticker | Return `{"error": "Could not find data for ticker '...'."}` |
| Yahoo Finance unreachable | Return `{"error": "Failed to fetch data: <exception message>"}` |

---

## 2. AI-Assisted Implementation

### 2.1 Files to Create

| File | Action | Description |
|------|--------|-------------|
| `04_live_demo/skills/yfinance_skill.py` | **Create** | Skill module with `get_stock_price(ticker: str) -> dict` |
| `04_live_demo/server.py` | **Create** | FastMCP server that imports the skill and registers the tool |
| `00_setup/requirements.txt` | **Modify** | Add `yfinance` if not present |

### 2.2 Skill Implementation Spec (`skills/yfinance_skill.py`)

```python
def get_stock_price(ticker: str) -> dict:
    """
    Fetch the latest stock price for a ticker from Yahoo Finance.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL", "MSFT").

    Returns:
        A dict with keys: ticker, name, price, currency.
        On error, a dict with an "error" key.
    """
```

**Implementation steps:**
1. Validate input (non-empty, strip whitespace, uppercase).
2. Use `yfinance.Ticker(ticker)` to get the stock object.
3. Read `.info` dict — try `currentPrice`, then `regularMarketPrice`, then `previousClose`.
4. Read `longName` or `shortName` for the company name.
5. Return the four fields. On any failure, return `{"error": "..."}`.

### 2.3 Server Implementation Spec (`server.py`)

```python
from fastmcp import FastMCP
from skills.yfinance_skill import get_stock_price as _get_stock_price

mcp = FastMCP("stock-price-server")

@mcp.tool()
def get_stock_price(ticker: str) -> dict:
    """Fetch the latest stock price for a company ticker."""
    return _get_stock_price(ticker)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["stdio", "http"], default="http")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8002)
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
```

### 2.4 Field Mapping

| Our Field | Yahoo Finance `.info` Key |
|-----------|--------------------------|
| `ticker` | (input, uppercased) |
| `name` | `longName` or `shortName` |
| `price` | `currentPrice` → `regularMarketPrice` → `previousClose` |
| `currency` | `currency` |

---

## 3. Validation & Verification

### 3.1 How to Run

```bash
# 1. Install dependencies
pip install -r 00_setup/requirements.txt

# 2. Start the server (HTTP mode — default)
python 04_live_demo/server.py

# Server will listen on http://localhost:8002/mcp
```

### 3.2 Test with MCP Inspector

```bash
# Option A — STDIO mode
npx @modelcontextprotocol/inspector python3 04_live_demo/server.py --transport stdio

# Option B — HTTP mode (two terminals)
# Terminal 1:
python3 04_live_demo/server.py
# Terminal 2:
npx @modelcontextprotocol/inspector
# In browser: Transport Type = "Streamable HTTP", URL = http://localhost:8002/mcp
```

### 3.3 Connect to Cline

```json
{
  "mcpServers": {
    "stock-price-server": {
      "disabled": false,
      "timeout": 60,
      "type": "streamableHttp",
      "url": "http://localhost:8002/mcp"
    }
  }
}
```

### 3.4 Checklist

- [ ] `yfinance` added to `00_setup/requirements.txt`
- [ ] `04_live_demo/skills/yfinance_skill.py` created with `get_stock_price()`
- [ ] `04_live_demo/server.py` created with FastMCP + HTTP transport
- [ ] Valid ticker returns `ticker`, `name`, `price`, `currency`
- [ ] Invalid ticker returns `{"error": "..."}`
- [ ] Empty ticker returns `{"error": "Ticker symbol is required."}`
- [ ] Lowercase/whitespace tickers are normalized
- [ ] Server starts without errors on port 8002
- [ ] MCP Inspector can connect and call the tool

---

## 4. Summary

This spec defines a **standalone Stock Price MCP server** that:
- Lives in `04_live_demo/` (independent from `01_mcp/` and `02_agents/`)
- Exposes a single tool: `get_stock_price(ticker)` → latest price
- Uses `yfinance` (pip installable, no API key needed)
- Runs with **HTTP Streamable** transport on port `8002`
- Handles edge cases: empty input, invalid tickers, network errors, case normalization

> **Next step:** Switch to ACT mode and ask the AI agent to implement this spec, or hand this `instructions.md` to Cline with the Developer Agent system prompt.