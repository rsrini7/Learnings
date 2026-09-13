# RTK, Headroom, Codex, and Antigravity (agy) Integration Guide

**Date**: 2026-09-13  
**Tags**: `rtk`, `headroom`, `codex`, `agy`, `antigravity`, `pi`, `token-optimization`, `homebrew`

---

## 1. Executive Summary

This document records the end-to-end diagnosis, upgrade, and multi-agent integration for our LLM token optimization stack:
1. **RTK (Rust Token Killer)**: Upgraded from `v0.45.0` (legacy Kimchi harness link) to `v0.49.0` via Homebrew core, resolving PATH shadowing.
2. **Codex + Headroom**: Identified why `hroom wrap codex` mutates `~/.codex/config.toml` (Codex WebSocket transport ignores env vars), how plain `codex` broke when proxy was offline, and how to use `headroom unwrap codex`.
3. **Antigravity CLI (`agy`) Integration**: Connected RTK via an automated `PreToolUse` lifecycle hook (`rtk-agy-hook.py`), and connected Headroom via Model Context Protocol (MCP stdio server).
4. **Lifetime Savings**: Verified over **654 Million tokens saved** combined (8.3M via RTK command filtering, 645.8M via Headroom proxy context compression, unlocking $3,900+ in prompt cache savings).

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Tool Execution Layer (RTK)                         │
│                                                                             │
│   • Pi Agent: pi-rtk wraps bash commands before tool execution              │
│   • Antigravity CLI (agy): PreToolUse hook rewrites run_command via RTK     │
│   • Terminal Shell: direct / alias execution (rtk git, rtk rg, rtk cargo)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Filters terminal noise (34.2% savings)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Context / Proxy Layer (Headroom)                    │
│                                                                             │
│   • Pi Agent (hpi)  ──► HTTP :8787 ──► Upstream API (OpenCode / OpenRouter) │
│   • Codex CLI       ──► HTTP :8787 ──► OpenAI API                          │
│   • Claude Code     ──► HTTP :8787 ──► Anthropic API                       │
│                                                                             │
│   • agy CLI (MCP)   ──► stdio MCP  ──► Headroom CCR / Memory Tools         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. RTK Provenance & Homebrew Migration

### The Problem
Running `which rtk` pointed to `/Users/srinivasanragothaman/.local/bin/rtk`, which was a symlink to:
```
~/.local/bin/rtk -> ~/.config/kimchi/harness/rtk/rtk
```
Kimchi originally auto-downloaded RTK `0.45.0` on August 19, 2026. Because Kimchi only checks for RTK updates during interactive startup once every 24 hours (`AUTO_INSTALL_INTERVAL_MS = 86400000`), RTK remained at `0.45.0` while upstream released `v0.49.0`.

### PATH Shadowing Resolution
On macOS, your `$PATH` checks `~/.local/bin` **before** `/opt/homebrew/bin`. Simply installing via Homebrew (`brew install rtk`) would result in Homebrew being shadowed by the old symlink in `~/.local/bin`.

### The Fix
1. Installed official formula from Homebrew Core:
   ```bash
   brew install rtk
   ```
2. Re-linked both global PATH and Kimchi's harness directory directly to the Homebrew binary:
   ```bash
   ln -sf /opt/homebrew/bin/rtk ~/.local/bin/rtk
   ln -sf /opt/homebrew/bin/rtk ~/.config/kimchi/harness/rtk/rtk
   ```
3. Verified: `rtk --version` -> `rtk 0.49.0`.

### Future Upgrades
For all future releases:
```bash
brew upgrade rtk
```
Because both symlinks point to `/opt/homebrew/bin/rtk`, a single `brew upgrade` automatically updates your shell, wrappers, and Kimchi harness without collisions.

---

## 4. Codex & Headroom: Wrap vs. Unwrap Mechanics

### Why `hroom wrap codex` Permanently Edits `config.toml`
When you execute `hroom wrap codex`, Headroom performs a **durable wrap**. 

Unlike Claude Code or Pi (which can be proxied via environment variables like `OPENAI_BASE_URL`), **OpenAI Codex ignores `OPENAI_BASE_URL` for its WebSocket transport**. Headroom is forced to inject custom provider configuration into `~/.codex/config.toml`:

```toml
# --- Headroom proxy (auto-injected by headroom wrap codex) ---
model_provider = "headroom"
openai_base_url = "http://127.0.0.1:8787/v1"
# --- end Headroom ---

[model_providers.headroom]
name = "OpenAI via Headroom proxy"
base_url = "http://127.0.0.1:8787/v1"
supports_websockets = true
requires_openai_auth = true
```

### Why Plain `codex` Failed
Once `config.toml` has `model_provider = "headroom"`, running plain `codex` causes Codex to look for `http://127.0.0.1:8787/v1`. If you did not start the Headroom proxy, port 8787 is closed, and Codex immediately fails with a connection error.

### How to Restore or Switch Modes

#### Mode A: Restore Original Codex (Direct OpenAI)
Headroom saves a snapshot at `~/.codex/config.toml.headroom-backup`. Run:
```bash
zsh -c 'source ~/ws/Learnings/Scripts/hroom.sh; hroom unwrap codex'
# or: uvx --from headroom-ai==0.37.0 headroom unwrap codex
```
This restores your original `config.toml` byte-for-byte and removes the Headroom injection. Plain `codex` will connect directly to OpenAI.

