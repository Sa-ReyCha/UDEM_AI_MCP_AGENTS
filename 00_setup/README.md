# 00 — Setup

Everything you need to get your environment ready before the workshop.

---

## 1. Install Python Dependencies

```bash
pip install -r 00_setup/requirements.txt
```

> Run this from the **repository root**. If you are already inside the `00_setup/` folder, use `pip install -r requirements.txt` instead.

---

## 2. Install MCP Inspector (Optional)

The **MCP Inspector** is a browser-based UI that lets you test and debug MCP servers without Cline. It requires **Node.js** (v18+).

```bash
# No install needed — just run with npx (downloads on first use)
npx @modelcontextprotocol/inspector
```

> If you don't have Node.js installed, download it from [nodejs.org](https://nodejs.org/) or install via Homebrew:
> ```bash
> brew install node
> ```

You can also point the Inspector directly at a server:

```bash
npx @modelcontextprotocol/inspector python3 01_mcp/server.py
```

This opens a browser UI (usually at `http://localhost:6274`) where you can browse tools, call them manually, and inspect JSON requests/responses in real time.

---

## 3. Get Your API Key

You need an API key from **OpenAI** or **Anthropic (Claude)** — pick the one you prefer.

| Provider  | Guide                                      | Key format          |
|-----------|--------------------------------------------|---------------------|
| OpenAI    | [openai_api_key_guide.md](openai_api_key_guide.md)       | `sk-proj-...`       |
| Anthropic | [anthropic_api_key_guide.md](anthropic_api_key_guide.md) | `sk-ant-api03-...`  |

> 💡 **No API key?** You can also use a **ChatGPT Plus** or **Claude Pro** subscription directly inside Cline — no API key required (see step 4).

---

## 4. Configure the Key in Cline

Open VS Code → Cline extension → **Settings (gear icon)**:

1. Under **API Provider**, select `OpenAI` or `Anthropic`
2. Paste your API key in the **API Key** field
3. Choose your model (e.g., `gpt-4o` or `claude-sonnet-4-6`)
4. Click **Save**

**Using a subscription instead of an API key:**
- **ChatGPT Plus** → select provider `OpenAI` → choose `Use ChatGPT` login option
- **Claude Pro** → select provider `Anthropic` → choose `Use Claude.ai` login option

---

## Files in This Folder

| File | Description |
|------|-------------|
| `requirements.txt` | Python dependencies for the project |
| `openai_api_key_guide.md` | Step-by-step guide to get an OpenAI API key |
| `anthropic_api_key_guide.md` | Step-by-step guide to get an Anthropic API key |
