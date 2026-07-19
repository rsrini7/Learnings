# Headroom Proxy: Standalone Context Compression Proxy

**Date**: 2026-07-02  
**Tags**: `headroom`, `proxy`, `llm`, `cost-optimization`, `shell`

---

## Problem

LLM applications send raw context to LLM providers, which can accumulate tokens fast, leading to higher costs.

## Solution

**Headroom** is a local context-compression proxy that compresses context before sending it to LLM providers, reducing token usage.

```
LLM App  →  localhost:8780 (Headroom)  →  Any OpenAI-compatible API
           ↑ compresses context
```

## Architecture

```
┌──────────┐      ┌──────────────────┐      ┌─────────────────────┐
│ LLM App  │ ───► │  Headroom proxy  │ ───► │  OpenAI-compatible  │
│ (any)    │      │  :8780           │      │  API endpoint       │
└──────────┘      └──────────────────┘      └─────────────────────┘
  sends raw         compresses context         receives compressed
  context           token savings             tokens, same response
```

## Headroom Proxy

Runs as local proxy on `:8780`.

Compresses:
- Semantic context layers
- Code-aware memory
- Cache-aligned prefix optimization

Health: `curl http://localhost:8780/health`

## Quick Start

### Basic usage
```bash
# Use hproxy function
hproxy

# Or run directly
uvx --python 3.12 --from "headroom-ai[proxy,ml,code,pytorch-mps]==0.28.0" headroom proxy --port 8780
```

### Using with CommandCode API
```bash
# 1. Set your API key
export OPENAI_API_KEY="<CMD_API_KEY>"

# 2. Start the proxy with target URL
hproxy --target https://api.commandcode.ai/provider/v1

# 3. Set base URLs to point to the local proxy
export OPENAI_BASE_URL="http://127.0.0.1:8780/v1"
export COMMANDCODE_BASE_URL="http://127.0.0.1:8780/v1"

# 4. Now use your Command Code client as usual—it will route through the proxy!

# Or test directly with curl
curl http://localhost:8780/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek/deepseek-v4-flash",
    "messages": [{"role": "user", "content": "Write a haiku about race conditions."}]
  }'
```

## Shell Functions

### hproxy — Headroom Proxy

**File**: `~/ws/Learnings/Scripts/hproxy.sh`

```bash
# Make executable
chmod +x ~/ws/Learnings/Scripts/hproxy.sh

# Run directly
~/ws/Learnings/Scripts/hproxy.sh

# Or add to PATH
export PATH="$HOME/ws/Learnings/Scripts:$PATH"
hproxy

# Pass extra flags
hproxy --extra-flag value
```

Equivalent to:
```bash
uvx --python 3.12 \
  --from 'headroom-ai[proxy,ml,code,pytorch-mps]==0.28.0' \
  headroom proxy --port 8780
```

Auto-detects Apple Silicon and adds `pytorch-mps` extra.

## Port Allocation

| Port | Owner | Purpose |
|------|-------|---------|
| 8780 | **hproxy** (this setup) | Standalone Headroom proxy |
| 8787 | hpi | Pi via Headroom |
| 8788 | Amsha | OpenRouter proxy |
| 8789 | Amsha | Groq proxy |
| 8790 | Amsha | NVIDIA proxy |
| 8791 | Amsha | Cerebras proxy |
| 8792 | Amsha | Gemini proxy |
| 8793 | Amsha | OpenAI proxy |
| 8794 | Amsha | Ollama proxy |
| 8795 | Amsha | OmniMLX proxy |
| 8796 | Amsha | Generic OpenAI proxy |
| 8797 | Amsha | llama.cpp proxy |

## Files

| File | Purpose | Git-tracked? |
|------|---------|--------------|
| `~/ws/Learnings/Scripts/hproxy.sh` | Shell function (hproxy) | ✅ (this repo) |
| `~/ws/Learnings/DevSetup/headroom-proxy.md` | This doc | ✅ (this repo) |

## Troubleshooting

```bash
# Check proxy health
curl -s http://localhost:8780/health | jq .

# View proxy stats
curl -s http://localhost:8780/stats | jq .summary

# Force restart (kill process on port 8780 and restart)
lsof -ti :8780 | xargs kill -9 2>/dev/null; hproxy
```

## References

- [Headroom GitHub](https://github.com/headroom-ai/headroom)

**Related:**- [GenAI-cost-Optimization](../AI-ML/LLMs/optimization/GenAI-cost-Optimization.md) — Standalone compression proxy is one implementation pattern within the broader GenAI cost-optimization toolkit.- [AI-Coding-Loops](../AI-ML/Agents/development/AI-Coding-Loops.md) — The same proxy architecture underpins coding-agent loops; this doc covers the generic app use case.- [MacMini-Setup](MacMini-Setup.md) — Proxy runs locally on a dev machine — install the shell/runtime prerequisites from the Mac Mini setup first.
