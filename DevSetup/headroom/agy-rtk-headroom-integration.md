# Antigravity CLI (`agy`) & RTK + Headroom Integration Guide

**Date**: 2026-09-13  
**Tags**: `agy`, `antigravity`, `rtk`, `headroom`, `mcp`, `hooks`, `token-optimization`

---

## 1. Overview & Architecture Reality

[Antigravity CLI](file:///Users/srinivasanragothaman/.antigravity/antigravity/bin/agy) (`agy`) connects directly to Google DeepMind / Google Cloud backends using Google's internal **Connect-RPC / gRPC** protocol (`StreamGenerateChat`). 

Because `agy` does **not** make standard OpenAI- or Anthropic-compatible HTTP/REST calls:
* **`agy` cannot be wrapped by an HTTP reverse-proxy** (such as Headroom proxy on `:8780` or `:8787`).
* Running `hroom wrap agy` is architecturally impossible and unsupported.

However, `agy` provides two powerful native extension mechanisms that enable full token optimization:
1. **Lifecycle Hooks (`PreToolUse`)**: Intercepts shell tool execution (`run_command`) and rewrites commands through **RTK (Rust Token Killer)**, saving **~34% on terminal output noise**.
2. **Model Context Protocol (MCP)**: Runs Headroom as a background stdio server (`headroom mcp serve`), granting `agy` access to Headroom's semantic compression, memory, and retrieval tools.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Antigravity CLI (`agy`)                           │
│                                                                             │
│   1. Model Stream (gRPC / Connect-RPC)                                      │
│      agy ───────────────────────────► Google DeepMind Backend (Direct)      │
│                                                                             │
│   2. Shell Tool Execution (PreToolUse Hook)                                 │
│      agy: run_command ──► rtk-agy-hook.py ──► rtk rewrite ──► Clean Output  │
│                                                                             │
│   3. Memory & Compression Tools (MCP stdio)                                 │
│      agy ──────────────── stdio MCP ────────► Headroom MCP Server           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. RTK Integration via `PreToolUse` Lifecycle Hook

### Why RTK Matters for `agy`
When `agy` executes shell commands (e.g. `git diff`, `git status`, `cargo test`, `ls`, `grep`), standard terminal outputs contain massive amounts of ASCII art, duplicated headers, blank lines, and decorative padding. This output is fed directly into the model context window, consuming tens of thousands of unnecessary prompt tokens.

RTK intercepts and filters these commands transparently:
* `git status` ➔ clean, compact git status table
* `git diff` ➔ compact hunk format
* `cargo check` ➔ error summary without compiler banners
* Average savings: **34.2% token reduction**.

### The Hook Script: `rtk-agy-hook.py`

File: [`~/ws/Learnings/Scripts/headroom/rtk-agy-hook.py`](file:///Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/rtk-agy-hook.py)

`agy` supports executing external commands during tool lifecycle events. When a tool call is about to run, `agy` pipes a JSON description of the call to stdin. The hook returns a JSON decision, optionally overwriting arguments.

```python
#!/usr/bin/env python3
import json
import subprocess
import sys


def main():
  try:
    payload = json.loads(sys.stdin.read() or '{}')
    tool_call = payload.get('toolCall', {})
    if tool_call.get('name') == 'run_command':
      cmd = tool_call.get('args', {}).get('CommandLine', '').strip()
      # Avoid double-wrapping if already prefixed with rtk
      if cmd and not cmd.startswith('rtk '):
        res = subprocess.run(
            ['rtk', 'rewrite', cmd],
            capture_output=True,
            text=True,
            timeout=2,
        )
        out = res.stdout.strip()
        if out and out != cmd:
          print(
              json.dumps(
                  {'decision': 'allow', 'overwrite': {'CommandLine': out}}
              )
          )
          return
  except Exception:
    pass
  print(json.dumps({'decision': 'allow'}))


if __name__ == '__main__':
  main()
```

### Hook Registration: `~/.agents/hooks.json`

File: [`~/.agents/hooks.json`](file:///Users/srinivasanragothaman/.agents/hooks.json)

```json
{
  "rtk-filter": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/rtk-agy-hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Whenever `agy` invokes `run_command`, it checks `rtk rewrite`. If RTK has an optimized parser for the command, the command line is transparently rewritten before execution.

---

## 3. Headroom Integration via Model Context Protocol (MCP)

Headroom provides an MCP server interface that allows any MCP-compatible agent to call its context-compression and memory tools.

### The Python `[mcp]` Extra Requirement

> [!IMPORTANT]
> The `headroom-ai` Python package on PyPI does **not** bundle the MCP SDK by default. Running `headroom mcp serve` without the extra fails with:
> `ImportError: MCP SDK not installed. Install with: pip install 'headroom-ai[mcp]'`
>
> When configuring the MCP server in `agy`, always specify the `[mcp]` extra:
> `uvx --from 'headroom-ai[mcp]==0.37.0' headroom mcp serve`

### Registering Headroom MCP in `agy`

To register Headroom with `agy`:
```bash
agy mcp add headroom -- uvx --from 'headroom-ai[mcp]==0.37.0' headroom mcp serve
```

Verify registration:
```bash
agy mcp list
```
Expected output:
```text
NAME      TYPE   STATUS   COMMAND/URL
headroom  stdio  enabled  uvx --from headroom-ai[mcp]==0.37.0 headroom mcp serve
```

### Tools Exposed to `agy`:
* **`headroom_compress`**: Compresses large text snippets, stack traces, or reference documents before injecting into conversation context.
* **`headroom_retrieve`**: Queries semantic code-memory layers for relevant context snippets.
* **`headroom_stats`**: Retrieves session compression and token savings statistics.

---

## 4. The `hagy` Launcher Wrapper

To make launching `agy` frictionless with all integrations verified, [`~/ws/Learnings/Scripts/headroom/hagy.sh`](file:///Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/hagy.sh) is provided and exposed as `hagy` in `~/.zshrc`.

### What `hagy` Automates:
1. **Verifies RTK Hook**: Checks if `~/.agents/hooks.json` exists; creates and activates it if missing.
2. **Verifies Headroom MCP**: Checks `agy mcp list` for `headroom`; registers it automatically if absent.
3. **Auto-Skips Permissions**: Injects `--dangerously-skip-permissions` by default for frictionless pair programming, while preserving any user-specified overrides.
4. **Preserves Vanilla `agy`**: Plain `agy` remains 100% available without modifications.

### Script Implementation

File: [`~/ws/Learnings/Scripts/headroom/hagy.sh`](file:///Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/hagy.sh)
```bash
#!/usr/bin/env zsh
HOOKS_FILE="$HOME/.agents/hooks.json"

# 1. Verify RTK hook
if [[ ! -f "$HOOKS_FILE" ]]; then
  mkdir -p "$HOME/.agents"
  cat <<'EOF' > "$HOOKS_FILE"
{
  "rtk-filter": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/rtk-agy-hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
fi

# 2. Verify Headroom MCP
if ! agy mcp list 2>/dev/null | grep -q "headroom"; then
  echo "▶ Registering Headroom MCP in agy..." >&2
  agy mcp add headroom -- uvx --from 'headroom-ai[mcp]==0.37.0' headroom mcp serve >/dev/null 2>&1 || true
fi

# 3. Launch agy (auto-includes --dangerously-skip-permissions)
local -a args=()
local has_skip_perms=0
for arg in "$@"; do
  if [[ "$arg" == "--dangerously-skip-permissions" ]]; then
    has_skip_perms=1
  fi
  args+=("$arg")
done

if (( ! has_skip_perms )); then
  args=(--dangerously-skip-permissions "${args[@]}")
fi

echo "▶ Launching Antigravity CLI (agy) [RTK Hook + Headroom MCP]..." >&2
command agy "${args[@]}"
```

### Shell Function in `~/.zshrc`

Defined in [`~/.zshrc`](file:///Users/srinivasanragothaman/.zshrc#L116-L118):
```zsh
# hagy = agy with verified RTK hook + Headroom MCP
hagy() { ~/ws/Learnings/Scripts/headroom/hagy.sh "$@"; }
```

---

## 5. Verification & Diagnostics

### 1. Testing the RTK Hook Manually
Pipe a mock tool-use payload into the hook:
```bash
echo '{"toolCall": {"name": "run_command", "args": {"CommandLine": "git diff"}}}' | \
  python3 ~/ws/Learnings/Scripts/headroom/rtk-agy-hook.py
```
Expected response:
```json
{"decision": "allow", "overwrite": {"CommandLine": "rtk git diff"}}
```

### 2. Testing Headroom MCP
Run:
```bash
agy mcp list
```
Ensure `headroom` has `STATUS: enabled`.

### 3. Running the Full Stack Verification
Run the unified 32-point test suite:
```bash
hverify
```
Confirms hook JSON validity, hook execution, MCP server registration, and `hagy` launcher output.

---

## 6. Cheatsheet

| Action | Command |
| :--- | :--- |
| **Launch Optimized AGY** | `hagy` |
| **Launch with Custom Prompt** | `hagy "analyze performance bottlenecks"` |
| **Plain Vanilla AGY** | `agy` |
| **Inspect MCP Servers in AGY** | `agy mcp list` |
| **Re-register Headroom MCP** | `agy mcp add headroom -- uvx --from 'headroom-ai[mcp]==0.37.0' headroom mcp serve` |
| **Remove Headroom MCP** | `agy mcp remove headroom` |
| **Verify AGY Setup Health** | `hverify` |

---

## 7. Related Guides

* [**Multi-Agent Integration Master Guide**](multi-agent-rtk-headroom-integration.md) — Unified architecture, RTK v0.49.0 upgrade, lifetime token savings, and common `~/.zshrc` setup.
* [**Codex Integration Guide**](codex-headroom-integration.md) — Dedicated guide on OpenAI Codex WebSocket isolation (`hcodex`) vs wrap/unwrap.
* [**Pi Agent Integration Guide**](headroom-pi-cost-saver.md) — Dedicated guide on Pi agent extension and HTTP proxy integration.
