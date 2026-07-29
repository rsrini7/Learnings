# Model Context Protocol Scalability: The Transition to Code-Mode Agents

**A Technical Whitepaper on Context Efficiency & Programmatic Tool Calling**

> **Version 3.0 — Updated February 20, 2026**
> This document has been substantially revised to incorporate Claude Sonnet 4.6 (February 17, 2026) and the general availability of Programmatic Tool Calling, Dynamic Filtering, and the full advanced tool use platform. The industry is moving: JSON-style tool calling is increasingly viewed as a legacy pattern for complex workflows, with Cloudflare, Anthropic, and open-source projects converging on Code Mode as the preferred approach.

---

## Executive Summary

The Model Context Protocol (MCP) emerged as the de facto standard for connecting AI agents to external tools and systems following its November 2024 launch. As adoption scaled, however, fundamental architectural limitations surfaced. This whitepaper examines the root causes of MCP's scalability crisis—excessive token consumption, intermediate result bloat, rigid tool binding—and presents the industry's evolving response: **Programmatic Tool Calling (Code Mode)**, now a generally available capability on Claude Sonnet 4.6.

The story has two chapters. The first (through early 2026) was about mitigations: Tool Search, CLI patterns, Skills, and progressive disclosure. The second chapter began on February 17, 2026, when Anthropic moved Programmatic Tool Calling from beta to **general availability** alongside Sonnet 4.6, completing an industry shift that Cloudflare had signaled in September 2025. JSON tool calling is not going away, but for production agents with complex workflows, many tools, or privacy requirements, **Code Mode is now the recommended default**.

### Key Findings

