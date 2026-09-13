# Multi-Agent Token Optimization Guide: RTK & Headroom across Pi, Codex, and AGY

**Date**: 2026-09-13  
**Tags**: `rtk`, `headroom`, `codex`, `agy`, `antigravity`, `pi`, `multi-agent`, `token-optimization`, `architecture`

---

## 1. Executive Summary

This master document records the unified token-optimization architecture and operational setup across our three primary coding agents: **Pi Agent**, **OpenAI Codex**, and **Google Antigravity CLI (`agy`)**.

By pairing **RTK (Rust Token Killer)** at the terminal/tool-execution layer with **Headroom** at the context/memory layer, we achieve massive, compounding token savings without compromising accuracy or speed:
1. **RTK Core Upgrade**: Migrated from legacy Kimchi harness (`v0.45.0`) to canonical Homebrew (`v0.49.0`), fixing PATH shadowing.
2. **Dedicated Agent Integrations**: Each agent connects to the stack using the pattern dictated by its native transport protocol:
   * **Pi Agent**: Local HTTP Reverse Proxy (`:8787`) + Agent Extension.
   * **OpenAI Codex**: Duplex WebSocket + Profile Layering (`--profile headroom` / `hcodex`).
   * **Antigravity CLI (`agy`)**: Connect-RPC + `PreToolUse` Lifecycle Hook + Model Context Protocol (MCP).
3. **Automated Verification**: Unified 32-point test suite (`hverify`) validating syntax, permissions, configs, and hooks.
4. **Lifetime Savings**: Over **654.1 Million tokens saved** combined ($217+ direct API savings, $3,916+ prompt cache savings).

---

