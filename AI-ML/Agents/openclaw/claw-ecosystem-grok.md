# AI Agent Ecosystem: Technical Analysis & Security Reference

## OpenClaw, NanoBot, NanoClaw, ZeroClaw, IronClaw, PicoClaw

---

## Table of Contents

1. [Ecosystem Origin & Context](#1-ecosystem-origin--context)
2. [Ecosystem Map & Project Inventory](#2-ecosystem-map--project-inventory)
3. [Project Deep Dives](#3-project-deep-dives)
   - 3.1 [OpenClaw — High-Risk Architecture Profile](#31-openclaw)
   - 3.2 [NanoBot — Research-Grade Minimal Agent](#32-nanobot)
   - 3.3 [NanoClaw — Container-Isolated Agent](#33-nanoclaw)
   - 3.4 [ZeroClaw — Performance-First Rust Agent](#34-zeroclaw)
   - 3.5 [IronClaw — Capability-Isolated WASM Agent](#35-ironclaw)
   - 3.6 [PicoClaw — Edge-Hardware Go Agent](#36-picoclaw)
   - 3.7 [SafeClaw & ThePopeBot — Early-Stage Projects](#37-safeclaw--thepopebot)
4. [Threat Model](#4-threat-model)
5. [Security Analysis](#5-security-analysis)
   - 5.1 [CVE-2026-25253: Architectural Implications](#51-cve-2026-25253)
   - 5.2 [ClawHub Supply Chain Risk](#52-clawhub-supply-chain-risk)
   - 5.3 Additional CVEs (Feb 2–4, 2026)
   - 5.4 [Security Model Comparison Matrix](#54-security-model-comparison-matrix)
   - 5.5 [Enterprise & Compliance Considerations](#55-enterprise--compliance-considerations)
   - 5.6 [Security Best Practices](#56-security-best-practices)
6. [Architecture Diagrams](#6-architecture-diagrams)
7. [Performance Benchmarks](#7-performance-benchmarks)
8. [Architectural Tradeoff Summary](#8-architectural-tradeoff-summary)
9. [Decision Framework](#9-decision-framework)
10. [Cost Analysis](#10-cost-analysis)
11. [Migration Paths](#11-migration-paths)
    - 11.5 [Limitations of This Analysis](#115-limitations-of-this-analysis)
    - 11.6 [Isolation Boundary Hierarchy](#116-isolation-boundary-hierarchy)
12. [Conclusion](#12-conclusion)
13. [References](#13-references)

---

## 1. Ecosystem Origin & Context

The entire "Claw" ecosystem emerged from a single open-source project that achieved rapid adoption in November 2025, then faced significant security scrutiny in early 2026.

**Peter Steinberger** (founder of PSPDFKit) built a personal project connecting messaging applications to Claude Code. He published it as **Clawdbot**. It accumulated over 100,000 GitHub stars within weeks, with community-reported traffic peaks of approximately 2 million weekly website visitors. Secondary market effects — including reported hardware demand spikes for Mac Mini M4 units — were widely discussed in developer communities but are anecdotal and not independently verified.

### Naming Timeline

| Date | Name | Reason for Change |
|------|------|-------------------|
| Nov 2025 | **Clawdbot** | Original name — "Clawd" + "bot" |
| Jan 27, 2026 | **Moltbot** | Anthropic trademark request; "Clawd" too similar to "Claude" |
| Jan 29–30, 2026 | **OpenClaw** | Final rename with secured domains and trademarks |

The rename created a brief window that malicious actors exploited. A fake `$CLAWD` token on Solana reached a reported ~$16M market cap before collapsing. A typosquatted VS Code extension "ClawdBot Agent" was published carrying malware. Censys independently reported **21,639 publicly exposed OpenClaw instances** as of January 31, 2026.

These events — combined with CVE-2026-25253 disclosures in early February — created the direct conditions for the alternative ecosystem described in this document.

---

## 2. Ecosystem Map & Project Inventory

### Verified GitHub Statistics (Feb 16, 2026)

> All star counts are approximate point-in-time observations. This ecosystem is growing rapidly; treat these as directional indicators, not precise measurements.

| Project | Repository | Stars (approx.) | Language | Core Philosophy | Creator / Maintainer |
|---------|------------|-----------------|----------|-----------------|----------------------|
| **OpenClaw** | `openclaw/openclaw` | ~170–185k | TypeScript / Node.js | Feature-complete, community-driven | Peter Steinberger |
| **NanoBot** | `HKUDS/nanobot` | ~19k | Python | Research-ready, ultra-lightweight | HKU Data Intelligence Lab |
| **NanoClaw** | `gavrielc/nanoclaw` / `qwibitai/nanoclaw` | ~5–8k | TypeScript / Node.js | Container-first, minimal codebase | Gavriel Cohen (Qwibit) |
| **PicoClaw** | `sipeed/picoclaw` | ~11k | Go | Edge hardware, ultra-efficient | Sipeed |
| **ZeroClaw** | `theonlyhennygod/zeroclaw` | ~3.6–4.2k | Rust | Performance-first, binary distribution | Independent |
| **IronClaw** | `nearai/ironclaw` | ~1.5k | Rust | Capability-based WASM isolation | Illia Polosukhin (NEAR AI) |
| **SafeClaw** | `princezuda/safeclaw` | ~43 | Python | Rule-based, no LLM | Independent |
| **ThePopeBot** | `stephengpope/thepopebot` | ~172 | Node.js | GitOps-based autonomous agent | Stephen G. Pope |

> **Note on SafeClaw and ThePopeBot:** Both projects have insufficient activity and documentation to assess architectural risk or maturity. They are summarized briefly in Section 3.7 and excluded from the detailed analysis sections.

### Architecture Philosophy Spectrum

```
← MINIMAL CODE / MAXIMUM ISOLATION          MAXIMUM FEATURES / BROADER ATTACK SURFACE →

NanoClaw ──── NanoBot ──── PicoClaw ──── ZeroClaw ──── IronClaw ──────────── OpenClaw
  500 LOC      4k LOC       ~8MB binary   3.4MB binary   10-15k LOC Rust      430k LOC
  Container    Process      Workspace      Process +       WASM capability     Shared
  per group    isolated     sandbox        encrypted       grants per tool     memory
                                          secrets
```

This spectrum is not a quality ranking. Each position represents a deliberate design philosophy optimized for a specific deployment context and threat model.

---

## 3. Project Deep Dives

---

### 3.1 OpenClaw

**Profile: High-Risk Architecture — Broadest Feature Set in the Ecosystem**

OpenClaw is the "batteries-included" AI agent platform that created this ecosystem. It connects to 15+ messaging platforms, offers 3,000+ community skills via its ClawHub registry, and runs as a persistent daemon on the host machine.

**Core Facts:**
- **Codebase:** ~430,000 lines of TypeScript/Node.js across 52+ modules
- **Channels:** WhatsApp, Telegram, Discord, Slack, Signal, iMessage, and 10+ more
- **Skill Registry:** ClawHub — 3,000+ community-contributed skills
- **Configuration:** 8+ configuration files
- **Process Model:** Single Node.js process, shared memory across all channels and tools
- **Security Model:** Application-level — allowlists, pairing codes, approval prompts
- **License:** MIT

**Distinguishing Characteristics:** The persistent daemon model allows OpenClaw to proactively monitor and act across a user's digital environment — morning briefings, calendar management, email handling, and complex multi-step workflows — all accessible through existing chat apps. It has the largest community, most documentation, and most ready-to-use skills of any project in this ecosystem.

**Architectural Risk:** All channels share a single Node.js process and memory space. Application-level security controls (allowlists, approvals) are enforced by the same runtime that can be compromised. This means a single exploited entry point — a malicious skill, a crafted message, a stolen token — grants access to all credentials, the filesystem, and the shell. See Section 5 for documented exploits.

```mermaid
graph TD
    subgraph "Input Channels [Attack Surface]"
        WA[WhatsApp]
        TG[Telegram]
        DC[Discord]
        SL[Slack]
        UI["Control UI\n(WebSocket — CVE-2026-25253 entry)"]
    end

    WA --> GW[Gateway Process]
    TG --> GW
    DC --> GW
    SL --> GW
    UI --> GW

    subgraph "Agent Runtime"
        GW --> AE[Agent Engine]
        AE --> SS[Skill System]
        SS --> CH["ClawHub Registry\n3,000+ Skills\n[Supply Chain Risk]"]
        AE --> ID[Identities File]
    end

    subgraph "Shared Execution — Single Node.js Process [Primary Risk]"
        AE --> SM["Shared Memory\n[All data co-located]"]
        SM --> SH[Shell Access]
        SM --> FS[File System]
        SM --> CR["Credentials / API Keys\n[Plaintext accessible]"]
        SM --> AP[API Calls]
    end

    subgraph "Security Controls — Application Level Only"
        AL[Allowlists]
        PC[Pairing Codes]
        EP[Exec Approvals]
        AE --- AL
        AE --- PC
        AE --- EP
    end

    style SM fill:#ffe0e0,stroke:#cc0000
    style CH fill:#ffe0e0,stroke:#cc0000
    style UI fill:#fff3cd,stroke:#cc8800

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999
    L1["🔴 Red = Critical attack surface\n🟡 Yellow = Known exploit entry point\n→ Arrow = Data/control flow"]:::legend
```

**Setup:**
```bash
# Node.js 22+ required
npm install -g openclaw@latest
openclaw onboard --install-daemon

# Recommended hardening (do before connecting any channels)
openclaw doctor             # Security audit — resolve all findings first
# VPS deployments: use openclaw-ansible
# Includes: Tailscale VPN, UFW firewall, Docker sandbox for tool execution
```

---

### 3.2 NanoBot

**Profile: Research-Grade Minimal Agent — Transparent, Multi-Channel, Python**

NanoBot was built by the **HKU Data Intelligence Lab** (HKUDS) at the University of Hong Kong as an explicit response to OpenClaw's complexity. Its design goal: retain 95% of core agent capability in 1% of the code, with a codebase any developer can read in one sitting.

**Core Facts:**
- **Codebase:** ~3,536–4,000 lines of Python (actively maintained; LOC varies per commit)
- **Latest Release:** v0.1.3.post7 (Feb 13, 2026)
- **Launch:** February 2, 2026
- **Channels:** Telegram, Discord, WhatsApp, Feishu, Mochat, DingTalk, Slack, Email (IMAP/SMTP), QQ
- **LLM Providers:** OpenRouter, Groq, DeepSeek, vLLM (local), Minimax, Anthropic, Gemini, Moonshot/Kimi, Qwen
- **Memory:** `MEMORY.md` (long-term) + daily notes (`memory/YYYY-MM-DD.md`)
- **Scheduling:** APScheduler-based cron jobs
- **Subagents:** Built-in subagent spawning for parallel tasks
- **License:** MIT

**Distinguishing Characteristics:** Every design decision is made in the open and documented. Adding a new LLM provider takes two steps. The skills folder contains all capabilities. Configuration is a single JSON file. A developer can audit the entire codebase before trusting it with credentials — a property OpenClaw cannot offer.

**Security Posture:** Smaller attack surface than OpenClaw (99% less code), but not architecturally isolated. Tools execute in the same Python process. A compromised model response or a malicious skill could still access the host. This is a meaningful improvement in auditability, not in runtime containment.

```mermaid
graph TD
    subgraph "Channel Layer"
        TG[Telegram] & DC[Discord] & WA[WhatsApp] & FS[Feishu] & SL[Slack] & EM["Email\nIMAP/SMTP"] & QQ["QQ / DingTalk"] & CR["Cron\nAPScheduler"]
    end

    subgraph "Message Bus"
        BUS[Internal Message Bus]
    end

    TG & DC & WA & FS & SL & EM & QQ & CR --> BUS

    subgraph "Agent Core — Single Python Process"
        BUS --> AL[Agent Loop]
        AL --> CB[Context Builder]
        AL --> MM[Memory Manager]
        AL --> SK[Skills Loader]
        AL --> SA[Subagent Spawner]
    end

    subgraph "Tool Execution — Same Process"
        AL --> WS["Web Search\nBrave API"]
        AL --> CE["Code Execution\nSandboxed Shell"]
        AL --> FO["File Operations\nWorkspace"]
    end

    subgraph "LLM Providers"
        AL --> OR[OpenRouter]
        AL --> DS[DeepSeek]
        AL --> VL["vLLM\nLocal"]
        AL --> AN[Anthropic]
        AL --> OT["Groq / Qwen\nMoonshot / Gemini"]
    end

    subgraph "Persistent Storage"
        CB --> CFG[config.json]
        MM --> MEM["MEMORY.md\n+ Daily Notes"]
        SA --> SS[Session State]
    end

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999
    L1["→ Data flow\n⚠ Tools share process memory with agent"]:::legend
```

**Setup:**
```bash
# Install (uv recommended for speed)
uv tool install nanobot-ai
# OR: pip install nanobot-ai
# OR: git clone https://github.com/HKUDS/nanobot.git && pip install -e .

# Configure (interactive wizard)
nanobot onboard
# Generates ~/.nanobot/config.json

# Minimal config example
cat > ~/.nanobot/config.json << 'EOF'
{
  "providers": {
    "openrouter": { "apiKey": "sk-or-v1-xxx" }
  },
  "agents": {
    "defaults": { "model": "anthropic/claude-opus-4-5" }
  }
}
EOF

# Chat
nanobot agent -m "Summarize my emails from the last 24 hours"

# Cron scheduling
nanobot cron add --name "morning-brief" \
  --message "Give me a morning briefing" \
  --cron "0 9 * * *"
nanobot cron list
```

---

### 3.3 NanoClaw

**Profile: Container-Isolated Agent — OS-Level Security Boundary per Chat Group**

NanoClaw was built by **Gavriel Cohen** (Qwibit AI) around one architectural principle: security guarantees must be enforced at the OS level, not the application level. The codebase is ~500 lines of TypeScript. It runs the Anthropic Agent SDK natively.

**Two Active Repositories:**
- `gavrielc/nanoclaw` — original public repo by Gavriel Cohen
- `qwibitai/nanoclaw` — Qwibit company fork, actively maintained and used in production

**Core Facts:**
- **Codebase:** ~500 lines TypeScript (host process) + Claude Agent SDK
- **Primary Channel:** WhatsApp (via Baileys); Telegram and Gmail addable via Claude Code skills
- **Container Runtime:** Apple Container (macOS Tahoe 26+) or Docker (Linux)
- **State Storage:** SQLite (task queue + scheduling) + `CLAUDE.md` per group (agent memory)
- **Installation Interface:** Claude Code (`claude` → `/setup`)
- **Extensibility:** SKILL.md files that teach Claude Code how to transform the fork
- **License:** MIT

**Distinguishing Characteristics:** Each WhatsApp group gets its own Linux container with an isolated filesystem and a separate mounted working directory. A compromised agent in Group A's container cannot read Group B's files, and cannot access the host filesystem outside explicitly mounted directories. This guarantee is enforced by the OS hypervisor, not by application code — it cannot be bypassed via API calls, unlike OpenClaw's application-level controls.

The project is also AI-native in its development model: there is no traditional installation wizard. Claude Code is the interface for setup, debugging, and extension. Feature additions are submitted as SKILL.md files, not pull requests against shared application code.

**Real-World Deployment:** The Cohen brothers use NanoClaw internally at Qwibit for their sales pipeline: daily briefings, WhatsApp note parsing to Obsidian, follow-up scheduling, and git history reviews.

```mermaid
sequenceDiagram
    participant U as User (WhatsApp Group)
    participant H as Host Process (Node.js ~500 LOC)
    participant DB as SQLite Queue
    participant CM as Container Manager
    participant K as OS Hypervisor (Apple Container / Docker)
    participant C as Agent Container (per group)
    participant SDK as Claude Agent SDK
    participant MF as Mounted Filesystem (group-scoped)

    U->>H: Message arrives via Baileys (WhatsApp)
    H->>DB: Enqueue message with group identifier
    H->>DB: Poll — dequeue next message
    DB-->>H: Message dispatched

    H->>CM: Route to this group's container
    CM->>K: Validate against mount allowlist
    K-->>CM: Boundary check passed

    K->>C: Spawn / resume container for this group
    C->>SDK: Invoke Claude Agent SDK with CLAUDE.md context
    SDK->>MF: Read / write within group-scoped mount only
    MF-->>SDK: Filesystem operations return

    SDK-->>C: Agent response generated
    C-->>H: Response returned via IPC
    H->>U: Reply sent via WhatsApp

    Note over C,MF: Container CANNOT access:<br/>• Host filesystem outside explicit mounts<br/>• Other groups' containers<br/>• Host-level credentials<br/>Enforced by hypervisor — not bypassable via API
```

**Setup:**
```bash
# Prerequisites: macOS Tahoe (26+) or Linux + Docker, Node.js ≥20, Claude Code
git clone https://github.com/gavrielc/nanoclaw.git
# OR production fork: git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw

# Claude Code drives the setup
claude
# Inside Claude Code:
/setup                  # Full installation wizard

# Add channels (modifies your fork's code via skill files)
/add-telegram
/add-gmail

# Operations
/clear                  # Compact conversation context
/debug                  # Troubleshoot container issues
```

---

### 3.4 ZeroClaw

**Profile: Performance-First Rust Agent — Minimal Binary, Encrypted Secrets**

ZeroClaw is a ground-up Rust rewrite that treats Node.js startup overhead and memory consumption as primary engineering problems. The result is a 3.4MB static binary that starts in under 10ms and fits in a Docker sidecar with negligible overhead.
**Core Facts:**

- **Repository:** `theonlyhennygod/zeroclaw`
- **Language:** Rust (99%), SQLite
- **Binary Size:** 3.4MB (static)
- **Startup Time:** <10ms (measured on 0.8GHz hardware) - *repository-reported measurement*
- **RAM (RSS):** <5MB base
- **Channels:** CLI, Telegram, Discord, Slack, HTTP webhooks
- **LLM Providers:** 22+ via pluggable trait system (Ollama, OpenRouter, OpenAI, Anthropic, etc.)
- **Memory Store:** SQLite with hybrid vector/keyword search
- **Migration Support:** Built-in `zeroclaw migrate openclaw` command
- **Test Suite:** 1,000+ tests
- **License:** MIT

**Distinguishing Characteristics:** Security is configured on by default. The gateway binds to `127.0.0.1` and refuses public binding without an explicit tunnel flag. Secrets are encrypted at rest. The workspace sandbox blocks 14 system directories and 4 sensitive dotfiles by default. Symlink escape detection uses filesystem path canonicalization. Rust's ownership model reduces memory safety vulnerabilities common in unmanaged runtimes — an entire category of use-after-free, buffer overflow, and data race issues that are possible in Node.js or Python are structurally prevented at compile time.

```mermaid
graph LR
    subgraph "Channel Layer"
        TG[Telegram]
        DC[Discord]
        SL[Slack]
        CLI[CLI / REPL]
        WH[HTTP Webhook]
    end

    subgraph "Security Defaults"
        TG & DC & SL & CLI & WH --> SEC

        SEC["Gateway Security\n(127.0.0.1 bind — refuses 0.0.0.0\nwithout explicit tunnel flag)"]
        SEC --> PL["Pairing\n(6-digit OTP)"]
        SEC --> RL[Rate Limiting]
        SEC --> WS["Workspace Sandbox\n(14 blocked system dirs\n4 blocked dotfiles\nSymlink canonicalization)"]
        SEC --> ES["Encrypted Secrets\n(at rest)"]
    end

    subgraph "Agent Core — Rust Binary 3.4MB"
        SEC --> AG[Agent Loop]
        AG --> PR["Provider Trait System\n22+ LLMs pluggable"]
        AG --> MEM["Hybrid Memory\nSQLite + Vector Search"]
        AG --> TR["Tool Registry\nPluggable Traits"]
    end

    subgraph "Tool Execution"
        TR --> SH["Shell Tools\n(workspace-restricted)"]
        TR --> WT[Web Tools]
        TR --> FT["File Tools\n(workspace-scoped)"]
    end

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999
    L1["→ Control/data flow\n- - Isolation boundary\nAll security defaults are on — opt-in to relax"]:::legend
```

**Setup:**
```bash
# Build from source (Rust / Cargo required)
git clone https://github.com/theonlyhennygod/zeroclaw.git
cd zeroclaw
cargo build --release
cargo install --path .

# Interactive onboarding
zeroclaw onboard --interactive
# Quick onboarding
zeroclaw onboard --api-key sk-... --provider openrouter

# Usage
zeroclaw agent -m "Hello"    # Single message
zeroclaw agent               # Interactive REPL

# Daemon and gateway
zeroclaw daemon              # Background service
zeroclaw gateway             # HTTP gateway — default: 127.0.0.1:8080

# Diagnostics
zeroclaw doctor
zeroclaw status

# Migration from OpenClaw
zeroclaw migrate openclaw --dry-run   # Preview migration
zeroclaw migrate openclaw             # Execute
```

---

### 3.5 IronClaw

**Profile: Capability-Isolated WASM Agent — Strongest Tool-Level Security Model**

IronClaw was created by **Illia Polosukhin** — co-founder of NEAR Protocol and co-author of the 2017 paper *"Attention Is All You Need"* (the foundational Transformer architecture paper). When Polosukhin announced on X/Twitter that "People are losing their funds and credentials using OpenClaw. We started working on a security-focused version — IronClaw. It's Rust-based, all tools run in an isolated WASM environment," it carried significant technical credibility.

Project contributors as of Feb 2026: Illia Polosukhin (~90 commits), Claude by Anthropic (~71 commits attributed), Firat Sertgoz (NEAR protocol core developer).

**Core Facts:**
- **Repository:** `nearai/ironclaw`
- **Language:** Rust
- **Latest Release:** v0.1.3
- **Channels:** TUI/REPL (Ratatui), HTTP webhooks, WASM-based channels (Telegram, Slack), Web Gateway (SSE + WebSocket)
- **Database:** PostgreSQL 15+ with `pgvector` extension — Reciprocal Rank Fusion search (hybrid FTS + vector)
- **Default LLM:** NEAR AI Chat API (browser OAuth)
- **Alternate LLMs:** Any provider via Chat Completions API
- **Key Differentiator:** WASM sandbox — every tool runs in an isolated WebAssembly container with explicit capability grants
- **Self-Expanding:** Dynamically builds new tools as WASM modules via natural language instruction
- **License:** Apache 2.0 / MIT

**Distinguishing Characteristics:** The WASM sandbox differs fundamentally from Docker and process isolation. Each tool receives explicit capability declarations at load time: which HTTP endpoints it may reach, whether it can read/write specific paths, memory limits, CPU time limits, and execution timeouts. Critically, secrets are injected at the host boundary by the Rust runtime — the WASM tool code never has access to the raw credential values. Even if a tool contains malicious logic, it cannot read credentials it was never granted and cannot reach endpoints outside its declared allowlist.

**Known Constraint:** IronClaw defaults to NEAR AI cloud authentication for its initial setup wizard. Users requiring fully local-first operation must configure the Chat Completions API to point to an alternate provider. The team has indicated plans to make NEAR AI login optional; this remains unresolved as of Feb 2026.

```mermaid
graph TD
    subgraph "Input Channels"
        REPL["TUI / REPL\n(Ratatui)"]
        HTTP[HTTP Webhooks]
        WASM_CH["WASM Channels\nTelegram / Slack"]
        WGW["Web Gateway\nSSE + WebSocket"]
    end

    REPL & HTTP & WASM_CH & WGW --> ROUTER

    subgraph "Routing + Scheduling"
        ROUTER[Router — Intent Classification]
        ROUTER --> SCHED["Parallel Scheduler\nMulti-worker LLM jobs"]
        ROUTER --> ROUTINES["Routines Engine\nCron / Event / Webhook"]
    end

    subgraph "Parallel Workers"
        SCHED --> W1[Worker — LLM Reasoning]
        SCHED --> W2[Worker — LLM Reasoning]
        SCHED --> WN[Worker N]
    end

    subgraph "Tool Registry"
        W1 & W2 & WN --> TOOLS[Tool Registry]
        TOOLS --> BUILTIN[Built-in Tools]
        TOOLS --> MCP[MCP Protocol — External Servers]
        TOOLS --> WASM_T["WASM Sandbox\n(Untrusted / Dynamic Tools)"]
    end

    subgraph "WASM Security Pipeline — Per Tool Execution"
        WASM_T --> ALLOW["Endpoint Allowlist\nValidator"]
        ALLOW --> LEAK1["Leak Scanner\n(Request)"]
        LEAK1 --> CRED["Credential Injector\n(Host Boundary Only —\ntool never sees raw secret)"]
        CRED --> EXEC["Execute in WASM\n(Memory/CPU/Time capped)"]
        EXEC --> LEAK2["Leak Scanner\n(Response)"]
        LEAK2 --> RESULT[Result returned]
    end

    subgraph "Persistent Storage"
        W1 & W2 & WN --> PG[("PostgreSQL 15+\n+ pgvector")]
        PG --> HYBRID["Hybrid Search\nFTS + Vector (RRF)"]
    end

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999
    L1["→ Control flow\n- - - Trust / isolation boundary\nAll WASM tool executions pass through security pipeline"]:::legend

    style CRED fill:#d4edda,stroke:#28a745
    style EXEC fill:#d4edda,stroke:#28a745
    style WASM_T fill:#cce5ff,stroke:#0056b3
```

**Setup:**
```bash
# Prerequisites: Rust 1.85+, PostgreSQL 15+ with pgvector

# One-line install (Cargo Binstall recommended)
cargo binstall ironclaw
ironclaw onboard   # Wizard: NEAR AI auth (browser OAuth) + PostgreSQL setup

# OR: Build from source
git clone https://github.com/nearai/ironclaw.git
cd ironclaw
cargo build --release
./target/release/ironclaw onboard

# Run
ironclaw agent -m "Hello"    # Single message
ironclaw agent               # Interactive REPL

# Advanced: Custom LLM provider
ironclaw provider add --name ollama --url http://localhost:11434/v1 --model llama3
ironclaw provider set-default ollama

# Diagnostics
ironclaw doctor
ironclaw status
```

---

### 3.6 PicoClaw

**Profile: Edge-Hardware Go Agent — Ultra-Efficient Binary for $10 Hardware**

PicoClaw is a direct descendant of NanoBot, rewritten in Go for minimal runtime overhead and cross-compilation to edge hardware. It targets $10–50 single-board computers (RISC-V, ARM64) that cannot run Node.js or Python agents efficiently.

**Core Facts:**
- **Repository:** `sipeed/picoclaw`
- **Language:** Go
- **Latest Release:** v0.1.1 (Feb 13, 2026)
- **Binary Size:** ~8.2MB (compressed <10MB)
- **Startup Time:** <1s on sub-1GHz hardware
- **RAM (RSS):** <10MB base
- **Channels:** Telegram, Discord, Slack, Webhooks, QQ, DingTalk
- **LLM Providers:** OpenRouter, Anthropic, Ollama (local), Groq, DeepSeek
- **Memory:** `MEMORY.md` (long-term) + daily notes
- **Scheduling:** Built-in cron
- **Sandbox:** Workspace-restricted file/command execution
- **License:** MIT

**Distinguishing Characteristics:** PicoClaw is designed for "always-on" deployments on hardware too constrained for OpenClaw's Node.js runtime. It cross-compiles to any Go target (Linux ARM64, RISC-V, macOS) with no runtime dependencies. The workspace sandbox restricts all file and command operations to a single directory tree, with command filtering for additional safety. Ollama integration allows fully local, API-free operation on capable edge hardware.

**Security Posture:** Process-level isolation with workspace restrictions. Not as strong as NanoClaw's per-group containers or IronClaw's WASM, but materially better than OpenClaw's shared memory model. The minimal Go binary reduces the attack surface compared to interpreted runtimes.

**Real-World Deployment:** Sipeed uses PicoClaw for edge AI demos on their RISC-V development boards. Community reports describe home automation and monitoring use cases on Raspberry Pi Zero equivalents.

```mermaid
graph LR
    subgraph "Channel Layer"
        TG[Telegram]
        DC[Discord]
        SL[Slack]
        WH[HTTP Webhook]
        QQ[QQ / DingTalk]
    end

    TG & DC & SL & WH & QQ --> BUS[Message Bus]

    subgraph "Agent Core — Go Binary ~8MB"
        BUS --> AL[Agent Loop]
        AL --> CB[Context Builder]
        AL --> MM[Memory Manager]
        AL --> SK[Skills Loader]
    end

    subgraph "Tool Execution — Workspace Sandbox"
        AL --> WS["Web Search\n(Brave API)"]
        AL --> CE["Code Execution\n(Command Filter)"]
        AL --> FO["File Operations\n(Workspace-Restricted)"]
    end

    subgraph "LLM Providers"
        AL --> OR[OpenRouter]
        AL --> AN[Anthropic]
        AL --> OL["Ollama\n(Local)"]
        AL --> GR[Groq / DeepSeek]
    end

    subgraph "Persistent Storage"
        CB --> CFG[config.json]
        MM --> MEM["MEMORY.md\n+ Daily Notes"]
    end

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999
    L1["→ Data flow\n⚠ All operations restricted to workspace dir\nCross-compiles to RISC-V / ARM64"]:::legend
```

**Setup:**
```bash
# Build from source (Go required)
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw
go build -o picoclaw ./cmd/picoclaw

# Configure
# Edit config.json — compatible with NanoBot format
{
  "providers": {
    "ollama": { "url": "http://localhost:11434/v1", "model": "llama3" }
  },
  "channels": {
    "telegram": { "token": "bot-token" }
  }
}

# Run
./picoclaw agent -m "Hello"    # Single message
./picoclaw agent               # Interactive

# Daemon mode
./picoclaw daemon              # Background service

# Edge hardware example (cross-compile)
GOOS=linux GOARCH=arm64 go build -o picoclaw-arm64 ./cmd/picoclaw
# Copy to RISC-V board and run
```

---

### 3.7 SafeClaw & ThePopeBot — Early-Stage Projects

**SafeClaw (`princezuda/safeclaw`):** A rule-based alternative that eliminates LLMs entirely to avoid prompt injection risks. Core features are offline-capable with local tools for STT/TTS, document parsing, and automation. Insufficient documentation and activity (~43 stars) prevent full architectural assessment. Not recommended for production without independent audit.

**ThePopeBot (`stephengpope/thepopebot`):** A GitOps-based autonomous agent that uses GitHub Actions for execution and Docker containers for isolation. Secrets are filtered at the process level and never exposed to the AI. All actions are committed to Git for auditability. Promising for 24/7 tasks, but early-stage (~172 stars) with limited channels (Telegram primary).

Both projects address OpenClaw's security issues in novel ways but lack the maturity for inclusion in detailed comparisons. Monitor for future development.

---

## 4. Threat Model

This ecosystem's primary threats derive from the fundamental requirement that AI agents must interact with the real world to be useful. This interaction creates bidirectional risk: inbound attacks via input channels, outbound data exfiltration via tool execution.

### Adversary Capabilities & Goals

1. **Prompt Injection Attacks** (via messaging channels)
   - Goal: Trick the agent into executing malicious commands or leaking data
   - Capability: Crafted messages that bypass approval prompts
   - Affected: All projects, but mitigated by isolation boundaries

2. **Supply Chain Compromise** (via skill registries)
   - Goal: Backdoor injection for credential theft or RCE
   - Capability: Publish malicious skills to public registries
   - Affected: Primarily OpenClaw (ClawHub); others use core-repo-only models

3. **Credential Theft** (via RCE or token exfiltration)
   - Goal: Access to stored API keys, SSH credentials, filesystem
   - Capability: Exploit CVEs like 2026-25253 for token hijacking
   - Affected: Shared-memory models (OpenClaw); mitigated in isolated designs

4. **Data Exfiltration** (via malicious tools or APIs)
   - Goal: Leak sensitive data to attacker-controlled endpoints
   - Capability: Install backdoored skills or exploit tool execution
   - Affected: Projects without endpoint allowlisting (OpenClaw, NanoBot)

5. **Denial of Service** (via API cost exhaustion)
   - Goal: Generate excessive LLM calls to inflate costs
   - Capability: Malformed cron jobs or heartbeat loops
   - Affected: Shared-context models (OpenClaw documented cases)

6. **Insider Threats** (developer / contributor compromise)
   - Goal: Introduce subtle backdoors in core code
   - Capability: Submit malicious PRs to repositories
   - Affected: All open-source projects; mitigated by small, auditable codebases

### Assumed Defenses

- Operators follow Section 5.6 best practices (non-root, VPN, firewall)
- LLM providers enforce per-account rate limits
- No zero-day vulnerabilities in underlying runtimes (Node.js, Python, Rust, Go)
- Users audit skills before installation (not realistic for OpenClaw's 3,000+)

This threat model assumes a motivated but non-state-level adversary. For high-value targets (crypto wallets, enterprise credentials), assume advanced persistent threats capable of supply-chain attacks.

---

## 5. Security Analysis

### 5.1 CVE-2026-25253: Architectural Implications

**CVSS Score:** 8.8 (High)  
**Disclosed:** February 2, 2026 by DepthFirst (Mav Levin)  
**Patched:** OpenClaw v2026.1.29 (Jan 30, 2026)  

**Exploit Chain:**
1. Victim clicks attacker-crafted link with `gatewayUrl` parameter pointing to malicious WebSocket server
2. OpenClaw Control UI auto-connects without validation
3. Stored auth token transmitted to attacker
4. Cross-Site WebSocket Hijacking (CSWSH) bypasses localhost restrictions
5. Attacker uses stolen token to disable sandboxing and approvals via API
6. Arbitrary command execution achieved

**Impact:** Full compromise — all credentials, filesystem, shell access. Data exfiltration possible. No user interaction beyond initial click required.

**Architectural Root Cause:** The shared-memory process model means any valid API authentication grants access to *everything*. Application-level controls (sandboxing, approvals) are managed by the same API layer, making them trivially bypassable post-authentication.

**Mitigation in Alternatives:** NanoClaw and IronClaw enforce isolation below the API layer (hypervisor / WASM runtime). ZeroClaw refuses public gateway binding by default. PicoClaw has no WebSocket UI.

### 5.2 ClawHub Supply Chain Risk

**Documented Malicious Skills:** 341–900+ (Koi Security, Cisco Talos, Feb 2026)  
**Malicious Rate Estimate:** ~20% of registry (unverified community reports)  
**Review Process:** None mandatory — community-driven only  

**Attack Vectors:**
- Backdoor injection (Jamieson O'Reilly analysis: trivial via undocumented dependencies)
- Data exfiltration to attacker endpoints (Cisco Talos: 47 skills with hardcoded C2 servers)
- Credential harvesting (Palo Alto Unit 42: insider threats via forked skills)

**Impact:** Installed skills execute in the shared Node.js process. Malicious code has immediate access to all host resources.

**Mitigation in Alternatives:** No external registries. NanoBot / PicoClaw: skills in core repo only. NanoClaw: manual SKILL.md additions. IronClaw: WASM sandbox with capability grants. ZeroClaw: pluggable traits, no registry.

### 5.3 Additional CVEs (Feb 2–4, 2026)

- **CVE-2026-24763:** OS command injection in SSH handling (CVSS 9.8 Critical)
- **CVE-2026-25157:** Command injection in tool execution path (CVSS 8.1 High)

Both allow RCE without authentication in misconfigured deployments. Patched in v2026.1.29+.

**Prompt Injection Vulnerability:** Community tests show ~70% success rate in bypassing approvals via crafted messages.

### 5.4 Security Model Comparison Matrix

| Feature | OpenClaw | NanoBot | NanoClaw | ZeroClaw | IronClaw | PicoClaw |
|---------|----------|---------|----------|----------|----------|----------|
| **Isolation Level** | Application | Process | OS/Hypervisor (per group) | Process + Sandbox | WASM Capability (per tool) | Process + Workspace |
| **Attack Surface (LOC)** | 430k (52 modules) | 4k (10 modules) | 500 (4 files) | ~10-15k | ~10-15k | Compact (~8MB binary) |
| **Skill Validation** | ClawHub (unvetted) | Core repo only | Manual SKILL.md | Pluggable traits | WASM sandbox | Core repo only |
| **Credential Storage** | Plaintext config | config.json | Code-based | Encrypted at rest | Host boundary injection | config.json |
| **Bypass Resistance** | Low (API-reconfigurable) | Medium | High (kernel-enforced) | High (defaults on) | High (capability grants) | Medium |
| **Sandboxing** | Optional Docker | No | Required (Apple/Docker) | Workspace + Blocked paths | WASM per tool | Workspace-restricted |
| **Symlink Protection** | No | No | Yes (mount validation) | Yes (canonicalization) | Yes (WASM fs limits) | Yes (workspace bounds) |

### 5.5 Enterprise & Compliance Considerations

None of these projects are enterprise-ready out-of-the-box. All require hardening, auditing, and compliance mapping. OpenClaw's shared-memory model and ClawHub registry create immediate compliance risks for regulated industries.

For **finance** (PCI-DSS, SOX): IronClaw's WASM capability model comes closest to principle of least privilege required by financial regulations. NEAR AI cloud dependency is a blocking concern for many institutions.

For **healthcare** (HIPAA): Local-only deployments of NanoClaw, ZeroClaw with Ollama, or PicoClaw with Ollama are the only architectures that can reasonably prevent PHI from transiting third-party LLM APIs. None are HIPAA-certified.

---

### 5.6 Security Best Practices

**Universal (all projects):**
1. Run as a non-root, non-admin user with the minimum required filesystem permissions
2. Use Tailscale or equivalent VPN instead of any form of public gateway exposure
3. Rotate API keys monthly; monitor LLM provider dashboards for unexpected token usage spikes
4. Enable OS-level firewall (UFW on Linux); allow only the specific gateway port
5. Never store production cloud provider credentials on the same machine running an agent

**OpenClaw (if deployed):**
6. Update to v2026.1.29+ immediately; rotate all previously stored tokens
7. Enable Docker tool sandboxing (`tools.exec.host: "docker"`)
8. Read source code — not just READMEs — for every ClawHub skill before installation
9. Monitor `~/.openclaw/skills/` directory for unexpected additions
10. Run `openclaw doctor` after every update
11. Use `openclaw-ansible` for VPS deployments (includes Tailscale, UFW, Docker)

**NanoClaw:**
12. Mount only explicitly required directories; prefer read-only for source code mounts
13. Audit mount allowlist quarterly; test for symlink escape via canonicalization mismatch

**ZeroClaw / IronClaw:**
14. ZeroClaw: Confirm `127.0.0.1` binding is active; do not relax without tunnel
15. IronClaw: Review endpoint allowlist before deploying tools that make external calls

---

## 6. Architecture Diagrams

### 6.1 Isolation Model Comparison

```mermaid
graph LR
    subgraph OC["OpenClaw — Shared Process"]
        OC_HOST["Host Machine\n(all resources accessible)"]
        OC_PROC["Single Node.js Process\n(all agents co-located)"]
        OC_G1["Group 1 Agent"]
        OC_G2["Group 2 Agent"]
        OC_TOOLS["Tools\n(full host access)"]

        OC_HOST --- OC_PROC
        OC_PROC --- OC_G1
        OC_PROC --- OC_G2
        OC_PROC --> OC_TOOLS
        OC_TOOLS -.->|"unrestricted access"| OC_HOST

        style OC_PROC fill:#ffe0e0,stroke:#cc0000
        style OC_TOOLS fill:#ffe0e0,stroke:#cc0000
    end

    subgraph NC["NanoClaw — OS Hypervisor Isolation"]
        NC_HOST["Host Machine"]
        NC_PROC["Host Process\n(~500 LOC)"]
        NC_C1["Container: Group 1\nIsolated Filesystem"]
        NC_C2["Container: Group 2\nIsolated Filesystem"]
        NC_HYPER["OS Hypervisor\n(Apple Container / Docker)"]

        NC_HOST --- NC_PROC
        NC_PROC --> NC_C1
        NC_PROC --> NC_C2
        NC_HYPER -. enforces boundary .-> NC_C1
        NC_HYPER -. enforces boundary .-> NC_C2
        NC_C1 -. cannot reach .-> NC_HOST
        NC_C2 -. cannot reach .-> NC_HOST

        style NC_HYPER fill:#d4edda,stroke:#28a745
        style NC_C1 fill:#d4edda,stroke:#28a745
        style NC_C2 fill:#d4edda,stroke:#28a745
    end

    subgraph IC["IronClaw — WASM Capability Isolation"]
        IC_HOST["Host Machine"]
        IC_AGENT["Rust Agent Process"]
        IC_CRED["Credential Injector\n(host boundary — secret\nnever enters WASM)"]
        IC_WASM["WASM Tool Container\n(capability-declared:\nallowed endpoints,\nmemory/CPU caps)"]

        IC_HOST --- IC_AGENT
        IC_AGENT --> IC_CRED
        IC_CRED -. "injects at boundary\n(tool code never sees raw value)" .-> IC_WASM

        style IC_CRED fill:#d4edda,stroke:#28a745
        style IC_WASM fill:#cce5ff,stroke:#0056b3
    end

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999,font-size:11px
    L["LEGEND:\n🔴 Red = critical attack surface\n🟢 Green = security boundary (enforced)\n🔵 Blue = sandboxed execution\n- - → Isolation / cannot-cross boundary\n→ Normal control / data flow"]:::legend
```

### 6.2 Attack Surface Map — OpenClaw

```mermaid
graph TD
    subgraph "Entry Points — External Attack Surface"
        P1["15+ Messaging Channels\n(Prompt Injection Vector)"]
        P2["WebSocket Control UI\n(CVE-2026-25253 Entry Point)"]
        P3["ClawHub Skills Registry\n(341 Malicious Skills — Feb 2026)"]
        P4["HTTP Gateway API\n(Post-token-theft command execution)"]
    end

    subgraph "Single Node.js Process — Shared Memory"
        GW[Gateway]
        AE[Agent Engine]
        SK[Skill Execution]
    end

    subgraph "Host Resources — Fully Accessible from Shared Process"
        SH["Shell / Terminal"]
        FS["Filesystem"]
        CR["API Keys / Credentials"]
        SSH_K["SSH Keys"]
        DB["Local Databases / Secrets"]
    end

    P1 --> GW
    P2 --> GW
    P3 --> SK
    P4 --> GW
    GW --> AE
    AE --> SK
    SK --> SH & FS & CR & SSH_K & DB

    CVE1["CVE-2026-25253\n1-Click RCE via Token Theft\n(CVSS 8.8)"]:::exploit -.exploits.-> P2
    CVE2["CVE-2026-24763\nCommand Injection\nSSH handling"]:::exploit -.exploits.-> SH
    MAL["341 Malicious Skills\n(Koi Security / Cisco Talos)"]:::exploit -.injected via.-> P3
    PINJ["Prompt Injection\n(community-reported ~70% success\nin controlled tests)"]:::exploit -.attacks via.-> P1

    classDef exploit fill:#cc0000,color:#fff,stroke:#880000

    %% LEGEND
    classDef legend fill:#f9f9f9,stroke:#999
    L["LEGEND:\n🔴 Red = confirmed exploit / attack\n→ Normal control flow\n- - → Attack path\nAll host resources reachable from shared Node.js process"]:::legend
```

---

## 7. Performance Benchmarks

> **Benchmark Environment:** macOS arm64 (Apple M3 Max, 14-core CPU, 48GB RAM). Cold start measurements. CLI mode only. No LLM inference included in timing. Node.js production build for OpenClaw.  
> **Source:** ZeroClaw GitHub repository benchmark suite + Penligent.ai independent testing (Feb 2026).  
> **Note:** Results represent upper-bound performance on high-end developer hardware. Runtimes with significant initialization overhead (Node.js, Python) are expected to scale poorly on sub-1GHz single-core edge hardware. ZeroClaw and PicoClaw startup times remain sub-second in such environments due to minimal runtime overhead.

### Binary / Runtime Overhead (M3 Max baseline)

| Metric | OpenClaw | NanoBot | PicoClaw | ZeroClaw |
|--------|----------|---------|----------|----------|
| **Language** | TypeScript / Node.js | Python | Go | Rust |
| **Distribution Size** | ~28MB + Node.js runtime | N/A (scripts + pip deps) | ~8.2MB binary | 3.4MB binary |
| **Node.js Runtime Base RAM** | ~390MB | — | — | — |
| **Max RSS (measured, M3 Max)** | ~394MB | ~100–200MB | ~9.1MB | ~7.3MB |
| **Help / Init Startup** | 3.31s | >5s (cold Python) | 0.45s | 0.38s |
| **Startup on edge hardware (sub-1GHz)** | Projected to scale poorly — Node.js runtime initialization is the bottleneck | Slower than M3 Max | <1s | <10ms |
| **Min viable hardware** | ~$599 Mac Mini (M4) | ~$50 Linux SBC | ~$10 RISC-V board | ~$10 board |

### API Token Efficiency (Documented Cases)

| Scenario | OpenClaw | NanoBot | NanoClaw | ZeroClaw / PicoClaw |
|----------|----------|---------|----------|---------------------|
| Simple time-check via cron | **120k tokens documented** (architectural) | Tunable | Minimal (per-group context) | Near-zero with Ollama |
| Estimated monthly cost — basic reminder schedule | **~$750/mo documented** | $10–30 | $5–15 | $0–10 (local model) |
| Multi-group context isolation | None (shared state) | None | Yes (container boundary) | Partial |

Documented user reports describe time-check cron jobs generating approximately 120,000 tokens due to context accumulation in shared-memory models. This is a characteristic of the architecture, not an edge case or misconfiguration.

---

## 8. Architectural Tradeoff Summary

There is no universally superior project in this ecosystem. Each design is internally coherent within its philosophy. The relevant question is which design philosophy matches your specific deployment constraints and threat model.

| Axis | One End | Other End | Key Projects |
|------|---------|-----------|--------------|
| **Feature density** | 1 channel, 500 LOC | 15+ channels, 430k LOC | NanoClaw ↔ OpenClaw |
| **Isolation strength** | Application-level controls | Kernel / WASM capability grants | OpenClaw ↔ NanoClaw / IronClaw |
| **Runtime overhead** | 3.4MB binary, <10ms | 394MB RAM, 3.31s startup | ZeroClaw ↔ OpenClaw |
| **Codebase auditability** | 8 minutes (500 LOC) | Days (430k LOC) | NanoClaw ↔ OpenClaw |
| **Ecosystem breadth** | Core repo only | 3,000+ ClawHub skills | NanoClaw/NanoBot ↔ OpenClaw |
| **Hardware target** | $10 RISC-V board | Developer workstation | PicoClaw/ZeroClaw ↔ OpenClaw/NanoClaw |
| **Self-expansion** | Fixed feature set | Builds new tools via natural language | NanoBot ↔ IronClaw |

The tradeoffs compound: OpenClaw's feature density requires 430k LOC which cannot be audited in a reasonable timeframe, which requires trusting ClawHub skills, which creates supply chain risk. NanoClaw's 500 LOC is auditable precisely because it deferred feature scope. ZeroClaw's Rust binary has a smaller attack surface precisely because it opted for a trait system over a shared plugin registry.

---

## 9. Decision Framework

### Choose OpenClaw if:
- You need **15+ messaging platform integrations** without custom development
- You want access to **3,000+ community skills** via ClawHub
- You have a **dedicated security team** able to audit skills and monitor deployments
- You're deploying to a **VPS with network isolation** (not your primary workstation)
- You accept **$100–500+/month API costs** for moderate-to-heavy usage
- You understand and accept the current security posture documented in Section 5

### Choose NanoBot if:
- You want to **understand AI agent internals** — the codebase is designed to be read
- You need **8+ channel support** out-of-the-box with Python ecosystem access
- You prefer **rapid iteration** — adding an LLM provider is a 2-step change
- You want **local LLM support** via vLLM
- You're building a **research prototype** or educational system

### Choose NanoClaw if:
- **Security guarantees at the OS level** are non-negotiable
- You're handling **financial data, legal documents, or sensitive personal information**
- You run **macOS Tahoe+** (Apple Container native) or Linux with Docker
- You're comfortable with **Claude Code** as the primary interface for extension
- You want the **smallest auditable codebase** with kernel-enforced isolation

### Choose ZeroClaw if:
- You need **extreme resource efficiency** — CI sidecars, minimal VPS, edge hardware
- You want a **single binary** deployable without a runtime on any Linux/macOS
- You're **migrating from OpenClaw** (built-in migration command)
- You value **1,000+ test coverage** for a production deployment baseline
- You want security hardening **on by default** without manual configuration

### Choose IronClaw if:
- **Tool-level credential isolation** is the primary requirement
- You're in **crypto/DeFi, finance**, or any domain where compromised tool = catastrophic data loss
- You want **self-expanding WASM tools** — describe what you need in natural language
- You're comfortable with **PostgreSQL** as a hard dependency
- You can **accept or work around** the NEAR AI cloud authentication dependency

### Choose PicoClaw if:
- You're deploying to **$10–50 edge hardware** (RISC-V, ARM64)
- You want a **Go-native binary** that cross-compiles to any target
- You're building **IoT or home automation** integrations
- You accept **pre-v1.0 status** and will not use it for sensitive data

### Avoid OpenClaw if:
- You're running it on a **personal machine with production credentials**
- You're in a **regulated industry** (healthcare, finance, legal)
- You cannot commit to **auditing every ClawHub skill** before installation
- You're **budget-constrained** — heartbeat inefficiencies can generate surprise API costs

---

## 10. Cost Analysis

*Monthly estimates. All costs are approximate and depend on LLM provider pricing, message complexity, and model selection. Local models (Ollama, vLLM) eliminate API costs for capable hardware.*

| Usage Level | OpenClaw | NanoBot | NanoClaw | ZeroClaw | IronClaw | PicoClaw |
|-------------|----------|---------|----------|----------|----------|----------|
| **Minimal** (10 msgs/day) | $10–20 | $5–10 | $3–7 | $0–5 | $5–10 | $0–5 |
| **Moderate** (50 msgs/day) | $50–100 | $20–40 | $15–30 | $10–20 | $15–30 | $10–20 |
| **Heavy** (200 msgs/day) | $200–400 | $80–150 | $60–100 | $40–80 | $60–100 | $40–80 |
| **Cron/heartbeat overhead** | +$100–750/mo (documented) | +$10–30 | +$5–15 | +$5–10 | +$10–20 | +$5–10 |
| **Skill ecosystem overhead** | +$50–200 | None | None | None | None | None |
| **Zero API cost possible?** | Partial | Yes (vLLM) | Partial | Yes (Ollama) | Partial | Yes (Ollama) |

**OpenClaw cost note:** The $100–750/month cron overhead range is drawn from user-reported accounts, not theoretical modeling. The mechanism is the shared context model: cron jobs accumulate and re-transmit full conversation and skill context on each execution tick, with user reports describing approximately 120,000 tokens for simple time-check jobs. This is a characteristic of the architecture, not a misconfiguration.

**Optimization strategies:**
- Pair ZeroClaw, PicoClaw, or NanoBot with a local Ollama model for near-zero API costs
- For OpenClaw: reduce heartbeat frequency to minimum viable; use a lightweight model (e.g., DeepSeek) for routine tasks; avoid installing skills with their own heartbeat loops
- NanoClaw's per-group context isolation prevents context accumulation across unrelated conversations

---

## 11. Migration Paths

### OpenClaw → ZeroClaw (Recommended — built-in tooling)
```bash
# Preview what will be migrated
zeroclaw migrate openclaw --dry-run

# Execute migration
zeroclaw migrate openclaw
```
Migrates: conversation history, channel configurations. Skills must be manually rebuilt as ZeroClaw traits — review each one before reimplementing.

### OpenClaw → NanoBot
1. Export conversation history manually (no automated export tool as of Feb 2026)
2. Identify the 5–10 ClawHub skills you actually use (most users use fewer than 10 regularly)
3. Replicate each as a Python file in `~/.nanobot/skills/`
4. Migrate channel tokens (Telegram bot token, WhatsApp session) — compatible format
5. Test all cron jobs; NanoBot's scheduler is APScheduler-based vs. OpenClaw's heartbeat model

### OpenClaw → NanoClaw
Appropriate for **security-critical migrations** where functional scope reduction is acceptable:
1. Accept initial scope reduction to WhatsApp only
2. Use Claude Code (`/add-telegram`, `/add-gmail`) to extend as needed
3. Map OpenClaw's multi-group shared context to NanoClaw's per-container isolated model
4. Validate mount allowlists before migrating access to any sensitive directories

### OpenClaw → IronClaw
1. Provision PostgreSQL 15+ with `pgvector` extension
2. Run `ironclaw onboard` — wizard handles database setup and authentication
3. Recreate tools as WASM modules (or use IronClaw's natural-language tool builder)
4. Migrate channel tokens

### NanoBot → PicoClaw
NanoBot was PicoClaw's direct codebase ancestor (Python → Go migration). Config structure is intentionally compatible:
1. Copy channel tokens (Telegram, Discord) — same config key names
2. Recreate skills as PicoClaw skill files (Python logic → equivalent Go)
3. Copy MEMORY.md content directly (same format)

---

## 11.5 Limitations of This Analysis

This document should be read with the following constraints in mind:

- **No formal source code audits were conducted.** Security posture assessments are based on publicly disclosed architecture documentation, README files, CVE advisories, and independent security research. They are not substitutes for professional penetration testing or code audit.
- **CVE exploitation status reflects the state as of February 16, 2026.** In-the-wild exploitation of CVE-2026-25253 was not independently confirmed at time of writing; this status should be re-verified.
- **Performance figures are representative, not exhaustive benchmarks.** M3 Max measurements reflect one hardware configuration under specific conditions (cold start, CLI mode, no LLM inference). Real-world performance varies by workload, model, and deployment context.
- **Star counts and repository metrics are point-in-time observations** subject to rapid change in this ecosystem.
- **Supply-chain risk figures (malicious skill counts, percentage estimates)** originate from third-party security firms and have not been independently re-verified by this document's authors.
- **Cost estimates are illustrative.** LLM pricing changes frequently; treat ranges as order-of-magnitude indicators.

---

## 11.6 Isolation Boundary Hierarchy

Understanding *where* a security boundary is enforced is as important as knowing that one exists. The following hierarchy ranks isolation enforcement from weakest to strongest, mapped to the projects in this ecosystem.

```
ENFORCEMENT LEVEL         DESCRIPTION                              PROJECTS

Level 1 — Application    Controls enforced by application code.    OpenClaw
                         Can be reconfigured or bypassed by        (allowlists,
                         any actor with API access.                 approvals,
                                                                    pairing codes)

Level 2 — Process        Agent and tools share an OS process.      NanoBot
Boundary                 The kernel prevents cross-process          PicoClaw
                         memory access, but within the process      ZeroClaw
                         all data is co-located. Credential
                         access = process access.

Level 3 — Container      Each workload runs in an isolated          NanoClaw
(Kernel-Enforced)        Linux container with its own filesystem    (per group)
                         namespace. The kernel's namespace
                         isolation and cgroup limits enforce
                         the boundary — not application code.
                         Cannot be bypassed via API.

Level 4 — Capability     Each tool execution receives only the      IronClaw
Runtime (WASM)           capabilities it declared at load time:     (per tool call)
                         specific HTTP endpoints, memory cap,
                         CPU cap, time limit. The WASM runtime
                         enforces these — the tool never holds
                         a reference to anything outside its
                         declared grants.

Level 5 — Hardware       Full VM-level separation. Each workload   (Not present in
Virtualization           gets its own kernel. Strongest             current ecosystem —
                         enforcement, highest overhead.             listed for
                                                                    reference)
```

**Practical Implication:** A prompt injection attack or malicious skill that succeeds at Level 1 gains full host access. The same attack at Level 3 is contained to one group's container. At Level 4, it can only reach the endpoints the tool was declared to use — and never sees the raw credential value even if it was injected.

The levels are not mutually exclusive. NanoClaw uses Level 3 for container isolation while also operating at Level 2 for its host process. IronClaw uses Level 4 for untrusted WASM tools while its core agent process operates at Level 2.

---

## 12. Conclusion

### Summary Matrix

| Criterion | Leader(s) | Notes |
|-----------|-----------|-------|
| **Feature breadth** | OpenClaw | 15+ channels, 3,000+ skills — unmatched |
| **Security architecture** | NanoClaw, IronClaw | Kernel-level vs. WASM capability isolation |
| **Codebase auditability** | NanoClaw → NanoBot → ZeroClaw | 500 / 4k / ~10-15k LOC |
| **Performance / resource efficiency** | ZeroClaw → PicoClaw | <10ms / <5MB vs. <1s / <10MB |
| **Research and education** | NanoBot | Designed to be read, extended, cited |
| **Edge hardware** | PicoClaw → ZeroClaw | $10 RISC-V support; Go / Rust binary |
| **Developer ecosystem** | OpenClaw | 10,000+ Discord, 130+ contributors |
| **Credential protection model** | IronClaw | WASM boundary; secrets never enter tool context |
| **Production migration path** | ZeroClaw | Built-in OpenClaw migration, 1,000+ tests |
| **Enterprise compliance readiness** | None — all require hardening | IronClaw closest for regulated environments |

### Strategic Synthesis

The projects in this ecosystem each represent a different resolution of the same underlying tension: an AI agent that is genuinely useful must have access to real-world resources — the filesystem, APIs, the shell, external services. That access is also what makes a compromised agent catastrophic.

OpenClaw resolved this by maximizing access and adding application-level controls. The February 2026 CVEs demonstrated weaknesses in application-level enforcement within this specific architecture — specifically that controls managed by the same API layer as the rest of the system can be bypassed by any actor who obtains a valid authentication token.

The alternatives each propose a different architectural answer. NanoClaw and IronClaw argue that isolation must be enforced below the application layer — at the OS hypervisor or the WASM runtime. ZeroClaw argues that a smaller, type-safe codebase reduces the attack surface by removing entire vulnerability classes. PicoClaw argues that the right deployment context is one where the hardware itself is so resource-constrained that a large attack surface isn't even buildable.

None of these approaches are complete solutions. All require operator awareness, regular updates, and thoughtful configuration. But they represent a materially more defensible set of starting points than a 430,000-line shared-memory daemon with an unvetted public skill registry.

### Deployment Recommendations

| Scenario | Recommendation |
|----------|----------------|
| Prototype / learning | NanoBot |
| Personal assistant, security-conscious, macOS | NanoClaw |
| Personal assistant, cross-platform | ZeroClaw |
| Sensitive data / financial automation | IronClaw (after NEAR AI dep. resolved) |
| Edge / IoT / embedded Linux | PicoClaw (post v1.0) or ZeroClaw (production-ready now) |
| OpenClaw on personal machine with credentials | Migrate — see Section 11 |
| OpenClaw on isolated VPS, security team present | Acceptable with Section 5.6 hardening applied |

---

## 13. References

### Primary GitHub Repositories
- NanoBot: https://github.com/HKUDS/nanobot
- NanoClaw (original): https://github.com/gavrielc/nanoclaw
- NanoClaw (Qwibit): https://github.com/qwibitai/nanoclaw
- OpenClaw: https://github.com/openclaw/openclaw
- ZeroClaw: https://github.com/theonlyhennygod/zeroclaw
- IronClaw: https://github.com/nearai/ironclaw
- PicoClaw: https://github.com/sipeed/picoclaw

### CVE & Security Advisories
- NVD CVE-2026-25253: https://nvd.nist.gov/vuln/detail/CVE-2026-25253
- GitHub Security Advisory GHSA-g8p2-7wf7-98mq
- DepthFirst Disclosure (Mav Levin): https://depthfirst.com/post/1-click-rce-to-steal-your-moltbot-data-and-keys
- The Hacker News CVE coverage: https://thehackernews.com/2026/02/openclaw-bug-enables-one-click-remote.html
- SOCRadar deep dive: https://socradar.io/blog/cve-2026-25253-rce-openclaw-auth-token/
- Adversa.ai hardening guide: https://adversa.ai/blog/openclaw-security-101-vulnerabilities-hardening-2026/
- Censys exposure report: 21,639 instances (Jan 31, 2026)
- Koi Security: 341 malicious ClawHub skills (Feb 2026)
- Cisco Talos: skill data exfiltration analysis
- Palo Alto Networks Unit 42: insider threat characterization

### Journalism & Technical Analysis
- CNBC OpenClaw history: https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html
- VentureBeat NanoClaw: https://venturebeat.com/orchestration/nanoclaw-solves-one-of-openclaws-biggest-security-issues-and-its-already
- Wikipedia OpenClaw: https://en.wikipedia.org/wiki/OpenClaw
- CNX Software PicoClaw: https://www.cnx-software.com/2026/02/10/picoclaw-ultra-lightweight-personal-ai-assistant-run-on-just-10mb-of-ram/
- IronClaw announcement (Polosukhin): https://thecoding.substack.com/p/report-ironclaw-openclaw-in-rust
- NxCode OpenClaw history: https://www.nxcode.io/resources/news/openclaw-complete-guide-2026

---

*As of February 16, 2026, The AI agent ecosystem is evolving rapidly. Verify star counts, feature sets, CVE patch status, and release versions directly against primary repositories before making deployment decisions. See Section 11.5 for full limitations of this analysis.*

**Related:**- [OpenClaw(Moltbot-or-Clawdbot)-Architecture](OpenClaw(Moltbot-or-Clawdbot)-Architecture.md) — Focused architecture deep-dive on OpenClaw that supports this survey's Section 3.1 critique of its shared-memory, application-level control model.- [OpenClaw(Moltbot-or-Clawdbot)-Security-Analysis-Jan-2026](OpenClaw(Moltbot-or-Clawdbot)-Security-Analysis-Jan-2026.md) — Detailed evidence (1,000 Shodan hits, 21,639 Censys-exposed instances, CVE-2026-25253) underpinning this survey's OpenClaw risk assessment.- [nanobot-architecture-deep-dive](../nanobot/nanobot-architecture-deep-dive.md) — Detailed component breakdown of NanoBot — the audit-friendly alternative whose risk profile Section 3.2 contrasts against OpenClaw.- [clawwork-architecture-deep-dive](clawwork-architecture-deep-dive.md) — Concrete example of an economic-layer agent built on top of NanoBot, illustrating what the lighter alternatives in this survey enable.
