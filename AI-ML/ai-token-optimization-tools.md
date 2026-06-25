# AI Token Optimization Tools — Consolidated Comparison

> A reference guide covering **Lean-CTX**, **RTK**, **Headroom**, **Caveman**, **Serena MCP**, **Ponytail**, **MCP-Compressor**, **Tulbase**, **LLMLingua-2**, and **Codebase-Memory** for AI coding agents (Claude Code, Cursor, Copilot, etc.)

---

## Quick Summary

| Tool | What It Is | Best For | Avg. Token Savings |
|---|---|---|---|
| **Lean-CTX** | MCP server — AST-based context intelligence | Large codebases with repeated file reads | 60%–99% |
| **RTK** | CLI proxy — terminal output filter | Shell-heavy workflows with noisy command output | 60%–90% |
| **Headroom** | Network proxy — multi-format payload compressor | Mixed workloads: logs, JSON, code, multi-agent | 50%–90% |
| **Caveman** | Prompt skill — conversational fluff remover | Quick interactive chat sessions | 60%–75% on output |
| **Serena MCP** | MCP server — LSP-driven semantic code navigator | Massive codebases needing symbol-level intelligence | Varies (precision, not bulk) |
| **Ponytail** | Agent skill — code minimalism enforcer | Preventing AI from over-generating code | 54% avg code reduction (up to 94%) |
| **MCP-Compressor** | MCP proxy — tool definition shrinker | Agents with many MCP servers connected | 70%–97% on tool definitions |
| **Tulbase** | MCP server — local-first context compression | Lightweight local compression alternative | Varies |
| **LLMLingua-2** | Research library — perplexity-based prompt compression | Custom pipelines needing deep compression | Up to 20× compression |
| **Codebase-Memory** | MCP server — Tree-sitter knowledge graph | Code graph navigation with minimal tokens | ~10× fewer tokens |

---

## 1. Lean-CTX

**GitHub:** `yvgude/lean-ctx`
**Architecture:** Rust binary running as an MCP server

### How It Works
- Uses **Tree-sitter AST parsing** across 18+ languages to rewrite dense function bodies into concise signatures
- Maintains a **local Property Graph** mapping project dependencies — sends only what matters, not whole files
- Implements a **~13-token file read cache** for subsequent turns (re-reads cost almost nothing)
- Maintains **persistent session state** across conversations

### Pros
- ✅ Holistic approach: handles files, searches, and terminal output in one tool
- ✅ Up to **99% savings on cached re-reads** — massive ROI on repeatedly accessed files
- ✅ Works across **70+ agents** via standard MCP integration
- ✅ Cross-session memory — context persists between conversations
- ✅ Syntax-aware: strips redundant comments and boilerplate without destroying logic

### Cons
- ❌ May **overly condense** important structural information (e.g., diffs, variable contexts in legacy code)
- ❌ Can cause agents to struggle with **complex code reviews** if compression is too aggressive
- ❌ Limited to **18 languages** via Tree-sitter (vs. 40+ for Serena via LSP)

---

## 2. RTK

**Architecture:** Shell hook / wrapper acting as a CLI proxy

### How It Works
- Intercepts and filters **terminal/shell output** before it reaches the agent context
- Dynamically strips noisy build logs, test output, and package manager dumps
- Minimal setup — install the hook and it works automatically

### Pros
- ✅ **Fastest and simplest** setup for shell-heavy workflows
- ✅ Effective at eliminating token waste from `git log`, `npm install`, test runners, etc.
- ✅ Zero configuration overhead — install and forget

### Cons
- ❌ **Shell-only scope** — does nothing for large file reads or repository indexing
- ❌ No persistent memory between commands
- ❌ Primarily suited for **shell-heavy workflows** — limited value for code-centric agents
- ❌ Still burns tokens on initial repo context indexing

---

## 3. Headroom

**GitHub:** `chopratejas/headroom`
**Creator:** Tejas Chopra, Senior Engineer at Netflix
**Stars:** 29.5K+ (as of June 2026)
**Architecture:** Local network proxy (Python library) sitting between agent and LLM API

### How It Works
Uses a **three-stage optimization pipeline:**

1. **Cache Aligner** — Moves dynamic fields (timestamps, UUIDs) to the end of context to maximize prefix cache hits
2. **Content Router** — Routes data to specialized compressors by type: JSON, code (via Tree-sitter for ~8 core languages), DOM/HTML, terminal logs
3. **Reversible Compression (CCR)** — Compresses payload, stores original locally in SQLite/Redis; LLM can call `headroom_retrieve` to fetch raw data if needed

