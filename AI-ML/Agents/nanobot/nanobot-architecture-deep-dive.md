# NanoBot Architecture Deep Dive
> **For: Developers & Architects** | **Level: Intermediate → Expert** | **Verified against: HKUDS/nanobot codebase (v0.1.3.post6, Feb 2026)**

---
![NanoBot Minimal Agent Runtime](../../assets/NanoBot-Minimal-Agent-Runtime.png)

---

## TL;DR in One Sentence

NanoBot strips an AI Agent down to its irreducible core: **message → context → LLM → tools → backfill → response** — and every single step is readable, swappable, and traceable.

| Metric | NanoBot | Typical Framework |
|---|---|---|
| Core LOC | ~3,510 lines | 200k–430k lines |
| Startup time | 0.8s | 8–12s |
| Base memory | 45 MB | 200–400 MB |
| GitHub stars | 15.9K | varies |
| Supported channels | 8+ | varies |
| LLM providers | 13+ | varies |

---

## Table of Contents

1. [Mental Model: What Kind of Thing Is This?](#1-mental-model)
2. [The Five Pillars](#2-the-five-pillars)
3. [Full Architecture Diagram](#3-full-architecture-diagram)
4. [Component-by-Component Breakdown](#4-component-breakdown)
   - [MessageBus — The Nervous System](#41-messagebus--the-nervous-system)
   - [AgentLoop — The Brain](#42-agentloop--the-brain)
   - [ContextBuilder — Memory & Identity](#43-contextbuilder--memory--identity)
   - [ToolRegistry — The Hands](#44-toolregistry--the-hands)
   - [Channels — The Ears & Mouth](#45-channels--the-ears--mouth)
   - [Cron & Heartbeat — The Pulse](#46-cron--heartbeat--the-pulse)
5. [Execution Flow: End-to-End Walkthrough](#5-execution-flow-end-to-end)
6. [Data Structures You Must Know](#6-data-structures-you-must-know)
7. [Security Model](#7-security-model)
8. What Got Deleted (and Why)
9. [Known Gaps & Production Risks](#9-known-gaps--production-risks)
10. [How to Extend NanoBot](#10-how-to-extend-nanobot)
11. [Reading Order for the Codebase](#11-reading-order-for-the-codebase)

---

## 1. Mental Model

**Do not call this a chatbot.** Call it what it is: an **Agent Runtime**.

The difference matters:

- A chatbot **responds**. Input → LLM → output. Done.
- An Agent Runtime **acts**. Input → reason → decide → execute tools → reflect → output. Repeat until goal is met.

NanoBot's design philosophy: **close the loop first, add features second.**

> Think of it as a minimal viable skeleton — not a product, not a framework with opinions baked in. It's the smallest possible thing that runs a real agent. You progressively bolt on memory, permissions, and observability.

---

## 2. The Five Pillars

### Accuracy Audit: Claims vs. Code

Before diving in, here's the senior-reviewed verification of every major architectural claim against the actual codebase:

| Feature Claimed | Verification | Verdict |
|---|---|---|
| MessageBus Decoupling | `bus/queue.py` — `InboundMessage`/`OutboundMessage` strictly separate transport from reasoning | ✅ Accurate |
| File-Based Context | `agent/context.py` — explicitly loads `BOOTSTRAP_FILES` at runtime per turn | ✅ Accurate |
| Tool Registry & Schema | `agent/tools/registry.py` — wraps Python classes into JSON Schema; not an if/else chain | ✅ Accurate |
| 0.8s Startup Time | Imports are minimal; no heavy frameworks (pandas, RAG stack) in core `__init__.py` paths | ✅ Plausible |
| Security Guardrails (`ExecTool`) | `agent/tools/shell.py` — deny_patterns implemented, but regex is bypassable. **Document must not imply sufficiency.** | ⚠️ Nuanced |
| Async High Performance | Network I/O is async, but tool execution is **sequential within a session**. Not suitable for high concurrency. | ⚠️ Nuanced |
| Memory Consolidation | `agent/memory.py` — consolidation is a heuristic, not a guaranteed rolling window. Context window exhaustion is a real risk. | ⚠️ Nuanced |

| Pillar | What It Solves | Key File(s) |
|---|---|---|
| **MessageBus** | Decouples channel I/O from agent logic | `nanobot/bus/queue.py`, `events.py` |
| **AgentLoop** | Drives the LLM ↔ Tools reasoning cycle | `nanobot/agent/loop.py` |
| **ContextBuilder** | Assembles identity, rules, memory into system prompt | `nanobot/agent/context.py` |
| **ToolRegistry** | Unified plugin system with JSON Schema validation | `nanobot/agent/tools/registry.py` |
| **Cron/Heartbeat** | Makes agent proactive — acts without waiting for user | `nanobot/cron/`, `nanobot/heartbeat/` |

Every other file in the repo is support infrastructure for these five.

---

## 3. Full Architecture Diagram

### System-Level Overview

```mermaid
graph TB
    subgraph INPUTS["📥 Input Layer (Channels)"]
        TG[Telegram<br/>long polling]
        DC[Discord<br/>WebSocket]
        WA[WhatsApp<br/>Node.js bridge]
        SL[Slack<br/>WebSocket]
        EM[Email<br/>IMAP/SMTP]
        CR[Cron / Heartbeat<br/>system injected]
    end

    subgraph BUS["🔀 Message Bus (Decoupling Layer)"]
        IQ[inbound: asyncio.Queue<br/>InboundMessage]
        OQ[outbound: asyncio.Queue<br/>OutboundMessage]
    end

    subgraph CORE["🧠 Agent Core"]
        AL[AgentLoop<br/>loop.py]
        CB[ContextBuilder<br/>context.py]
        TR[ToolRegistry<br/>tools/registry.py]
        SS[SessionStore<br/>JSONL history]
        MS[MemoryStore<br/>MEMORY.md / daily notes]
    end

    subgraph TOOLS["🛠️ Tool Layer"]
        FS[Filesystem<br/>read/write/edit/list]
        SH[Shell / ExecTool<br/>commands + deny list]
        WB[Web<br/>search + fetch]
        MC[MCP Client<br/>external tool servers]
        SP[SpawnTool<br/>subagents]
    end

    subgraph LLM["🤖 LLM Providers"]
        LT[LiteLLM<br/>OpenRouter / Anthropic<br/>OpenAI / Gemini / Groq]
        VL[vLLM<br/>local models]
    end

    subgraph CTX["📁 File-Based Context (Workspace)"]
        AG[AGENTS.md]
        SO[SOUL.md]
        US[USER.md]
        TO[TOOLS.md]
        ID[IDENTITY.md]
        ME[memory/]
        SK[skills/]
    end

    TG & DC & WA & SL & EM --> IQ
    CR -->|inject system message| IQ
    IQ --> AL
    AL --> CB
    CB --> CTX
    CB -->|assembled system prompt| AL
    AL --> SS
    AL --> MS
    AL --> TR
    TR --> TOOLS
    AL <-->|messages + tool schemas| LLM
    TOOLS -->|tool results| AL
    AL --> OQ
    OQ --> TG & DC & WA & SL & EM

    style INPUTS fill:#e8f4fd,stroke:#2196F3
    style BUS fill:#fff3e0,stroke:#FF9800
    style CORE fill:#f3e5f5,stroke:#9C27B0
    style TOOLS fill:#e8f5e9,stroke:#4CAF50
    style LLM fill:#fce4ec,stroke:#E91E63
    style CTX fill:#f9fbe7,stroke:#8BC34A
```

---

### The AgentLoop in Detail

```mermaid
flowchart TD
    START([New InboundMessage\narrives from bus]) --> SESSION
    SESSION[Load or create Session\nfetch last N messages from JSONL] --> CONTEXT
    CONTEXT[ContextBuilder assembles\nsystem prompt:\nIDENTITY + SOUL + USER +\nAGENTS + TOOLS + MEMORY] --> PACK

    PACK["Pack messages array:\n[system_prompt]\n+ history[]\n+ current_user_message"] --> LLM_CALL

    LLM_CALL[Call LLM Provider\npass tool schemas as\nfunction definitions] --> RESPONSE

    RESPONSE{LLM response\ncontains tool_calls?}

    RESPONSE -->|YES| EXECUTE
    RESPONSE -->|NO| FINAL

    EXECUTE[Execute each tool call\nvia ToolRegistry] --> VALIDATE
    VALIDATE{Parameter\nvalidation passes?}
    VALIDATE -->|FAIL| ERROR_MSG[Convert error\nto readable string]
    VALIDATE -->|PASS| RUN_TOOL[Run tool.execute]
    RUN_TOOL --> RESULT[Append ToolResult\nas tool role message]
    ERROR_MSG --> RESULT
    RESULT --> ITER_CHECK

    ITER_CHECK{iteration_count\n< max_iterations\n default 20?}
    ITER_CHECK -->|YES| LLM_CALL
    ITER_CHECK -->|NO| FORCE_FINAL[Force stop\nlog warning]

    FINAL[Extract final text content] --> WRITE_SESSION
    FORCE_FINAL --> WRITE_SESSION
    WRITE_SESSION[Write to Session JSONL\n~/.nanobot/sessions/] --> OUTBOUND
    OUTBOUND([Push OutboundMessage\nto bus → Channel]) --> DONE([Done])

    style START fill:#4CAF50,color:#fff
    style DONE fill:#4CAF50,color:#fff
    style RESPONSE fill:#FF9800,color:#fff
    style VALIDATE fill:#FF9800,color:#fff
    style ITER_CHECK fill:#FF9800,color:#fff
    style LLM_CALL fill:#9C27B0,color:#fff
    style EXECUTE fill:#2196F3,color:#fff
```

---

### ContextBuilder File Assembly

```mermaid
flowchart LR
    subgraph DISK["💾 Workspace Files (Disk)"]
        direction TB
        ID2[IDENTITY.md\nname, style]
        SO2[SOUL.md\npersonality, values, limits]
        US2[USER.md\nwho the user is]
        AG2[AGENTS.md\nhow to work]
        TO2[TOOLS.md\ncapability descriptions]
        MEM[memory/MEMORY.md\nlong-term facts]
        DAY[memory/YYYY-MM-DD.md\ntoday's notes]
        SK2[skills/*/SKILL.md\nprogressive loading]
    end

    subgraph CB2["ContextBuilder.build_system_prompt"]
        P1[1. get_identity]
        P2[2. load_bootstrap_files]
        P3[3. get_memory_context]
        P4[4. load_skills\nalways=true only]
        P5[5. join with\n--- separator]
    end

    ID2 --> P1
    SO2 & US2 & AG2 & TO2 --> P2
    MEM & DAY --> P3
    SK2 --> P4
    P1 & P2 & P3 & P4 --> P5
    P5 --> SYS_PROMPT[System Prompt\nfed to LLM]

    style SYS_PROMPT fill:#9C27B0,color:#fff
```

---

### Tool Registration & Execution Flow

```mermaid
sequenceDiagram
    participant LLM as LLM Provider
    participant AL as AgentLoop
    participant TR as ToolRegistry
    participant BT as BaseTool
    participant ET as ExecTool

    AL->>TR: get_schemas()
    TR-->>AL: JSON Schema array for all tools
    AL->>LLM: messages + tool schemas
    LLM-->>AL: tool_call { name:"exec", args:{command:"df -h"} }

    AL->>TR: get_tool("exec")
    TR-->>AL: ExecTool instance

    AL->>BT: validate_params(args)
    BT-->>AL: ✅ valid (or ❌ error string)

    AL->>ET: execute(command="df -h")
    ET->>ET: check deny_patterns (rm -rf, fork bombs…)
    ET-->>AL: stdout result

    AL->>AL: append tool_result to messages[]
    AL->>LLM: messages (now includes tool result)
    LLM-->>AL: final text response
```

---

### Channel Abstraction

```mermaid
classDiagram
    class BaseChannel {
        +channel_id: str
        +bus: MessageBus
        +config: ChannelConfig
        +allowFrom: list[str]
        +start() async
        +stop() async
        +send(msg: OutboundMessage) async
        #_normalize(platform_event) InboundMessage
    }

    class TelegramChannel {
        Uses long polling
        Downloads media to ~/.nanobot/media
        Voice → Whisper transcription (optional)
        Converts Markdown → Telegram HTML
    }

    class DiscordChannel {
        Uses WebSocket Gateway
        Standard discord.py integration
    }

    class WhatsAppChannel {
        Python ↔ Node.js bridge
        Node runs Baileys library
        Communicates via local WebSocket
    }

    class SlackChannel {
        WebSocket long connection
        message_id dedup cache
        Sends reaction on receipt
    }

    BaseChannel <|-- TelegramChannel
    BaseChannel <|-- DiscordChannel
    BaseChannel <|-- WhatsAppChannel
    BaseChannel <|-- SlackChannel
```

---

### Cron & Heartbeat: Proactivity Architecture

```mermaid
flowchart TB
    subgraph CRON["CronService"]
        CJ[~/.nanobot/cron/jobs.json\nstored scheduled tasks]
        CS[CronScheduler\nchecks time each minute]
        CS -->|trigger time hit| INJ1
    end

    subgraph HBEAT["HeartbeatService"]
        HT[Timer: every 30 min]
        HF[Read HEARTBEAT.md]
        HT --> HF
        HF -->|has pending items| INJ2
        HF -->|empty| SKIP[do nothing]
    end

    INJ1[Inject InboundMessage\nas 'system' sender] --> IQ2[MessageBus inbound queue]
    INJ2[Inject InboundMessage\nas 'heartbeat' sender] --> IQ2

    IQ2 --> AL2[AgentLoop\nsame pipeline as user messages]
    AL2 --> RESP[Response delivered\nto configured channel]

    style IQ2 fill:#FF9800,color:#fff
    style AL2 fill:#9C27B0,color:#fff
```

---

## 4. Component Breakdown

### 4.1 MessageBus — The Nervous System

**File:** `nanobot/bus/queue.py` + `nanobot/bus/events.py`

**The problem it solves:** Without a bus, every channel must know how the agent works, and the agent must know every channel's message format. That creates N×M coupling.

**The solution:**

```
Telegram  ──┐
Discord   ──┤──→ [ inbound Queue ] ──→ AgentLoop ──→ [ outbound Queue ] ──→ ChannelManager
WhatsApp  ──┘                                                                      │
                                                                          ┌─────────┘
                                                                   dispatches by channel_id
```

**Key design:** All platform-specific messages are normalized into `InboundMessage`. The agent never touches raw Telegram or Discord objects.

```python
# nanobot/bus/events.py (conceptual)
@dataclass
class InboundMessage:
    channel: str        # "telegram", "discord", "cron", etc.
    sender_id: str
    chat_id: str
    content: str
    attachments: list   # media, files

@dataclass
class OutboundMessage:
    channel: str
    chat_id: str
    content: str
```

**Why the queue matters:** Adding rate limiting, audit logging, or message prioritization happens at the queue layer — zero changes to the agent or channels.

---

### 4.2 AgentLoop — The Brain

**File:** `nanobot/agent/loop.py`

This is the only file you truly need to understand. Everything else serves it.

**The loop, simplified:**

```python
# Pseudocode of AgentLoop._run()
while True:
    message = await bus.inbound.get()
    session = load_or_create_session(message)
    history = session.get_recent(N)

    system_prompt = context_builder.build_system_prompt()
    messages = [system_prompt] + history + [message]

    for iteration in range(max_iterations):  # default: 20
        response = await llm.generate(messages, tools=registry.get_schemas())

        if not response.tool_calls:
            break  # LLM is done reasoning

        for tool_call in response.tool_calls:
            result = registry.execute(tool_call)  # validate + run
            messages.append(tool_result(result))  # backfill

    session.save(messages)
    await bus.outbound.put(OutboundMessage(response.content))
```

**The critical insight:** LLM never "does" anything — it only decides what tools to call. Tools do the actual work. Results flow back as evidence. The LLM's final response is grounded in real execution output, not hallucinated results.

**`max_iterations` guard:** Without this cap, a confused model can call tools in an infinite loop. 20 iterations is enough for complex tasks while preventing runaway loops.

---

### 4.3 ContextBuilder — Memory & Identity

**File:** `nanobot/agent/context.py`, `nanobot/agent/memory.py`

**Core idea:** The agent's "personality," rules, and memory live in **plain text files on disk**. The LLM receives them as part of the system prompt every turn.

```
BOOTSTRAP_FILES = ["AGENTS.md", "SOUL.md", "USER.md", "TOOLS.md", "IDENTITY.md"]
```

**Why files instead of hardcoded config?**

| Benefit | Explanation |
|---|---|
| Version control | Git tracks when a rule was added and why |
| Hot-editable | Change `SOUL.md`, next message gets new personality — no restart |
| Human-readable | Non-engineers can edit agent behavior directly |
| Portable | Copy the files, copy the agent |

**Memory layers:**

| Layer | File | Use Case |
|---|---|---|
| Long-term | `memory/MEMORY.md` | Persistent facts about the user, preferences, ongoing projects |
| Daily notes | `memory/YYYY-MM-DD.md` | What happened today, session summaries |
| History | `HISTORY.md` | Append-only log for audit / replay |

**Skill progressive loading:** Not all skills are injected into the system prompt upfront (which would bloat context). Instead:

- Skills marked `always=true` → loaded into prompt
- Other skills → only name + description in prompt
- When the agent needs a skill → it reads the `SKILL.md` file itself via `read_file` tool

---

### 4.4 ToolRegistry — The Hands

**Files:** `nanobot/agent/tools/registry.py`, `tools/base.py`, `tools/filesystem.py`, `tools/shell.py`, `tools/web.py`

**The problem with naive tool implementations:** Tools become scattered `if-else` chains. Parameter parsing is convention-based. Errors blow up the whole loop.

**NanoBot's approach — tools as registered plugins:**

```python
# All tools look the same to AgentLoop
class BaseTool:
    name: str
    description: str
    parameters: dict  # JSON Schema

    def validate_params(self, args: dict) -> str | None:
        # Returns error string or None
        ...

    async def execute(self, **kwargs) -> str:
        # Always returns a string (even errors)
        ...
```

```python
# Registration is explicit
registry.register(ReadFileTool())
registry.register(WriteFileTool())
registry.register(ExecTool(workspace=config.workspace))
registry.register(WebSearchTool(api_key=config.brave_key))
registry.register(SpawnTool(subagent_manager))
```

**Built-in tools:**

| Tool | File | What It Does |
|---|---|---|
| `read_file` | `filesystem.py` | Read file content |
| `write_file` | `filesystem.py` | Write/overwrite file |
| `edit_file` | `filesystem.py` | Targeted string replacement |
| `list_dir` | `filesystem.py` | Directory listing |
| `exec` | `shell.py` | Run shell commands |
| `web_search` | `web.py` | Brave Search API |
| `web_fetch` | `web.py` | HTTP fetch, returns structured JSON |
| `message` | `message.py` | Send message to a specific channel |
| `spawn` | `spawn.py` | Launch a subagent |

**`web_fetch` returns structured JSON, not raw HTML:**

```json
{
  "finalUrl": "https://example.com/page",
  "status": 200,
  "extractor": "readability",
  "truncated": false,
  "text": "Extracted article body..."
}
```

This is intentional — the model needs to know if the page redirected, if content was truncated, and what extractor was used. Returning raw HTML would be noise.

---

### 4.5 Channels — The Ears & Mouth

**Files:** `nanobot/channels/`

**Architectural role:** Channels are boundary adapters. Their only job is to normalize platform-specific events into `InboundMessage` and send `OutboundMessage` back.

**Channel implementation details:**

| Channel | Protocol | Notable Detail |
|---|---|---|
| **Telegram** | Long polling | Voice → optional Groq/Whisper transcription; Markdown → safe HTML |
| **Discord** | WebSocket Gateway | Standard `discord.py` |
| **WhatsApp** | Node.js bridge via local WebSocket | Uses `Baileys` library; voice not supported from bridge side |
| **Slack** | WebSocket | message_id dedup cache; sends reaction as "read receipt" |
| **Email** | IMAP/SMTP | Full async polling |
| **Cron/Heartbeat** | Internal injection | Sends message directly to inbound queue, bypassing channel |

**⚠️ Security note on `allowFrom`:** If `allowFrom` is empty, `BaseChannel` defaults to accepting messages from anyone. In a production multi-channel deployment, treat `allowFrom` as a hard security boundary, not optional config.

---

### 4.6 Cron & Heartbeat — The Pulse

**Files:** `nanobot/cron/`, `nanobot/heartbeat/`

**The problem:** Most agents are reactive — they wait for a human. NanoBot solves this with two mechanisms.

**Cron — explicit scheduled tasks:**

```bash
# CLI interface
nanobot cron add --name "daily-standup" --message "Summarize my tasks" --cron "0 9 * * *"
nanobot cron list
nanobot cron remove <job_id>
```

Jobs are stored in `~/.nanobot/cron/jobs.json`. When triggered, `CronService` injects an `InboundMessage` as if a user sent it — AgentLoop processes it identically to real user input.

**Heartbeat — lightweight periodic check-in:**

`HeartbeatService` wakes every 30 minutes and reads `HEARTBEAT.md`. If the file has pending items, it triggers the agent. If not, nothing happens. This is a deliberate design choice — the interface for proactivity is a single markdown file, not a complex workflow DSL.

**Subagent Spawn:**

For complex or long-running tasks, the main agent can `spawn` a subagent. The subagent is an isolated `AgentLoop` with **fewer tools** (no `message` tool, no `spawn` tool). The absence of the `spawn` tool is a deliberate safety design in `subagent.py` — it prevents infinite recursive spawning. This is a smart constraint worth preserving; contributors should not add `spawn` back to the subagent tool set without implementing a depth/budget guard first.

```
Main Agent → SpawnTool → SubagentManager → Isolated AgentLoop
                                                   ↓ (result done)
Main Agent ← system message ← MessageBus ──────────┘
```

---

## 5. Execution Flow: End-to-End

**Scenario:** User sends "Check disk usage and summarize for me" via Telegram.

```
Step 1: INGESTION
  TelegramChannel receives update
  → normalizes to InboundMessage(channel="telegram", content="Check disk usage...")
  → pushes to bus.inbound queue

Step 2: PICKUP
  AgentLoop.inbound.get() wakes up
  → loads session (or creates new one)
  → fetches last N messages from JSONL history

Step 3: CONTEXT ASSEMBLY
  ContextBuilder.build_system_prompt():
  → reads IDENTITY.md, SOUL.md, USER.md, AGENTS.md, TOOLS.md
  → reads memory/MEMORY.md + today's daily note
  → packages into single system prompt string

Step 4: FIRST LLM CALL
  messages = [system_prompt] + history + [user_message]
  → LLM receives tool schemas for all registered tools
  → LLM responds: tool_call { name:"exec", args:{command:"df -h"} }

Step 5: TOOL EXECUTION
  ToolRegistry.get_tool("exec")
  → validate_params({ command: "df -h" }) → passes
  → ExecTool.execute(command="df -h")
  → check deny_patterns: "df -h" is safe ✅
  → runs subprocess, captures stdout
  → returns: "Filesystem      Size  Used Avail Use%\n/dev/sda1  100G  45G  55G  45%"

Step 6: BACKFILL
  messages.append(tool_result("Filesystem Size Used..."))
  iteration_count = 1 (< 20, continue)

Step 7: SECOND LLM CALL
  LLM receives messages + tool result
  → no more tool calls needed
  → returns: "Your disk is 45% full (45GB used of 100GB). Plenty of space available."

Step 8: PERSIST & RESPOND
  session.save(all messages as JSONL)
  bus.outbound.put(OutboundMessage(content="Your disk is 45% full..."))
  TelegramChannel picks up OutboundMessage
  → converts to Telegram-safe HTML
  → sends to user
```

Total time: ~2–4 seconds (network + LLM inference dependent)

---

## 6. Data Structures You Must Know

### InboundMessage

```python
@dataclass
class InboundMessage:
    id: str              # unique message ID
    channel: str         # "telegram" | "discord" | "cron" | "heartbeat"
    sender_id: str       # platform user ID
    chat_id: str         # platform chat/room ID
    content: str         # text content
    attachments: list    # files, images, etc.
    timestamp: datetime
    metadata: dict       # platform-specific extras
```

### Session (JSONL format)

```jsonl
{"session_id": "abc123", "created": "2026-02-18T10:00:00", "channel": "telegram"}
{"role": "user", "content": "Check disk usage", "timestamp": "..."}
{"role": "assistant", "content": null, "tool_calls": [{"name": "exec", "args": {"command": "df -h"}}]}
{"role": "tool", "name": "exec", "content": "Filesystem..."}
{"role": "assistant", "content": "Your disk is 45% full..."}
```

First line = metadata. Each subsequent line = one message turn. This format is human-readable and trivially replayable for debugging.

### Tool Schema (sent to LLM)

```json
{
  "name": "exec",
  "description": "Execute a shell command in the workspace",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "The shell command to execute"
      }
    },
    "required": ["command"]
  }
}
```

---

## 7. Security Model

### ExecTool: Defense-in-Depth (Current State)

> ⚠️ **CRITICAL SECURITY WARNING**
> **Do not run NanoBot with `ExecTool` enabled on a bare-metal host machine with sensitive data.** Run it inside the provided `Dockerfile`/container. The regex deny list below is a minimal speed bump — not a security boundary. A prompt injection attack or a confused LLM can bypass it through hex encoding, indirect shell expansion, or obscure binaries the patterns don't cover.

```python
# shell.py — deny_patterns (coarse-grained guardrails)
DENY_PATTERNS = [
    r"rm\s+-rf\s+/",        # root deletion
    r":\(\)\{.*\}",          # fork bombs
    r"dd\s+if=.*of=/dev",    # disk overwrite
    r"mkfs",                 # filesystem format
    r"chmod\s+777\s+/",      # root permission change
    # ... more patterns
]
```

**Why regex is fragile:** These patterns match *known* dangerous strings. They do not match semantically equivalent commands written differently, piped through `eval`, or executed through a wrapper binary. Treat this as "defense against accidents," not "defense against adversaries."

**What to add before any production or team deployment:**

| Gap | Recommended Supplement |
|---|---|
| Regex-only blocking | Replace with explicit **allowlist** of permitted commands |
| No audit trail | Add **immutable execution log** (append-only, off-host) |
| No confirmation | Add **two-factor confirmation** for destructive operations |
| Workspace unbounded | Set strict `workspace` root with filesystem-level chroot/container boundary |
| No sandboxing | Run the entire agent in a **Docker container** with network and filesystem restrictions |

### Channel `allowFrom`

Controls who can trigger the agent. An empty `allowFrom` list means **anyone can interact**. Treat this as a security boundary, not a UX setting.

---

## 8. What Got Deleted (and Why)

NanoBot is 3,510 lines. A typical framework is 200k–430k lines. Here's what was cut:

| Deleted | Why It's Fine for a Skeleton | Where to Add It |
|---|---|---|
| **Vector database / RAG** | Memory is Markdown files. Fast to set up, enough for most use cases. | Add Pinecone, Milvus, or ChromaDB as a `MemoryStore` replacement |
| **Complex orchestration graph** | The tool calling loop IS the orchestration. Simple while loop suffices. | Add LangGraph-style DAG if you need parallel branches |
| **Frontend / UI** | The "UI" is Telegram, Discord, etc. Already exists. | Build if needed, connect via a Channel adapter |
| **Multi-agent mesh** | `spawn` handles delegation simply. | Upgrade `SubagentManager` for full multi-agent coordination |
| **Permission RBAC** | Not needed for single-user local agent. | Add before team deployment |
| **Retry/backoff strategies** | Tools execute serially, errors returned as strings. | Wrap `BaseTool.execute` with retry decorator |
| **Streaming responses** | Not implemented in core loop. | Add streaming-aware response handling in `AgentLoop` |

---

## 9. Known Gaps & Production Risks

| Gap | Impact | Fix |
|---|---|---|
| `process_direct()` ignores `session_key` | Cron/Heartbeat messages may mix with CLI sessions — **state corruption** | Fix `SubagentManager` to pass correct session_key |
| Memory is flat Markdown | No semantic search; as `MEMORY.md` grows, retrieval degrades | Swap `MemoryStore` for vector DB when content > ~50KB |
| Session path is `~/.nanobot/sessions` | **Not portable across machines; incompatible with serverless (AWS Lambda, Cloud Run) without modifying storage layer** | Make session path configurable, or use a DB backend |
| `allowFrom: []` defaults open | Any user on a connected channel can trigger agent | Always set `allowFrom` before exposing to a team |
| Tool calls are sequential within a session | If `web_fetch` takes 30s, the entire `AgentLoop` instance is blocked. **Architecture optimizes for latency, not throughput — not designed for 10,000 concurrent users on a single instance.** | Implement parallel tool execution; or scale via separate process-per-user |
| No streaming | Users see nothing until full response | Add streaming support for long-running tasks |
| Context window exhaustion | `HISTORY.md` grows unbounded; consolidation in `memory.py` is a heuristic, not a guarantee. Long-running tasks will eventually exceed LLM context limits, causing crashes or massive API cost spikes. | Implement a hard rolling window (last N tokens); use vector search for older history |
| ExecTool on bare metal | Regex deny list is bypassable via prompt injection | **Run inside Docker container** with filesystem + network restrictions |
| Subagent recursion | Subagents cannot spawn their own subagents (enforced in `subagent.py` — no `spawn` tool registered) — this prevents infinite recursion loops. Worth knowing: it's a deliberate constraint, not a missing feature. | This is intentional; document clearly for contributors |

---

## 10. How to Extend NanoBot

### Adding a New Tool (5 steps)

```python
# Step 1: Create the tool class
# nanobot/agent/tools/my_tool.py
from .base import BaseTool

class StockPriceTool(BaseTool):
    name = "get_stock_price"
    description = "Fetch the current stock price for a given ticker symbol"
    parameters = {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
            }
        },
        "required": ["ticker"]
    }

    async def execute(self, ticker: str) -> str:
        # Your implementation
        price = await fetch_price(ticker)
        return f"{ticker}: ${price:.2f}"

# Step 2: Register in AgentLoop._register_default_tools()
self.tools.register(StockPriceTool())

# Step 3: Update TOOLS.md to describe the new capability
# Step 4: Test via CLI: nanobot chat
# Step 5: Done — LLM will discover and call it automatically via schema
```

### Adding a New Channel

```python
# nanobot/channels/my_channel.py
from .base import BaseChannel
from ..bus.events import InboundMessage, OutboundMessage

class MyChannel(BaseChannel):
    async def start(self):
        # Subscribe to your platform's events
        async for event in my_platform.events():
            msg = self._normalize(event)
            await self.bus.inbound.put(msg)

    def _normalize(self, event) -> InboundMessage:
        return InboundMessage(
            channel="my_platform",
            sender_id=event.user_id,
            chat_id=event.room_id,
            content=event.text
        )

    async def send(self, msg: OutboundMessage):
        await my_platform.send(msg.chat_id, msg.content)
```

### Upgrading Memory to Vector Store

```python
# Replace MemoryStore with a vector-backed implementation
class VectorMemoryStore(MemoryStore):
    def __init__(self, client: PineconeClient):
        self.client = client

    def get_memory_context(self, query: str) -> str:
        # Semantic search instead of full file read
        results = self.client.query(query, top_k=5)
        return "\n".join(r.text for r in results)
```

---

## 11. Reading Order for the Codebase

Follow this order. Do not skip ahead.

```
1. nanobot/bus/events.py
   → Understand InboundMessage / OutboundMessage
   → These two classes flow through the entire system

2. nanobot/agent/loop.py
   → Read the main loop end to end
   → Trace every variable: where does it come from? where does it go?

3. nanobot/agent/context.py
   → Understand how the system prompt gets assembled
   → Open AGENTS.md, SOUL.md in your workspace to see what feeds in

4. nanobot/agent/tools/base.py + registry.py
   → Understand BaseTool interface
   → See how registry converts Python classes to JSON Schema

5. nanobot/agent/tools/shell.py
   → Read ExecTool, especially deny_patterns
   → This is where security happens (or doesn't)

6. nanobot/cron/service.py + nanobot/heartbeat/service.py
   → See how proactivity injects into the bus
   → Connects back to loop.py (same pipeline)

7. nanobot/channels/telegram.py
   → A complete, real channel implementation to reference
   → Then read others as needed

8. nanobot/agent/subagent.py
   → Read last — it's a subset of the main loop with fewer tools
```

---

## Summary: The Architecture in One Paragraph

NanoBot implements an AI Agent as a minimal pipeline: messages arrive from any channel (Telegram, Discord, Slack, etc.) and get normalized into `InboundMessage` objects pushed onto an async queue. `AgentLoop` consumes the queue, assembles a system prompt from version-controlled Markdown files on disk, packs it with conversation history, and calls the LLM with a full set of JSON Schema tool definitions. If the LLM returns tool calls, `ToolRegistry` validates parameters and executes each tool — filesystem, shell, web, or subagent spawning — backfilling results into the message list so the LLM can reason from real evidence. When the LLM stops calling tools, the final response is persisted to a JSONL session file and pushed to the outbound queue for the originating channel to deliver. `CronService` and `HeartbeatService` inject messages directly into the inbound queue on schedule, making the agent proactive. The whole thing is ~3,510 lines, starts in 0.8 seconds, and uses 45 MB of memory — because everything unnecessary has been deliberately removed.

---

*Repository: [https://github.com/HKUDS/nanobot](https://github.com/HKUDS/nanobot) | Version: v0.1.3.post6 | Verified: February 2026*
