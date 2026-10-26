# Tokenomics & Model Routing for Coding Workflows

Use the cheapest model that reliably completes the task. Spend more when a missed dependency, security boundary, or design mistake would create expensive rework.

This guide adapts the supplied directive for a workflow centered on **VS Code (95%)**, with **Claude Code CLI (5%)** for tasks that benefit from an automated edit–test loop. These percentages describe the intended workflow, not an optimal allocation established by experiments.

**Integration scope:** the VS Code extension/provider is not specified. Routing applies generally; slash commands, thinking controls, billing-path TTLs, and session telemetry below are **Claude Code only** unless your extension documents equivalent support. Per-message effort is a Claude API feature, not a guaranteed editor control.

**Brief before tools:** state the task, guardrails, and definition of done. The repository supplies code; priorities and acceptable trade-offs still need explicit evidence. Plan first for unfamiliar or cross-cutting work, rather than making Plan Mode mandatory for every edit.

## 1. Route by the work, not habit

The names below come from the supplied catalog. Treat the matrix as a **starting policy to evaluate**, not a benchmark ranking. Check exact model availability, pricing, and supported reasoning settings in your provider. The source’s “GPT 6 Lune” spelling refers here to the verified **GPT 6 Luna** model; the original GPT 5.6 routing is retained, with GPT 6 Luna compared below.

“Low-Cost,” “Balanced,” and “High-Cost” are the directive's planning labels, not verified relative prices across providers. In particular, GPT 6 Sol should not automatically be assumed more expensive than GPT 5.6 Sol. [OpenAI pricing](https://developers.openai.com/api/docs/pricing)

### 1a. GPT routing

| Stage | Starting model | Environment | Effort* | Planning tier | Risk when downgrading too far |
|---|---|---|---|---|---|
| 1. Intake & clarification | GPT 5.6 Sol | VS Code | Medium | Balanced | Overlooks ambiguous requirements |
| 2. Architecture & dependencies | GPT 5.6 Sol; GPT 6 Sol if complex | VS Code | Medium → High if needed | Balanced → High-Cost | Misses callers, side effects, or contracts |
| 3. Scope freeze | Current planning model; Luna at a boundary | VS Code | Keep current effort; Low at a boundary | Current tier / Low-Cost | Marks an incomplete checklist as complete |
| 4. Targeted implementation | GPT 5.6 Sol | VS Code | Medium | Balanced | Produces plausible code that breaks integration |
| 5. Spec alignment | GPT 5.6 Sol | VS Code | Medium | Balanced | Checks wording but misses behavioral gaps |
| 6. Execution flow & tests | GPT 5.6 Sol | VS Code | Medium | Balanced | Omits failure paths or weakens assertions |
| 7. Security & performance audit | GPT 6 Sol | VS Code | High | High-Cost | Misses auth, concurrency, or resource risks |
| 8. PR description & feedback | GPT 5.6 Luna | VS Code | Low | Low-Cost | Drops an important finding from the summary |

*Effort is an intent, not a portable API setting. Use Off only where supported and appropriate for straightforward formatting.*

### 1b. Claude routing (org-supported models only)

