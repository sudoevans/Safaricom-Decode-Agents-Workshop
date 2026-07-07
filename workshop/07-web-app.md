# 07 - Deploy the Chat Web App

## 1) Overview

The `webapp/` folder contains a standalone Flask chat interface for Biashara Agent. It connects to **Microsoft Foundry** (Microsoft Foundry or Foundry Local) for the LLM and reads the same JSON data files as the MCP server directly — **you do not need the MCP server running for this step**. The idea here is to see your agent in action.

```
Browser → Flask (webapp/app.py) → Microsoft Foundry / Foundry Local
                ↓
        mcp-server/data/*.json (menu + FAQs)
```

## 2) Configure your LLM backend

The web app supports two backends — choose the one that works for you:

### Option A — Microsoft Foundry (cloud)

Use your Microsoft Foundry project endpoint and API key.

In a new terminal, ensuring you are in the virtual environment you created, set your credentials:

```bash
export AZURE_AI_ENDPOINT="https://<your-project>.services.ai.azure.com"
export AZURE_AI_KEY="your-api-key"
```

> **Tip:** You can also create a `webapp/.env` file with these variables — the app loads `.env` files automatically.

### Option B — Foundry Local (no API key needed)

Foundry Local runs models on your machine — no cloud credentials required.

1. Install Foundry Local if you haven't already (see [Foundry Local docs](https://learn.microsoft.com/ai/foundry-local/get-started)).
2. Start the local server and set the environment variable:

```bash
foundry local start
export USE_FOUNDRY_LOCAL=true
```

> The default model for Foundry Local is `phi-4`. You can override it with `export MODEL="your-model-name"`.

## 3) Start the web app

```bash
python webapp/app.py
```

You should see:

```
🍽️  Biashara Agent Web App starting...
   Backend: Microsoft Foundry
   Model: gpt-4.1-mini
   Endpoint: https://<your-project>.services.ai.azure.com
   Open http://127.0.0.1:5000 in your browser
```

Or if using Foundry Local:

```
🍽️  Biashara Agent Web App starting...
   Backend: Foundry Local
   Model: phi-4
   Endpoint: http://localhost:5272/v1
   Open http://127.0.0.1:5000 in your browser
```

## 4) Chat with Biashara Agent

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Try these questions:

```text
I'm in a rush — what's a quick and affordable breakfast option?
```

```text
Niko Kilimani. Mnatuma huku na ni free delivery?
```

```text
We have a meeting tomorrow with 20 people — can you handle that on short notice?
```

## 5) How it works

| Component | Description |
|-----------|-------------|
| `webapp/app.py` | Flask backend with the system prompt, tool definitions, and an agentic tool-calling loop |
| `webapp/templates/index.html` | Chat UI with a green/purple Savanna Bites theme |
| `mcp-server/data/*.json` | Shared data files (menu + FAQs) — same as the MCP server |
| Microsoft Foundry / Foundry Local | LLM inference via the OpenAI-compatible endpoint |

The app mirrors the two MCP tools (`search_business_faqs`, `get_product_catalogue`) as OpenAI function-calling tools. When the model decides it needs data, Flask executes the tool locally and feeds the result back — up to 5 rounds per message.

## 6) Configuration

You can customise the app with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_AI_ENDPOINT` | *(required for cloud)* | Your Microsoft Foundry project endpoint |
| `AZURE_AI_KEY` | *(required for cloud)* | Your Microsoft Foundry API key |
| `USE_FOUNDRY_LOCAL` | `false` | Set to `true` to use Foundry Local instead |
| `MODEL` | `gpt-4.1-mini` (cloud) / `phi-4` (local) | Model name to use |
| `ENDPOINT` | `http://localhost:5272/v1` | Override the Foundry Local endpoint (only used when `USE_FOUNDRY_LOCAL=true`) |

Continue to [08-export-code.md](08-export-code.md).