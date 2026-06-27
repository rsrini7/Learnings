# Headroom + Pi: LLM Cost Compression Setup

**Date**: 2026-06-27
**Tags**: `pi`, `headroom`, `llm`, `cost-optimization`, `shell`

---

## Problem

Pi coding agent sends raw context to LLM providers. Long sessions accumulate
tokens fast, especially with tool-heavy workflows (read, edit, bash). Token
costs add up 30-60% more than necessary.

## Solution

**Headroom** is a local context-compression proxy that sits between pi and the
LLM provider. It compresses semantic layers in the context window before
forwarding requests, reducing token usage by 30-60% without losing meaning.

```
pi  →  localhost:8787 (Headroom)  →  opencode.ai/zen/go/v1
         ↑ compresses context         

**Note**: Proxy expects `/v1` prefix, not `/openai/v1`.
```

## Architecture

```
┌─────────┐      ┌──────────────────┐      ┌─────────────────────┐
│   pi    │ ───► │  Headroom proxy  │ ───► │  opencode.ai        │
│ (local) │      │  :8787           │      │  (OpenCode Go API)  │
└─────────┘      └──────────────────┘      └─────────────────────┘
  sends raw         compresses context         receives compressed
  context           30-60% savings             tokens, same response
```

## Token Reduction Stack

Two layers work together for maximum savings:

```
Tool output  →  pi-rtk (filters 60-90%)  →  pi context  →  Headroom (compresses 30-60%)  →  LLM
                   ↑ client-side                                     ↑ proxy-side
```

| Layer | What | Where | Savings |
|-------|------|-------|--------|
| **pi-rtk** | Filters tool output (bash, read, grep) | Pi client | 60-90% |
| **Headroom** | Compresses full context window | Proxy :8787 | 30-60% |

### pi-rtk

Installed as pi package: `npm:pi-rtk`
Config: `~/.pi/agent/rtk-config.json`

Filters:
- Source code: strip comments, keep signatures
- Build output: errors/warnings only
- Test output: failures only
- Git: compact diffs
- Search: group by file
- ANSI stripping

Commands: `/rtk-stats`, `/rtk-on`, `/rtk-off`, `/rtk-what`

### Headroom

Runs as local proxy on `:8787`.

Compresses:
- Semantic context layers
- Code-aware memory
- Cache-aligned prefix optimization

Health: `curl http://localhost:8787/stats`

## What Changed

### 1. Pi Extension (`~/.pi/agent/extensions/headroom-proxy.ts`)

Overrides the `opencode-go` provider baseUrl to route through the local proxy:

```typescript
pi.registerProvider("opencode-go", {
  baseUrl: "http://localhost:8787/v1",
});
```

### 2. Shell Function (`~/ws/Learnings/Scripts/hpi.sh`)

Self-contained zsh function that:
- Starts Headroom proxy on `:8787` if not running (via `uvx`)
- Auto-detects Apple Silicon for MPS embedder offload
- Launches pi with the extension and sensible defaults
- Supports `--stop` to kill the proxy

### 3. Port Allocation

| Port | Owner | Purpose |
|------|-------|---------|
| 8787 | **hpi** (this setup) | Pi via Headroom |
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

## Usage

```bash
# Load the function
source ~/ws/Learnings/Scripts/hpi.sh

# Interactive (auto-starts proxy, defaults to opencode-go/mimo-v2.5-pro/high)
hpi

# One-shot print mode
hpi -p "explain this error: ..."

# Override model/thinking
hpi --model openrouter/claude-sonnet-4
hpi --thinking xhigh

# Kill the proxy
hpi --stop

# Normal pi (no compression)
pi
```

## Files

| File | Purpose | Git-tracked? |
|------|---------|--------------|
| `~/ws/Learnings/Scripts/hpi.sh` | Shell function source | ✅ (Learnings repo) |
| `~/ws/Learnings/DevSetup/headroom-pi-cost-saver.md` | This doc | ✅ (Learnings repo) |
| `~/.pi/agent/extensions/headroom-proxy.ts` | Pi extension | ❌ (pi config) |
| `~/.zshrc` (last 3 lines) | Sources hpi.sh | ❌ (dotfile) |

## How Headroom Works

Headroom uses **semantic compression layers**:

1. **Memory context** — builds a compressed memory of prior conversation turns
2. **Code-aware compression** — understands code structure, preserves signatures/types
3. **Net-cost cache mutation** — only compresses when the math works out:
   ```
   gain = dT * (w + r*(R - 1)) - P_alive * (w - r) * S
   ```
   Where `w`=cache write cost, `r`=cache read discount, `R`=expected reads,
   `P_alive`=cache survival probability, `S`=suffix tokens.

4. **Safety rails**:
   - Error-output passthrough (failed tool calls verbatim)
   - Pipeline circuit breaker (3 failures → passthrough for 60s)
   - Library inflation guard (reverts when compression inflates)

## Cold Start Behavior

First `hpi` invocation after reboot:
- `uvx` downloads `headroom-ai[proxy,ml,code,pytorch-mps]==0.27.0` (~30s)
- Embedder model loads into memory (~5s)
- Subsequent starts are instant (cached)

## Troubleshooting

```bash
# Check proxy health
curl -s http://localhost:8787/health | jq .

# View proxy logs
cat ~/.pi/agent/headroom.log

# Force restart
hpi --stop && hpi

# Verify extension loads
pi --extension ~/.pi/agent/extensions/headroom-proxy.ts --list-models
```

## References

- [Headroom GitHub](https://github.com/headroom-ai/headroom)
- [Pi Custom Providers](https://pi.dev/docs/custom-provider)
- Amsha project: `.mise/tasks/headroom/README.md`