### Pros
- ✅ **Truly reversible compression** — no information is permanently lost
- ✅ Works globally and transparently across **multiple tools and agents**
- ✅ Addresses **prefix cache misses** — a hidden cost most tools ignore
- ✅ Strong for mixed payloads: JSON blobs, thick logs, raw DB responses, code
- ✅ Collective impact: users have saved **200B+ tokens (~$700K)**
- ✅ Minimal to zero code changes required to integrate
- ✅ Tree-sitter code compression available (gated, off by default for safety)
- ✅ Native integrations: LangChain, Agno, Strands, LiteLLM, Vercel AI SDK

### Cons
- ❌ Tree-sitter code compression is **disabled by default** and requires explicit config (`HEADROOM_CODE_AWARE_ENABLED=true`)
- ❌ Code compression auto-skips on review/debug/explain intents and recent edits — can feel unpredictable
- ❌ Python-based — adds a runtime dependency vs. Lean-CTX's Rust binary
- ❌ Supports only **~8 core languages** for code-aware compression

### Tree-sitter in Headroom (Clarification)
Headroom **does** use Tree-sitter internally via its `CodeCompressor` module, but it is protected by safety guardrails:
- Auto-disabled if user intent includes "explain," "review," or "debug"
- Skipped if the code was modified/read within the last 4 turns
- Skipped for snippets under 50 words

---

## 4. Caveman

**GitHub:** `juliusbrussee/caveman` | **Site:** `getcaveman.dev`
**Architecture:** Prompt-engineering skill / system prompt injection

### How It Works
- Injects a **system prompt modifier** that instructs the LLM to skip conversational preambles and respond in ultra-terse style ("Auth middleware broken. Fix line 12.")
- Modifies **output tokens only** — does not touch input files, logs, or code
- Non-reversible (output format change only)

### Pros
- ✅ **Zero configuration** — no installation, no proxy, no runtime
- ✅ Dramatically reduces typing latency in interactive sessions
- ✅ Cuts discursive/polite AI filler by up to **75%**
- ✅ Pairs well with Lean-CTX or Headroom (complementary, not overlapping)
- ✅ Works in any chat interface

### Cons
- ❌ **Minimal total impact** — only ~4–10% overall token reduction (output-only)
- ❌ Non-reversible format change — terse output may be unsuitable for documentation or explanation tasks
- ❌ Does absolutely nothing for input token costs (file reads, logs, codebase indexing)
- ❌ Not suitable for autonomous terminal agents — best only for interactive chat

---

## 5. Serena MCP

**Architecture:** MCP server with LSP (Language Server Protocol) integration + optional JetBrains plugin backend

### How It Works
- Indexes the project using **LSP** to understand symbols, references, call graphs, and types
- Sends only **relevant symbols and file portions** — not whole files
- Supports **atomic cross-file refactoring** in a single agent call
- Can tap into **JetBrains IDE plugins** (IntelliJ, PyCharm, WebStorm) for deeper analysis

### Pros
- ✅ Broadest language support: **40+ languages** via LSP
- ✅ **Symbol-aware** — understands function call chains, type definitions, and where logic lives
- ✅ Atomic refactoring: cross-file renames and structural moves in one reliable call
- ✅ IDE-level intelligence: unique JetBrains plugin integration
- ✅ Ideal for Java/Go/Rust/TypeScript in large microservice architectures

### Cons
- ❌ Higher setup complexity — requires LSP and optionally IDE plugin configuration
- ❌ Less focused on **bulk compression** — optimizes precision over raw token savings
- ❌ Overkill for small or mid-size codebases where simpler tools suffice
- ❌ JetBrains integration limits portability for non-JetBrains users

---

## 6. Ponytail ⭐ New & Trending