**Routing catalog:** Haiku 5.5 joins Sonnet 5/5.5 and Opus 4.8/5/5.5. Use it where your organization and integration expose it; public release does not establish access in every editor. API model ID: `claude-haiku-5-5`. [Haiku overview](https://platform.claude.com/docs/en/models/haiku-5-5/overview)

**Standard API list prices, checked October 15, 2026 ($ per million tokens):**

| Model | Input | Output | Cache read |
|---|---|---|---|
| Haiku 5.5, prompt ≤100K | $0.10 | $0.50 | $0.01 |
| Haiku 5.5, prompt >100K | $0.50 | $2.50 | $0.05 |
| Sonnet 5 | $2 | $10 | $0.20 |
| Sonnet 5.5 | $2 | $10 | $0.10 |
| Opus 4.8 / 5 | $5 | $25 | $0.50 |
| Opus 5.5 | $4 | $20 | $0.20 |

Sonnet 5 is not cheaper per token than 5.5; Opus 5.5 is cheaper per token than 5/4.8. Task token use, quality, contracted rates, and subscription allowances still determine value. [Anthropic list pricing](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing)

| Stage | Starting model | Escalate / alternate | Environment | Effort* | Planning tier | Risk when downgrading too far |
|---|---|---|---|---|---|---|
| 1. Intake & clarification | Sonnet 5.5 | Opus 5.5 | VS Code | Medium | Balanced | Overlooks ambiguous requirements |
| 2. Architecture & dependencies | Sonnet 5.5 | Opus 5.5 if complex | VS Code | Medium → High if needed | Balanced → High-Cost | Misses callers, side effects, or contracts |
| 3. Scope freeze | Current planning model; Haiku 5.5 at a boundary | Sonnet 5.5 for unresolved semantics | VS Code | Keep current effort; Low on Haiku | Current tier / Low-Cost | Marks an incomplete checklist as complete |
| 4. Targeted implementation | Sonnet 5.5 | Opus 5.5 | VS Code | Medium | Balanced | Produces plausible code that breaks integration |
| 5. Spec alignment | Sonnet 5.5 | Opus 5.5 | VS Code | Medium | Balanced | Checks wording but misses behavioral gaps |
| 6. Execution flow & tests | Sonnet 5.5 | Opus 5.5 | VS Code | Medium | Balanced | Omits failure paths or weakens assertions |
| 7. Security & performance audit | Opus 5.5 | Opus 5/4.8 if evaluations favor them | VS Code | High | High-Cost | Misses auth, concurrency, or resource risks |
| 8. PR description & feedback | Haiku 5.5 | Sonnet 5.5 if key findings are lost | VS Code | Low | Low-Cost | Drops an important finding from the summary |

*Effort is an intent, not a portable setting; map it to whatever reasoning/thinking control your VS Code integration or Claude Code exposes.*

### 1c. Haiku 5.5 vs GPT 6 Luna

**Standard direct API rates, checked October 15, 2026.** These are not Copilot credit rates or subscription allowances. Each price tuple is **input / output / cache read, $ per million tokens**.

| Aspect | Haiku 5.5 | GPT 6 Luna |
|---|---|---|
| API ID | `claude-haiku-5-5` | `gpt-6-luna` |
| Short-prompt rates | ≤100K: **$0.10 / $0.50 / $0.01** | ≤272K: **$0.10 / $0.50 / $0.01** |
| Longer-prompt rates | >100K: **$0.50 / $2.50 / $0.05** | >272K: **$0.20 / $0.75 / $0.02** |
| Advertised context / max output | 1M / 128K | 1.05M / 128K |
| Reasoning controls | Adaptive thinking; use Low for checkable work; Claude Code cannot disable it | API effort supports `none`, `low`, `medium`, `high`, `xhigh`, `max`; editor controls may differ |
| First tasks to evaluate | Extraction, checklist matching, summaries, scoped discovery | The same tasks; particularly worth testing for 100K–272K prompts |

Sources: [Haiku specifications and pricing](https://platform.claude.com/docs/en/models/haiku-5-5/overview), [Claude Code controls](https://code.claude.com/docs/en/model-config), [GPT 6 Luna specifications](https://developers.openai.com/api/docs/models/gpt-6-luna), [OpenAI rate card](https://developers.openai.com/api/docs/pricing).

**What this means:** below 100K there is no base-rate winner. Between 100K and 272K, Luna’s listed rates are one-fifth Haiku’s; above 272K Luna also has a premium. Threshold pricing applies to the request, not just excess tokens; cached content counts toward prompt length. Cache writes are separate categories—do not add ordinary input charges again for the same written tokens.

**Illustration:** 150K ordinary input tokens plus 10K billed output tokens cost **$0.10 on Haiku vs $0.02 on Luna**, excluding cache writes, tools, and other modifiers. This normalizes token counts for arithmetic; tokenizers, hidden reasoning, retries, and quality can make actual task costs different.

**Routing rule:** prefer the validated option already in your harness for small tasks; test Luna when Haiku’s >100K boundary matters. Compare both on the same accepted checklist/summary tasks and count omissions, repairs, latency, and total billed cost. Neither price nor a larger window proves better coding ability; keep architecture and risk-sensitive reviews on a proven stronger tier.

**Stage 2 escalation triggers:** changes to public contracts; multiple callers or modules; persistence, auth, or concurrency; migrations; or unclear requirements. Any hit routes architecture review to **GPT 6 Sol or Opus 5.5 at High**. Resolve uncertainty before implementation; this is a conservative workflow rule, not a benchmark claim.

**Keep the default simple:** Haiku 5.5 for checkable extraction, explicit checklists, and summaries; Sonnet 5.5 for implementation and semantic review; Opus 5.5 for unresolved complexity or high-risk review. Promote Haiku only after it passes the same acceptance checks; do not automatically move architecture or security audits to it. Opus 5 and 4.8 are alternatives only if evaluations show a benefit. Retain Sonnet 5 for mechanical tasks only if it achieves lower total task cost at acceptable quality; test whether thinking can be disabled in your integration rather than assuming it.

**Downgrade when evidence supports it:** reduce effort or use a cheaper proven option for mechanical work. Haiku 5.5, Sonnet 5.5, and Opus 5.5 cannot disable thinking in Claude Code; `/effort` controls reasoning intensity. Escalate whenever task risk warrants it. [Claude Code thinking controls](https://code.claude.com/docs/en/costs#adjust-extended-thinking)

```mermaid
flowchart TD
    A[Define acceptance checks] --> B{Task has unresolved complexity?}
    B -->|Yes| C[Resolve design with deeper reasoning]
    B -->|No| D[Choose cheapest proven model]
    C --> D
    D --> E[Implement and run checks]
    E --> F{Checks and review pass?}
    F -->|Yes| G[Summarize and prepare PR]
    F -->|No| H[Inspect failure and missing context]
    H --> I[Repair context or escalate model]
    I --> E
```

Claude escalation for step I, after repairing context: **Haiku 5.5 → Sonnet 5.5 → Opus 5.5**, starting at the tier appropriate to the task. Opus 5/4.8 are evaluated alternatives, not cost-saving steps.

**Review behavior, not just presence:** map each acceptance criterion to the implementation and a test or concrete execution path. Mechanical checklist checks can run at Low effort; keep semantic alignment at Medium by default. Escalate based on risk and missed findings, not simply the model that wrote the code.

**Reasoning has a cost:** OpenAI reasoning and Claude thinking tokens are billed as output tokens, including reasoning not shown in the answer. Bound the question (for example, concurrency, state changes, and API compatibility); use provider-supported budget controls where available. Low/Medium/High do not imply universal token caps or a fixed cost multiplier. [OpenAI reasoning billing](https://developers.openai.com/api/docs/guides/reasoning) · [Claude thinking billing](https://code.claude.com/docs/en/costs#adjust-extended-thinking)

**Reduce switching friction:** the eight stages are checkpoints, not eight required model or effort changes. Keep stages 4–6 on the same model and effort unless evidence warrants a change.

| Working group | Stages | Practical default |
|---|---|---|
| Discover & lock scope | 1–3 | Balanced model; escalate unresolved architecture, then save a handoff |
| Build & validate | 4–6 | Stay on GPT 5.6 Sol or Sonnet 5.5 for the edit–test–review loop |
| Audit & prepare PR | 7–8 | High effort by default for audit; summarize with the cheapest proven option |

## 2. Keep useful context; drop the debate

Before switching from planning to coding, save a compact handoff: **goal, acceptance criteria, design decisions, affected files and interfaces, constraints, known risks, and test commands**. Start fresh when obsolete exploration obscures the task, but compare the reset cost with continuing a cached session. Include the handoff and relevant code, not just a vague summary.

```markdown
## Handoff: [ticket/module]
- Objective and acceptance criteria:
- Target files and public interface changes:
- Design decisions, constraints, and non-goals:
- Edge cases and known risks:
- Test commands and current results:
```

Make non-goals concrete—for example, “no new helper framework or public API changes”—to constrain unnecessary abstractions and scope expansion.

| Token driver | Practical response |
|---|---|
| Repeated full-file reads | Send the diff plus enough surrounding code and callers to understand behavior |
| Growing conversation history | Carry forward settled decisions; remove obsolete alternatives |
| Long tool logs and retry loops | Keep actionable errors; diagnose before repeating commands |
| Excessive reasoning or output | Ask for a bounded result; increase effort when failures justify it |
| Lost cache reuse | Compare total input cost, including cache writes, before resetting or compacting |
| Large instruction files | Keep essential rules short; load detailed references on demand and enforce style with tooling |

**Illustrative arithmetic:** resending an unchanged 20,000-token block over five requests contributes 100,000 input tokens. This is not a bill estimate: caching and provider rates affect cost. Context growth is not inherently exponential. [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

**Switch at useful boundaries:** prefer changing model/effort after stage 3 or before stage 7, carrying a compact handoff, relevant diff, and check results. Start fresh if that removes obsolete context, but compare reset/write costs with continuing the cached session. Within discovery, keep stage 3 at the current planning effort (normally Medium, High after escalation). Lower effort for stage 8 at a summary boundary only when worthwhile; use supported per-message effort where the integration exposes it. Escalate promptly if risk demands it, regardless of boundaries.

**Preserve reusable context:** keep instructions and tool definitions stable, followed by changing task details. Cache hits require matching eligible prefixes; resets, compaction, and model changes may lose reuse. Effort-change behavior is version/route-specific: current Claude Code preserves it by default on supported 5.5 direct routes, with cloud/gateway exceptions; supported append-only changes can preserve earlier prefixes elsewhere. [Claude Code cache behavior](https://code.claude.com/docs/en/prompt-caching) · [OpenAI caching](https://developers.openai.com/api/docs/guides/prompt-caching) · [Claude caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

**Watch lifetime and rates** (billing-path details rechecked October 26): Claude API defaults to five minutes, refreshed on reuse and measured from request start, so response generation time counts against the lifetime. Writes cost 1.25× base input for five minutes or 2× for one hour, in place of, not on top of, the 1× base rate. Within this catalog, reads cost 0.1×, except Opus 5.5 and Sonnet 5.5 at 0.05×. Claude Code uses one hour on subscriptions, five minutes by default on API/cloud or usage credits, with separate configurable subagent TTLs. See the [cross-harness comparison](Context-Windows-Compaction-and-Cache-Breaks-2026.md#cache-policy-depends-on-the-harness-model-and-billing-path). Check `/usage` for the effective TTL. Batch useful work without rushing review or sending keep-alive prompts. [Cache rates](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing) · [Claude Code TTL](https://code.claude.com/docs/en/costs#why-usage-climbs-in-a-long-session)

Give the model symbol definitions, references, and compiler/type-checker output when needed. AST-aware tools help locate dependencies; neither a large context window nor high reasoning guarantees that the right evidence was supplied. Stop increasing effort when it adds no measurable improvement.

### Smaller working budgets and long breaks

A 1M context window is capacity, not a bill for 1M tokens. Cache expiry depends on time and matching prefixes, not whether the window fills. Earlier compaction bounds accumulated history but can itself cost tokens and rebuild part of the cache.

For small/medium work, trial an absolute token threshold rather than blindly choosing 40%: 40% of 1M is still about 400K. Keep enough room for the task, recent evidence, and output. Before a planned long break, save decisions, unfinished work, paths, and check results; resume the old session when that evidence is still needed, or use the handoff to start focused. Auto-compaction is a safety net, not a replacement for these boundaries.

See [Context Windows, Compaction, and Cache Breaks](Context-Windows-Compaction-and-Cache-Breaks-2026.md) for the video analysis, OMP’s actual defaults, a 40% configuration example, and cost trade-offs. Configuration examples are documentation only; no installed settings were changed.

### Filter output without losing evidence

Prefer targeted search, symbol navigation, and deterministic noise filtering before semantic rewriting. Preserve exit codes, relevant stack frames, type definitions, and meaningful JSON values; keep original logs available through a path or retrieval tool. Fixed head/tail limits can hide the actual failure. Compress new tool output once and retain its representation unchanged; rewriting old history can break cache reuse.

**Evidence has limits:** the [CAPC preprint](https://arxiv.org/abs/2607.15516) finds both cost increases from query-aware compression and savings from cache-aware compression. [tokbench](https://github.com/Entelligentsia/tokbench) reports 237 versus 180 turns in a pilot with one run per arm. Neither proves a universal savings rate or that compression caused extra turns.

Keep instruction files focused; load specialist references and skills when needed. Anthropic’s under-200-line CLAUDE.md target is guidance, not a hard limit. Test skills against a baseline and keep those that improve outcomes. Deferred tool loading means MCP definitions are not necessarily all sent up front. [Claude memory](https://code.claude.com/docs/en/memory) · [Tool search](https://code.claude.com/docs/en/mcp)

## 3. When Claude Code earns its place

Choose the CLI when automated navigation, coordinated edits, and test execution save enough manual work to justify extra agent turns. VS Code agent modes can also make multiple model/tool calls; an editor is not inherently cheaper or limited to one request.

| Situation | Claude Code model | Why |
|---|---|---|
| Routine edit–test loop, plan already approved | Sonnet 5.5 | Settled design; the loop does the work |
| Mechanical changes or scoped discovery | Haiku 5.5 Low, once validated | Checkable work; preserve context and measure retries |
| Repeated failures or unresolved design complexity | Opus 5.5 | Escalate after context repair, not before |
| High-stakes cross-cutting change | Opus 5.5 | Cost of a missed dependency exceeds model cost |

Model choice stays subject to your org's pricing and measured results; Opus 4.8 can be added to the comparison as another Opus-tier data point; do not assume it is cheaper.

**Keep loops bounded:** if the same failure repeats twice without new evidence, pause for diagnosis before another edit. This is a practical tripwire, not a mandatory session reset. Preserve the error, inspect the cause, and repair context or seek help. For supported non-interactive runs, set a spend cap with `--max-budget-usd`; use available turn limits too.

Use targeted tests during iteration, then run the required broader checks before completion. When discovery history becomes distracting, consider `/compact` with instructions to preserve decisions, code changes, and test results; compaction can reduce cache reuse. Inspect `/usage` for token counts; v2.1.251+ shows cache warmth and TTL. Session dollars are list-price estimates unless admins configure `modelPricing`, not subscription-seat bills. Use provider billing for actual spend. [Claude Code cost management](https://code.claude.com/docs/en/costs)

There is **no defensible universal “three files” threshold**. A small change can be risky; a large rename can be mechanical. Prefer whichever environment provides the necessary tools with less handoff overhead. [Claude Code cost management](https://code.claude.com/docs/en/costs)

```mermaid
flowchart LR
    A[Approved plan] --> B{Automated edit-test loop useful?}
    B -->|No| C[Stay in VS Code]
    B -->|Yes| D[Use Claude Code]
    C --> E[Validate diff and behavior]
    D --> E
```

**Bound autonomy:** use least-privilege permissions, sandboxing, and isolated worktrees where appropriate. Hooks can enforce specific checks, but are code that needs testing—not a zero-risk or zero-cost guarantee. Keep publishing, destructive actions, and commits within explicit authorization. Rewind does not undo every external side effect. [Security](https://code.claude.com/docs/en/security) · [Hooks](https://code.claude.com/docs/en/hooks)

Delegate noisy research only when isolation is useful; subagents add their own billable calls. Use an available, validated model and cap parallel work, time, and spend. Scheduled/headless runs need the same acceptance checks and stop conditions. Prefer measurable budgets over automatic resets after 15–25 turns or at a fixed context percentage.

## 4. Make the savings empirical

Compare representative tasks using the same acceptance checks. Record model and effort, uncached/cached input, output and billed reasoning tokens where available, retries, tokens/spend attributable to fixes or reverts, elapsed time, review time, and defects found. Avoid counting reasoning tokens twice if the provider already includes them in output totals. Keep task complexity comparable; repeat before generalizing.

**Read the whole invoice:** input contains more than your prompt—retained history, tool results, instructions, and loaded schemas also count. Thinking and tool-call arguments are generated tokens; cache reads/writes are distinct input billing categories where applicable. Workers, retries, and compaction add requests, while hosted tools, storage, containers, and CI can add separate fees. Avoid double-counting thinking or included credits. See [The AI Coding Invoice](AI-Coding-Invoice-Beyond-Input-and-Output-2026.md) for a presentation-ready breakdown, worked example, video validation, and audience questions.

Run three focused Claude comparisons, holding task scope and acceptance checks constant:

| Stages | Comparison | Primary metric |
|---|---|---|
| 3, 8: checklists and summaries | Haiku 5.5 Low vs Sonnet 5.5 Low; Sonnet 5 optional | Total task cost at equal acceptance quality, including switching/cache costs |
| 7: audit | Opus 5.5 vs Opus 5/4.8 | Seeded defects caught, with false positives and task cost recorded |
| 2: architecture | Sonnet 5.5 High vs Opus 5.5 High | Required dependencies/contracts identified and design checks passed, with task cost recorded |

**Cost per accepted change = total model/tool spend ÷ accepted changes.** Track developer time separately, or convert it using an explicit hourly rate. A cheap first response is a poor saving if it creates repeated repairs.

Run compilation/type checks, linting, and relevant tests in stage 4 before stage 5 alignment review. Stage 6 assesses test adequacy, failure paths, and missing cases; stage 7 reviews security and performance risks. Keep these checks and human review as the quality gates. “Zero defects” is an aspiration; no model routing policy proves it.

## 5. Integration-specific controls

These tips apply only when you use the named product; they do not identify which extension your org uses.

| Surface | Useful controls and billing caveats |
|---|---|
| GitHub Copilot in VS Code | Paid Auto selection offers a 10% discount and task-aware routing; it is not limited to cheap models. Paid inline completions/next edits do not consume AI credits. Inspect Agent Debug Logs → Cache Explorer for actual reuse. |
| Copilot caching | Generic GitHub guidance says OpenAI 24h/most others 1h; actual model-generation policy needs request/usage evidence. Use Copilot’s rate card. Content exclusions do not protect Edit/Agent/cloud modes. |
| Claude Code | `/context` inspects usage; `/doctor prompt-audit` and `/skill-doctor` audit guidance where supported. `claude plugin eval` compares plugin-on/off runs. Native isolation uses `claude --worktree <name>`. |
| Claude Code reasoning and goals | `ultrathink` is recognized for deeper reasoning on one turn, without a fixed 32k budget; `think hard` is ordinary text. `/goal` can keep work moving, but a natural-language turn limit is not a hard runtime cap. |

Sources: [Copilot Auto](https://docs.github.com/en/copilot/concepts/models/auto-model-selection), [billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing), [cache guidance](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage), [Cache Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer), [exclusions](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/content-exclusion), [Claude commands](https://code.claude.com/docs/en/commands), [model configuration](https://code.claude.com/docs/en/model-config), [goals](https://code.claude.com/docs/en/goal).

## 6. Source validation

Collected video and community claims were checked on October 11, 2026. See the [point-by-point validation](Tokenomics-Source-Validation-Oct-2026.md) for command corrections, Copilot-specific billing/cache details, and unsupported numerical claims. Driving-autonomy levels, step-success arithmetic, and “industry consensus” labels do not establish measured agent reliability.

---

**Related:**
- [Context Windows, Compaction, and Cache Breaks](Context-Windows-Compaction-and-Cache-Breaks-2026.md) — Smaller working budgets, handoffs, and OMP configuration trade-offs.
- [Tokenomics Source Validation](Tokenomics-Source-Validation-Oct-2026.md) — Detailed evidence and qualifications behind the collected tips.
- [GenAI Cost Optimization](GenAI-cost-Optimization.md) — Broader practices for reducing inference and infrastructure spend.
- [The AI Coding Invoice](AI-Coding-Invoice-Beyond-Input-and-Output-2026.md) — Token buckets, request multipliers, separate fees, and presentation questions.
- [Headroom & RTK: Real-World Feedback](Headroom-RTK-Real-World-Feedback-2026.md) — Cache and correctness risks that make end-to-end measurement necessary.
