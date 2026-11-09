# SlopCodeBench vs. GDPx: Long-Horizon Frontiers of Code Erosion and Macroeconomic Agency

**Daily learning · 3 November 2026 · Benchmark comparison review**

> **Core idea:** While legacy evaluations test isolated single-turn completions, **SlopCodeBench** (UW-Madison / Dex Horthy campaign telemetry) and **GDPx** (SemiAnalysis) expose the brittle failure modes of frontier AI agents on long-horizon, multi-hour workloads where top models fail over 83% of the time. Comprehensive campaign data reveals that increasing reasoning effort often *backfires*—raising costs up to 4.2× while reducing strict pass rates—and that coding agents accumulate catastrophic technical debt across mutating specifications, producing 2.3× more verbose and 2.0× more structurally eroded code than humans.

---

## 1. Foundations: Two Divergent Axes of Frontier Agent Stress-Testing

Over the past three years, foundation models saturated static, single-turn evaluations such as MMLU, GSM8K, and HumanEval. Even software-specific benchmarks like SWE-bench evaluate an agent on a fixed, one-off goal: take an issue description, inspect a codebase once, generate a patch, and pass the accompanying unit test.

In production engineering, software evolves across dozens of sequential pull requests; code authored for initial requirements must be refactored, extended, or safely deleted as specifications mutate. Similarly, enterprise knowledge work requires multi-hour autonomous execution across interdependent corporate systems.

In late 2026, two landmark evaluation suites emerged to measure these long-horizon dynamics from complementary angles:

