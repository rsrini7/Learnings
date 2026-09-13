# OpenAI Codex & Headroom Integration: `hcodex` vs. Wrap/Unwrap Deep Dive

**Date**: 2026-09-13  
**Tags**: `codex`, `headroom`, `openai`, `proxy`, `token-optimization`, `profiles`, `troubleshooting`

---

## 1. Overview & Problem Statement

When using OpenAI Codex CLI for extensive agentic coding, context tokens accumulate rapidly across long turns, file edits, and multi-file code reviews. 

[Headroom](https://github.com/headroom-ai/headroom) provides local context compression and cache-prefix alignment, cutting token consumption by 30%–60%. However, integrating Headroom with Codex introduces a architectural dilemma:

1. **How Codex Communicates**: Codex uses a persistent WebSocket connection (`wss://chatgpt.com/backend-api/...` / wire API) rather than standard one-off HTTP REST requests.
2. **Ignored Environment Variables**: Because Codex connects via WebSocket, standard HTTP proxy environment variables like `OPENAI_BASE_URL`, `HTTP_PROXY`, and `ALL_PROXY` are completely ignored.
3. **The Global Wrap Pitfall**: Headroom's built-in `headroom wrap codex` command solves this by directly mutating `~/.codex/config.toml`. While functional, this globally hijacks your Codex configuration, meaning **plain `codex` completely fails if Headroom is not running**.
4. **The Terminal Exit Crash**: When starting Codex via `hroom wrap codex`, exiting Codex previously caused the entire terminal window to close immediately due to process replacement (`exec`).

This document provides a deep dive into the mechanics of `headroom wrap codex`, `headroom unwrap codex`, and explains why we built **`hcodex`**—the zero-pollution profile isolation pattern that gives you the best of both worlds.

---

## 2. Deep Dive: `headroom wrap codex` & `headroom unwrap codex`

### Why Does Headroom Mutate Files Instead of Setting Env Vars?

For standard CLI tools (such as Pi or Curl-based apps), Headroom simply exports:
```bash
export OPENAI_BASE_URL="http://127.0.0.1:8787/v1"
```
Codex CLI, however, bypasses standard HTTP client stacks. When Codex connects to OpenAI, its internal Rust/Node engine opens a direct duplex WebSocket stream. Codex only reads custom provider URLs if they are explicitly configured in its configuration file: `~/.codex/config.toml`.

To force Codex through its proxy, Headroom implements a "durable wrap":

```
headroom wrap codex
```

### What `headroom wrap codex` Does Under the Hood
1. Scans `~/.codex/config.toml`.
2. Sets the active model provider to `headroom`:
   ```toml
   model_provider = "headroom"
   openai_base_url = "http://127.0.0.1:8787/v1"
   ```
3. Injects the provider definition at the end of `~/.codex/config.toml`:
   ```toml
   [model_providers.headroom]
   name = "OpenAI via Headroom proxy"
   base_url = "http://127.0.0.1:8787/v1"
   supports_websockets = true
   requires_openai_auth = true
   env_http_headers = { "X-Headroom-Project" = "HEADROOM_PROJECT" }
   ```

### The Pitfalls of Global Wrap

> [!WARNING] The Offline Proxy Trap
> Because `~/.codex/config.toml` was edited globally, **any subsequent invocation of `codex`** (in any terminal, tab, or background script) will attempt to connect to `http://127.0.0.1:8787`. If you haven't started Headroom, plain `codex` will crash with:
> `Connection refused: http://127.0.0.1:8787`

### Why Did Exiting Codex Close the Entire Terminal?

A common frustration when running `hroom wrap codex` from shell functions was the abrupt closing of the user's terminal window upon quitting Codex.

* **Unix Process Architecture**:
  In Unix shells, when you run a program normally (`codex`), the shell forks a child process and waits for it. When `codex` exits, control returns to the parent shell.
* **The Root Cause**:
  In `~/.zshrc`, `hroom.sh` was sourced directly into the login shell:
  ```zsh
  source ~/ws/Learnings/Scripts/headroom/hroom.sh
  ```
  Inside `hroom.sh`, the tool launch was written as:
  ```bash
  exec uvx ... headroom "$@"   # ❌ BUG: replaces current shell process!
  ```
  The `exec` system call replaces the currently executing process with the new process. Because `hroom.sh` was sourced into your active terminal shell, `exec uvx` **replaced your terminal's login zsh shell**!
* **The Outcome**:
  When you finished your Codex session and pressed `Ctrl+C` or typed `/exit`, `uvx` terminated. Because the original shell process had been destroyed, the terminal emulator (iTerm2 / Terminal.app) detected that its child process had exited, and immediately closed the tab or window.
* **The Fix**:
  In [`~/ws/Learnings/Scripts/headroom/hroom.sh`](file:///Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/hroom.sh), we removed `exec` so that `uvx` runs as a standard child process:
  ```bash
  uvx --python "$python_ver" --from "$package_spec" headroom "$@"  # ✅ Safe child process
  ```

### How `headroom unwrap codex` Works

When you want to restore Codex to its vanilla state, you run:
```bash
headroom unwrap codex
# or via wrapper:
hroom unwrap codex
```

What it does:
1. Opens `~/.codex/config.toml`.
2. Removes `model_provider = "headroom"` and `openai_base_url = "http://127.0.0.1:8787/v1"`.
3. Removes the `[model_providers.headroom]` table.
4. Restores your default provider (e.g., direct OpenAI ChatGPT authentication).

Verify that your config is clean with:
```bash
codex doctor
```
Under **Connectivity**, it should show:
```text
✓ websocket    connected (HTTP 101 Switching Protocols)
      endpoint wss://chatgpt.com/backend-api/...
```

---

## 3. The Recommended Solution: Profile-Isolated `hcodex`

Constantly wrapping and unwrapping is error-prone. If you forget to unwrap and the proxy dies, plain `codex` breaks.

To solve this permanently, we built **`hcodex`**, leveraging Codex's built-in, non-destructive **profile layering mechanism**.

### Architectural Comparison

```
Global Wrap Pattern (headroom wrap):
┌─────────────────────────┐
│   ~/.codex/config.toml  │ ◄── Permanently modified with 127.0.0.1:8787
└────────────┬────────────┘
             │
     ┌───────┴───────┐
     ▼               ▼
   codex           hroom codex
 (CRASHES if     (Works, but pollutes global state)
  proxy down)

────────────────────────────────────────────────────────────────────────────────

Profile Isolation Pattern (hcodex):
┌─────────────────────────┐         ┌────────────────────────────────┐
│   ~/.codex/config.toml  │         │ ~/.codex/headroom.config.toml  │
│  (100% CLEAN / VANILLA) │         │ (Layered only when requested)  │
└────────────┬────────────┘         └───────────────┬────────────────┘
             │                                      │
             ▼                                      ▼
           codex                                 hcodex
  (Direct to OpenAI API)            (Uses --profile headroom via :8787)
```

### 1. Isolated Profile Configuration: `~/.codex/headroom.config.toml`

Codex supports passing `--profile <name>`. When this flag is passed, Codex automatically loads `~/.codex/<name>.config.toml` and merges it on top of `~/.codex/config.toml` in-memory, without altering `config.toml` on disk.

File: [`~/.codex/headroom.config.toml`](file:///Users/srinivasanragothaman/.codex/headroom.config.toml)
```toml
# Headroom profile for Codex (layered on top of ~/.codex/config.toml)
model_provider = "headroom"
openai_base_url = "http://127.0.0.1:8787/v1"

[model_providers.headroom]
name = "OpenAI via Headroom proxy"
base_url = "http://127.0.0.1:8787/v1"
supports_websockets = true
requires_openai_auth = true
env_http_headers = { "X-Headroom-Project" = "HEADROOM_PROJECT" }

[mcp_servers.headroom]
command = "uvx"
args = ["--from", "headroom-ai[mcp]==0.37.0", "headroom", "mcp", "serve"]
```

### 2. The `hcodex` Launcher Script

File: [`~/ws/Learnings/Scripts/headroom/hcodex.sh`](file:///Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/hcodex.sh)

The script handles the complete lifecycle:
1. **Health Check & Auto-Start**: Pings `http://127.0.0.1:8787/health`. If the proxy is not running, it automatically starts the Headroom proxy in the background and waits for it to become healthy.
2. **Config Verification**: Ensures `~/.codex/headroom.config.toml` exists.
3. **Execution**: Invokes `codex --profile headroom "$@"`, forwarding all flags, subcommands, and session inputs.
4. **Zero Process Replacement**: Runs as a standard subshell—never kills your terminal session on exit.

```bash
#!/usr/bin/env zsh
source "${0:A:h}/headroom-env.sh"
PROXY_PORT=8787

# 1. Start proxy if offline
if ! curl -s --max-time 1 "http://127.0.0.1:${PROXY_PORT}/health" >/dev/null 2>&1; then
  echo "▶ Starting Headroom proxy on :${PROXY_PORT}..." >&2
  local extras=$(hroom_resolve_extras)
  uvx --python 3.12 \
    --from "headroom-ai[${extras}]==${HROOM_VERSION}" \
    headroom proxy --port "$PROXY_PORT" >/dev/null 2>&1 &
  
  for _ in {1..20}; do
    if curl -s --max-time 1 "http://127.0.0.1:${PROXY_PORT}/health" >/dev/null 2>&1; then
      break
    fi
    sleep 0.2
  done
fi

# 2. Launch with isolated headroom profile
echo "▶ Launching Codex via Headroom profile (:8787)..." >&2
codex --profile headroom "$@"
```

### 3. Shell Function in `~/.zshrc`

Defined in [`~/.zshrc`](file:///Users/srinivasanragothaman/.zshrc#L113-L115):
```zsh
# hcodex = codex through Headroom proxy (:8787) without touching default config.toml
hcodex() { ~/ws/Learnings/Scripts/headroom/hcodex.sh "$@"; }
```

---

## 4. Side-by-Side Comparison

| Feature | `headroom wrap codex` | `hcodex` (Recommended) | Plain `codex` |
| :--- | :--- | :--- | :--- |
| **Config Target** | Mutates `~/.codex/config.toml` | Isolated `~/.codex/headroom.config.toml` | Reads `~/.codex/config.toml` |
| **Default `codex` Behavior** | Hijacked to local proxy | 100% vanilla (direct to OpenAI) | 100% vanilla |
| **Proxy Down Behavior** | ❌ Hard crash (connection refused) | ✅ Auto-starts proxy seamlessly | ✅ Unaffected (bypasses proxy) |
| **Terminal Exit** | Fixed (previously killed terminal) | ✅ 100% safe (child process) | ✅ Safe |
| **Unwrap Maintenance** | Requires `headroom unwrap codex` | ❌ Zero maintenance needed | Not applicable |
| **WebSocket Compression** | ✅ Yes | ✅ Yes | ❌ No (raw tokens) |
| **Token Savings** | 30%–60% | 30%–60% | 0% |

---

## 5. Everyday Operational Cheatsheet

### 1. Daily Usage

```bash
# Want token compression & cache optimization? Use hcodex:
hcodex "refactor the payment module"

# Want vanilla, direct-to-OpenAI Codex without proxy? Use plain codex:
codex "quick question about rust error"
```

### 2. Checking Proxy Health & Savings

```bash
# Check if Headroom proxy is active on port 8787
curl -s http://127.0.0.1:8787/health | jq .

# Check lifetime token savings across Codex and Pi
~/ws/Learnings/Scripts/headroom/rtk-stats.sh

# Open Headroom live web dashboard
hroom dashboard
```

### 3. Health & Sanity Verification

Run the automated verification suite anytime:
```bash
hverify
```
Checks:
- `~/.codex/config.toml` is clean.
- `~/.codex/headroom.config.toml` exists and targets port 8787.
- `codex doctor` reports zero connectivity issues.

### 4. Emergency Recovery: If You Accidentally Ran `headroom wrap codex`

If someone ran `headroom wrap codex` manually and plain `codex` starts failing:
```bash
# Step 1: Unwrap codex
hroom unwrap codex

# Step 2: Verify config.toml is clean
codex doctor

# Step 3: Run full verification
hverify
```

---

## 6. Summary

* **`headroom wrap codex`** is Headroom's built-in mechanism that forces Codex to route through its proxy by editing `~/.codex/config.toml`. It is a global change that can break plain `codex` when the proxy is offline.
* **`headroom unwrap codex`** cleans up `~/.codex/config.toml` and restores vanilla direct routing.
* **`hcodex`** uses Codex's native `--profile headroom` flag and `~/.codex/headroom.config.toml`. It auto-starts the proxy, provides full token compression, leaves default `codex` completely untouched, and never closes your terminal window on exit.

---

## 7. Related Guides

* [**Multi-Agent Integration Master Guide**](multi-agent-rtk-headroom-integration.md) — Unified architecture, RTK v0.49.0 upgrade, lifetime token savings, and common `~/.zshrc` setup.
* [**Antigravity CLI (agy) Integration Guide**](agy-rtk-headroom-integration.md) — Dedicated guide on Google Antigravity CLI (`agy`), Connect-RPC, PreToolUse RTK hooks, and Headroom MCP integration.
* [**Pi Agent Integration Guide**](headroom-pi-cost-saver.md) — Dedicated guide on Pi agent extension and HTTP proxy integration.
