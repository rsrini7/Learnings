# NanoBot: Minimalist Agent Runtime Architecture and Execution Internals

Learning note · Revised March 2026 · Agent Runtime Engineering
*By Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

> "A chatbot is an episodic responder: input arrives, the model generates text, and execution halts. An Agent Runtime is an autonomous state machine: input arrives, the model plans, issues tool calls against the environment, observes physical results, and repeats until the objective is achieved. NanoBot strips an agent runtime down to its irreducible core—closing the execution loop in 3,510 lines of transparent, fully auditable Python without heavy framework bloat."

---

## 1. Foundations: The Minimalist Agent Paradigm

Developed by the **HKU Data Intelligence Lab (HKUDS)** at the University of Hong Kong, NanoBot was engineered as an explicit counter-response to monolithic agent frameworks containing hundreds of thousands of lines of code. NanoBot isolates the five universal primitives required to operate an autonomous agent, making every component readable, swappable, and traceable in a single afternoon.

```mermaid
flowchart LR
    A["Inbound Message<br/>(Telegram / Discord / Slack)"] --> B["MessageBus<br/>(Decoupling Queue)"]
    B --> C["AgentLoop<br/>(Reasoning & Execution)"]
    C <--> D["ContextBuilder<br/>(Plaintext Files on Disk)"]
    C <--> E["ToolRegistry<br/>(Dynamic JSON Schema)"]
    F["Cron & Heartbeat<br/>(Proactivity Engine)"] --> B
    C --> G["Outbound Message<br/>(Normalized Delivery)"]
```

### 1.1 Mental Model: Chatbot vs. Autonomous Agent Runtime

| Operational Phase | Conversational Chatbot | Autonomous Agent Runtime (NanoBot) |
| :--- | :--- | :--- |
| **Input Trigger** | User sends message in active UI window | User message, scheduled cron job, or heartbeat check |
| **Execution Loop** | Single-turn feed-forward inference | Multi-turn reasoning loop (`AgentLoop`) with evidence backfill |
| **Environmental Action** | None (read-only text completion) | Direct interaction via tools (filesystem, shell, web APIs) |
| **Context Assembly** | Ephemeral chat array in memory | Plaintext Markdown state (`IDENTITY.md`, `MEMORY.md`, `SOUL.md`) |
| **Termination Criteria** | End-of-sequence token | Model decides task is complete OR hits iteration cap (`max_iterations = 20`) |

### 1.2 Accuracy Audit: Claims vs. Code Verification

A code audit of the `HKUDS/nanobot` repository (v0.1.3.post6) verifies the following architectural mechanisms:

| Architectural Claim | Codebase Verification | Verdict & Engineering Reality |
| :--- | :--- | :--- |
| **MessageBus Decoupling** | `bus/queue.py` & `events.py` strictly decouple transport adapters from reasoning via `asyncio.Queue`. | ✅ **Accurate:** Eliminates $N \times M$ platform coupling. |
| **File-Based Context Assembly** | `agent/context.py` loads `BOOTSTRAP_FILES` from disk dynamically on every turn. | ✅ **Accurate:** Enables live hot-editing of agent rules and memory. |
| **Unified Tool Schema Engine** | `agent/tools/registry.py` inspects Python classes to generate standard OpenAI/Anthropic tool schemas. | ✅ **Accurate:** Zero hardcoded `if/else` execution chains. |
| **0.8-Second Cold Startup** | Core `__init__.py` paths omit heavy dependencies (pandas, langchain, torch, chromadb). | ✅ **Accurate:** Idle base memory is ~45 MB RAM. |
| **Shell Security Guardrails** | `agent/tools/shell.py` enforces regex-based `DENY_PATTERNS`. | ⚠️ **Fragile:** Regex pattern matching is easily bypassed via encoding; Docker containment is mandatory. |
| **Concurrency Characteristics** | Network I/O is async, but tool execution is **strictly sequential per session**. | ⚠️ **Nuanced:** Designed for low latency per user, not thousands of concurrent users on a single node. |
| **Long-Term Memory Scaling** | `agent/memory.py` uses heuristic markdown consolidation without native vector RAG. | ⚠️ **Nuanced:** Context windows will saturate if memory files exceed ~50KB. |

