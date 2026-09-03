# Headroom and RTK: Real-World Feedback (2026)

**Date**: 2026-09-03  
**Scope**: Public issue reports, an independent RTK field report, and current project documentation.  
**Bottom line**: RTK currently looks like the safer first experiment for shell-heavy agents. Headroom can help on repetitive, large payloads, but its end-to-end value depends heavily on provider caching, integration path, workload, and version.

## What users are actually seeing

### RTK

- **Independent positive result**: Soba Labs routed 1,456 Claude Code/OpenCode commands through RTK and measured 1.3M raw-output tokens reduced to 644.9K, or **49.6% fewer command-output tokens**. They explicitly note this is not the same as a 49.6% reduction in the API bill because cached input and generated output are separate cost components. [Soba Labs field report](https://sobalabs.ai/blog/halving-claude-code-token-usage-with-rtk/)
- **Practical user feedback**: a Hacker News user who had used RTK for several weeks called it “pretty solid”; the main annoyance was that troubleshooting output can be suppressed, requiring a raw rerun. [Hacker News discussion](https://news.ycombinator.com/item?id=47081527)
- **Important scope limit**: RTK compresses shell/Bash output, not the entire agent context. Claude Code built-in `Read`, `Grep`, and `Glob` calls bypass the Bash hook. The project also says its absolute token figures are approximate (`bytes / 4`) and its percentages are output reduction, not bill reduction. [RTK README](https://github.com/rtk-ai/rtk)
- **Performance edge case**: an open report measured `rtk grep` on a 20 MB input at 246.8 MiB peak memory and 1.41 s versus plain `grep` at 7.9 MiB and 289 ms, while both printed 2,579 bytes. This is a large-input corner case, but it shows the proxy can cost more CPU/RAM than the saved context in some commands. [RTK #3392](https://github.com/rtk-ai/rtk/issues/3392)
- **Safety issue to watch**: an open report says the auto-rewrite hook dropped stdin for commands such as `wrangler secret put/bulk`, resulting in empty production secrets; the reporter says two real secrets were affected. The proposed fix is still a pull request at this snapshot. Exclude stdin-consuming commands until this is fixed and verified in the installed release. [RTK #2431](https://github.com/rtk-ai/rtk/issues/2431) · [proposed fix #2575](https://github.com/rtk-ai/rtk/pull/2575)
- **Correctness issue to watch**: an open report on the `develop` branch says colored `rtk git diff`/`git show` can return only a summary while silently dropping the patch body with exit code 0. Treat colored diff handling as untrusted until the fix lands in the release you use. [RTK #3842](https://github.com/rtk-ai/rtk/issues/3842)

### Headroom

- **A positive field test exists, but savings were modest**: a Kimi Code user measured **3.17% effective compression** on three workload requests, 3/3 cache-hit requests, 88.4% cache-hit tokens, zero cache busts, and roughly 8–6 ms warm proxy overhead. They also found a token-accounting discrepancy between per-request and aggregate numbers. [Headroom discussion #3182](https://github.com/headroomlabs-ai/headroom/discussions/3182)
- **A serious negative field result also exists**: a contributor measured a long Claude Code workload where Headroom 0.37.0 changed cache-hit rate from 90% to 52% and input cost from about $2.01 to $4.40 on the same workload. The report attributes this to background recompression changing bytes already accepted into the provider cache. [Headroom #3379](https://github.com/headroomlabs-ai/headroom/issues/3379)
- **The cache regression has a merged fix**, with tests and a live patched-deployment check described in [PR #3380](https://github.com/headroomlabs-ai/headroom/pull/3380). However, the same repository still has active cache-related work, so verify the exact installed version and run a before/after canary rather than assuming every release is cache-safe.
- **Correctness/integration risks remain visible in the tracker**: #3345 reports a semantic-cache collision that can return a response for a different tool schema; #3407 reports generated Codex configuration silently selecting local rather than remote compaction. Both were open at the research date. [#3345](https://github.com/headroomlabs-ai/headroom/issues/3345) · [#3407](https://github.com/headroomlabs-ai/headroom/issues/3407)
- **Do not read the README headline as bill savings**: Headroom’s current README reports 21–57% reductions on four seeded, offline payload scenarios and separate accuracy tests at N=100; it also says short, dense, or prose payloads may see little reduction. Those are useful component tests, not proof of lower end-to-end agent cost. [Headroom README](https://github.com/headroomlabs-ai/headroom)

## Practical recommendation

1. Start with RTK for `git`, test runners, linters, logs, and other noisy shell commands; keep `rtk proxy` available for full output.
2. Add explicit exclusions for stdin-sensitive commands and test the exact `git diff`/color/path combinations your agents use.
3. Treat Headroom as a canary-only experiment first: compare provider-reported cache reads/writes, total input/output cost, number of agent turns, latency, and task success against a control session.
4. Do not stack both tools globally on day one. RTK reduces shell noise; Headroom changes broader payloads and cache behavior, so enable one layer at a time and keep rollback simple.

## Sources

- [Headroom official repository](https://github.com/headroomlabs-ai/headroom)
- [RTK official repository](https://github.com/rtk-ai/rtk)
- [Soba Labs: How we halved Claude Code token usage with RTK](https://sobalabs.ai/blog/halving-claude-code-token-usage-with-rtk/)
- [Hacker News: Rust Token Killer](https://news.ycombinator.com/item?id=47081527)

---

**Related:**
- [ai-token-optimization-tools](ai-token-optimization-tools.md) — Broader comparison of token-reduction layers and agent tooling.
- [GenAI-cost-Optimization](GenAI-cost-Optimization.md) — Cost measurement, caching, routing, and model-selection practices.
- [headroom-proxy](../../../DevSetup/headroom-proxy.md) — Local Headroom proxy setup and operational details.
- [headroom-pi-cost-saver](../../../DevSetup/headroom-pi-cost-saver.md) — Combined Headroom and RTK setup for Pi.