#### Mode B: Permanent Headroom Proxy
To keep using Headroom with Codex without typing `hroom wrap codex` every time:
```bash
# Run standalone proxy in background
hproxy &
```
With the proxy running in the background on port `8787`, plain `codex` will always succeed.

### Why Terminal Was Closing When Exiting Codex
* **Root Cause**: In `~/.zshrc`, `hroom.sh` is sourced directly into your interactive login shell (`source ~/ws/Learnings/Scripts/hroom.sh`), making `hroom()` an in-shell function. Inside `hroom.sh`, the launch line previously used `exec uvx ...`. The `exec` command replaced your interactive shell process with `uvx`. When you exited Codex, `uvx` terminated, and because your original shell had been replaced, the terminal window closed immediately.
* **The Fix**: Removed `exec` from `~/ws/Learnings/Scripts/hroom.sh` so `uvx` runs as a child process. Exiting Codex now returns you cleanly to your zsh prompt.

---

## 5. Antigravity CLI (`agy`) Integration

### Architecture Reality
Antigravity CLI connects directly to Google DeepMind / Google Cloud backends via Google's internal **Connect-RPC / gRPC** protocol (`StreamGenerateChat`). Because `agy` does not use standard OpenAI/Anthropic REST endpoints for its agent loop, **its model stream cannot route through Headroom's HTTP proxy**.

However, `agy` can fully leverage both tools through its native extension points:

### 1. RTK via `PreToolUse` Lifecycle Hook
Antigravity executes shell commands through the `run_command` tool. We integrated RTK using Antigravity's lifecycle hooks.

* **Hook Script**: `~/ws/Learnings/Scripts/rtk-agy-hook.py`
  ```python
  #!/usr/bin/env python3
  import sys, json, subprocess, os

  def main():
      try:
          payload = json.loads(sys.stdin.read() or "{}")
          tool_call = payload.get("toolCall", {})
          if tool_call.get("name") == "run_command":
              cmd = tool_call.get("args", {}).get("CommandLine", "").strip()
              if cmd and not cmd.startswith("rtk "):
                  res = subprocess.run(["rtk", "rewrite", cmd], capture_output=True, text=True, timeout=2)
                  out = res.stdout.strip()
                  if out and out != cmd:
                      print(json.dumps({"decision": "allow", "overwrite": {"CommandLine": out}}))
                      return
      except Exception:
          pass
      print(json.dumps({"decision": "allow"}))

  if __name__ == "__main__":
      main()
  ```

* **Hook Registration**: `~/.agents/hooks.json`
  ```json
  {
    "rtk-filter": {
      "PreToolUse": [
        {
          "matcher": "run_command",
          "hooks": [
            {
              "type": "command",
              "command": "/Users/srinivasanragothaman/ws/Learnings/Scripts/rtk-agy-hook.py",
              "timeout": 5
            }
          ]
        }
      ]
    }
  }
  ```

Every time `agy` executes a shell tool call, it automatically checks `rtk rewrite`. Supported commands (`git`, `cargo`, `grep`, `npm`, `diff`) run through `rtk` transparently.

### 2. Headroom via Model Context Protocol (MCP)
Headroom exposes its retrieval and code-memory server via `headroom mcp serve`. We registered this into `agy` using the `agy mcp` CLI:

```bash
agy mcp add headroom -- uvx --from headroom-ai==0.37.0 headroom mcp serve
```

Verify with:
```bash
agy mcp list
# Output:
# NAME      TYPE   STATUS   COMMAND/URL
# headroom  stdio  enabled  uvx --from headroom-ai==0.37.0 headroom mcp serve
```

---

## 6. Token Savings & Verification

Run the unified dashboard anytime:
```bash
~/ws/Learnings/Scripts/rtk-stats.sh
```

### Measured Real-World Lifetime Impact

| Metric | Headroom Proxy | RTK Filter | Total Combined |
| :--- | :--- | :--- | :--- |
| **Tokens Saved** | **645.8 Million** | **8.3 Million** | **~654.1 Million tokens** |
| **Direct Dollars Saved** | **$211.61** | **~$5.87** | **~$217.48** |
| **Prompt Cache Savings** | **$3,916.55** | *(Enables cache hits)* | **$3,916.55** |
| **Activity Count** | 52,787 requests | 13,152 commands | — |
| **Average Reduction** | Variable (session-based) | **34.2%** | — |

---

## 7. Quick Reference Cheatsheet

| Task | Command |
| :--- | :--- |
| **Upgrade RTK** | `brew upgrade rtk` |
| **Check RTK stats** | `rtk gain` |
| **Check Headroom stats** | `hroom stats` *(or `hroom savings`)* |
| **Open Headroom web dashboard** | `hroom dashboard` |
| **Combined RTK + Headroom Dashboard** | `~/ws/Learnings/Scripts/rtk-stats.sh` |
| **Restore Codex to normal** | `zsh -c 'source ~/ws/Learnings/Scripts/hroom.sh; hroom unwrap codex'` |
| **Wrap Codex with Headroom** | `zsh -c 'source ~/ws/Learnings/Scripts/hroom.sh; hroom wrap codex'` |
| **Start background proxy** | `hproxy &` |
| **Inspect agy MCP servers** | `agy mcp list` |
| **Test agy RTK hook** | `echo '{"toolCall": {"name": "run_command", "args": {"CommandLine": "git diff"}}}' \| ~/ws/Learnings/Scripts/rtk-agy-hook.py` |