---

## 2. Deep Technical Mechanism: The Five Pillars

Every module in NanoBot supports one of five core architectural pillars:

```
THE FIVE PILLARS OF NANOBOT
├── 1. MessageBus (bus/): Decouples channel transports from agent reasoning
├── 2. AgentLoop (agent/loop.py): Drives multi-turn tool calling and evidence backfill
├── 3. ContextBuilder (agent/context.py): Assembles disk files into the system prompt
├── 4. ToolRegistry (agent/tools/): Provides unified schema generation and validation
└── 5. Cron & Heartbeat (cron/, heartbeat/): Drives proactive background autonomy
```

### 2.1 Pillar 1: MessageBus Decoupling (`queue.py` & `events.py`)

Without a decoupled bus, every messaging channel must understand agent execution internals, and the agent must handle platform-specific message structures. NanoBot eliminates this coupling by normalizing all inputs and outputs:

```mermaid
flowchart TD
    subgraph Ingress["Channel Normalization"]
        T["Telegram Long-Polling"] -->|Normalize| IN_T["InboundMessage"]
        D["Discord Gateway WS"] -->|Normalize| IN_D["InboundMessage"]
        W["WhatsApp Baileys Bridge"] -->|Normalize| IN_W["InboundMessage"]
        S["Slack Socket Mode"] -->|Normalize| IN_S["InboundMessage"]
        E["Email IMAP Poller"] -->|Normalize| IN_E["InboundMessage"]
        C["Cron / Heartbeat Injection"] -->|Normalize| IN_C["InboundMessage"]
    end

    IN_T & IN_D & IN_W & IN_S & IN_E & IN_C --> IQ["bus.inbound: asyncio.Queue[InboundMessage]"]
    
    IQ --> AL["AgentLoop (Consumes Queue Single-Turn)"]
    AL --> OQ["bus.outbound: asyncio.Queue[OutboundMessage]"]

    OQ --> Dispatcher{"Channel Dispatcher<br/>(routes by channel_id)"}
    Dispatcher -->|Telegram| SendT["Telegram API (HTML)"]
    Dispatcher -->|Discord| SendD["Discord API"]
    Dispatcher -->|WhatsApp| SendW["Node.js Baileys Bridge"]
    Dispatcher -->|Slack| SendS["Slack API (Reactions)"]
    Dispatcher -->|Email| SendE["SMTP Client"]
```

```python
# Normalized message primitives from nanobot/bus/events.py
@dataclass
class InboundMessage:
    id: str              # Unique message identifier
    channel: str         # "telegram" | "discord" | "whatsapp" | "slack" | "cron"
    sender_id: str       # Normalized platform user ID
    chat_id: str         # Destination room or conversation ID
    content: str         # Clean textual content
    attachments: list    # Media objects, voice notes, file attachments
    timestamp: datetime
    metadata: dict       # Raw platform headers

@dataclass
class OutboundMessage:
    channel: str
    chat_id: str
    content: str
```

### 2.2 Pillar 2: AgentLoop Reasoning Engine (`loop.py`)

`AgentLoop` is the heartbeat of NanoBot. It drives the model-tool interaction loop, manages sessions, and enforces execution boundaries:

```mermaid
flowchart TD
    Start(["bus.inbound.get() wakes up"]) --> Session["Load Session History<br/>(~/.nanobot/sessions/ JSONL)"]
    Session --> Context["ContextBuilder: Assemble Prompt<br/>(IDENTITY + SOUL + USER + MEMORY)"]
    Context --> Pack["Pack Message Array:<br/>[system_prompt] + history + [current_user_msg]"]

    Pack --> LLMCall["Call LLM Provider with Tool Schemas<br/>(LiteLLM / vLLM)"]
    
    LLMCall --> Branch{"Contains tool_calls?"}
    
    Branch -->|"Yes"| ExecTools["Execute Tools via ToolRegistry"]
    Branch -->|"No (Final Response)"| Persist["Save Session to JSONL"]
    
    ExecTools --> CheckParams{"Params valid?"}
    CheckParams -->|"Pass"| Run["Run tool.execute()"]
    CheckParams -->|"Fail"| Err["Format error string"]
    
    Run --> Backfill["Append ToolResult to Message Array"]
    Err --> Backfill
    
    Backfill --> IterGuard{"Iteration < max_iterations (20)?"}
    IterGuard -->|"Yes"| LLMCall
    IterGuard -->|"No (Cap Hit)"| Warn["Log Warning & Force Terminate"]
    Warn --> Persist
    
    Persist --> OutQueue["Push OutboundMessage to bus.outbound"]
    OutQueue --> Done(["Channel delivers response"])
```