| Finding | Detail |
|---------|--------|
| **Context bloat baseline** | Traditional MCP consumes ≈97K–134K tokens in tool definitions before any work begins (97K in the reference 5-server scenario; 134K in Anthropic's internal deployment) |
| **Tool Search (Jan 2026)** | Up to 85% token reduction; up to ~25 points accuracy improvement on internal MCP evals (e.g., Opus 4: 49% → 74%) |
| **Cloudflare Code Mode (Sep 2025)** | 30–81% token reduction in batch/complex workflows; up to ~98% in extreme cases |
| **Sonnet 4.6 Dynamic Filtering (Feb 2026)** | ~11% average quality improvement, ~24% fewer input tokens on web search benchmarks |
| **BrowseComp benchmark** | Sonnet: 33% → 46% (+13 pts); Opus: 45% → 61% (+16 pts) |
| **Deep Search QA benchmark** | Sonnet F1: 52% → 59% (+7 pts); Opus: ~8-pt F1 improvement |
| **Programmatic Tool Calling — GA** | Recommended default (per this whitepaper's 2026 guidance) for complex, multi-tool, multi-step agent workflows |

### The 2026 Recommendation in One Sentence

For agents with fewer than 10 simple tools: traditional JSON calling remains practical. For everything else — multi-step pipelines, 10+ tools, privacy-sensitive data, or complex orchestration — **Programmatic Tool Calling is our new baseline recommendation for non-trivial agents**.

---

## Table of Contents

1. [MCP Architecture and Initial Promise](#1-mcp-architecture-and-initial-promise)
2. [The Scalability Crisis: Root Cause Analysis](#2-the-scalability-crisis-root-cause-analysis)
3. [Quantified Impact: Benchmarks](#3-quantified-impact-benchmarks)
4. [MCP Tool Search: The First Wave Solution (January 2026)](#4-mcp-tool-search-the-first-wave-solution-january-2026)
5. [Anthropic's February 2026 Platform Update: Sonnet 4.6 and the GA of Code Mode](#5-anthropics-february-2026-platform-update-sonnet-46-and-the-ga-of-code-mode)
6. [Programmatic Tool Calling (Code Mode): Architecture and Implementation](#6-programmatic-tool-calling-code-mode-architecture-and-implementation)
7. [Alternative Approaches: CLI, Scripts, and Skills](#7-alternative-approaches-cli-scripts-and-skills)
8. [Advanced Pattern: MCP-Zero Active Tool Discovery](#8-advanced-pattern-mcp-zero-active-tool-discovery)
9. [Trade-offs and Decision Matrix](#9-trade-offs-and-decision-matrix)
10. [Real-World Case Study: Prediction Markets Agent](#10-real-world-case-study-prediction-markets-agent)
11. [Security Considerations](#11-security-considerations)
12. [Future Roadmap and Evolution](#12-future-roadmap-and-evolution)
13. [Implementation Recommendations](#13-implementation-recommendations)
14. [Conclusion](#14-conclusion)
15. [Appendix A: Sonnet 4.6 vs Opus 4.6 — Cost and Performance Guide](#15-appendix-a-sonnet-46-vs-opus-46-cost-and-performance-guide)
16. [Appendix B: API Quick Reference for Sonnet 4.6 Features](#16-appendix-b-api-quick-reference-for-sonnet-46-features)
17. [References and Further Reading](#17-references-and-further-reading)

---

## 1. The MCP Architecture and Initial Promise

### 1.1 What Is MCP?

The Model Context Protocol is an open standard providing a universal interface for connecting AI agents to external systems. Rather than requiring custom integrations for each tool-agent pairing, MCP abstracts tools and data sources into standardized "servers" that any agent can consume.

**Core Components:**
- **MCP Clients**: AI agents that consume tools and resources
- **MCP Servers**: Standards-compliant tool providers
- **Transport Layer**: JSON-RPC based communication
- **Standard Features**: Tools, Resources, Prompts, Sampling

### 1.2 Why MCP Adoption Was Rapid

MCP solved a real problem: fragmentation and duplicated effort in building agent integrations. Before MCP, connecting an agent to Slack, Google Drive, and Salesforce required three separate custom implementations. MCP unified this into a single standardized pattern.

Since November 2024, the community has built thousands of MCP servers across every major platform, SDKs for all major programming languages, and achieved industry-wide adoption as the de facto standard. But MCP's success created the conditions for its own scalability crisis.

---

## 2. The Scalability Crisis: Root Cause Analysis

### 2.1 Problem 1: Tool Definition Overload

**The Core Issue:** MCP loads all tool definitions upfront, directly into the model's context window.

#### Real-World Example

A developer using five standard MCP servers for AI coding (Filesystem, Code Editor, Package Manager, Git, and Docker) experiences:

| Metric | Value |
|--------|-------|
| Total Tool Definitions | 97,000 tokens |
| Claude Sonnet Context Window | 200,000 tokens |
| Percentage Consumed | 48% |
| Remaining for User Query | 52% |

Even though the agent may only use 2–3 tools per request, all 97,000 tokens consume context before the agent begins work.

At Anthropic's own scale, tool definitions consumed **134,000 tokens** before optimization (per the Advanced Tool Use blog post, November 2025).

**Performance Degradation:** Research shows LLMs perform similarly to GPT-3.5-era systems when asked to choose among dozens of tools — the "token overwhelm" effect where excessive context makes the model less capable, not more.

#### Mathematical Model

```
Context Used = Σ(Tool Definitions) + System Prompt + User Query
```

Where for MCP:
- n = number of connected MCPs
- Each tool set = full definitions, not just needed ones
- No selective loading mechanism in traditional MCP

### 2.2 Problem 2: Intermediate Result Bloat

**The Secondary Issue:** Every tool call result passes back through the model's context window, forcing repetition of data.

#### Example Flow: Google Drive → Salesforce Integration

```
Step 1: Agent receives: "Download transcript and add to Salesforce"
        Context: Tool definitions (97K tokens) + Query (100 tokens)

Step 2: Call gdrive.getDocument(documentId: "abc123")
        Returns: Full transcript text (50,000 tokens)
        Context now: 97K + System Prompt + 50K transcript

Step 3: Call salesforce.updateRecord()
        Full transcript MUST be re-read from context

TOTAL: Transcript flows through context TWICE
       Additional cost: +50,000 tokens for a single integration
```

This is the problem Programmatic Tool Calling was designed to eliminate: intermediate I/O stays inside the sandbox and **never touches the model's context window**.

### 2.3 Problem 3: No Progressive Disclosure

**The Architectural Gap:** Traditional MCP had no built-in mechanism for "discovering" tools on-demand.

An e-commerce platform might expose 500+ tools across product management, inventory, customer management, and reporting. A single request might need 5–10 tools, yet all 500 descriptions consume tokens. Unlike Unix filesystems where you list a directory only when needed, traditional MCP had no equivalent — all tools were always "visible" to the model.

### 2.4 Problem 4: The "Human Context vs. Machine Context" Mismatch

**A Deeper Design Tension:** JSON tool schemas are optimized for human developers, not for LLMs.

Human developers like JSON because it's explicit and structured. For the model, however, JSON tool schemas are a **synthetic format** — one that occupies context tokens and is not what the model was primarily trained on. LLMs are trained on **billions of lines of code** across Python, TypeScript, Go, and more. Writing code to orchestrate tools is more "native" to the model than emitting rigid JSON blobs that conform to synthetic schemas.

This insight — code-first is more natural to LLMs than JSON-first — is the intellectual foundation of Programmatic Tool Calling. Every token spent on JSON schema enforcement is a token taken from the model's actual strength.

### 2.5 Problem 5: Rigid Tool Binding

**The Design Limitation:** Tools are statically defined; new capabilities cannot be generated dynamically.

If an agent needs to combine multiple API calls into a custom workflow — filter a dataset, loop over results, retry on failure — it cannot create a new tool on the fly. Instead, it must orchestrate multiple existing tools, each consuming context and incurring latency.

---

## 3. Quantified Impact: Benchmarks

### 3.1 Token Consumption Comparison

Benchmark: Agent integrating Google Drive → Salesforce with 5 MCPs connected.

| Aspect | Traditional MCP | Tool Search | PTC (Code Mode) | Reduction |
|--------|-----------------|-------------|-----------------|-----------|
| **Input Tokens** | 15,417/call | ~2,300/call | 3,310/call | 85% / 78.5% |
| **Tool Definitions** | All 97K loaded | 3–5 tools (~10K) | Only needed | ~90% / ~85% |
| **Intermediate Results** | In context | In context | In sandbox | ~90% via PTC |
| **Output Tokens** | 87 | ~150 | 192 | — |
| **Total Tokens** | 775,197 | ~116,000 | 175,081 | 85% / 77.4% |
| **Success Rate** | 100% | 100% | 100% | Same |
| **Latency** | 9.66s | 11–12s | 10.37s | +7–24% |

**At Anthropic's internal scale (from Advanced Tool Use blog, Nov 2025):**
- Traditional approach: ~77K tokens for 50+ MCP tools before any work begins
- With Tool Search: ~8.7K tokens — preserving **95% of context window**
- Opus 4 accuracy: 49% → 74% with Tool Search enabled
- Opus 4.5 accuracy: 79.5% → 88.1% with Tool Search enabled

### 3.2 Scaling Characteristics

How token consumption grows with tool count:

| Tool Count | Traditional MCP | Tool Search | PTC (Code Mode) | MCP-Zero |
|------------|-----------------|-------------|----------------------|----------|
| 10 tools | 10K tokens | 3K tokens | 1.5K tokens | 1.2K tokens |
| 50 tools | 50K tokens | 10K tokens | 2.2K tokens | ~2K tokens |
| 100 tools | 100K tokens | 12K tokens | 2.8K tokens | ~2.5K tokens |
| 500 tools | 500K tokens | 15K tokens | 4.2K tokens | ~4K tokens |

**Key Insight:** Tool Search, PTC, and dynamic approaches maintain near-constant token consumption as tools scale; traditional MCP scales linearly.

---

## 4. MCP Tool Search: The First Wave Solution (January 2026)

### 4.1 Anthropic's Native Solution

In January 2026, Anthropic introduced the MCP Tool Search feature, allowing clients to dynamically load tools into context only when needed. This was the first major MCP-native mitigation of context bloat, predating the full Programmatic Tool Calling GA.

**Key Mechanics:**
- Claude initially loads only the `tool_search` tool (~500 tokens)
- When a query arrives, the system searches the tool catalog for relevant tools
- Only the full definitions of 3–5 relevant tools are loaded into context
- Achieves up to 85% token reduction when tool definitions occupy >10% of context

### 4.2 Tool Search Variants

**Regex-based Search** — Claude writes patterns (e.g., `weather.*`, `get_star_data`). Best for tools with consistent naming conventions.

```json
{
  "tool": "tool_search",
  "parameters": {
    "pattern": "weather.*",
    "type": "regex"
  }
}
```

**BM25 (Keyword-based Search)** — Claude uses natural language queries. Better when tool names and descriptions vary widely.

```json
{
  "tool": "tool_search",
  "parameters": {
    "query": "tools for fetching weather data",
    "type": "bm25"
  }
}
```

**Custom Search** — You can implement custom search tools using embeddings or other strategies. The Claude Developer Platform provides regex and BM25 out of the box.

### 4.3 Implementation

**Client-Side Setup:**
1. Enable beta: Add the appropriate header to your API request
2. Add `tool_search_tool_regex_20251119` or BM25 variant; do NOT set `defer_loading: true` on it
3. Mark non-essential tools with `defer_loading: true`
4. Keep 3–5 frequently used tools with `defer_loading: false`

```json
{
  "tools": [
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {"...": "..."},
      "defer_loading": true
    }
  ]
}
```

For entire MCP servers:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true},
  "configs": {
    "search_files": {"defer_loading": false}
  }
}
```

**Server-Side Best Practices:**
- Lead descriptions with the primary function
- Keep descriptions to one or two sentences
- Include searchable keywords: "fetch," "get," "retrieve," and synonyms
- Use `server_instructions` to guide Claude on tool workflow and ordering

### 4.4 When to Use Tool Search

**Use Tool Search when:**
- You have 10 or more MCP tools
- Tool definitions occupy >10% of context
- Tools have varying usage patterns (some frequent, many occasional)
- You want a simple client-side solution with no server changes

**Skip Tool Search when:**
- Fewer than 10 tools total
- All tools are used every session
- Latency is absolutely critical (search adds 1–2 seconds)

### 4.5 Tool Search in Context: Relationship to Programmatic Tool Calling

Tool Search and Programmatic Tool Calling are **complementary, not competing** solutions:

- **Tool Search** handles *discovery* — which tools exist and should be loaded
- **Programmatic Tool Calling** handles *execution* — how those tools are called and how their results are managed

In a mature 2026 production system, you would use both: Tool Search to discover tools on-demand, PTC to execute them in a sandbox without polluting the context window.

---

## 5. Anthropic's February 2026 Platform Update: Sonnet 4.6 and the GA of Code Mode

### 5.1 What Changed on February 17, 2026

Claude Sonnet 4.6 arrived with five tools moving from beta to **general availability** simultaneously:

1. **Code Execution** — Sandboxed Python execution environment
2. **Memory** — Cross-session persistent state for agents
3. **Programmatic Tool Calling (Code Mode)** — Tools invoked via code, not JSON
4. **Tool Search Tool** — Dynamic tool discovery (regex + BM25)
5. **Tool Use Examples** — Demonstrating correct tool usage patterns in context

This was not an incremental update. The GA of PTC marks the moment the industry standard shifted.

### 5.2 Sonnet 4.6: Model Capabilities

Beyond tool use, Sonnet 4.6 is a significant intelligence upgrade:

| Capability | Detail |
|------------|--------|
| **Price** | $3/$15 per million input/output tokens (same as Sonnet 4.5) |
| **Context Window** | 200K standard; 1M token context window in beta |
| **Max Output Tokens** | 64K |
| **Thinking** | Adaptive Thinking (`thinking: {type: "adaptive"}`) |
| **Computer Use** | Major improvement; 72.5% on OSWorld-Verified (highest in category) |
| **Availability** | claude.ai (default Free/Pro), Claude Cowork, Messages API, Claude Code, Amazon Bedrock, Google Vertex AI |
| **API Model ID** | `claude-sonnet-4-6` |

In Claude Code early testing, developers preferred Sonnet 4.6 over Sonnet 4.5 **70% of the time**, and even preferred it over the previous frontier Opus 4.5 **59% of the time** — at a lower price point.

### 5.3 Dynamic Filtering: Code Mode Applied to Web Search

The most tangible expression of Programmatic Tool Calling in Sonnet 4.6 is **Dynamic Filtering for web search**. Previously, web search dumped raw page content into the context window — navigation menus, ads, boilerplate, all of it. The model then had to reason through the noise.

**New behavior with Dynamic Filtering:**

1. Claude runs an initial web search
2. Claude writes and executes code in a Python sandbox to post-process results
3. Code filters by recency, site authority, and relevance
4. Only filtered snippets and summaries are injected into the model's context
5. The model sees signal, not noise

**Technical enablement:**
```python
# Enable dynamic filtering with versioned tool types
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["code-execution-web-tools-2026-02-09"],
    tools=[
        {
            "type": "web_search_20260209",  # Versioned for dynamic filtering
            "name": "web_search",
        }
    ],
    messages=[{"role": "user", "content": "Your query here"}]
)
```

For the search API with data fetching enabled, **dynamic filtering is on by default** — no code changes required.

### 5.4 Benchmark Results: Dynamic Filtering

| Benchmark | What It Tests | Sonnet 4.6 Before | Sonnet 4.6 After | Improvement |
|-----------|---------------|-------------------|------------------|-------------|
| **BrowseComp** | Navigate multiple sites to find hard-to-find facts | 33% | 46% | +13 points |
| **Deep Search QA** | Find ALL correct answers via web search (F1) | 52% | 59% | +7 points F1 |

| Benchmark | Opus 4.6 Before | Opus 4.6 After | Improvement |
|-----------|----------------|----------------|-------------|
| **BrowseComp** | 45% | 61% | +16 points |
| **Deep Search QA** | ~51% | ~59% | +~8 points F1 |

**Overall:** ~11% average quality improvement, ~24% fewer input tokens across both benchmarks with Dynamic Filtering enabled.

### 5.5 The Opus Paradox: Token Cost Caveat

An important nuance: the relationship between Dynamic Filtering and token cost is **model-dependent**.

For **Sonnet 4.6**: Price-weighted token usage decreases on both benchmarks. You get more quality and lower cost simultaneously.

For **Opus 4.6**: Price-weighted tokens can *increase*, because Opus writes more complex, thorough filtering code. The additional computation cost of the code it writes outweighs the savings from a smaller final context. The quality improvement is real, but it costs more.

**Practical implication:** For high-volume production workloads prioritizing cost efficiency, Sonnet 4.6 with Dynamic Filtering is the optimal choice. For tasks where Opus-level reasoning depth is genuinely required, expect improved quality but potentially higher cost.

### 5.6 Context Compaction: Infinite Conversations

Alongside Sonnet 4.6, Anthropic released the **Context Compaction API** — automatic, server-side context summarization. When a conversation approaches the context window limit, the API automatically summarizes earlier parts, enabling effectively infinite conversation history for long-running agents.

```python
# Context Compaction is enabled via API configuration
# When context approaches window limit, server summarizes automatically
# Agents can continue indefinitely without manual context management
```

This directly addresses one of the core scalability problems: conversations that grow too long to fit in context.

---

## 6. Programmatic Tool Calling (Code Mode): Architecture and Implementation

### 6.1 The Fundamental Architectural Shift

Traditional tool calling and Programmatic Tool Calling differ fundamentally in **where tool results live**:

```
Traditional JSON Tool Calling:
User → Agent → [JSON tool call] → [Tool executes] → [Result injected into context]
                                                          ↑
                                          All intermediate I/O accumulates here
                                          Growing context pollution with each step

Programmatic Tool Calling (Code Mode):
User → Agent → [Claude writes orchestration code]
                      ↓
              [Sandbox executes code]
                      ↓
              [Code calls tools directly]
                      ↓
              [Intermediate results stay in sandbox]
                      ↓
              [Only final summary returned to model context]
```

The model's context window receives only the final answer. All intermediate I/O — raw data, API responses, intermediate computations — stay inside the sandbox and are discarded.

### 6.2 Why Code Mode Is More Reliable Than JSON Calling

LLMs are trained on billions of lines of code. Writing loops, conditionals, error handlers, and data transformations is native to them. Emitting rigidly structured JSON function call schemas is not — it's a synthetic format the model must conform to rather than express naturally.

Code Mode lets the model play to its strengths:
- **Natural orchestration**: loops, retries, branching are expressed in code, not inferred
- **Explicit control flow**: what happens next is in the code, not implicit in the model's next inference
- **Error handling**: try/catch in code, not vague natural-language uncertainty
- **Data transformation**: filter, map, reduce in code before anything hits context

### 6.3 Implementation Pattern: Filesystem as API

The recommended architecture exposes tools as typed TypeScript or Python modules organized in a filesystem:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   ├── searchFiles.ts
│   ├── uploadFile.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   ├── queryRecords.ts
│   ├── createRecord.ts
│   └── index.ts
└── slack/
    ├── sendMessage.ts
    ├── getChannelHistory.ts
    └── index.ts
```

Each module defines typed input/output interfaces:

```typescript
// servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
  fields?: string;
}

interface GetDocumentResponse {
  content: string;
  metadata: Record<string, any>;
}

export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>('google_drive__get_document', input);
}
```

### 6.4 Example: Budget Compliance Workflow

Consider a business task: "Which team members exceeded their Q3 travel budget?"

**Traditional JSON approach:**
- Fetch team members → 20 people returned to context
- For each person, fetch Q3 expenses → 20 tool calls, each returning 50–100 line items
- All 2,000+ expense line items (50KB+) enter Claude's context
- Claude manually sums expenses, looks up budgets, compares — slow and error-prone

**With Programmatic Tool Calling:**

```python
# Claude writes this orchestration code
team = await get_team_members("engineering")

# Fetch budgets for all levels in parallel
levels = list(set(m["level"] for m in team))
budgets = {level: await get_budget_by_level(level) for level in levels}

# Check compliance - results stay in sandbox
over_budget = []
for member in team:
    expenses = await get_expenses(member["id"], "Q3")
    total = sum(e["amount"] for e in expenses)
    limit = budgets[member["level"]]
    if total > limit:
        over_budget.append({
            "name": member["name"],
            "total": total,
            "limit": limit,
            "overage": total - limit
        })

# Only this compact result returns to Claude's context
print(f"Over-budget members: {over_budget}")
```

The model's context receives only the final `over_budget` list — not thousands of expense line items.

### 6.5 Agent Workflow: Drive → Salesforce with PTC

**Request:** "Download meeting transcript from Google Drive and add key points to Salesforce"

**Agent-Generated Code:**
```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

// Load transcript — stays in sandbox, not in model context
const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;

// Transform in execution environment
const keyPoints = transcript
  .split('\n')
  .filter(line => line.startsWith('ACTION:') || line.startsWith('DECISION:'))
  .join('\n');

// Only the filtered summary flows to Salesforce
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { KeyPoints: keyPoints }  // ~200 tokens, not 50,000
});

console.log("Meeting key points updated in Salesforce");
```

**Context consumed:** ~2,000 tokens instead of 147,000+.

### 6.6 Benefits Summary

**1. Progressive Tool Discovery** — Models discover tools by exploring the filesystem, reading only what's needed for the current step.

**2. Context-Efficient Data Transformation** — Large datasets are filtered inside the sandbox before returning to model context:
```typescript
// Without PTC: Load all 10,000 rows into context
// With PTC: Filter in sandbox, return only 50 relevant rows
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(row => row["Status"] === 'pending');
console.log(pendingOrders); // Agent sees only the 50 rows that matter
```

**3. Deterministic Control Flow** — Loops, conditionals, and retries execute in code, not inferred from natural language:
```typescript
let found = false;
let attempt = 0;
while (!found && attempt < 10) {
  const messages = await slack.getChannelHistory({ channel: 'C123456' });
  found = messages.some(m => m.text.includes('deployment complete'));
  if (!found) {
    await new Promise(r => setTimeout(r, 5000 * Math.pow(2, attempt)));
    attempt++;
  }
}
```

**4. PII Shield** — Sensitive data never reaches the model context:
```typescript
const sheet = await gdrive.getSheet({ sheetId: 'abc123' });
for (const row of sheet.rows) {
  // MCP harness intercepts and tokenizes PII before returning to model
  await salesforce.updateRecord({
    objectType: 'Lead',
    recordId: row.id,
    data: {
      Email: row.email,    // [EMAIL_1] in model context
      Phone: row.phone,    // [PHONE_1] in model context
    }
  });
  // Real data flows to Salesforce; model never sees raw PII
}
```

**5. Skill Persistence** — Agents can save effective code for reuse across sessions:
```typescript
// First run: Agent generates and saves a reusable function
async function saveSheetAsCsv(sheetId: string) {
  const data = await gdrive.getSheet({ sheetId });
  const csv = data.map(row => row.join(',')).join('\n');
  await fs.writeFile(`./workspace/sheet-${sheetId}.csv`, csv);
}
await fs.writeFile('./skills/save-sheet-as-csv.ts', functionCode);

// Later runs: Agent reuses the saved skill
import { saveSheetAsCsv } from './skills/save-sheet-as-csv';
```

### 6.7 Tool Use Examples: Teaching Correct Usage

Alongside PTC, Anthropic introduced **Tool Use Examples** — a mechanism for demonstrating correct tool usage patterns. JSON schemas define what's structurally valid but can't express usage conventions: when to include optional parameters, which combinations make sense, or what API expectations exist.

Tool Use Examples fill this gap by showing Claude actual usage patterns, improving correctness beyond what schema validation alone can guarantee.

### 6.8 Migration Path: From JSON to Code Mode

A pragmatic migration approach:

1. **Keep existing JSON tools** for simple, one-shot calls and third-party integrations you don't control
2. **Introduce Code Mode for complex flows**: web/RAG retrieval with filtering, analytics pipelines, multi-service orchestration
3. **Prefer the pattern**: `Model → code → sandbox → final result → model` over `Model → tool call → model → next tool call → ...`
4. Expand Code Mode adoption progressively as you gain confidence and measure results

---

## 7. Alternative Approaches: CLI, Scripts, and Skills

While Tool Search and Programmatic Tool Calling are the primary 2026 solutions, a spectrum of approaches exists. Understanding where each fits is essential for pragmatic architecture decisions.

### 7.1 CLI-First Approach

**The Pattern:** Use command-line interfaces as the primary integration layer. Agents interact with CLI tools via system prompts.

```
# Available Tools
- `ks-cli market search <query>` - Search Kalshi prediction markets
- `ks-cli market get <id>` - Get market details
- `ks-cli order list` - List your orders

## How to Use
Read market schema: ks-cli market schema
Use three-step workflow: Search → Get details → Report
```

**Token Cost:** Only 200–300 tokens for a well-documented CLI.

| Aspect | CLI | MCP | Tool Search | PTC (Code Mode) |
|--------|-----|-----|-------------|-----------------|
| Context consumption | ~300 tokens | 97K tokens | ~10K tokens | ~2K tokens |
| Flexibility | High | Medium | Medium | Highest |
| Operational overhead | Low | Low | Low | Medium |
| Multi-agent support | Good | Good | Good | Excellent |
| Works for humans too | Yes | Partial | Partial | No |

**When to Use:** First iteration of new tools; simple stable interfaces; teams using the same tools as humans; small tool sets (<20).

### 7.2 Script-Based Approach with Progressive Disclosure

**The Pattern:** Single-file, self-contained scripts with prompt engineering for selective loading.

```
scripts/
├── market-search.py
├── market-details.py
├── sentiment-analysis.py
└── portfolio-manager.py

README.md  ← Only this loads upfront
```

**Token Cost:** <2,000 tokens initially; scripts loaded on-demand.

**When to Use:** Medium complexity (10–50 scripts); privacy-sensitive workloads; tools you control and can update.

### 7.3 Claude Skills

**The Pattern:** Anthropic's native skills ecosystem combining skill.md descriptions with on-demand code loading.

```
skills/
├── prediction-markets/
│   ├── skill.md          # Loaded upfront (~200 tokens)
│   ├── search.ts         # Loaded on need
│   ├── sentiment.ts      # Loaded on need
│   └── portfolio.ts      # Loaded on need
```

**Token Cost:** 200–300 tokens for skill.md only; detailed scripts load on-demand.

**Key trade-off:** Skills are Claude-native. Porting to other models requires adaptation. Substantial flexibility gains for Claude-native systems.

**When to Use:** Building exclusively with Claude; complex multi-tool enterprise workflows; Anthropic-managed infrastructure preferred.

---

## 8. Advanced Pattern: MCP-Zero Active Tool Discovery

### 8.1 The Problem It Solves

Current solutions still require either pre-loading or search-based discovery. MCP-Zero introduces **active tool discovery**: agents autonomously request specific tools based on task requirements.

**Experimental status note:** MCP-Zero is a research/advanced pattern. Production systems should first adopt Tool Search + Programmatic Tool Calling before considering MCP-Zero. MCP-Zero's hierarchical tool discovery can also be implemented *within* a PTC sandbox.

### 8.2 How It Works

**Three Core Mechanisms:**

**1. Active Tool Request** — Agent generates structured requests for specific tools:
```
<tool_request>
server: google_drive
tool: search_files
capability: Find files matching pattern
domain: document_management
</tool_request>
```

**2. Hierarchical Semantic Routing** — Two-stage matching:
- Server matching: "I need google_drive capabilities" → find google_drive server
- Tool matching: "I need to find files" → find search_files, find_by_date, etc.

**3. Iterative Capability Extension** — As the agent works, it progressively requests new capabilities only when needed.

### 8.3 Benchmark Results

| Metric | Traditional MCP | Tool Search | Dynamic Toolset | MCP-Zero |
|--------|-----------------|-------------|-----------------|----------|
| Initial context | 85K tokens | ~10K tokens | 4K tokens | 1.2K tokens |
| Mid-task context growth | Linear +20K | +2K/search | +2K/domain | +1.5K/domain |
| Final context | 125K+ tokens | ~16K tokens | 8K tokens | 4.8K tokens |
| Tool discovery latency | Zero (pre-loaded) | ~1–2s/search | ~50ms | ~100ms |
| Success rate | 100% | 100% | 99.8% | 99.7% |

MCP-Zero trades minimal latency (~50–100ms per discovery) for dramatic token savings, but requires research-grade infrastructure to implement well.

> **Note:** Values in the table above are illustrative, based on synthetic experiments from the MCP-Zero research paper. MCP-Zero is a research pattern; treat these numbers as directional estimates, not production benchmarks.

---

## 9. Trade-offs and Decision Matrix

### 9.1 Comprehensive Comparison (2026 Edition)

| Dimension | Traditional MCP | Tool Search | CLI | Scripts | Skills | PTC (Code Mode) | MCP-Zero |
|-----------|-----------------|-------------|-----|---------|--------|-----------------|----------|
| **Token Efficiency** | Low | High | Medium | High | High | Very High | Very High |
| **2026 Recommendation** | Legacy for complex | Primary mitigation | First iteration | Privacy workloads | Claude-native | **New default** | Research |
| **Setup Cost** | High | Low | Low | Low | Medium | Medium | Very High |
| **Operational Complexity** | Low | Low | Low | Medium | Low | Medium | Very High |
| **Security / PII** | Basic | Basic | Manual | Manual | Advanced | **Advanced** | Advanced |
| **Ecosystem Lock-in** | None | None | None | None | Claude | None | None |
| **Multi-agent Ready** | Good | Good | Fair | Fair | Fair | **Excellent** | Good |
| **Flexibility** | Low | Medium | Medium | High | High | **Very High** | Very High |
| **Scaling (Tool Count)** | Linear | Constant | Linear | Constant | Constant | **Constant** | Constant |
| **Industry Adoption** | Highest | Growing | Low | Low | Growing | **GA / Growing Fast** | Emerging |

### 9.2 Decision Framework (2026 Guidance)

**Choose Traditional MCP (JSON Calling) when:**
- Integrating external, third-party tools you don't control (Slack, Notion, Stripe)
- Tool set is small (<10 tools) and stable
- Need maximum predictability and simple setup
- Working with single, well-focused agents with simple tasks

**Choose Tool Search when:**
- Using MCP with 10+ tools consuming >10% of context
- Want simple client-side solution with no server changes
- Can tolerate 1–2s search latency
- Tools have varying usage patterns (some frequent, many occasional)

**Choose CLI when:**
- First iteration of a new tool
- Simple, stable interface (REST API wrapper)
- Same integration needed for human developers
- Small tool sets (<20 tools)

**Choose Scripts when:**
- Multiple interconnected tools (20–100 range)
- Complex data transformations needed
- Privacy-sensitive workloads
- Control over exact data flow is critical

**Choose Skills when:**
- Building exclusively with Claude
- Complex, multi-tool enterprise workflows
- Want Anthropic-managed infrastructure

**Choose Programmatic Tool Calling (Code Mode) when:**
- Large tool catalogs (10+ tools with complex interactions)
- Multi-step workflows with data transformation
- Data privacy paramount (PII must not enter model context)
- Complex orchestration: loops, retries, parallel calls, branching
- Building production agents for 2026 and beyond
- **This is our recommended default (2026 architecture guidance) for non-trivial agent systems**

**Choose MCP-Zero when:**
- Production enterprise system with many domains
- Tools must be discovered dynamically across domains
- Can justify research-grade infrastructure cost

### 9.3 The Revised 80/10/10 Rule (2026 Edition)

The original 80/10/10 rule (CLI → MCP → Code Execution) described an adoption ladder that made sense in 2025. In 2026, with PTC at GA, the recommendation shifts:

| Scenario | Approach | Rationale |
|----------|----------|-----------|
| **Design Philosophy** | Code APIs first | Design tools as typed libraries; wrap as CLI/MCP as needed |
| **Simple tools (<10)** | CLI or MCP with Tool Search | Fast iteration, works everywhere |
| **Standard integrations** | MCP with Tool Search | Third-party tools, existing servers |
| **Complex workflows** | Programmatic Tool Calling | Multi-step, privacy-sensitive, large catalogs |

**The 2026 inversion:** Rather than "start with CLI, graduate to Code Execution," the guidance is now: **design for code APIs (typed libraries) first; expose as CLI, MCP, or Skills as operational packaging.**

---

## 10. Real-World Case Study: Prediction Markets Agent

### 10.1 Scenario

Build an agent that analyzes prediction markets (Kalshi) to: search relevant markets, analyze sentiment from order books, report aggregated predictions, and optionally execute trades.

### 10.2 Traditional MCP Approach

**Token consumption:**
```
System prompt:           2,000 tokens
Tool definitions (13):   6,500 tokens
User query:               200 tokens
TOTAL BEFORE WORK:       8,700 tokens
After market search (200 markets × 50 tokens): +10,000 tokens
FINAL CONTEXT:          18,700 tokens
```

### 10.3 Tool Search Approach

**Token consumption:**
```
System prompt:           2,000 tokens
tool_search tool:          300 tokens  
Essential tools (3):     1,500 tokens
User query:               200 tokens
TOTAL BEFORE WORK:       4,000 tokens
After search (5 relevant tools loaded): +2,500 tokens
WORKING CONTEXT:         6,500 tokens   ← 65% reduction
```

### 10.4 CLI Approach

**Token consumption:**
```
System prompt:        2,000 tokens
CLI documentation:      200 tokens
User query:             200 tokens
TOTAL BEFORE WORK:    2,400 tokens   ← 72% reduction vs Traditional
```

### 10.5 Programmatic Tool Calling (Code Mode) Approach

**Token consumption:**
```
System prompt:        2,000 tokens
Tool discovery hint:    150 tokens
User query:             200 tokens
TOTAL BEFORE WORK:    2,350 tokens
Code written by agent: ~1,500 tokens
WORKING TOTAL:        ~3,850 tokens   ← 79% reduction vs Traditional
```

Plus: 200 markets of data are processed inside the sandbox. Only aggregated sentiment statistics (~200 tokens) return to the model context — not 10,000 tokens of raw market data.

### 10.6 Comparative Analysis

| Metric | Traditional MCP | Tool Search | CLI | PTC (Code Mode) |
|--------|-----------------|-------------|-----|-----------------|
| Initial context | 8,700 | 4,000 | 2,400 | 2,350 |
| After market search (200 markets) | 18,700 | 6,500 | 2,400 | ~3,850 |
| Agent analysis capacity | 181K tokens | 193.5K | 197.6K | ~196K |
| **Capacity advantage** | Baseline | +6.4% | +8.7% | +8.3% |
| Intermediate data in context | Full market data | Full market data | Command output | Filtered summary only |
| PII exposure | Full in context | Full in context | Command args | Filtered in sandbox |
| Data transformation | Manual | Manual | CLI parsing | In-sandbox filtering |
| Setup overhead | Medium | Low | Low | Medium |

**Key Insight:** For this workflow, Tool Search provides ~54% savings vs traditional MCP with minimal setup. PTC saves similar context space *and* keeps intermediate data private, eliminating the biggest risk in the traditional approach.

---

## 11. Security Considerations

### 11.1 PTC Sandbox Security Requirements

Running agent-generated code requires robust infrastructure:

1. **Sandboxing**: Isolated execution environment (containers, VMs, specialized runtimes like Anthropic's native code execution tool)
2. **Resource limits**: CPU, memory, disk, network constraints
3. **Capability restrictions**: API bindings instead of open network access
4. **Monitoring**: Logging all executed code and external calls
5. **Timeout handling**: Preventing infinite loops

**Authentication in PTC — the right pattern:**
```typescript
// Wrong (credentials potentially visible in generated code):
const apiKey = process.env.SALESFORCE_KEY;
const result = fetch(`https://api.salesforce.com`, {
  headers: { 'Authorization': `Bearer ${apiKey}` }
});

// Right (credentials in pre-authenticated binding):
const salesforce = env.SALESFORCE;  // Pre-authenticated; key never in code
const result = await salesforce.updateRecord(...);
```

### 11.2 PTC's Privacy Advantage

Programmatic Tool Calling provides a structural privacy guarantee: **PII can stay in bindings and sandboxes, never entering model context**. This is a fundamental improvement over traditional MCP where all data flows through context.

```typescript
// MCP harness intercepts and tokenizes PII automatically
const rows = await gdrive.getSheet({ sheetId: 'abc123' });
for (const row of rows) {
  await salesforce.updateRecord({
    objectType: 'Lead',
    recordId: row.id,
    data: {
      Email: row.email,    // Becomes [EMAIL_1] in model-visible context
      Phone: row.phone,    // Becomes [PHONE_1] in model-visible context
    }
  });
  // Real data flows to Salesforce; model never processes raw PII
}
```

Anthropic now provides **code execution as a managed capability** for Claude agents, reducing the infrastructure burden of sandboxing. Teams don't need to build isolation themselves.

### 11.3 MCP/Tool Search Security Trade-offs

**MCP/Tool Search advantages:**
- Tool definitions are explicit; no arbitrary code execution
- Credentials managed by MCP server
- Failed calls don't crash the system
- Search patterns are transparent and auditable

**MCP/Tool Search disadvantages:**
- All data flows through context; harder to implement PII protection
- Traditional MCP has no concept of OAuth or stateful authentication natively
- No intermediate filtering before data reaches the model

### 11.4 Prompt Injection Resistance

Computer use and agentic scenarios face prompt injection risks — malicious actors hiding instructions on websites or in documents. Claude Sonnet 4.6 is a major improvement over Sonnet 4.5 in prompt injection resistance, performing similarly to Opus 4.6 on these evaluations. See Anthropic's [security hardening documentation](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) for mitigation strategies.

---

## 12. Future Roadmap and Evolution

### 12.1 Where MCP Is Heading

The introduction of Tool Search (Jan 2026) and Programmatic Tool Calling GA (Feb 2026) signals Anthropic's direction:

1. **Dynamic discovery over static loading** — Moving away from "all tools upfront"
2. **Code as the orchestration layer** — Claude writes code; sandbox executes; context receives summaries
3. **Context compaction as infrastructure** — Infinite conversations via server-side summarization
4. **Managed sandbox infrastructure** — Anthropic managing code execution, reducing ops burden

**Likely future developments:**
- MCP spec v2 incorporating progressive disclosure and Code Mode as core patterns
- Native OAuth/credential handling standardization
- Tool versioning and capability negotiation
- Semantic search improvements beyond BM25
- Cross-provider programmatic tool calling standardization (LiteLLM already supports this)

### 12.2 Industry Adoption Timeline

- **September 2025**: Cloudflare publishes "Code Mode: The Better Way to Use MCP" — 30–81% token reduction reported
- **November 2025**: Anthropic publishes "Code Execution with MCP: Building More Efficient Agents" — token usage from 150,000 to 2,000 in their test case; Advanced Tool Use beta released
- **Late 2025 – Early 2026**: Open-source adoption — Blocks Goose Agent adds Code Mode MCP support; LiteLLM adds native support across providers
- **January 2026**: Anthropic releases Tool Search Tool to GA — 85% token reduction, accuracy improvements of up to ~25 points on internal MCP evals (e.g., Opus 4: 49% → 74%)
- **February 17, 2026**: Claude Sonnet 4.6 + full GA of Programmatic Tool Calling, Dynamic Filtering, Memory, and Code Execution — the de facto standard for complex agents shifts toward Code Mode

### 12.3 The 2026 Architecture: Hybrid as Default

```
┌───────────────────────────────────────┐
│            AI Agent (LLM)             │
│         Chat / Orchestration Layer    │
│  User messages, system prompt, memory │
│         Final answers only            │
└──────────┬──────────────┬─────────────┘
           │              │
     ┌─────┴────┐   ┌─────┴─────────────┐
     │ MCP with │   │ Programmatic Tool │
     │  Tool    │   │ Calling Sandbox   │
     │  Search  │   │ (Code Execution)  │
     └─────┬────┘   └─────┬─────────────┘
           │              │
     ┌─────┴──────────────┴─────────────┐
     │     Tool Servers / MCP Backends  │
     │  REST, gRPC, DB, vector stores   │
     │  Credentials in bindings, not    │
     │  in model context                │
     └──────────────────────────────────┘
```

**MCP with Tool Search**: for stable, external, third-party tools (Slack, Notion, Stripe)  
**Programmatic Tool Calling**: for complex, privacy-sensitive, multi-step internal workflows  
**Unified sandbox**: managing credentials, security boundaries, and resource limits

---

## 13. Implementation Recommendations

### 13.1 For New Projects (2026 Guidance)

**Phase 1: Foundation (Week 1–2)**
- Implement CLI for each tool/API with `--help` documentation
- Create TypeScript or Python typed wrappers
- Establish a tool registry as the single source of truth

**Phase 2: Agent Integration (Week 3–4)**
- If tool count < 10: Enable traditional MCP or CLI
- If tool count ≥ 10: Enable Tool Search from day one
- If any workflow has 3+ sequential tool calls with data transformation: Enable Programmatic Tool Calling
- Measure token consumption from the start

**Phase 3: Optimization (Week 5+)**
- Enable Dynamic Filtering for any web search use cases
- Migrate complex data-heavy workflows to PTC sandbox
- Add Context Compaction for long-running agents
- Monitor: token usage, latency, success rates, PII exposure

### 13.2 For Existing MCP Implementations

**Assessment first:**
1. Measure actual token consumption
2. Count total tools in your MCP servers
3. Identify high-token tools and high-data-volume calls
4. Analyze query patterns (which tools are used together)

**Quick Win: Enable Tool Search**
If you have 10+ tools:
1. Add `tool_search_tool_regex_20251119` or BM25 variant to your tool list
2. Mark infrequently-used tools with `defer_loading: true`
3. Keep 3–5 essential tools with `defer_loading: false`
4. Optimize tool descriptions with action verbs and keywords
5. Expect 70–85% token reduction

**Enable Dynamic Filtering (Immediate Improvement)**
If you use web search:
1. Switch to `web_search_20260209` tool version
2. Add `betas=["code-execution-web-tools-2026-02-09"]`
3. Get ~11% quality improvement and ~24% token reduction automatically

**Gradual Migration to Programmatic Tool Calling:**
1. Identify 3–5 highest-data-volume tool calls
2. Implement those calls inside a Code Mode sandbox
3. Keep MCP with Tool Search for external/stable tools
4. Monitor improvements and expand

**Example transformation:**
```
BEFORE (Traditional MCP):
├── Google Drive MCP     (12K tokens, 50K data in context)
├── Salesforce MCP       (8K tokens, 20K data in context)
├── Slack MCP            (5K tokens)
└── Custom API MCP       (15K tokens, 100K data in context)

AFTER (Hybrid 2026):
├── Google Drive + Salesforce → PTC Sandbox (data filtered; 2K tokens returned)
├── Slack MCP with Tool Search (5K → ~1.5K tokens, loaded on-demand)
└── Custom API → PTC Sandbox  (100K data filtered to 3K summary)

SAVINGS: ~200K token flow → ~10K tokens (95% reduction)
```

### 13.3 Metrics to Track

| Metric | Measure | Goal |
|--------|---------|------|
| **Initial context load** | Tokens consumed at start | < 5% of context window |
| **Per-request token growth** | Additional tokens per tool call | < 3K tokens per call |
| **Intermediate bloat ratio** | Context size growth during execution | < 1.5× from start (PTC) |
| **Success rate** | % of requests completing correctly | > 98% |
| **End-to-end latency** | Time from request to response | < 15 seconds |
| **Agent autonomy** | % of requests handled without human intervention | > 90% |
| **Tool search hit rate** | % of searches finding relevant tools first try | > 85% |
| **PII leakage rate** | Instances of raw PII appearing in model context | 0 |

---

## 14. Conclusion

The Model Context Protocol solved the fragmentation problem. It then created the context crisis. The solution to the context crisis is now generally available.

The arc from November 2024 to February 2026 is clean: MCP standardized connections → context bloat emerged at scale → Tool Search mitigated discovery bloat → Programmatic Tool Calling eliminated intermediate result bloat → Dynamic Filtering extended Code Mode to web search → Sonnet 4.6 brought it all to GA at no price increase.

### 14.1 Key Takeaways

**The problem is fundamental.** Traditional MCP's design prioritized standardization over efficiency. More tools = more context bloat, regardless of relevance. This was architectural, not incidental.

**The solution stack is layered.** Tool Search handles discovery. Programmatic Tool Calling handles execution. Dynamic Filtering handles web retrieval. Context Compaction handles conversation length. Each layer addresses a specific facet of the context crisis.

**Code Mode is now the de facto standard for complex agents in 2026 — at least in our assessment.** With Sonnet 4.6 and Cloudflare's Code Mode widely deployed, Programmatic Tool Calling is our recommended baseline for any system expected to grow beyond a handful of simple tools. JSON calling remains valid for simple, one-shot, third-party integrations.

**The Opus paradox matters for cost planning.** Dynamic Filtering improves quality for both Sonnet and Opus, but price-weighted token costs behave differently. Sonnet gets cheaper; Opus may get more expensive. Plan accordingly.

**Hybrid is the production architecture.** MCP with Tool Search for external/stable tools; Programmatic Tool Calling for internal/complex workflows; unified sandbox for credentials and security.

### 14.2 For Different Stakeholders

**For MCP creators (Anthropic):** GA of the full advanced tool use platform is a major step. Continue formalizing Code Mode patterns into the MCP spec. Standardize OAuth handling. Define semantic search improvements beyond BM25.

**For AI engineers:** If using MCP with 10+ tools, enable Tool Search immediately. If any workflow involves 3+ sequential tool calls with data transformation, move to Programmatic Tool Calling. Enable Dynamic Filtering for all web search. Measure token consumption continuously.

**For tool vendors:** Provide both MCP servers with Tool Search-optimized descriptions *and* typed code libraries for PTC integration. The market is bifurcating: simple integrations stay JSON; complex workflows go code-first.

**For enterprises:** Audit MCP usage and actual token costs. Enable Tool Search for quick wins. Adopt PTC for privacy-sensitive workloads — the PII Shield pattern keeps sensitive data out of model context by design. Plan for Context Compaction to enable long-running autonomous agents.

### 14.3 The Bigger Picture

This evolution reflects a broader principle: **abstractions must be judged by their actual impact on system goals**, not their architectural purity. MCP is valuable for its standardization benefit. Tool Search extends that value at scale. Programmatic Tool Calling provides the execution layer that MCP's design always needed but couldn't include without sacrificing simplicity.

The best architecture is one that matches each layer to its purpose. We now have the full stack to build agents that are powerful, context-efficient, cost-effective, and secure — all at the same time.

---

## Appendix A: Claude Sonnet 4.6 vs Opus 4.6 — Cost and Performance Guide

### A.1 Pricing and Specs

| Attribute | Sonnet 4.6 | Opus 4.6 |
|-----------|------------|----------|
| **Input tokens** | $3/M | ≈5× Sonnet pricing |
| **Output tokens** | $15/M | ≈5× Sonnet pricing |
| **Context window** | 200K (1M beta) | 200K (1M beta) |
| **Max output** | 64K tokens | 128K tokens |
| **Extended thinking** | Adaptive Thinking | Adaptive Thinking + Fast Mode |
| **Fast Mode** | Not available | Up to 2.5× faster at premium price |
| **Best for** | Production workloads, coding, agents | Deep reasoning, complex analysis |

### A.2 When to Use Each

**Use Sonnet 4.6 when:**
- High-volume production workloads (cost efficiency matters)
- Coding and agentic tasks (Sonnet 4.6 beats Opus 4.5 in 59% of coding sessions)
- Dynamic Filtering for web search (token savings make economics work)
- Computer use automation (major gains on OSWorld-Verified; see Sonnet 4.6 system card for domain-specific results)
- Office document tasks (matches Opus 4.6 on OfficeQA benchmark)

**Use Opus 4.6 when:**
- Deep technical reasoning where Opus's broader capability matters
- Tasks requiring 128K output tokens
- Research-grade analysis where quality trumps cost
- Using Fast Mode for latency-sensitive premium applications

### A.3 Dynamic Filtering Economics by Model

| Model | Quality Gain | Token Cost | Net Value |
|-------|-------------|------------|-----------|
| **Sonnet 4.6** | +11% avg quality | **Decreases ~24%** | Positive: more quality, lower cost |
| **Opus 4.6** | +11% avg quality | **May increase** | Quality gain at potential cost increase |

**Bottom line:** For most production agent systems, Sonnet 4.6 with full Tool Search + PTC + Dynamic Filtering is the optimal configuration — frontier-adjacent intelligence at mid-tier pricing, with better economics from Code Mode than any previous approach.

---

## Appendix B: API Quick Reference for Sonnet 4.6 Features

> **Important:** Versioned tool type names (e.g., `web_search_20260209`, `tool_search_tool_regex_20251119`) and beta flags shown in this appendix mirror Anthropic's naming conventions as of February 2026. Always verify current IDs against the [official API docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) before using in production, as these values are updated with each release.

### B.1 Dynamic Filtering (Web Search)

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["code-execution-web-tools-2026-02-09"],
    tools=[
        {
            "type": "web_search_20260209",  # Versioned for dynamic filtering
            "name": "web_search",
        }
    ],
    messages=[{"role": "user", "content": "Your search query here"}]
)
```

### B.2 Tool Search Tool

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    tools=[
        # The search tool itself - never deferred
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        
        # Your tools - deferred for on-demand discovery
        {
            "name": "github.createPullRequest",
            "description": "Creates a GitHub pull request. Use to propose code changes.",
            "input_schema": {"type": "object", "properties": {"...": "..."}},
            "defer_loading": True
        },
        # Keep essential tools immediately available
        {
            "name": "slack.sendMessage",
            "description": "Send a Slack message to a channel or user.",
            "input_schema": {"type": "object", "properties": {"...": "..."}},
            "defer_loading": False  # Loaded immediately
        }
    ],
    messages=[{"role": "user", "content": "Your request here"}]
)
```

### B.3 Adaptive Thinking

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},  # Claude decides when and how much to think
    messages=[{"role": "user", "content": "Complex reasoning task here"}]
)

# For most use cases, set effort to medium to balance speed/cost/performance
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    effort="medium",  # low / medium / high / max
    messages=[{"role": "user", "content": "Your task here"}]
)
```

### B.4 Context Compaction (Infinite Conversations)

```python
# Context Compaction is server-side and automatic
# Enabled via API configuration when context approaches window limit
# No additional code required — the API handles summarization automatically
# Long-running agents can continue indefinitely
```

> **Note:** Exact configuration flags may differ from what is shown here; refer to the [latest Anthropic API docs](https://platform.claude.com) for current options.

### B.5 1M Token Context Window (Beta)

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["interleaved-thinking-2025-05-14"],  # Required for 1M context beta
    messages=[{
        "role": "user",
        "content": "Analyze this entire codebase..."  # Can include entire repos
    }]
)
```

---

## References and Further Reading

### Official Anthropic Sources

- Anthropic: "Introducing Claude Sonnet 4.6" (February 17, 2026) — [anthropic.com](https://www.anthropic.com/news/claude-sonnet-4-6)
- Anthropic: "Introducing Advanced Tool Use on the Claude Developer Platform" (November 24, 2025) — [anthropic.com](https://www.anthropic.com/engineering/advanced-tool-use)
- Anthropic: "Code Execution with MCP: Building More Efficient Agents" (November 2025)
- Anthropic: "What's New in Claude 4.6" — API Docs — [platform.claude.com](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6)
- Anthropic: "Programmatic Tool Calling" — [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- Anthropic: "Introducing Claude Skills" (2025)
- Anthropic: Claude Sonnet 4.6 System Card (2026)
- Model Context Protocol Specification — [mcp.com](https://mcp.com)

### Partner Sources

- Cloudflare: "Code Mode: The Better Way to Use MCP" (September 2025) — [blog.cloudflare.com](https://blog.cloudflare.com/code-mode/)
- WorkOS: "Cloudflare Code Mode Cuts Token Usage by 81%" (2025)
- GitHub: Claude Sonnet 4.6 General Availability in GitHub Copilot (February 18, 2026)
- Databricks, Replit, Cursor, Cognition, Windsurf, GitHub — Customer testimonials, February 2026

### Community and Research

- MCP-Zero: Active Tool Discovery (arXiv)
- LiteLLM: Native Programmatic Tool Calling Support (Multi-provider)
- Blocks Goose Agent: Code Mode MCP Support
- Speakeasy: "Reducing MCP Token Usage by 100x" (2025)
- OSWorld-Verified Benchmark — [os-world.github.io](https://os-world.github.io/)
- Vending-Bench Arena — [andonlabs.com](https://andonlabs.com/evals/vending-bench-arena)

---

## Changelog

### Version 3.0 (February 20, 2026) — Major Revision
- **New framing**: Repositioned as "The Transition to Code-Mode Agents"
- **Sonnet 4.6 coverage**: Full section on February 17 release and GA of Programmatic Tool Calling
- **Dynamic Filtering**: New dedicated section with benchmark data (BrowseComp, Deep Search QA)
- **Opus Paradox**: Added nuanced cost analysis for Opus 4.6 vs Sonnet 4.6 in Code Mode
- **Updated decision matrix**: PTC elevated to "new default" for complex agent workflows
- **Revised 80/10/10 Rule**: Inverted to "code-APIs first" design philosophy
- **Context Compaction**: New section on infinite conversation API
- **Appendix A**: Sonnet 4.6 vs Opus 4.6 cost and performance guide
- **Appendix B**: Complete API quick reference for all Sonnet 4.6 features
- **Security**: Added PII Shield section and prompt injection resistance updates
- **MCP-Zero**: Repositioned as research/advanced pattern, not production default
- **Tool Use Examples**: Added as new GA feature from advanced tool use platform

### Version 2.0 (January 16, 2026)
- Added comprehensive section on MCP Tool Search (Section 4)
- Updated benchmarks with Tool Search data
- Enhanced case study with Tool Search comparison
- Updated decision matrix and trade-offs
- Revised executive summary and conclusion
- Added references to January 2026 announcements

### Version 1.0 (December 2025)
- Initial release
- Comprehensive analysis of MCP scalability issues
- Code execution, CLI, Scripts, and Skills approaches
- Original benchmarks and case studies

**Related:**
- [Agent-Skills](../Agents/skills/Agent-Skills.md) — Skills are positioned as one of the mitigations in v3's evolutionary story alongside Tool Search and Code Mode.
- [OpenClaw(Moltbot-or-Clawdbot)-Architecture](../Agents/openclaw/OpenClaw%28Moltbot-or-Clawdbot%29-Architecture.md) — Updated OpenClaw architecture where dynamic tool discovery addresses the v3-quantified scalability bottlenecks.
- [AI-Coding-Loops](../Agents/development/AI-Coding-Loops.md) — AI-coding loop patterns that benefit most from v3's Code Mode default for multi-tool, multi-step agent workflows.
