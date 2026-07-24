# Headroom + Pi: LLM Cost Compression Setup

**Date**: 2026-06-27  
**Updated**: 2026-07-09 (shared config, hroom, hproxy)  
**Tags**: `pi`, `headroom`, `rtk`, `llm`, `cost-optimization`, `shell`

---

## Problem

Pi coding agent sends raw context to LLM providers. Long sessions accumulate
tokens fast, especially with tool-heavy workflows (read, edit, bash). Token
costs add up 30-60% more than necessary.

## Solution

**Headroom** is a local context-compression proxy that sits between pi and the
LLM provider. **pi-rtk** wraps commands with the external RTK binary for
client-side filtering. Together they reduce token usage by 60-90%.

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
Tool output  →  pi-rtk (wraps with rtk binary)  →  pi context  →  Headroom (compresses 30-60%)  →  LLM
                   ↑ client-side                                                ↑ proxy-side
```

| Layer | What | Where | Savings |
|-------|------|-------|---------|
| **pi-rtk** | Wraps bash commands with `rtk` binary | Pi client | 60-90% |
| **pi-headroom** | Routes through proxy + CCR retrieval | Pi client | 30-60% |
| **Headroom** | Compresses full context window | Proxy :8787 | 30-60% |

## Pi Packages

### pi-rtk

**Repo**: [github.com/rsrini7/pi-rtk](https://github.com/rsrini7/pi-rtk)  
**Install**: `pi install git:rsrini7/pi-rtk`

Token reduction by wrapping commands with external RTK binary.

Features:
- **External RTK wrapping** — Wraps bash commands with `rtk` binary (headroom tracks savings)
- **In-process fallback** — If no rtk binary, filters output in JavaScript
- Source code filtering (strip comments, keep signatures)
- Build output: errors/warnings only
- Test output: failures only
- Git: compact diffs
- Search: group by file
- ANSI stripping

Config: `~/.pi/agent/rtk-config.json`  
Commands: `/rtk-stats`, `/rtk-on`, `/rtk-off`, `/rtk-what`

### pi-headroom

**Repo**: [github.com/rsrini7/pi-headroom](https://github.com/rsrini7/pi-headroom)  
**Install**: `pi install git:rsrini7/pi-headroom`

Headroom proxy extension with CCR retrieval support.

Features:
- **Proxy routing** — Redirects `opencode-go` through Headroom proxy
- **headroom_retrieve tool** — Registers tool for CCR (Cache-Compress-Retrieve)
- **Auto-detection** — Checks if proxy is running, falls back gracefully
- **Configurable** — Port, host via config file

Config: `~/.pi/agent/headroom-config.json`

### Headroom Proxy

Runs as local proxy on `:8787`.

Compresses:
- Semantic context layers
- Code-aware memory
- Cache-aligned prefix optimization
- CCR (Cache-Compress-Retrieve) for reversible compression

Health: `curl http://localhost:8787/health`

## Quick Start

```bash
# 1. Install packages
pi install git:rsrini7/pi-rtk
pi install git:rsrini7/pi-headroom

# 2. Start Headroom proxy (or use hpi function)
hpi

# 3. Use pi with both extensions
pi -e ~/ws/pi-rtk -e ~/ws/pi-headroom
```

## Shared Config

**File**: `~/ws/Learnings/Scripts/headroom-env.sh`

Single source of truth for version and extras. All wrapper scripts source this.

```bash
HROOM_VERSION="0.30.0"       # ← bump this one line to update all scripts
HROOM_BASE_EXTRAS="proxy,ml,code"
hroom_resolve_extras()        # auto-appends pytorch-mps on Apple Silicon
```

Scripts that source it: `hpi.sh`, `hroom.sh`, `hproxy.sh`, `hlrn.sh`.

## Shell Functions

### hpi — Pi through Headroom

**File**: `~/ws/Learnings/Scripts/hpi.sh`

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

# Skip RTK extension (headroom only)
hpi --no-rtk

# Kill the proxy
hpi --stop

# Normal pi (no compression)
pi
```

**Key env vars set by hpi:**
| Variable | Value | Purpose |
|----------|-------|---------|
| `HEADROOM_OUTPUT_SHAPER` | `1` | Enable output shaping |
| `HEADROOM_VERBOSITY_LEVEL` | `2` | Moderate verbosity |
| `HEADROOM_VERBOSITY_AUTOTUNE` | `1` | Auto-tune verbosity |
| `HEADROOM_OUTPUT_HOLDOUT` | `0.1` | Hold back 10% of output for retrieval |
| `HEADROOM_EMBEDDER_RUNTIME` | `pytorch_mps` | Apple Silicon MPS embedder (arm64 only) |

**Note:** `pi` is launched with `-ne` flag (non-interactive edit mode).

### hroom — Generic Headroom Wrapper

**File**: `~/ws/Learnings/Scripts/hroom.sh`

Generic wrapper for any headroom subcommand. Sources `headroom-env.sh` for
version/extras. Can be run directly or sourced to define `hroom()` function.

```bash
# Direct execution
~/ws/Learnings/Scripts/hroom.sh proxy
~/ws/Learnings/Scripts/hroom.sh proxy --port 8780
~/ws/Learnings/Scripts/hroom.sh learn --apply --verbosity
~/ws/Learnings/Scripts/hroom.sh run "echo hello"