#### Key Engineering Details
- **The Critical Principle:** The LLM never touches the environment directly—it only requests tool calls. Physical execution is handled by Python classes, and output text is appended as evidence before the LLM reasons again.
- **The Iteration Guard (`max_iterations = 20`):** Confused or hallucinatory models can enter infinite tool execution loops. Capping iterations at 20 prevents runaway compute and API billing exhaustion.

### 2.3 Pillar 3: ContextBuilder & Plaintext State (`context.py`)

NanoBot maintains state, memory, and persona entirely in plain text Markdown files on the local filesystem:

```
WORKSPACE CONTEXT DIRECTORY
├── IDENTITY.md    # Operating persona, name, core character traits
├── SOUL.md        # Communication style, humor boundaries, tone constraints
├── USER.md        # Facts about the user, preferences, organizational role
├── TOOLS.md       # Human-readable documentation of environment capabilities
├── AGENTS.md      # Operating instructions and development standards
├── memory/
│   ├── MEMORY.md  # Distilled long-term heuristics and persistent facts
│   └── YYYY-MM-DD.md # Dated daily interaction logs
└── skills/        # Modular extensions (progressive loading)
```

```mermaid
flowchart LR
    subgraph Disk["Local Filesystem (Disk)"]
        ID["IDENTITY.md"]
        SO["SOUL.md"]
        US["USER.md"]
        TO["TOOLS.md"]
        MEM["memory/MEMORY.md"]
        DAY["memory/YYYY-MM-DD.md"]
        SK["skills/*/SKILL.md"]
    end

    subgraph Assembly["ContextBuilder.build_system_prompt()"]
        P1["1. Extract Identity"]
        P2["2. Read Bootstrap Files"]
        P3["3. Load Memory State"]
        P4["4. Ingest Progressive Skills<br/>(always=true only)"]
        P5["5. Join with '---' Delimiters"]
    end

    ID --> P1
    SO & US & TO --> P2
    MEM & DAY --> P3
    SK --> P4
    P1 & P2 & P3 & P4 --> P5
    P5 --> Prompt["Final System Prompt Context"]
```

#### Progressive Skill Loading
To prevent context window bloat, NanoBot does not inject all skills into the system prompt upfront. Only skills flagged `always=true` are embedded. For other skills, only the name and description are listed; the agent uses the `read_file` tool to inspect full skill instructions dynamically when required.

### 2.4 Pillar 4: ToolRegistry Plugin System (`registry.py`)

NanoBot avoids fragile `if/else` tool routing by using a reflection-based registry that dynamically generates standard JSON schemas:

```mermaid
sequenceDiagram
    autonumber
    participant LLM as LLM API (LiteLLM / vLLM)
    participant AL as AgentLoop
    participant TR as ToolRegistry
    participant BT as BaseTool
    participant ET as ExecTool (Subprocess)

    AL->>TR: get_schemas()
    TR-->>AL: Array of tool JSON Schemas
    AL->>LLM: Send messages[] + tool schemas
    LLM-->>AL: tool_call { name: "exec", args: { command: "df -h" } }

    AL->>TR: get_tool("exec")
    TR-->>AL: ExecTool instance
    AL->>BT: validate_params(args)
    BT-->>AL: Parameters valid
    AL->>ET: execute(command="df -h")
    Note over ET: Checks deny_patterns (regex guard)
    ET-->>AL: Command stdout string
    AL->>AL: Append ToolResult to messages[]
    AL->>LLM: Send messages[] (with evidence)
    LLM-->>AL: Final conversational response
```