**GitHub:** `DietrichGebert/ponytail`
**Creator:** Dietrich Gebert
**Stars:** 38.5K+ (trending #2 on GitHub as of June 2026)
**Architecture:** Agent skill / always-on rule injection (works across Claude Code, Codex, Cursor, Windsurf, Cline, Aider, Copilot, Gemini)

### How It Works
- Injects a **six-rung decision ladder** into every agent session, forcing agents to think before writing code:
  1. **YAGNI** — Does this need to exist at all?
  2. **Stdlib** — Does the standard library already cover it?
  3. **Native platform** — Is there a built-in browser/OS feature?
  4. **Existing dependency** — Does an installed package do this?
  5. **Minimal custom** — Can it be done in under 20 lines?
  6. **Full build** — Only if all above fail
- Rule re-injects every turn — the "lazy senior dev" constraint is always active
- Compounding effect: less code generated now = less code read back in future turns

### Pros
- ✅ **Unique angle** — attacks token waste at *generation time*, not compression time
- ✅ Up to **94% less code** in over-build scenarios (54% average)
- ✅ **100% safety score** on adversarial test tier — doesn't drop guard cases
- ✅ Slash commands: `/ponytail-debt`, `/ponytail-audit`, `/ponytail-gain` for visibility into savings
- ✅ Works in all major agents — widest compatibility of any tool here
- ✅ Includes a behavior evaluation framework to verify the ruleset actually fires
- ✅ Zero infrastructure — no proxy, no binary, no runtime

### Cons
- ❌ **Output style only** — does not compress existing context or file reads
- ❌ Terse output can conflict with tasks that need thorough explanations or documentation
- ❌ Relies on the agent respecting injected rules — can be inconsistent with weaker models
- ❌ Does not address token costs from reading large existing codebases

> **Key distinction:** Ponytail prevents bloat from being *created*. All other tools compress bloat that *already exists*. Use both together for maximum effect.

---

## 7. MCP-Compressor ⭐ New

**GitHub:** `atlassian-labs/mcp-compressor`
**Creator:** Atlassian Labs (open source)
**Architecture:** MCP proxy wrapper — available in TypeScript, Python, and Rust

### How It Works
- Wraps existing MCP servers via **stdio, HTTP, or SSE** protocols
- Compresses **tool definition schemas** into a two-step interface: browse compressed summaries first, expand full schema only when needed
- No external data files required
- Targets the "context suicide" problem: connecting many MCP servers balloons tool definition tokens before any real work starts

### Pros
- ✅ **Fills a gap no other tool covers** — specifically targets MCP tool definition bloat
- ✅ **70–97% reduction** in tool definition tokens
- ✅ Schema-based tool calling is preserved — agents still call tools correctly
- ✅ Available in three languages (TS, Python, Rust) — easy to integrate into any stack
- ✅ Transparent wrapper — existing MCP servers need no changes
- ✅ Backed by Atlassian Labs — production-grade quality and maintenance

### Cons
- ❌ Addresses **only tool definitions**, not payload content or file reads
- ❌ Adds a proxy hop — slight latency overhead per tool call
- ❌ Relatively new (Jan 2026) — ecosystem integrations still maturing

> **When this matters most:** If you have 5+ MCP servers connected (Jira, GitHub, Confluence, DB tools, etc.), tool definitions alone can consume 50K–100K+ tokens per session. This is the tool for that problem.

---

## 8. Tulbase

**Site:** `compre.sh` | MIT licensed open-source core
**Architecture:** MCP server — local-first context compression for LLM agents

### How It Works
- Runs as a local MCP server, compressing context before it reaches the LLM
- Open-source core pairs with **Compresh** (compre.sh) paid tier for Q-protective ranking (quality-preserving compression prioritization)
- Local-first design — data does not leave the machine

### Pros
- ✅ **Privacy-first** — fully local, no data sent to external services
- ✅ MIT licensed open-source core with a clear upgrade path
- ✅ MCP-native — drop-in for any MCP-compatible agent

### Cons
- ❌ **Early-stage** — less battle-tested than Headroom or Lean-CTX
- ❌ Advanced features (Q-protective ranking) require the paid Compresh tier
- ❌ Smaller community and documentation than established tools
- ❌ Savings figures not independently benchmarked yet

---

## 9. LLMLingua / LLMLingua-2

**GitHub:** `microsoft/LLMLingua`
**Creator:** Microsoft Research
**Architecture:** Python library — small LM-based token perplexity compression

### How It Works
- Uses a **small language model** (GPT-2 or LLaMA-7B) to compute perplexity of each prompt token
- Removes tokens with low perplexity (low information content) using a coarse-to-fine strategy:
  1. **Budget Controller** — allocates compression ratios across prompt segments (instructions, examples, questions)
  2. **Token-level compression** — iteratively removes low-info tokens while preserving dependencies
  3. **Distribution alignment** — bridges gap between compressor model and target LLM
- **LLMLingua-2** adds task-agnostic compression via data distillation from GPT-4, framing compression as a token classification problem

### Pros
- ✅ Most **academically rigorous** approach — extensively peer-reviewed and benchmarked
- ✅ Up to **20× compression ratio** with minimal performance degradation
- ✅ Task-agnostic (LLMLingua-2) — works across diverse prompt types, not just code
- ✅ Proven on standard benchmarks: GSM8K, BBH, ShareGPT, NaturalQuestions
- ✅ LongLLMLingua variant handles RAG scenarios — 21.4% performance *improvement* with 4× fewer tokens

### Cons
- ❌ **Not plug-and-play** — requires integrating a compression model into your pipeline
- ❌ The compressor model itself consumes compute and adds latency
- ❌ Not designed for IDE agent workflows (Claude Code, Cursor) — better suited for custom LLM applications
- ❌ Requires Python environment and model weights; heavy dependency footprint
- ❌ No MCP integration or agent-native tooling

> **Bottom line:** LLMLingua is the right pick if you're *building* an LLM application and control the full pipeline. It's not for developers who just want to optimize their daily Claude Code or Cursor sessions.

---

## 10. Codebase-Memory (via MCP)

**Paper:** arXiv:2603.27277
**Architecture:** MCP server exposing a Tree-sitter knowledge graph of the codebase

### How It Works
- Builds a **pre-indexed semantic knowledge graph** of the entire repository using Tree-sitter
- Exposes the graph via MCP — agents query for specific functions, types, call chains instead of reading raw files
- Implements a "**pointers over copies**" philosophy: agent gets a reference to a definition, not the entire file

### Pros
- ✅ **~10× fewer tokens** than file-dump approaches — verified across 31 repositories
- ✅ Complements Serena MCP and Lean-CTX — different indexing strategy
- ✅ MCP-native — works with any MCP-compatible agent
- ✅ Pre-indexed — fast lookups with no per-query parsing overhead

### Cons
- ❌ Requires an initial indexing pass — not instant on first use
- ❌ Index can become stale on fast-moving codebases — needs re-indexing strategy
- ❌ Research project origin — production readiness varies
- ❌ Overlaps significantly with Serena MCP and Lean-CTX; pick one for code graph duties

---

## Decision Guide

```
Is your token problem mainly...

Noisy terminal / shell output?
  → RTK (fastest fix, zero config)

Large file reads and repeated codebase indexing?
  → Lean-CTX (deep AST compression + re-read cache)

Mixed payloads (logs + JSON + code) across multiple agents?
  → Headroom (global proxy, reversible, cache-aware)

AI chattiness and conversational filler in interactive sessions?
  → Caveman (output trimmer, pairs with any other tool)

Finding logic across a massive codebase / Java microservices?
  → Serena MCP (symbol-level precision, LSP-powered)

AI generating bloated, over-engineered code?
  → Ponytail (prevents token waste at generation time)

Too many MCP servers ballooning tool definition tokens?
  → MCP-Compressor (Atlassian Labs — compresses tool schemas)

Privacy-first local-only compression?
  → Tulbase (local MCP server, MIT core)

Building a custom LLM pipeline needing deep prompt compression?
  → LLMLingua-2 (Microsoft Research, up to 20× compression)

Code graph navigation with minimal tokens?
  → Codebase-Memory (Tree-sitter knowledge graph via MCP)
```

---

## Layer Model

These tools operate at distinct layers — most can be combined without conflict:

```
┌─────────────────────────────────────────────────────────┐
│  GENERATION LAYER (what the agent writes)               │
│  → Ponytail                                             │
├─────────────────────────────────────────────────────────┤
│  TOOL DEFINITION LAYER (MCP schema tokens)              │
│  → MCP-Compressor                                       │
├─────────────────────────────────────────────────────────┤
│  CODE INTELLIGENCE LAYER (how code is read/navigated)   │
│  → Serena MCP · Lean-CTX · Codebase-Memory             │
├─────────────────────────────────────────────────────────┤
│  PAYLOAD COMPRESSION LAYER (logs, JSON, RAG, history)   │
│  → Headroom · Tulbase · LLMLingua-2                     │
├─────────────────────────────────────────────────────────┤
│  SHELL OUTPUT LAYER (terminal noise)                    │
│  → RTK                                                  │
├─────────────────────────────────────────────────────────┤
│  OUTPUT FORMAT LAYER (AI verbosity)                     │
│  → Caveman                                              │
└─────────────────────────────────────────────────────────┘
```

---

## Recommended Stacks

| Workflow | Recommended Combination |
|---|---|
| Claude Code on large Java/Quarkus repo | **Serena MCP** + **Lean-CTX** + **Ponytail** + **Caveman** |
| Claude Code with many MCP servers | **MCP-Compressor** + **Ponytail** + **Caveman** |
| SRE / DevOps with heavy log analysis | **Headroom** + **Caveman** |
| Shell-heavy CI/CD debugging | **RTK** + **Caveman** |
| Cursor on a mid-size project | **Lean-CTX** + **Ponytail** + **Caveman** |
| Multi-agent framework (mixed I/O) | **Headroom** + **MCP-Compressor** |
| Custom LLM application pipeline | **LLMLingua-2** (standalone, full control) |
| Privacy-sensitive / air-gapped environment | **Tulbase** + **Ponytail** |

---

*Sources: GitHub repositories (DietrichGebert/ponytail, atlassian-labs/mcp-compressor, chopratejas/headroom, yvgude/lean-ctx, microsoft/LLMLingua), Tejas Chopra's Headroom presentation (Netflix), arXiv:2603.27277 (Codebase-Memory), arXiv:2310.06839 (LLMLingua), and community comparisons. Verify specific savings figures in your own environment as they vary by codebase and workflow.*