# Override version/extras on the fly
~/ws/Learnings/Scripts/hroom.sh --version 0.27.0 proxy
~/ws/Learnings/Scripts/hroom.sh --extras proxy,ml proxy
~/ws/Learnings/Scripts/hroom.sh --no-mps proxy     # skip MPS detection
```

### hproxy — Headroom Proxy (standalone)

**File**: `~/ws/Learnings/Scripts/hproxy.sh`

Start headroom proxy on port 8780 (default). Sources `headroom-env.sh`.

```bash
hproxy                                      # start on :8780
hproxy --target https://api.example.com     # custom upstream
hproxyt                                     # shortcut: commandcode.ai upstream
```

### hlrn — Headroom Learn

**File**: `~/ws/Learnings/Scripts/hlrn.sh`

Runs `headroom learn` to train/compress the context model.

```bash
hlrn                                        # run with defaults
hlrn --extra-flag value                     # pass-through args
```

Equivalent to:
```bash
uvx --python 3.12 \
  --from 'headroom-ai[proxy,ml,code,pytorch-mps]==0.30.0' \
  headroom learn --verbosity --apply
```

Version/extras come from `headroom-env.sh`. Auto-detects Apple Silicon for `pytorch-mps`.

## Port Allocation

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

## Important: Proxy URL Prefix

The proxy expects `/v1` prefix, **not** `/openai/v1`. This is set via `OPENAI_TARGET_API_URL`.

## How RTK Integration Works

### External RTK Binary (default)

When the external `rtk` binary is found in PATH:

1. **`tool_call`** — pi-rtk wraps bash commands with `rtk` before execution
2. **RTK binary** — Filters output, tracks lifetime stats
3. **`rtk gain`** — Headroom reads stats via `rtk gain --format json`

This is the **recommended** mode — headroom dashboard shows RTK savings.

### In-Process Fallback

If no external `rtk` binary:

1. **`tool_result`** — pi-rtk filters output after execution
2. Metrics saved to `~/.pi/agent/rtk-metrics.json`
3. Headroom cannot see these savings

## How Headroom CCR Works

CCR (Cache-Compress-Retrieve) makes compression reversible:

1. **Compress** — Headroom compresses tool outputs, stores originals with hash
2. **Inject** — Adds `headroom_retrieve` tool to LLM tools array
3. **Retrieve** — LLM calls `headroom_retrieve(hash, query)` to get original

**pi-headroom** registers this tool so pi can handle the calls.

## Files

| File | Purpose | Git-tracked? |
|------|---------|--------------|
| `~/ws/pi-rtk/` | pi-rtk package | ✅ [rsrini7/pi-rtk](https://github.com/rsrini7/pi-rtk) |
| `~/ws/pi-headroom/` | pi-headroom package | ✅ [rsrini7/pi-headroom](https://github.com/rsrini7/pi-headroom) |
| `~/ws/Learnings/Scripts/headroom-env.sh` | Shared version/extras config | ✅ (this repo) |
| `~/ws/Learnings/Scripts/hpi.sh` | Shell function (hpi) | ✅ (this repo) |
| `~/ws/Learnings/Scripts/hroom.sh` | Shell function (hroom) | ✅ (this repo) |
| `~/ws/Learnings/Scripts/hproxy.sh` | Shell function (hproxy) | ✅ (this repo) |
| `~/ws/Learnings/Scripts/hlrn.sh` | Shell function (hlrn) | ✅ (this repo) |
| `~/ws/Learnings/DevSetup/headroom-pi-cost-saver.md` | This doc | ✅ (this repo) |
| `~/.pi/agent/extensions/headroom-proxy.ts` | Installed extension | ❌ (pi config) |
| `~/.pi/agent/rtk-config.json` | RTK config | ❌ (pi config) |
| `~/.pi/agent/headroom-config.json` | Headroom config | ❌ (pi config) |
| `~/.zshrc` (headroom block) | Sources hpi.sh, defines hroom/hproxy/hlrn | ❌ (dotfile) |

## Troubleshooting

```bash
# Check proxy health
curl -s http://localhost:8787/health | jq .

# View proxy stats (including RTK savings)
curl -s http://localhost:8787/stats | jq .summary

# View proxy logs
cat ~/.pi/agent/headroom.log

# Check RTK binary stats
rtk gain --format json

# Force restart
hpi --stop && hpi

# Verify extension loads
pi --extension ~/ws/pi-headroom --list-models
```

## References

- [Headroom GitHub](https://github.com/headroom-ai/headroom)
- [RTK GitHub](https://github.com/rtk-ai/rtk)
- [pi-rtk](https://github.com/rsrini7/pi-rtk)
- [pi-headroom](https://github.com/rsrini7/pi-headroom)
- Amsha project: `.mise/tasks/headroom/README.md`

**Related:**
- [GenAI-cost-Optimization](../AI-ML/LLMs/optimization/GenAI-cost-Optimization.md) — Proxy-layer token reduction complements GenAI cost strategies like caching, routing, and quantization.
- [headroom-proxy](headroom-proxy.md) — Generic standalone headroom proxy variant (port 8780) for any OpenAI-compatible app beyond pi.