#### Core Built-in Tools
- **Filesystem Tools:** `read_file`, `write_file`, `edit_file`, `list_dir`.
- **System Execution:** `exec` (subprocess runner).
- **Web Retrieval:** `web_search` (Brave Search API) and `web_fetch` (structured JSON extraction via readability).
- **Subagent Orchestration:** `spawn` (delegates complex tasks to isolated sub-agents).

### 2.5 Pillar 5: Proactivity via Cron & Heartbeat

NanoBot transforms from a passive responder into a proactive agent via two autonomous trigger daemons:
- **`CronService`:** Reads scheduled definitions from `~/.nanobot/cron/jobs.json`. When a trigger fires, it synthesizes an `InboundMessage` from sender `"system"` and injects it directly into `bus.inbound`.
- **`HeartbeatService`:** Wakes every 30 minutes, inspects `HEARTBEAT.md`, and if tasks are pending, injects an operational check message.
- **`SubagentManager` Isolation:** When the agent spawns a sub-agent for long-running work, the sub-agent receives an isolated `AgentLoop` with the `spawn` tool stripped out, structurally preventing infinite recursive fork bombs.

---

## 3. Architectural Visual: NanoBot Runtime Topology

The following diagram illustrates NanoBot's end-to-end architecture, showing the decoupled `MessageBus`, the `AgentLoop` reasoning cycle, plaintext disk state assembly, and containerized tool boundaries.

![NanoBot Minimalist Agent Runtime Architecture](../../assets/NanoBot-Minimal-Agent-Runtime-Architecture-2026.svg)

---

## 4. Production Implementations & Code Recipes

### 4.1 Custom Tool Recipe (`BaseTool` Implementation)

Adding a tool requires implementing parameter validation and execution without touching the reasoning loop:

```python
"""
NanoBot Custom Tool Implementation: StockPriceTool
Extends BaseTool with JSON Schema validation and asynchronous execution.
"""

from typing import Dict, Any, Optional
from nanobot.agent.tools.base import BaseTool

class StockPriceTool(BaseTool):
    name: str = "get_stock_price"
    description: str = "Retrieve real-time equity pricing and daily volume for a stock ticker."
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "Stock equity symbol (e.g., AAPL, GOOGL, NVDA)"
            }
        },
        "required": ["ticker"]
    }

    def validate_params(self, args: Dict[str, Any]) -> Optional[str]:
        ticker = args.get("ticker", "")
        if not ticker or not ticker.isalpha():
            return "Invalid ticker format: symbol must consist of alphabetic characters only."
        return None

    async def execute(self, ticker: str) -> str:
        ticker = ticker.upper()
        # Simulated lookup; replace with actual financial API call
        price_data = {"AAPL": 224.50, "GOOGL": 182.30, "NVDA": 138.25}
        price = price_data.get(ticker, 100.00)
        return f"{ticker}: ${price:.2f} USD (Daily Volume: 42.1M)"

# Registration in AgentLoop:
# registry.register(StockPriceTool())
```

### 4.2 Custom Boundary Channel Adapter

```python
"""
NanoBot Channel Adapter Template
Normalizes platform events into InboundMessage and dispatches OutboundMessage.
"""

import asyncio
from nanobot.channels.base import BaseChannel
from nanobot.bus.events import InboundMessage, OutboundMessage

class CustomWebhookChannel(BaseChannel):
    async def start(self):
        # Start server or websocket connection
        pass

    def _normalize(self, raw_payload: dict) -> InboundMessage:
        return InboundMessage(
            id=raw_payload.get("event_id", "evt-01"),
            channel="custom_webhook",
            sender_id=raw_payload.get("user_id", "usr-anonymous"),
            chat_id=raw_payload.get("channel_id", "chan-main"),
            content=raw_payload.get("text", "").strip(),
            attachments=raw_payload.get("files", []),
            timestamp=raw_payload.get("timestamp"),
            metadata=raw_payload
        )

    async def send(self, msg: OutboundMessage):
        # Deliver message back to originating platform
        pass
```

### 4.3 Hardened Docker Containerization Recipe

Because regex pattern matching in `ExecTool` is bypassable, NanoBot must run inside an isolated Docker container:

```dockerfile
# Hardened Dockerfile for NanoBot Agent Runtime
FROM python:3.11-slim-bookworm

# 1. Install runtime dependencies and create non-root user
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1001 -s /bin/bash nanouser

WORKDIR /app

# 2. Install NanoBot via uv
RUN pip install --no-cache-dir uv && \
    uv tool install nanobot-ai

ENV PATH="/root/.local/bin:$PATH"

# 3. Create isolated workspace directory with strict ownership
RUN mkdir -p /workspace /app/config && \
    chown -R nanouser:nanouser /workspace /app/config

USER nanouser
WORKDIR /workspace

# Run NanoBot daemon
CMD ["nanobot", "daemon", "--config", "/app/config/config.json"]
```

---

## 5. Security Model, Gaps & Failure Modes

### 5.1 The `ExecTool` Regex Guardrail Fragility

In `nanobot/agent/tools/shell.py`, commands are checked against `DENY_PATTERNS`:

```python
DENY_PATTERNS = [
    r"rm\s+-rf\s+/",        # Root directory deletion
    r":\(\)\{.*\}",          # Fork bombs
    r"dd\s+if=.*of=/dev",    # Direct block device overwrites
    r"mkfs",                 # Filesystem format
    r"chmod\s+777\s+/",      # Root permission alteration
]
```

#### Why Regex Is Insufficient
1. **Hex & Base64 Obfuscation:** An attacker can execute `echo cm0gLXJmIC8= | base64 -d | sh`, completely bypassing the regex engine.
2. **Indirect Binary Invocation:** Commands can be triggered via Python (`python3 -c "import os; os.system('...')"`), perl, or awk.
3. **Operational Recommendation:** Never rely on regex deny-lists. Enforce kernel-level filesystem boundaries using Docker, read-only system mounts, and restricted non-root users.

### 5.2 Architectural Tradeoffs & Known Limitations

| Architectural Dimension | Tradeoff Chosen in NanoBot | Operational Consequence & Risk | Recommended Production Remediation |
| :--- | :--- | :--- | :--- |
| **Concurrency Model** | Sequential tool calls per session | Long web fetches block session throughput | Scale via separate OS processes per user |
| **Memory Storage** | Flat Markdown files (`MEMORY.md`) | Context saturation when memory exceeds ~50KB | Upgrade `MemoryStore` to hybrid vector DB |
| **Session Portability** | Plaintext JSONL at `~/.nanobot/` | Incompatible with serverless (AWS Lambda) | Mount persistent volumes or use SQLite |
| **Channel Security** | `allowFrom: []` defaults to open | Accepts messages from any user on channel | Enforce explicit user ID allowlists |

### 5.3 Common Claims vs. Technical Realities

| Common Industry Claim | Technical Reality & Code Verification |
| :--- | :--- |
| *"You need LangChain or LlamaIndex to build production AI agents."* | **Disproven:** NanoBot implements the complete agent lifecycle (reasoning, tool reflection, memory, multi-channel I/O) in 3,510 lines using standard async Python. |
| *"Plaintext Markdown files are insufficient for long-term agent memory."* | **Practical Context:** Markdown files are version-controllable, human-readable, and hot-editable. For personal agents (&lt;50KB context), flat files outperform complex vector infrastructure. |
| *"Agent frameworks must support multi-level subagent recursion."* | **Safety Hazard:** Unchecked sub-agent recursion causes exponential fork bombs. NanoBot's deliberate removal of `spawn` from sub-agents is a critical safety control. |

---

## 6. Practical Adoption Blueprint & Verification Checklist

```
[ ] 1. Core Installation & Environment Setup
    ├── Install via uv: uv tool install nanobot-ai
    ├── Verify installation: nanobot --version
    └── Run onboarding wizard: nanobot onboard

[ ] 2. Identity & Context Initialization
    ├── Configure ~/.nanobot/workspace/IDENTITY.md and SOUL.md
    ├── Populate USER.md with operational preferences
    └── Verify ~/.nanobot/config.json contains authorized API keys

[ ] 3. Security Boundary Hardening
    ├── Restrict ~/.nanobot/config.json permissions: chmod 600 config.json
    ├── Set channel allowFrom: ["AUTHORIZED_USER_ID"] in config
    └── Verify Docker sandbox container execution is enabled

[ ] 4. Proactive Services Verification
    ├── Add test cron job: nanobot cron add --name "test-ping" --message "Report uptime" --cron "*/30 * * * *"
    └── Validate HEARTBEAT.md reads cleanly without state corruption
```