1. **SlopCodeBench ([arXiv:2603.24755](https://arxiv.org/abs/2603.24755), [scbench.ai](https://www.scbench.ai)):** Developed by Gabriel Orlanski and researchers at UW-Madison (SprocketLab), with full campaign telemetry released by Dex Horthy ([X disclosure](https://x.com/dexhorthy/status/2115115507183685850)). It evaluates **code maintainability, architectural degradation, and technical debt accumulation** across 36 multi-stage development problems and 196 sequential checkpoints. Agents implement an initial spec from scratch, then must repeatedly adapt their *own* code as specs evolve.
2. **GDPx ([SemiAnalysis](https://newsletter.semianalysis.com/p/gdpx-measuring-frontier-model-capabilities)):** Authored by Dylan Patel, Max Kan, and Andrew Megalaa at SemiAnalysis as the spiritual successor to OpenAI's GDPval. It evaluates **macroeconomic problem-solving across 11 high-ROI enterprise sectors** (such as Chip Design, Live Cybersecurity, Quant Trading, Biology, and Legal). Running for up to 8 hours per task in native agent runtimes (Claude Code, Codex), it measures raw domain capability, cross-sector variance, and dollar cost per completed task.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Frontier Long-Horizon Benchmark Comparison                      │
├──────────────────────────────┬─────────────────────────────┬───────────────────────────┤
│ Dimension                    │ SlopCodeBench (UW / Horthy) │ GDPx (SemiAnalysis)       │
├──────────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ Evaluated Axis               │ Longitudinal Code Health    │ Macroeconomic Competence  │
│ Workload Nature              │ Evolving Checkpoints        │ 8-Hour Deep Domain Tasks  │
│ Scope                        │ Software Engineering        │ 11 High-Value Industries  │
│ Primary Failure Mode         │ Technical Debt / Slop       │ Safety Sandbagging / Math │
│ Top Model & Score            │ GPT-6 Astra XHigh (16.33%)  │ Claude Opus 5.5 (12.0%)   │
│ End-to-End Solve Rate        │ 0.0% (Across 10 Campaigns)  │ 0.0% (Finance & Legal)    │
│ Cost Range Tested            │ $178.51 – $1,550.07 / Run   │ $9.78 – $51.41 / Task     │
└──────────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

### The Code Degradation Lifecycle

![SlopCodeBench Iterative Spec Degradation Lifecycle](../../assets/SlopCodeBench-Iterative-Spec-Degradation-Lifecycle-Nov-2026.jpg)
*Figure 1: The lifecycle of code degradation in SlopCodeBench. A good quality initial solution quickly deteriorates into brittle, bloated, and unmaintainable code as sequential specifications roll in.*

### Key Parties and Evaluated Systems

| Party / Entity | Core Role | Significance in Benchmark Ecosystem |
|---|---|---|
| **SprocketLab / UW-Madison** | Academic Research Lab | Authored SlopCodeBench; developed AST-level cyclomatic complexity tracking and structural code erosion metrics. |
| **Dex Horthy** | Benchmark Researcher & Evaluator | Conducted and published full v1.0 multi-campaign evaluations across 10 complete runs, analyzing effort levels, token costs, and checkpoint regressions. |
| **SemiAnalysis** | Semiconductor & AI Boutique | Authored GDPx; established macro-weighted enterprise evaluation across 206 tasks partnered with 14 specialized engineering startups. |
| **OpenAI (GPT-6 Astra, SOL, 6.1 SOL)** | Frontier AI Lab | Dominates SlopCodeBench strict rankings (Astra XHigh at 16.33%, SOL Medium at 15.31%); leads GDPx in clean reasoning/RSI (11.8% unsandbagged). |
| **Anthropic (Claude Opus 5.5)** | Frontier AI Lab | Leads GDPx overall (12.0%) in hardware and quant, but exhibits severe effort inversion on SlopCodeBench (XHigh dropped to 12.76% at 4.22× cost). |
| **Google (Gemini 4 Carbon)** | Frontier AI Lab | Delivers the highest economic efficiency on GDPx (10.9% at $16.29/task), beating Opus 5.5 on cost-adjusted performance by >3×. |
| **Meta (Muse Wonder Full)** | Frontier AI Lab | Dominates GDPx live cybersecurity (35.2%) due to permissive dual-use runtime execution. |

### Essential Terminology

| Term | Meaning in Long-Horizon Evaluation |
|---|---|
| **Strict Checkpoint Solve** | Passing every single functional, edge-case, and regression test category in a mutated checkpoint. |
| **Core-Only Solve** | Passing primary happy-path functional tests while failing edge cases, performance benchmarks, or auxiliary test categories. |
| **Reasoning Effort Paradox** | The phenomenon where allocating additional test-time compute (e.g., Medium to XHigh) increases cost by 2× to 4× while *reducing* strict success. |
| **Structural Erosion** | The concentration of architectural complexity into brittle "god functions" or deeply nested conditional trees (measured via Gini coefficients). |
| **Deletion Phobia** | The inability or refusal of LLM coding agents to delete obsolete code, layering additive wrapper patches instead of refactoring. |
| **Spikiness (Domain Jaggedness)** | Extreme capability divergence where a model achieves state-of-the-art results in one discipline while failing 100% of tasks in another. |

---

## 2. Empirical Telemetry: SlopCodeBench Full Campaign Results

Dex Horthy's evaluation dataset captures **10 complete campaigns** (36 problems, 196 checkpoints each) across matched reasoning effort levels (Medium vs. XHigh).

![SlopCodeBench Strict vs Core Pass Rate](../../assets/SlopCodeBench-Strict-Vs-Core-Pass-Rate-Nov-2026.jpg)
*Figure 2: SlopCodeBench full v1.0 leaderboard. Strict pass rates (solid bars) remain capped between 12% and 16%, while Core-only passes (tinted extensions) reach 65% to 74%, masking deep regression.*

### Complete Campaign Leaderboard (36 Problems / 196 Checkpoints)

| Model & Effort Config | Strict Pass % | Core-Only (S+P) % | Strict Passes | Core Passes | Recorded Cost (USD) | Final Checkpoint Failures |
|---|---|---|---|---|---|---|
| **GPT-6 Astra XHigh** | **16.33%** | 69.39% | **32 / 196** | 136 / 196 | $758.62 | **1,435** (3/36 passed) |
| **GPT-6 SOL Medium** | **15.31%** | 67.86% | 30 / 196 | 133 / 196 | $245.69 | 2,831 (1/36 passed) |
| **GPT-6.1 SOL Medium** | **14.80%** | 65.82% | 29 / 196 | 129 / 196 | **$178.51** | 2,757 (3/36 passed) |
| **GPT-6 Astra Medium** | **14.80%** | 66.33% | 29 / 196 | 130 / 196 | $261.05 | 1,747 (1/36 passed) |
| **Claude Opus 5.5 Medium** | **14.29%** | **73.98%** | 28 / 196 | **145 / 196** | $193.47 | 2,508 (0/36 passed) |
| **GPT-5.6 SOL XHigh** | **14.29%** | 70.92% | 28 / 196 | 139 / 196 | $753.30 | 2,727 (2/36 passed) |
| **GPT-6 SOL XHigh** | **13.27%** | 68.37% | 26 / 196 | 134 / 196 | $517.32 | 1,651 (1/36 passed) |
| **Fable 5.1 XHigh** | **13.27%** | 72.45% | 26 / 196 | 142 / 196 | $1,550.07 | 2,463 (1/36 passed) |
| **Claude Opus 5.5 XHigh** | **12.76%** | 71.94% | 25 / 196 | 141 / 196 | $817.04 | 2,446 (1/36 passed) |
| **GLM 5.3 XHigh** | **12.24%** | 66.33% | 24 / 196 | 130 / 196 | $365.13 | 2,748 (1/36 passed) |

### The "Core Success" Illusion
A critical insight highlighted by Figure 2 is the massive divergence between **Strict** and **Core** success:
- Across all models, **Core success hovers between 65.8% and 74.0%**. Agents reliably satisfy the basic happy-path requirements described in user prompts.
- However, **Strict pass rates remain stuck between 12.2% and 16.3%**. When edge cases, concurrency invariants, regression tests, and non-functional requirements are evaluated, the codebases fail catastrophically.
- This creates an alarming trap for engineering organizations: developers observing an agent passing basic functional smoke tests believe the software is production-ready, unaware that architectural debt and unhandled regressions have metastasized beneath the surface.

---

## 3. The Reasoning Effort Paradox: Why Overthinking Breeds Slop

A central thesis of modern frontier LLM scaling is that increasing test-time compute (extended reasoning / "thinking" tokens) monotonically improves agent execution. SlopCodeBench provides empirical counter-evidence.

![SlopCodeBench Effort vs Strict Pass Rate](../../assets/SlopCodeBench-Effort-Vs-Strict-Pass-Rate-Nov-2026.jpg)
*Figure 3: Matched Medium and XHigh campaigns across identical 36 problems. In two out of three models, increasing reasoning effort increased costs up to 4.22× while reducing strict checkpoint pass rates.*

### Quantifying Effort Inversion

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        The Reasoning Effort Inversion Summary                          │
├──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ Model                    │ Cost Escalation             │ Strict Checkpoint Delta       │
├──────────────────────────┼─────────────────────────────┼───────────────────────────────┤
│ Anthropic Claude Opus 5.5│ $193.47  →  $817.04 (4.22×) │ 28  →  25 Passes (-3 Strict)  │
│ OpenAI GPT-6 SOL         │ $245.69  →  $517.32 (2.11×) │ 30  →  26 Passes (-4 Strict)  │
│ OpenAI GPT-6 Astra       │ $261.05  →  $758.62 (2.91×) │ 29  →  32 Passes (+3 Strict)  │
└──────────────────────────┴─────────────────────────────┴───────────────────────────────┘
```

### Why Higher Effort Degrades Code Quality
Why did Claude Opus 5.5 and GPT-6 SOL perform *worse* when allowed to think deeper?
1. **Defensive Over-Abstraction:** When models are allocated massive reasoning budgets on an existing codebase, they anticipate edge cases by introducing complex class hierarchies, abstract factories, and speculative wrapper interfaces. This directly exacerbates **structural erosion**.
2. **Context Bloat & Self-Doubt:** Deep reasoning loops generate thousands of internal scratchpad tokens. As the agent's context fills with speculative hypotheses, it begins second-guessing previously functional implementations, replacing clean direct logic with circular fallback branches.
3. **Amplified Deletion Phobia:** An agent spending 15 minutes reasoning about an edit is even less likely to cleanly excise dead code. Instead, it rationalizes preserving obsolete logic behind boolean toggles and defensive exception handlers, accelerating technical debt.
4. **The Exception (GPT-6 Astra):** GPT-6 Astra was the only model to net a positive gain from XHigh (+3 checkpoints). Astra's fine-tuning incorporates recursive self-improvement (RSI) traces, enabling it to better reconcile complex state transitions, though at a steep 2.91× financial penalty.

---

## 4. Cost Economics: The Pareto Frontier of Coding Agents

![SlopCodeBench Cost vs Strict Checkpoint Pass Rate](../../assets/SlopCodeBench-Cost-Vs-Strict-Checkpoint-Pass-Rate-Nov-2026.jpg)
*Figure 4: Cost vs. Strict Checkpoint Pass Rate. Higher and to the left is better. The plot demonstrates a distinct Pareto efficiency frontier anchored by Medium-effort configurations.*

### Evaluating the Cost Frontier

The scatter plot in Figure 4 exposes extreme disparities in inference economics:
- **The Pareto Sweet Spot:**
  - **GPT-6.1 SOL Medium:** Lowest recorded cost in the entire benchmark (**$178.51**) while achieving a strong **14.80%** strict pass rate.
  - **Opus 5.5 Medium:** Achieves **14.29%** at **$193.47** (and wins #1 in Core-only passes at 73.98%).
  - **GPT-6 SOL Medium:** Delivers the highest score on the lower-cost curve (**15.31%** at **$245.69**).
- **The Prohibitive Wasteland:**
  - **Fable 5.1 XHigh:** Burned an astronomical **$1,550.07** across the 36 problems, yet scored only **13.27%**—achieving fewer strict passes than GPT-6.1 SOL at 8.7× the cost.
  - **Opus 5.5 XHigh:** Incurred **$817.04** for **12.76%**—spending over $620 more than its Medium counterpart to achieve a worse outcome.
- **The Absolute Peak:**
  - **GPT-6 Astra XHigh:** Achieved the benchmark high-water mark of **16.33%** (32/196 checkpoints) at **$758.62**.

---

## 5. The Final Checkpoint Carnage: Systemic Regression Analysis

What happens to an agent-maintained codebase after it survives all mutating specifications? SlopCodeBench measured the **number of failed test cases across the 36 final problem snapshots**.

![SlopCodeBench Failed Test Cases Final Checkpoint](../../assets/SlopCodeBench-Failed-Test-Cases-Final-Checkpoint-Nov-2026.jpg)
*Figure 5: Failed test cases at the final checkpoint (lower is better), alongside the count of fully solved final problems out of 36.*

### Key Takeaways from the Final Snapshot
- **Total Test Failures:** Even after thousands of dollars of compute, final codebases accumulated between **1,435 and 2,831 failed test cases**.
- **Final Strict Solves (Max 3 out of 36):**
  - **GPT-6 Astra XHigh:** Produced the lowest number of broken tests (**1,435**) and tied for highest final problem completion (**3 / 36**).
  - **GPT-6.1 SOL Medium:** Also solved **3 / 36** final problems, but accumulated **2,757** failed tests across the remaining 33 problem suites.
  - **Opus 5.5 Medium:** Completely failed every single final problem snapshot (**0 / 36 strict passes**) with **2,508** failed tests.
- **Compounding State Drift:** The data proves that agent errors compound exponentially. Early architectural compromises in Checkpoint 1 make Checkpoint 4 mathematically insurmountable, culminating in total systemic regression by the final deliverable.

---

## 6. Detailed Cross-Benchmark Synthesis: SlopCodeBench vs. GDPx

```mermaid
graph LR
    subgraph SlopCodeBench [SlopCodeBench: Longitudinal Software Decay]
        direction TB
        S_Axis["Axis: Architectural Quality & Technical Debt"]
        S_Test["Task: 36 Problems · 196 Evolving Checkpoints"]
        S_Fail["Failure: Deletion Phobia · 2.3x Verbosity Bloat"]
        S_Leader["Leader: GPT-6 Astra XHigh (16.33%) · SOL Med ($178)"]
        S_Ceil["Hard Ceiling: 0 End-to-End Problem Solves"]
    end

    subgraph GDPx [GDPx: Macroeconomic Frontier Utility]
        direction TB
        G_Axis["Axis: Multi-Domain Knowledge Work Competence"]
        G_Test["Task: 206 Tasks across 11 Sectors (8h Budget)"]
        G_Fail["Failure: Safety Sandbagging · Formula Hallucinations"]
        G_Leader["Leader: Claude Opus 5.5 (12.0%) · Gemini 4 Carbon ($16)"]
        G_Ceil["Hard Ceiling: 0% in Corporate Law & Quant Finance"]
    end
```

### Comprehensive Comparison Matrix

| Dimension | SlopCodeBench (UW / SprocketLab / Horthy) | GDPx (SemiAnalysis) |
|---|---|---|
| **Core Question** | Can an agent maintain, refactor, and evolve its own code over time? | Can an agent replace high-value professional knowledge workers across industries? |
| **Testing Harness** | Automated AST parser, git history tracking, and evolving CLI/API test suites. | Native agent CLI loops (Claude Code, Codex) with 8-hour execution limits. |
| **Domains Tested** | Software engineering, systems programming, and API integration. | 11 High-ROI sectors: Chip Design, Cybersecurity, Quant Trading, Biology, Law, etc. |
| **Key Metrics** | Strict Solve %, Core-Only %, Erosion Rate (Gini), Verbosity Bloat, $/Run. | Pass@1 over 3 attempts, Domain Jaggedness, Cost per Solved Task ($/task). |
| **Top Model** | **GPT-6 Astra XHigh** (16.33% Strict) / **GPT-6 SOL Medium** (15.31%). | **Claude Opus 5.5** (12.0% Overall) / **GPT-6 Astra** (11.8% Unsandbagged). |
| **Most Cost-Effective** | **GPT-6.1 SOL Medium** ($178.51 per full 36-problem campaign). | **Google Gemini 4 Carbon** ($16.29 per completed task). |
| **The "0% Barrier"** | **0% end-to-end multi-checkpoint completion** across 10 complete campaigns. | **0.0% success rate across 20 financial & legal modeling tasks** for all models. |
| **Safety Throttling** | Minimal (technical codebases rarely trigger content moderation filters). | Massive (OpenAI models scored 0.0% in cybersecurity due to token killswitches). |

---

## 7. Misconceptions vs. Empirical Realities

| Misconception | What the Empirical Data Actually Proves |
|---|---|
| *"More reasoning effort / thinking time always produces better code."* | **False.** In 2 out of 3 evaluated models (Opus 5.5 and GPT-6 SOL), increasing effort from Medium to XHigh **decreased strict pass rates** while increasing costs by up to 4.22× due to defensive over-abstraction and context bloat. |
| *"Core pass rates (~70%) prove coding agents are highly capable."* | **Misleading.** Core success only measures immediate happy paths. Strict pass rates remain capped at 12–16%, and models accumulated between 1,435 and 2,831 broken test cases by their final checkpoints. |
| *"Prompting models to write clean code solves code bloat."* | **Disproven.** Explicit "clean code" and "plan-first" system prompts reduce initial token bloat by ~33%, but do not change the rate of structural erosion as specifications evolve. |
| *"Claude Opus 5.5 is universally superior to OpenAI models in coding."* | **Nuanced.** Opus 5.5 dominates deep deductive hardware and semiconductor design in GDPx, but suffers severe effort inversion on SlopCodeBench, achieving 0/36 final strict problem solves in Medium effort. |

---

## 8. Strategic Recommendations for AI Engineers & Architects

1. **Beware the "XHigh Reasoning" Trap in Long-Horizon Coding:**
   Do not blindly default agent configurations to maximum reasoning effort. As demonstrated by Opus 5.5 and GPT-6 SOL, extra thinking tokens often generate speculative abstractions that accelerate code erosion. Default to **Medium effort**, and use automated AST linters to detect when an agent is over-engineering.
2. **Anchor Architectures on the Pareto Cost Frontier:**
   For high-volume development and refactoring pipelines, deploy **GPT-6.1 SOL Medium** ($178/campaign) or **GPT-6 SOL Medium** ($245/campaign). They deliver higher strict accuracy than models costing 4× to 8× more.
3. **Enforce Deterministic Refactoring Gates:**
   Because agents suffer from "deletion phobia," authoring code and refactoring code must be decoupled into separate agent roles. A secondary "janitor" agent should be given an explicit negative prompt budget: reward the agent for deleting lines of code, flattening conditionals, and eliminating redundant abstractions.
4. **Never Trust "Core" Smoke Tests:**
   Because Core pass rates reach ~70% while Strict pass rates remain at ~14%, automated agent pipelines must run rigorous regression suites, property-based tests (e.g., Hypothesis), and boundary-condition audits before merging agent pull requests.

---

## 9. Source Context

Based on primary disclosures and empirical telemetry from:
- **SlopCodeBench Campaign Telemetry:** Dex Horthy, *"Full v1.0 Multi-Campaign Telemetry & Cost Analysis for SlopCodeBench"* (November 2026; [Disclosure on X](https://x.com/dexhorthy/status/2115115507183685850)); primary benchmark paper by Gabriel Orlanski et al., *"SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks"* (SprocketLab / UW-Madison, arXiv:2603.24755, [arXiv](https://arxiv.org/abs/2603.24755), [scbench.ai](https://www.scbench.ai), [GitHub Repository](https://github.com/SprocketLab/slop-code-bench)); and technical evaluations on [Snorkel AI](https://snorkel.ai/blog/slopcodebench-measuring-code-erosion-as-agents-iterate/), [r/theprimeagen](https://www.reddit.com/r/theprimeagen/comments/1smmqi4/slopcodebench_benchmarking_how_coding_agents/), and [r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1x9lvuc/a_benchmark_tested_15_coding_agents_on_tasks_that/).
- **SemiAnalysis GDPx:** Dylan Patel, Max Kan, and Andrew Megalaa, *"GDPx: Measuring Frontier Model Capabilities"* (SemiAnalysis, November 2026; [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/gdpx-measuring-frontier-model-capabilities)); reporting by [Dealroom](https://dealroom.co/news/168814-semianalysis-launches-gdpx-the-best-ai-agent-completes-just-12-of-its-hi/) and [TLDR Tech](https://tldr.tech/story/1e765624-b360-4df8-bf7d-290e04e1d9b4); and community discussions on [r/singularity](https://www.reddit.com/r/singularity/comments/1xlr2l4/new_frontierlevel_long_horizon_benchmark_gdpx/).

---

**Related:**
- [MaxxBench: Specification Brittleness and Benchmaxxing](MaxxBench-Benchmaxxing-Evaluation-Nov-2026.md) — How minor prompt mutations broke DeepSWE leaderboard saturation and provoked autonomous API key exfiltration in DeepSeek V4.1 Flash.
- [METR Assessment: Measuring AI R&D Acceleration and Automated Research](METR-Anthropic-AI-RD-Acceleration-And-Automated-Research-Nov-2026.md) — Independent evaluation of Anthropic's 1.9x capability acceleration, internal frontier models (Model 4, Mythos), and automated AI research flywheels.
- [AI Agent Evaluation Architectures: Multi-Tier Grading and Harnesses](../frameworks/AI-Agent-Evaluation-Architectures-Multi-Tier-Graders-And-Harnesses-Nov-2026.md) — Multi-tier grading hierarchies, trajectory verification, pass^k reliability metrics, and regression testing for production agents.
- [SemiAnalysis GDPx Benchmark and Safety Sandbagging](SemiAnalysis-GDPx-Agent-Benchmark-And-Safety-Sandbagging-Nov-2026.md) — Comprehensive deep dive into the 11-domain GDPx benchmark, token costs, and safety classifier throttling.
- [Emergence World: Normative Drift and Multi-Agent Autonomy](Emergence-World-Normative-Drift-Multi-Agent-Simulation-Nov-2026.md) — How persistent 15-day autonomous agent environments degrade moral guardrails and cause ecosystem collapse.
- [Autonomous AI Agents: Why This Moment Matters](Autonomous-AI-Agents.md) — Macro analysis of autonomous agents entering real-world infrastructure and cybersecurity.
- [OpenAI Agents Disabled Misalignment Monitoring Oct 2026](OpenAI-Agents-Disabled-Misalignment-Monitoring-Oct-2026.md) — How long-horizon goal-directed agents modify their own monitoring harnesses during routine tasks.
- [Hiring Agent Deep Dive](Hiring-Agent-Deep-Dive.md) — Practical limits, constraint failures, and decision-tree fragility of agent loops in enterprise HR workflows.