## 2. Multi-Agent Architecture Overview

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
│   • Pi Agent (hpi)      ──► HTTP :8787 ──► Upstream API (OpenCode/OpenRouter│
│   • Codex CLI (hcodex)  ──► HTTP :8787 ──► OpenAI Duplex WebSocket         │
│   • Claude Code         ──► HTTP :8787 ──► Anthropic API                    │
│                                                                             │
│   • agy CLI (hagy)      ──► stdio MCP  ──► Headroom CCR / Memory Tools      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Agent Integration Matrix

Each agent has unique protocol requirements and is documented in its own dedicated deep-dive guide:

| Agent | Transport Protocol | Headroom Integration | RTK Integration | Launcher | Dedicated Deep Dive Guide |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pi Agent** | HTTP / REST | Local Proxy `:8787` (`headroom-proxy.ts`) | Bash tool filter (`pi-rtk`) | `hpi` | [**`headroom-pi-cost-saver.md`**](headroom-pi-cost-saver.md) |
| **OpenAI Codex** | WebSocket Duplex | Layered Profile (`headroom.config.toml`) | Native CLI tool execution | `hcodex` | [**`codex-headroom-integration.md`**](codex-headroom-integration.md) |
| **Antigravity (`agy`)** | Connect-RPC / gRPC | stdio MCP (`headroom mcp serve`) | `PreToolUse` Hook (`rtk-agy-hook.py`)| `hagy` | [**`agy-rtk-headroom-integration.md`**](agy-rtk-headroom-integration.md) |

---

## 4. RTK Core Foundation & Homebrew Migration

### The Provenance Issue
Before this integration, running `which rtk` pointed to `~/.local/bin/rtk`, which was a symlink to:
```bash
~/.local/bin/rtk -> ~/.config/kimchi/harness/rtk/rtk
```
Kimchi originally auto-downloaded RTK `0.45.0` on August 19, 2026. Because Kimchi only checks for updates during interactive startup once every 24 hours (`AUTO_INSTALL_INTERVAL_MS = 86400000`), RTK remained at `0.45.0` while upstream released `v0.49.0`.

### PATH Shadowing Resolution
On macOS, your `$PATH` checks `~/.local/bin` **before** `/opt/homebrew/bin`. Simply running `brew install rtk` resulted in Homebrew's binary being shadowed by the older Kimchi symlink.

### The Migration:
1. **Installed Official Formula**:
   ```bash
   brew install rtk
   ```
2. **Re-linked Canonical Paths**:
   ```bash
   ln -sf /opt/homebrew/bin/rtk ~/.local/bin/rtk
   ln -sf /opt/homebrew/bin/rtk ~/.config/kimchi/harness/rtk/rtk
   ```
3. **Verified**: `rtk --version` ➔ `rtk 0.49.0`.
4. **Future Upgrades**: Run `brew upgrade rtk`. Because both paths point to Homebrew, updates apply everywhere simultaneously.

---

## 5. Agent Highlights & Dedicated Guides

### 1. Pi Agent (HTTP Proxy Pattern)
* **How it works**: Pi uses an extension (`headroom-proxy.ts`) to route all outbound LLM completions through the local Headroom proxy daemon on port `8787`.
* **Zero Pollution**: Plain `pi` runs vanilla; `hpi` runs through Headroom.
* 📖 **Full Deep Dive**: [**`headroom-pi-cost-saver.md`**](headroom-pi-cost-saver.md)

### 2. OpenAI Codex (Profile Isolation Pattern)
* **How it works**: Codex communicates via WebSockets and ignores HTTP proxy env vars. Instead of mutating `~/.codex/config.toml` (which breaks vanilla Codex when the proxy is offline), we use Codex's native `--profile headroom` flag pointing to `~/.codex/headroom.config.toml`.
* **Zero Terminal Killing**: Removed `exec` from `hroom.sh` so exiting Codex never closes the terminal window.
* **Zero Pollution**: Plain `codex` is 100% untouched and direct to OpenAI; `hcodex` runs through Headroom.
* 📖 **Full Deep Dive**: [**`codex-headroom-integration.md`**](codex-headroom-integration.md)

### 3. Antigravity CLI (`agy`) (Hook + MCP Pattern)
* **How it works**: `agy` connects via Connect-RPC/gRPC directly to Google backends, so reverse HTTP proxies cannot intercept model streams.
* **Dual Integration**:
  1. **RTK**: Automated `PreToolUse` lifecycle hook in `~/.agents/hooks.json` rewrites `run_command` calls via `rtk rewrite`.
  2. **Headroom**: Registered as an MCP stdio server (`headroom-ai[mcp]==0.37.0`), providing memory and compression tools.
* **Zero Pollution**: Plain `agy` remains standard; `hagy` launches with verified hooks and auto-skip permissions.
* 📖 **Full Deep Dive**: [**`agy-rtk-headroom-integration.md`**](agy-rtk-headroom-integration.md)

---

## 6. Centralized Shell Integration (`~/.zshrc`)

All tool integrations are centralized in [`~/.zshrc`](file:///Users/srinivasanragothaman/.zshrc#L89-L121):

```zsh
# ── Headroom + RTK Multi-Agent Integrations (Pi, Codex, AGY) ────────────────
# hpi     = pi through Headroom compression proxy (:8787)
# hroom   = Headroom CLI wrapper (proxy, learn, savings, serve, ...)
# hlrn    = headroom learn with --verbosity --apply
# hproxy  = headroom proxy on :8780 (standalone)
# hproxyt = hproxy shortcut targeting commandcode.ai upstream
# hcodex  = Codex through Headroom proxy (:8787) with isolated profile (plain codex untouched)
# hagy    = Antigravity CLI (agy) with verified RTK hook + Headroom MCP
# hverify = Run health check & verification suite for all multi-agent integrations
# pi/codex/agy = plain default execution (no proxy / vanilla behavior)
# Shared config: ~/ws/Learnings/Scripts/headroom/headroom-env.sh
# Docs:          ~/ws/Learnings/DevSetup/headroom/multi-agent-rtk-headroom-integration.md (Master Guide)
#                ~/ws/Learnings/DevSetup/headroom/agy-rtk-headroom-integration.md
#                ~/ws/Learnings/DevSetup/headroom/codex-headroom-integration.md
#                ~/ws/Learnings/DevSetup/headroom/headroom-pi-cost-saver.md
export HEADROOM_CODE_AWARE_ENABLED=1
export HEADROOM_OUTPUT_SHAPER=1

source ~/ws/Learnings/Scripts/headroom/hpi.sh
source ~/ws/Learnings/Scripts/headroom/hroom.sh    # defines hroom() function

# hlrn = headroom learn with --verbosity --apply
hlrn() { ~/ws/Learnings/Scripts/headroom/hlrn.sh "$@"; }

# hproxy = headroom proxy --port 8780 (standalone)
hproxy() { ~/ws/Learnings/Scripts/headroom/hproxy.sh "$@"; }

# hproxyt = hproxy shortcut to commandcode.ai upstream
hproxyt() { hproxy --target https://api.commandcode.ai/provider/v1 }

# hcodex = codex through Headroom proxy (:8787) without touching default config.toml
hcodex() { ~/ws/Learnings/Scripts/headroom/hcodex.sh "$@"; }

# hagy = agy with verified RTK hook + Headroom MCP
hagy() { ~/ws/Learnings/Scripts/headroom/hagy.sh "$@"; }

# hverify = verify all RTK, Headroom, Codex, AGY integrations
hverify() { ~/ws/Learnings/Scripts/headroom/verify-setup.sh "$@"; }
```

### Key Design Tenets
1. **Zero Pollution / Vanilla Fallback**: Plain `codex`, `pi`, and `agy` run direct to providers without interception or mandatory proxies. The `h*` prefixed commands (`hpi`, `hcodex`, `hagy`) activate the optimized paths.
2. **No Terminal Killing**: `hroom.sh` and child wrappers run functions without `exec`, preserving the interactive terminal shell when tools exit.
3. **Lazy Execution**: Heavy Python environments are resolved lazily via `uvx` with pin-consistent extra tags (`headroom-ai[mcp]==0.37.0`).

---

## 7. Unified Verification Suite (`hverify`)

To ensure that future dotfile edits, Homebrew upgrades, or package updates never break the integrations, an automated test suite is provided:
* **Script**: [`~/ws/Learnings/Scripts/headroom/verify-setup.sh`](file:///Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/verify-setup.sh)
* **Command**: `hverify`

```text
═══ 1. Shell Configuration & ~/.zshrc ═══
  ✓ PASS  ~/.zshrc syntax is valid
  ✓ PASS  HEADROOM_CODE_AWARE_ENABLED=1 is exported in ~/.zshrc
  ✓ PASS  HEADROOM_OUTPUT_SHAPER=1 is exported in ~/.zshrc
  ✓ PASS  Function 'hpi' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hroom' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hlrn' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hproxy' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hproxyt' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hcodex' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hagy' is properly defined in ~/.zshrc
  ✓ PASS  Function 'hverify' is properly defined in ~/.zshrc

═══ 2. Scripts & File Permissions ═══
  ✓ PASS  hpi.sh exists and is executable
  ✓ PASS  hroom.sh exists and is executable
  ✓ PASS  hlrn.sh exists and is executable
  ✓ PASS  hproxy.sh exists and is executable
  ✓ PASS  hcodex.sh exists and is executable
  ✓ PASS  hagy.sh exists and is executable
  ✓ PASS  verify-setup.sh exists and is executable
  ✓ PASS  rtk-agy-hook.py exists and is executable
  ✓ PASS  rtk-stats.sh exists and is executable
  ✓ PASS  headroom-env.sh exists and is executable

═══ 3. RTK (Rust Token Killer) Integrity ═══
  ✓ PASS  RTK version is current: 0.49.0 (/Users/srinivasanragothaman/.local/bin/rtk)
  ✓ PASS  Homebrew rtk (0.49.0) matches active rtk (0.49.0)
  ✓ PASS  RTK rewrite engine works ('git status' -> 'rtk git status')

═══ 4. Codex Profile Isolation ═══
  ✓ PASS  Default ~/.codex/config.toml is clean (plain 'codex' routes direct to OpenAI)
  ✓ PASS  Isolated ~/.codex/headroom.config.toml exists and routes to :8787
  ✓ PASS  hcodex launcher successfully executes (codex-cli detected)

═══ 5. Antigravity CLI (agy) Hooks & MCP ═══
  ✓ PASS  ~/.agents/hooks.json is valid JSON with 'rtk-filter' registered
  ✓ PASS  rtk-agy-hook.py correctly rewrote 'git diff' to 'rtk git diff'
  ✓ PASS  Headroom MCP server is registered in agy
  ✓ PASS  hagy launcher successfully executes

═══ 6. Unified Dashboard Health ═══
  ✓ PASS  Unified rtk-stats.sh dashboard runs successfully

══════════════════════════════════════════════════════════════
Verification Summary:
  Passed:   32 | Warnings: 0 | Failures: 0
══════════════════════════════════════════════════════════════
✓ All core integrations and shell configurations are healthy!
```

---

## 8. Lifetime Token Savings & Metrics

Run the unified dashboard anytime:
```bash
~/ws/Learnings/Scripts/headroom/rtk-stats.sh
```

### Measured Real-World Lifetime Impact

| Metric | Headroom Proxy | RTK Filter | Total Combined |
| :--- | :--- | :--- | :--- |
| **Tokens Saved** | **645.8 Million** | **8.3 Million** | **~654.1 Million tokens** |
| **Direct Dollars Saved** | **$211.61** | **~$5.87** | **~$217.48** |
| **Prompt Cache Savings** | **$3,916.55** | *(Enables cache hits)* | **$3,916.55** |
| **Activity Count** | 52,787 requests | 13,169 commands | — |
| **Average Reduction** | Variable (session-based) | **34.2%** | — |

---

## 9. Master Quick Reference Cheatsheet

| Category | Task | Command | Description |
| :--- | :--- | :--- | :--- |
| **Diagnostics** | **Verify All 3 Integrations** | `hverify` | Runs 32 automated unit/health tests across the setup |
| | **Combined Savings Dashboard** | `~/ws/Learnings/Scripts/headroom/rtk-stats.sh` | RTK command stats + Headroom proxy token savings |
| | **RTK SQLite Stats** | `rtk gain` | Direct RTK SQLite database stats |
| | **Headroom Savings Summary** | `hroom stats` *(or `hroom savings`)*| Proxy compression and cache statistics |
| | **Headroom Web Dashboard** | `hroom dashboard` | Web UI for live request compression trees |
| **Codex** | **Codex via Headroom** | `hcodex` | Isolated profile on `:8787` (config.toml untouched) |
| | **Codex Plain (Default)** | `codex` | Direct to OpenAI via official WebSocket transport |
| | **Codex Health Check** | `codex doctor` | Validates clean config and WebSocket transport |
| | **Codex Emergency Unwrap** | `hroom unwrap codex` | Restores config.toml if accidentally wrapped |
| **Antigravity (`agy`)** | **Antigravity CLI (Optimized)** | `hagy` | RTK hook + Headroom MCP + auto-skip permissions |
| | **Antigravity CLI (Plain)** | `agy` | Standard CLI invocation |
| | **Inspect agy MCP Servers** | `agy mcp list` | Lists registered MCP tools in agy |
| | **Test agy RTK Hook** | `echo '{"toolCall": {"name": "run_command", "args": {"CommandLine": "git diff"}}}' \| python3 ~/ws/Learnings/Scripts/headroom/rtk-agy-hook.py` | Manual hook test |
| **Pi Agent** | **Pi Agent via Headroom** | `hpi` | Runs Pi agent through local Headroom proxy :8787 |
| | **Pi Agent Plain** | `pi` | Standard Pi invocation without proxy |
| **Proxies & Core** | **Start Standalone Proxy** | `hproxy &` | Headroom compression proxy on port :8780 |
| | **Upgrade RTK** | `brew upgrade rtk` | Upgrades Homebrew canonical binary |

---

## 10. Dedicated Architecture & Setup Guides

* 📖 [**`codex-headroom-integration.md`**](codex-headroom-integration.md) — Deep dive on OpenAI Codex WebSocket duplex transport, `hcodex` profile isolation, and `headroom wrap/unwrap` mechanics.
* 📖 [**`agy-rtk-headroom-integration.md`**](agy-rtk-headroom-integration.md) — Deep dive on Google Antigravity CLI (`agy`), Connect-RPC, PreToolUse RTK hooks, and Headroom MCP integration.
* 📖 [**`headroom-pi-cost-saver.md`**](headroom-pi-cost-saver.md) — Deep dive on Pi Agent context compression, `headroom-proxy.ts` extension, and token cost benchmarks.
* 📖 [**`headroom-proxy.md`**](headroom-proxy.md) — Standalone Headroom proxy usage for arbitrary OpenAI-compatible clients.
