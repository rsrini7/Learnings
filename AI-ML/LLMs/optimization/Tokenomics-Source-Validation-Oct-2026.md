# Tokenomics Source Validation — October 2026

**Checked October 11, 2026.** Companion evidence ledger for [the concise routing guide](Empirical-Tokenomics-and-Model-Routing-2026.md). Repeated assertions are grouped; all distinct claims in the supplied compilation are covered below. Recommendations are distinguished from documented behavior and measured results. “Unverified” means the supplied evidence and primary sources inspected do not establish the claim, not proof it never occurred. Product commands and billing can change.

**Main corrections:** distinguish the harness from the editor; compare billed task cost rather than token counts; preserve recoverable evidence; avoid universal thresholds, fixed reasoning budgets, and unsupported industry-consensus labels.

## A. Intent, autonomy, compression, and cost claims

| Supplied point | Verdict | Validated interpretation / evidence |
|---|---|---|
| Intent, roadmap, tribal knowledge require steering | Qualified | Information may live in docs too; state priorities, constraints, and non-goals rather than expecting inference. Engineering guidance, not a measured limitation. |
| Aggressive automatic pruning causes context rot/hallucination | Qualified | Lossy pruning can remove needed evidence; neither automation nor lack of consent establishes degradation. Evaluate retrieval and task outcomes. [CAPC](https://arxiv.org/abs/2607.15516) |
| Meta-agents drastically increase cost/latency | Qualified | Extra inference adds spend; parallelism can reduce wall-clock latency. Five verification loops is hypothetical, not measured. [Claude costs](https://code.claude.com/docs/en/costs) |
| Developer tools are autonomy Level 2–3 | Unsupported | Driving levels are an analogy, not an accepted software-agent classification. |
| Terminal permissions affect blast radius/secrets | Supported | Restrict permissions and sandbox execution; prompts alone are not an access-control boundary. [Security](https://code.claude.com/docs/en/security) |
| 95% step success yields <60% over ten steps | Conditional arithmetic | 0.95^10 ≈ 59.9%, narrowly below 60%; valid only for independent equal-probability steps and requiring every step to succeed. It is not measured agent reliability. |
| 99% over 50 steps ≈61%; 95% ≈8% | Conditional arithmetic | 0.99^50 ≈60.5%; 0.95^50 ≈7.69%. Real actions are dependent and agents recover; tests do not magically reset error probability. |
| Worktrees/linting/branch tools beat LLM multitasking | Qualified | Use explicit isolation and executable checks; “far faster” needs measurement. [Worktrees](https://code.claude.com/docs/en/common-workflows) |
| Manual compact/clear always cheaper than meta-cognition | Unsupported comparison | Compare total inference, lost cache, and recovery cost; manual and automatic compaction both have trade-offs. |
| Developer preferences belong in config/rules | Supported | Specify permitted scope and workflow preferences. [Settings](https://code.claude.com/docs/en/settings) |
| Headroom is simply a Rust compression proxy | Qualified | Current project offers Python/TypeScript interfaces and native components; implementation language does not establish savings. [Repository](https://github.com/headroomlabs-ai/headroom) |
| 30% fewer tokens can mean 40% higher invoice | Illustrative only | Possible in principle; supplied pairing is not a reproduced measurement. |
| Song et al. study proves compression increases cost 40–46% | Misattributed / overgeneralized | Yan Song’s CAPC preprint reports +40.1% for query-aware compression on tau-bench retail, while its cache-aware method reduces cost. Not a universal coding-agent result; +46% not established. [Paper](https://arxiv.org/abs/2607.15516) |
| tokbench compressed agents used 237 vs 180 turns | Verified pilot only | Repository reports N=1 per arm. Longer run and token totals do not prove compression caused degradation. Distinguish provider-billed tokens from dollar spend. [tokbench](https://github.com/Entelligentsia/tokbench) |
| Query-adaptive rewriting breaks every turn’s cache | Qualified | Rewriting an already cached prefix can break reuse; compressing new output once and retaining it unchanged need not. [Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) |
| Cached reads always cost 10%; output always 4–5× input | Incorrect universals | Rates vary by model/provider. This catalog includes Opus 5.5 reads at 0.05×; check pricing. [Rates](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing) |
| 50k cached at 0.1× vs 25k uncached gives 5× cost | Valid illustration | 5k vs 25k base-input equivalents, excluding output, cache-write premiums, and subsequent reuse. Not a measured whole-session multiplier. |
| Extra 50 reasoning turns erase all savings | Unsupported universal | Depends on actual input/output, retries, cache rates, and completion quality. |
| Headroom++ guarantees lower $31k bill | Unsupported | No supplied invoice, task baseline, or reproducible guarantee. |
| Never compress static prefix; only new tail | Useful conservative policy | Preserve existing history; stable once-compressed reusable prefixes can also be beneficial (CAPC). “Never” is too strong. [CAPC](https://arxiv.org/abs/2607.15516) |
| Strip ANSI/progress, deduplicate traces, project JSON | Qualified | Noise filtering can help; preserve causal errors, types, null-vs-absent semantics, exit status, and access to originals. Deterministic is not automatically lossless. |
| Agent only reads first 30 errors; use 50+20 lines | Unsupported rule | Output selection is task-dependent; keep complete raw logs plus targeted retrieval. |
| Discovery must use Haiku/local; frontier only for edits/planning | Qualified | Run simple searches as tools; delegate substantive exploration only if useful. Haiku is outside the stated org catalog. |
| 4–6h sessions biggest bill driver; clear after 15/20/25 turns | Unsupported ranking / thresholds | Idle duration alone is not billed inference. Act on context, cache misses, task boundaries, and budgets, not fixed turn counts. [Costs](https://code.claude.com/docs/en/costs) |
| CLI $650/% vs editor $220/% proves 3× shipped-code cost | Unverified private anecdote | Ratio ≈2.95, but progress percentages, billing, task difficulty, and quality are undefined; cannot compare products. |
| VS Code one request; CLI 8–20 calls | Incorrect distinction | Both can run agentic loops; count actual calls/tools, not UI type. [VS Code agent mode](https://code.visualstudio.com/docs/copilot/agents/overview) |
| Fixed 2k/300-token editor workload, 120k/45min CLI growth | Illustrative only | No measured universal payload/time; context depends on mode, configuration, and work. |
| Ultrathink always max 32k, $0.50–$0.80 hidden cost | Incorrect fixed budget | See Claude validation below; price and token use are model-specific. |
| Reserve highest effort strictly for architecture/hard bugs | Qualified | Sensible default; implementation/testing may also warrant deeper reasoning. |
| VS Code should be 85%+ of execution | Preference only | Original 95/5 split is a user workflow, not an empirically optimal allocation. |


## B. Copilot claims

Repeated bullets are grouped, but each distinct factual assertion is covered. Supported = official documentation; qualified = useful with scope/caveat; unsupported = no evidence or inaccurate.

| ID | Supplied claim | Verdict / correction | Source |
|---|---|---|---|
| C01 | Right-size reasoning; do not default to Opus | Supported; task capability matters. | [Optimization](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) |
| C02 | Universal 24× cost gap | Unsupported as universal; compare named models, token categories, tiers. | [Rate card](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) |
| C03 | Avoid reasoning for all implementation; small models more faithful | Qualified: some execution-heavy tasks overthink; no blanket quality guarantee. | [Optimization](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) |
| C04 | Auto task routing and discounted rate | Supported; paid plans get 10% discount. | [Auto](https://docs.github.com/en/copilot/concepts/models/auto-model-selection) |
| C05 | Auto restricts requests to cheap models | Incorrect; all tier models remain available; complex work may route upward. | [Auto](https://docs.github.com/en/copilot/concepts/models/auto-model-selection) |
| C06 | Minimum sufficient context / precise paths / stopping criteria | Supported. | [Optimization](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) |
| C07 | Severe forgetting at 50–70% context | Unsupported fixed threshold; reset unrelated tasks or compact useful long threads. | [Context guidance](https://code.visualstudio.com/docs/agents/guides/optimize-usage) |
| C08 | Research → plan → fresh implementation | Qualified: supported strategy, not mandatory for every small task. Preserve useful handoff. | [Optimization](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) |
| C09 | Tests, linters, scanners reduce compounding mistakes | Supported; tests only cover asserted behavior, not all correctness. | [Optimization](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) |
| C10 | 99%^50≈61%, 95%^50≈8% | Arithmetic valid only under independent, equal-probability, all-steps-must-succeed assumptions; not measured agent reliability. | Mathematical illustration, not empirical claim |
| C11 | Concise instructions based on observed errors | Supported; manual-only authorship and quarterly pruning are preferences. | [Instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| C12 | Base instructions must be 5–10 lines | Unsupported limit; keep necessary project rules, scope specialized instructions. | [Instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| C13 | Prompt files / skills instead of always-on domain rules | Supported with scope: skills load metadata then body/resources; targeted instruction files also available. | [Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) |
| C14 | Delete skills because models improve | Qualified: evaluate actual task value, not model age alone. | [Customization](https://code.visualstudio.com/docs/copilot/concepts/customization) |
| C15 | Role-scoped custom agents with restricted tools | Supported. Tool allowlists reduce available actions; not a complete security boundary. | [Agent config](https://docs.github.com/en/copilot/reference/custom-agents-configuration) |
| C16 | Stop using all custom agents | Unsupported and contrary to official recommendation; use concise scoped profiles. | [Custom agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents) |
| C17 | Every MCP schema sent every turn | Outdated blanket claim; modern tool search defers schemas to context tail. | [Harness efficiency](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot) |
| C18 | Prune unused MCP tools / avoid unnecessary screenshots | Qualified: reduce irrelevant payload; retain tools/context needed for correctness. | [Cache diagnostics](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer) |
| C19 | Research subagents isolate noise | Supported; subagents have separate context, still incur model costs. | [Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) |
| C20 | Prefer gh/rtk and batch calls | Qualified engineering heuristic; measure outputs, retrieval loss, total task cost. No universal MCP overhead advantage. | [Harness efficiency](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot) |
| C21 | /chronicle cost-tips identifies inefficiency | Supported, Copilot CLI (also Copilot app), not universal VS Code command. | [Chronicle](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/chronicle) |
| C22 | Skip Please / caveman prompts / return only code | Qualified stylistic advice; clarity and requirements matter more than a few words; terse prompts can create rework. | [Instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| C23 | /fix, /tests, #selection | Supported interface-dependent controls; use current slash-command menu / selected-code attachment. | [Cheat sheet](https://code.visualstudio.com/docs/agents/reference/ai-features-cheat-sheet) |
| C24 | Close irrelevant tabs | Qualified: relevant open files can inform context; not every open tab is always injected in full. | [Usage optimization](https://code.visualstudio.com/docs/agents/guides/optimize-usage) |
| C25 | Content exclusions protect agent context | Incorrect for Edit/Agent modes and cloud agent; exclusions have surface limitations. | [Exclusions](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/content-exclusion) |
| C26 | copilot-setup-steps.yml cleans chat context | Incorrect category: deterministic cloud-agent environment setup, not VS Code context reset. | [Environment](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment) |
| C27 | Agent workloads caused token-based billing transition | Qualified: transition confirmed June 1; claims about subscriptions regularly losing money are unverified. | [Announcement](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/) |
| C28 | 1 AI credit = $0.01; input/output/cache pricing | Supported. | [Billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing) |
| C29 | Paid completions and next edits zero credits/unlimited | Supported; included subscription benefit, not globally free product. | [Billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing) |
| C30 | Pro/Pro+ monthly allowances | Supported currently: $10/1,500 credits; $39/7,000 credits. Flex allotments can change; unused credits expire monthly. | [Billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing) |
| C31 | Business/Enterprise allowances | Supported currently: 1,900/3,900 credits per seat, pooled. | [Org billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing) |
| C32 | Additional prepaid credits / caps | Qualified: actual current mechanism is additional-usage budgets and billing; admin policy applies. | [Org billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing) |
| C33 | PR review billed credits only | Incomplete: code review also consumes Actions minutes. | [Rate card](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) |
| C34 | Two-line prompt always means 30–40k tokens | Unsupported fixed estimate; overhead depends on harness, tools, files, instructions/history. | [Harness efficiency](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot) |
| C35 | Entire skills and all open files always injected | Incorrect: progressive skills and deferred tools; context selection depends on harness. | [Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) |
| C36 | Full history repeated, paid at full rate | Qualified: retained history contributes input, but cached portions discounted and compaction changes history. | [Cache diagnostics](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer) |
| C37 | Automatic compaction; summary billable | Qualified: compaction is model work; no universal fixed trigger or separate flat charge established. | [Usage optimization](https://code.visualstudio.com/docs/agents/guides/optimize-usage) |
| C38 | 2,000-line file always 12–15k tokens / 100-token summary enough | Unsupported fixed token ratios and sufficient-summary guarantee. | [Context guidance](https://code.visualstudio.com/docs/agents/guides/optimize-usage) |
| C39 | Plan before every agent run | Qualified, risk-dependent; avoid process overhead for trivial edits. | [Usage optimization](https://code.visualstudio.com/docs/agents/guides/optimize-usage) |
| C40 | Cache Drop Notifier VS Code extension | Incorrect name/platform: supplied gist is Cache Break Notifier plugin for Copilot CLI. Prefer built-in VS Code Cache Explorer. | [Gist](https://gist.github.com/burkeholland/647ad0e579c06a43346ce6a373261eba), [Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer) |
| C41 | OpenAI TTL 30m / Claude 5m in Copilot | Incorrect current Copilot scope: official guidance says OpenAI 24h, most others 1h; not direct-provider defaults or guaranteed hits. | [Optimization](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) |
| C42 | Switching model loses reuse | Supported; prefer context boundaries; Auto manages boundaries. | [Auto](https://docs.github.com/en/copilot/concepts/models/auto-model-selection) |
| C43 | Changing reasoning always immediately breaks every cache | Qualified: GitHub recommends stable configuration; actual reuse provider/harness-dependent. Confirm actual metrics. | [Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer) |
| C44 | Configure MCP/skills upfront | Qualified: static prefix changes reduce reuse; deferred loading can preserve prefix. | [Harness efficiency](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot) |
| C45 | Providers keep branch/diff graphs; reverting restores cache | Unsupported internal architecture and guarantee; old matching prefix might still exist, inspect telemetry. | [Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer) |
| C46 | Instruction edits never take effect until /clear | Qualified only by harness: CLI loads persistent instructions at session start; VS Code supports per-request discovered/scoped files. Restart reliably applies updated base instructions, but avoid universal assertion. | [CLI customization](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features), [VS Code instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) |
| C47 | Sequential prefix caching; early divergence affects later prefix | Supported principle, subject to provider breakpoints; unchanged earlier prefix can survive. | [Explorer](https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer) |
| C48 | VS Code one prompt = one API call; CLI always 8–20 | Incorrect: VS Code agentic sessions also have multiple model requests; no fixed roundtrip count. | [Harness efficiency](https://code.visualstudio.com/blogs/2026/06/17/improving-token-efficiency-in-github-copilot) |



## C. Claude Code: 32 tricks — each checked

| # | Verdict | Validated wording / correction |
|---|---|---|
|1 `/init` every project|Qualify|Useful starter for a new repo; inspect/edit generated instructions, do not repeatedly overwrite good existing rules.|
|2 `/statusline`|Supported|Custom status-line feature exists.|
|3 `/voice`|Supported|Native dictation exists; availability depends on platform/authentication.|
|4 small focused context|Supported|Keep sufficient relevant context; do not remove needed evidence.|
|5 `/context`|Supported|Shows context usage and optimization suggestions.|
|6 compact at 60%, clear tasks|Qualify|`/compact` and `/clear` real; no universal 60% threshold. Compact for continuity, clear unrelated tasks.|
|7 always Plan Mode|Correct|Plan for complex/unfamiliar changes; skip overhead for straightforward work.|
|8 junior-dev/open questions|Qualify|Metaphor, not technical fact; specify task, constraints, desired outcome.|
|9 force clarifying questions|Qualify|Ask when ambiguity matters, not mandatory before every small task.|
|10 verification in lists|Supported|Provide runnable checks and success criteria.|
|11 parallel subagents|Supported|Separate contexts; parallelism can increase total spend.|
|12 `.claude/skills/`|Supported|Project skills use `.claude/skills/<name>/SKILL.md`.|
|13 Haiku workers|Qualify|Choose capable cheaper model and measure retry cost; no guarantee all discovery cheaper/better.|
|14 constantly refresh, <200 lines|Qualify|Audit periodically; under 200 lines is target, not strict size limit.|
|15 route external docs|Supported|On-demand skill/reference loading; `@` imports load upfront, do not reduce context.|
|16 Escape and reprompt|Supported|Interrupt drift early and give corrected scope.|
|17 challenge aggressively|Qualify|Specific evidence/checks outperform vague intensity; not a quantified quality guarantee.|
|18 `/rewind`, `/re`|Supported|Checkpoint code/conversation rewind exists; not rollback of arbitrary external effects.|
|19 notification hooks|Supported|`/hooks` views configuration; use suitable Notification/Stop events.|
|20 screenshots|Supported|Useful visual reference/check, with image-token costs.|
|21 Chrome DevTools|Qualify|Browser interaction supported via Claude in Chrome and/or separate MCP; not every setup has DevTools.|
|22 replicate inspiration|Qualify|Design technique, not token-saving fact; describe intended pattern and validate result.|
|23 `claude-worktree`|Correct|Native command is `claude --worktree <name>` or `claude -w <name>`; named wrapper not built-in.|
|24 API instead heavy MCP|Qualify|Compare tool schemas, result size, discovery, auth, integration cost; MCP tool search defers definitions.|
|25 `/loop`|Supported|Recurring prompts while session stays open; not inherently persistent unattended server.|
|26 VPS always-on|Qualify|Deployment choice, not automatic cost/quality optimization; session/runtime/security controls still needed.|
|27 phone/browser remote|Supported|`/remote-control` continues local session; machine/session must remain running.|
|28 database NL CLI|Qualify|Claude can invoke CLI with permissions; BigQuery CLI itself is not a universal natural-language interface.|
|29 ultrathink maximum 32k|Correct|`ultrathink` recognized one-turn in-context deeper-reasoning instruction; API effort unchanged, no fixed 32k allocation.|
|30 permission allow/deny|Supported|Use permissions plus sandboxing where appropriate; avoid blanket bypass.|
|31 Agent Teams|Supported|Collaborating sessions exist; cost/scoping matter; not required for ordinary work.|
|32 Context7 MCP|Qualify|Official docs list Context7 integration; useful third-party docs retrieval, not guarantee freshness/correctness.|

Sources: [commands](https://code.claude.com/docs/en/commands), [best practices](https://code.claude.com/docs/en/best-practices), [voice](https://code.claude.com/docs/en/voice-dictation), [subagents](https://code.claude.com/docs/en/sub-agents), [worktrees](https://code.claude.com/docs/en/worktrees), [MCP](https://code.claude.com/docs/en/mcp), [teams](https://code.claude.com/docs/en/agent-teams), [model config](https://code.claude.com/docs/en/model-config).

## D. Context-window claims — each checked

| Claim | Verdict / correction |
|---|---|
|13.6k initial tokens, 2k system, 9.4k tools, 194 CLAUDE.md, 2k skills|Unverified session-specific measurements; not fixed product baseline. Use `/context` locally.|
|Deferred tools name-only, 0 tokens|Correct zero: tool names/listing/search consume context; full deferred schemas load when needed.|
|Proxy disables search, +10k|Mechanism supported; numeric increment configuration-specific. Non-first-party ANTHROPIC_BASE_URL disables search by default; ENABLE_TOOL_SEARCH=true requires gateway tool_reference support.|
|Full history every request|Supported in general; actual context may be compacted or old results cleared.|
|One user prompt many API turns|Supported; no fixed calls-per-prompt. Tool batching changes request count.|
|Cache first writes then reads/new writes|Supported; eligible stable prefix reused, provider rules apply.|
|Opus reads 1/20th|Qualify version: Opus 5.5 specifically 0.05x, not all Opus.|
|TTL 5m key, 1h subscription|Supported with usage-credits caveat: drops to 5m drawing credits unless chosen explicitly; TTL refresh from request start.|
|Stepping away resets|Qualify only expiry; no immediate reset just because developer pauses.|
|Context rot and rising costs|Possible task/model dependent; no universal accuracy cliff. Cache discounts repeated history.|
|Compact preserves rules/last answers and disk pointers|Qualify summarize selectively; precise preserved content depends mechanism, do not promise full losslessness.|
|Autocompact 967k /33k buffer|Current native 1M defaults about 967k supported; configurable/model/gateway-specific.|
|Subagents independent context, summary|Supported; fork differs by inheriting context. Workers billed separately.|
|Clear zero cost resets 13.8k|Clear itself no model cost; fixed baseline unsupported; subsequent fresh prompts still billed, warm history discarded.|
|Every CLAUDE.md line costs each request|Context included, but repeat prefixes usually cached; costs not fresh 1x each time.|
|Skills single reference until invoked|Skill listings cost tokens; bodies load on invocation; not zero-overhead.|
|Compact between tasks, clear new work|Qualify compact for continuing work; clear unrelated tasks; unnecessary compaction itself costs.|

Sources: [cost management](https://code.claude.com/docs/en/costs), [model/auto-compaction configuration](https://code.claude.com/docs/en/model-config), [MCP/tool search](https://code.claude.com/docs/en/mcp), [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills).

## E. Top 1% — each numbered point and its subclaims

| # | Verdict | Validated wording / correction |
|---|---|---|
|1 briefs instead Plan|Qualify|No source provided for Boris HN attribution; task/guardrails/DoD useful. Plan remains recommended for complex work. Interactive artifact after every edit unnecessary; evidence/diff/check results usually enough.|
|2 default effort, keywords obsolete|Correct keyword claim|`think`, `think hard` ordinary text; `ultrathink` specifically recognized. Medium default on current 5.5 models; official Opus 5.5 Medium vs Opus 5 High comparison exists, not blanket all-model rule.|
|3 double-check redundant, 2–3x tests|Qualify|Executable verifiers valuable; unsupported universal 2–3x and redundancy claim. Checks only prove what they cover; independent semantic review remains necessary.|
|4 `/goal` evaluator and hard limit|Qualify|Real feature, evaluator sees transcript, doesn't independently run/read. Condition includes measurable end state/check/invariants. `or stop after 20 turns` is evaluator-judged natural language, not enforceable numeric CLI cap. Runtime/budget flags for hard bounds.|
|5 <200 CLAUDE.md, 80% removed, nested100 lines|Qualify/omit numbers|Under200 target documented; no primary evidence found for 80% removal or nested preview100 rule. `@` eager loading supported. Correct audit `/doctor prompt-audit` >=2.1.283, not `/doctor prompt audit`. Index four-item taxonomy optional.|
|6 failure-driven skills, recording|Qualify|Start with baseline and add demonstrated missing guidance; no universal prohibition on anticipatory skills. Desktop recording feature not independently validated; omit without source.|
|7 7/9 dummy benchmark, eval doctor|Mixed|Unverified 7/9; `claude plugin eval` valid case-sensitive CLI, plugin A/B; `/skill-doctor` >=2.1.252, not `/skill doctor`; usage listing cost inspection supported.|
|8 hooks zero overhead guarantee|Correct absolutes|Command hooks can enforce particular covered checks without another model call. Output may add context; prompt/agent hooks consume model tokens. Correctness depends implementation, event coverage, permission/sandbox; no universal enforcement guarantee.|
|9 dynamic agents static obsolete concurrency config|Qualify|Isolation and bounded fanout useful. Static custom agents remain officially supported. No specific concurrency configuration key verified; avoid inventing one.|
|10 headless async events enterprise norm|Qualify|CLI noninteractive/background/GitHub integrations documented; CRM/webhook event orchestration requires configured external system. Directional preference, not universal standard or mandatory developer role.|

Sources: [best practices](https://code.claude.com/docs/en/best-practices), [goal](https://code.claude.com/docs/en/goal), [model config](https://code.claude.com/docs/en/model-config), [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [hooks](https://code.claude.com/docs/en/hooks).

## F. Industry-consensus table — all ten rows

1. Conditional planning sensible; claimed multi-vendor consensus/one-sentence diff rule unsubstantiated.
2. Structured effort parameters documented; universal deprecated prompt thinking false due ultrathink and model-specific guidance.
3. Deterministic checks strongly recommended; universal standard and complete ground truth overclaims.
4. Bounded loops prudent; natural-language goal limits not hard enforcement, evaluator transcript-only verified.
5. Under200 target official; 200–300 standard incorrect range; @ organization does not reduce startup context.
6. Baseline/failure-driven iteration documented; universal best practice label too strong.
7. Baseline A/B evals documented; claim EDD replaced all prompt curation unsupported.
8. Programmatic gates useful; 'outperform in every benchmark' unsupported; command versus model hooks distinction essential.
9. Context isolation supported; rigid graphs universally obsolete unsupported, static subagent profiles still official.
10. Headless/event-based integrations exist; industry trajectory commentary, not measured consensus.



---

**Related:**
- [Empirical Tokenomics and Model Routing](Empirical-Tokenomics-and-Model-Routing-2026.md) — Concise policy incorporating the validated guidance.
- [Headroom & RTK: Real-World Feedback](Headroom-RTK-Real-World-Feedback-2026.md) — Existing evidence on cost and correctness trade-offs.
- [AI Token Optimization Tools](ai-token-optimization-tools.md) — Broader tooling comparison; savings need end-to-end validation.
