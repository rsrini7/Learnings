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

```bash
# Use hproxy function
hproxy

# Or run directly
uvx --python 3.12 --from "headroom-ai[proxy,ml,code,pytorch-mps]==0.28.0" headroom proxy --port 8780
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
| `~/ws/Learnings/DevSetup/headroom-pxoxy.md` | This doc | ✅ (this repo) |

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
