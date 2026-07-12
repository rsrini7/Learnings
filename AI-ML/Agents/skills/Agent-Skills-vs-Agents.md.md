# **AI Coding Agents in Practice (2026)**

Why Passive Context Beat Agent Skills — and When Skills Still Matter**

**A consolidated analysis of two recent YouTube videos from the Better Stack ecosystem examining Vercel’s Agent Skills vs AGENTS.md approach.**

<i class="fas fa-play-circle"></i> Skills Had ONE Job (They Failed)

<i class="fas fa-play-circle"></i> [Why Skills is the Wrong Abstraction for Agents](https://www.youtube.com/watch?v=A_1ELXEVp5w)

---

## 1. Executive Summary

Two closely related videos published in late January 2026 provide one of the **clearest real-world evaluations** to date of modern AI coding agent techniques:

* **Skills Had ONE Job (They Failed) Video** presents a **controlled internal evaluation by Vercel**, comparing *Agent Skills* (active retrieval) against a simple *AGENTS.md* file (passive context).
* **Why Skills is the Wrong Abstraction for Agents Video** demonstrates **how Agent Skills still work well** when used intentionally for narrow, action-oriented tasks.

**Core conclusion:**

> For *general framework knowledge and correctness*, **passive context (AGENTS.md)** significantly outperforms **on-demand Agent Skills**.
> For *specialized workflows and tooling*, **Skills remain valuable**.

This finding runs counter to much of the recent hype around modular, retrieval-based agent architectures.

---

## 2. Skills Had ONE Job (They Failed) — Why “Skills” Underperformed in Practice

### Context

Vercel evaluated how well AI coding agents could adopt **Next.js 16 APIs** that were:

* Newly released
* Absent from model training data
* Behaviorally distinct from prior versions

This makes the test especially credible: **the models could not rely on memorization**.

### Objective

Teach agents to correctly use Next.js 16 APIs such as:

* `'use cache'`
* `connection()`, `cacheLife()`, `cacheTag()`
* `forbidden()`, `unauthorized()`
* Async `cookies()` / `headers()`
* `after()`, `updateTag()`, `refresh()`
* `proxy.ts`

---

## 3. Approaches Compared

### A. Agent Skills (Active Retrieval)

**Definition**

* An open standard (`agentskills.io`)
* Packaged documentation + tools
* Loaded *only if* the agent decides to invoke them

**Observed Issues**

1. **Invocation failure**

   * In ~56% of runs, the agent never invoked the skill at all.
2. **Prompt fragility**

   * Minor wording changes (“explore project first” vs “invoke skill first”) caused large outcome swings.
3. **Decision bottleneck**

   * The agent must *realize it doesn’t know* something before it can retrieve knowledge.
4. **Noise cost**

   * Installed but unused skills still add cognitive overhead.

---

### B. AGENTS.md (Passive Context)

**Definition**

* A single markdown file placed at repo root
* Automatically injected into the agent’s system prompt *every turn*

**Key Design Choices**

* **Compressed documentation index (~8KB)**, not full docs
* Index maps concepts → actual `.mdx` files in a local docs folder
* Explicit instruction to override pretrained assumptions:

> *“Prefer retrieval-led reasoning over pre-training-led reasoning for any Next.js tasks.”*

This single line proved surprisingly powerful.

---

## 4. Evaluation Results (As Reported)

| Configuration               | Overall  | Build | Lint | Tests |
| --------------------------- | -------- | ----- | ---- | ----- |
| Baseline (no docs)          | 53%      | 84%   | 95%  | 63%   |
| Skill (default)             | 53%      | 84%   | 89%  | 58%   |
| Skill + forced instructions | 79%      | 95%   | 100% | 84%   |
| **AGENTS.md (doc index)**   | **100%** | 100%  | 100% | 100%  |

---

## 5. Why Passive Context Won

This outcome wasn’t about *more tokens*—it was about **eliminating uncertainty**.

**AGENTS.md advantages:**

* Zero decision latency
* No “should I load this?” reasoning step
* Stable across retries
* Works with current agent architectures
* Extremely token-efficient when compressed correctly

In short: **agents reason better when the knowledge is already present**.

---

## 6. Why Skills is the Wrong Abstraction for Agents — Where Agent Skills *Do* Work Well

The second video reframes Skills correctly—not as a replacement for context, but as **task-specific augmentations**.

### Effective Use Cases for Skills

* Code migrations
* Framework upgrades
* Opinionated best-practice enforcement
* Tool-driven workflows (Stripe, Tailwind, Shadcn/UI, Remotion)
* Repetitive multi-step actions

### Why They Work Here

* Clear entry point
* Narrow scope
* Action-oriented outcomes
* Reduced ambiguity about *when* to invoke the skill

---

## 7. Reconciled Mental Model (Important)

**This is not a contradiction — it’s a layering model.**

| Layer                  | Best Tool                        |
| ---------------------- | -------------------------------- |
| Foundational knowledge | **AGENTS.md / CLAUDE.md**        |
| Framework semantics    | **Passive context + local docs** |
| Specialized actions    | **Agent Skills**                 |
| One-off workflows      | **Explicit prompting**           |

Trying to make Skills do *everything* introduces fragility.

---

## 8. Practical Recommendations (2026-Ready)

### For Framework / Platform Teams

* Ship **AGENTS.md by default**
* Include compressed doc indexes, not full manuals
* Add explicit instructions to override pretrained assumptions

> Vercel already provides:
> `npx @next/codemod@canary agents-md`

### For Tooling / DevEx Teams

* Use Skills for:

  * Codemods
  * Enforcement
  * Repeatable workflows
* Avoid Skills for:

  * General framework understanding
  * Core API semantics

### For Enterprise Engineering Orgs

* Treat AI agents like **junior engineers with perfect recall but weak judgment**
* Reduce decision points
* Bias toward **always-available context**

---

## 9. Final Takeaway

The most important insight from these videos is not about Skills vs AGENTS.md—it’s about **how current AI agents think**.

> *Agents don’t fail because they lack tools.
> They fail because they hesitate to use them.*

Until agent reasoning improves, **passive, well-designed context will outperform “smart” retrieval systems** for correctness-critical engineering tasks.


<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" integrity="sha384-gfdkjb5BdAXd+lj+gudLWI+BXq4IuLW5IT+brZEZsLFm++aCMlF1V92rMkPaX4PP" crossorigin="anonymous">

**Related:**- [Agent-Skills](Agent-Skills.md) — the canonical Skills definition and folder structure that this Vercel eval is critiquing.- [Agent-Specs-vs-Rules-vs-Skills](Agent-Specs-vs-Rules-vs-Skills.md) — UACF's master AGENTS.md is exactly the passive-context approach this article recommends over on-demand Skills.- [claude-agents-vs-sub-agents-vs-projects-vs-workflow-vs-rules-vs-mcp-vs-skills](claude-agents-vs-sub-agents-vs-projects-vs-workflow-vs-rules-vs-mcp-vs-skills.md) — Rules (CLAUDE.md) and Projects serve the same passive-context role as AGENTS.md in the Skills vs. passive-context debate.- [AI-Coding-Loops](../development/AI-Coding-Loops.md) — its 'smallest autonomy that solves the problem' framing validates the article's preference for always-loaded context over retrieval.