### Essential Diagnostic Commands

```bash
# 1. Inspect active session history and recent turns
tail -n 20 ~/.nanobot/sessions/*.jsonl

# 2. Audit scheduled proactive cron tasks
nanobot cron list

# 3. Test interactive CLI agent execution loop
nanobot agent -m "List files in the current workspace"
```

### Recommended Codebase Reading Order

Follow this strict progression to master NanoBot's codebase:
1. `nanobot/bus/events.py` — Inbound and outbound message dataclasses.
2. `nanobot/agent/loop.py` — The core reasoning and execution loop.
3. `nanobot/agent/context.py` — File assembly and system prompt packaging.
4. `nanobot/agent/tools/base.py` & `registry.py` — Tool schema engine.
5. `nanobot/agent/tools/shell.py` — Subprocess execution and security checks.
6. `nanobot/cron/service.py` — Scheduled proactivity injection.
7. `nanobot/channels/telegram.py` — Complete channel adapter implementation.
8. `nanobot/agent/subagent.py` — Subagent execution constraints.

---

## 7. Timeline & System Evolution

- **January 2026:** HKU Data Intelligence Lab initiates NanoBot as a research vehicle for minimal agent architectures.
- **February 2, 2026:** NanoBot v0.1.0 released, accumulating over 15,000 GitHub stars within weeks.
- **February 9, 2026:** Sipeed uses NanoBot as the architectural blueprint to synthesize PicoClaw in Go for RISC-V edge hardware.
- **February 13, 2026:** Release of v0.1.3.post7, adding structured JSON extraction for `web_fetch` and refined sub-agent isolation.
- **March 2026:** NanoBot serves as the runtime foundation for ClawWork economic survival benchmarking.

---

## 8. Primary Sources & References

1. [HKUDS NanoBot GitHub Repository](https://github.com/HKUDS/nanobot) — Primary open-source codebase, architecture documentation, and issue tracker.
2. [HKUDS ClawWork Repository](https://github.com/HKUDS/ClawWork) — Economic evaluation layer built directly on top of NanoBot.
3. [Sipeed PicoClaw Repository](https://github.com/sipeed/picoclaw) — Go-native edge agent runtime derived from NanoBot's architecture.
4. [LiteLLM Documentation](https://docs.litellm.ai) — Underlying multi-provider inference bridge used by NanoBot.
5. [vLLM High-Throughput Inference Engine](https://github.com/vllm-project/vllm) — Local model inference engine supported natively for private deployments.

---

## 9. Supplementary Visuals

The original architecture overview diagram below illustrates the foundational component layout across the message bus, agent core, and file context layers:

![NanoBot Minimal Agent Runtime](../../assets/NanoBot-Minimal-Agent-Runtime.png)
*Figure 9.1: Component breakdown of NanoBot's message queue, agent core, and plaintext workspace.*

---

**Related:**
- [ClawWork-Agent-Architecture-And-Economic-Survival-2026](../openclaw/ClawWork-Agent-Architecture-And-Economic-Survival-2026.md) — The economic layer that wraps NanoBot's `AgentLoop` and meters token consumption.
- [Claw-Ecosystem-And-Agent-Topology-2026](../openclaw/Claw-Ecosystem-And-Agent-Topology-2026.md) — Comprehensive comparative taxonomy mapping NanoBot within the broader Claw ecosystem.
- [OpenClaw-Moltbot-Clawdbot-Architecture-2026](../openclaw/OpenClaw-Moltbot-Clawdbot-Architecture-2026.md) — The 430k LOC Node.js daemon that NanoBot was designed to contrast with.
- [NanoBot-NanoClaw-OpenClaw-Security-Comparison-2026](NanoBot-NanoClaw-OpenClaw-Security-Comparison-2026.md) — Security analysis contrasting NanoBot's process model against containerized and shared-memory runtimes.
